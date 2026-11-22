#!/usr/bin/env python3
"""Render a git change range (or file hotspots) as a self-contained interactive HTML page.

Usage:
  change-map.py --base origin/main --head HEAD --out changes.html     # what changed
  change-map.py --hotspots --since "1 year ago" --out hotspots.html   # where change concentrates
Stdlib only. Run from anywhere with --repo <path>.
"""
import argparse, json, os, re, subprocess, sys, html
from collections import Counter

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, errors="replace")
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr}")
    return r.stdout


def file_sizes(repo, ref):
    sizes = {}
    for line in git(repo, "ls-tree", "-r", "-l", ref).splitlines():
        meta, path = line.split("\t", 1)
        parts = meta.split()
        if parts[1] == "blob" and parts[3] != "-":
            sizes[path] = int(parts[3])
    return sizes


def numstat(repo, base, head):
    out = {}
    for line in git(repo, "diff", "--numstat", "-M", base, head).splitlines():
        a, d, path = line.split("\t", 2)
        if " => " in path:  # rename: a/{x => y}/b or x => y
            m = re.match(r"(.*)\{(.*) => (.*)\}(.*)", path)
            old, new = (m.group(1) + m.group(2) + m.group(4), m.group(1) + m.group(3) + m.group(4)) if m else path.split(" => ")
            path = new.replace("//", "/")
            renamed_from = old.replace("//", "/")
        else:
            renamed_from = None
        binary = a == "-"
        out[path] = {"add": 0 if binary else int(a), "del": 0 if binary else int(d),
                     "binary": binary, "from": renamed_from}
    status = git(repo, "diff", "--name-status", "-M", base, head)
    for line in status.splitlines():
        parts = line.split("\t")
        code, path = parts[0][0], parts[-1]
        if path in out:
            out[path]["status"] = {"A": "added", "D": "deleted", "R": "renamed"}.get(code, "modified")
    return out


def blast_radius(repo, head, changed):
    """Heuristic: files at head that mention a changed file's module name as a whole word."""
    radius = {}
    for path in list(changed)[:60]:
        stem = os.path.splitext(os.path.basename(path))[0]
        if len(stem) < 4 or stem in {"index", "main", "init", "__init__", "utils", "types", "README", "SKILL"}:
            continue
        r = subprocess.run(["git", "-C", repo, "grep", "-l", "-w", "-I", stem, head, "--"],
                           capture_output=True, text=True, errors="replace")
        users = [l.split(":", 1)[1] for l in r.stdout.splitlines() if ":" in l]
        users = [u for u in users if u != path and u not in changed][:15]
        if users:
            radius[path] = users
    return radius


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=".")
    p.add_argument("--base")
    p.add_argument("--head", default="HEAD")
    p.add_argument("--hotspots", action="store_true")
    p.add_argument("--since", default="1 year ago")
    p.add_argument("--out", default="change-map.html")
    p.add_argument("--max-diff-lines", type=int, default=300)
    a = p.parse_args()
    repo = a.repo

    head_sha = git(repo, "rev-parse", "--short", a.head).strip()
    sizes = file_sizes(repo, a.head)
    title_repo = os.path.basename(os.path.abspath(git(repo, "rev-parse", "--show-toplevel").strip()))
    data = {"repo": title_repo, "head": head_sha, "mode": "hotspots" if a.hotspots else "changes"}

    if a.hotspots:
        counts = Counter(l for l in git(repo, "log", f"--since={a.since}", "--name-only", "--format=", a.head).splitlines() if l)
        data["files"] = [{"path": f, "size": s, "commits": counts.get(f, 0)} for f, s in sizes.items()]
        data["subtitle"] = f"Commits per file since {a.since} at {head_sha}"
        data["commits"] = []
    else:
        base = a.base
        if not base:
            has_parent = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "-q", f"{a.head}~1"],
                                        capture_output=True).returncode == 0
            base = f"{a.head}~1" if has_parent else EMPTY_TREE
        base_label = "(empty)" if base == EMPTY_TREE else git(repo, "rev-parse", "--short", base).strip()
        changes = numstat(repo, base, a.head)
        # deleted files aren't in head tree; show them with their old size
        if base != EMPTY_TREE:
            old_sizes = file_sizes(repo, base)
            for f, c in changes.items():
                if c.get("status") == "deleted":
                    sizes[f] = old_sizes.get(f, 1)
        diffs = {}
        for f in changes:
            d = git(repo, "diff", "-M", base, a.head, "--", f, check=False)
            if c := changes[f].get("from"):
                d = git(repo, "diff", "-M", base, a.head, "--", c, f, check=False)
            lines = d.splitlines()
            body = [l for l in lines if not l.startswith(("diff --git", "index ", "--- ", "+++ ", "new file mode", "deleted file mode", "similarity index", "old mode", "new mode"))]
            if len(body) > a.max_diff_lines:
                body = body[:a.max_diff_lines] + [f"… {len(body) - a.max_diff_lines} more lines"]
            diffs[f] = "\n".join(body)
        data["files"] = [{"path": f, "size": max(s, 1), **changes.get(f, {})} for f, s in sizes.items()]
        data["diffs"] = diffs
        data["blast"] = blast_radius(repo, a.head, changes)
        rng = f"{base}..{a.head}" if base != EMPTY_TREE else a.head
        log = git(repo, "log", "--format=%h\x1f%an\x1f%ad\x1f%s", "--date=short", rng, check=False)
        data["commits"] = [dict(zip(["sha", "author", "date", "subject"], l.split("\x1f"))) for l in log.splitlines()]
        tot_a = sum(c["add"] for c in changes.values()); tot_d = sum(c["del"] for c in changes.values())
        data["subtitle"] = f"{base_label} → {head_sha} · {len(changes)} files · +{tot_a} −{tot_d}"

    page = TEMPLATE.replace("__TITLE__", html.escape(f"{title_repo} change map")).replace(
        "__DATA__", json.dumps(data).replace("</", "<\\/"))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as fh:
        fh.write(page)
    print(f"Wrote {a.out}")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fbfaf8;--panel:#fff;--ink:#1d1d1b;--muted:#6b6a66;--line:#e4e2dc;--grey:#e9e7e2;--grey-ink:#8a8883;
 --add:#2f8f5b;--del:#c8483b;--mix:#c98a1b;--hot:#c8483b;--focus:#2b6cb0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161615;--panel:#1f1f1d;--ink:#ecebe7;--muted:#a19f99;
 --line:#34332f;--grey:#2a2a27;--grey-ink:#77756f;--add:#4fb57e;--del:#e0695c;--mix:#d9a441;--hot:#e0695c;--focus:#6ea8e6}}
:root[data-theme="dark"]{--bg:#161615;--panel:#1f1f1d;--ink:#ecebe7;--muted:#a19f99;--line:#34332f;--grey:#2a2a27;--grey-ink:#77756f;
 --add:#4fb57e;--del:#e0695c;--mix:#d9a441;--hot:#e0695c;--focus:#6ea8e6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 16px 8px;max-width:1400px;margin:auto}h1{font-size:20px;margin:0 0 4px}.sub{color:var(--muted)}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0 0;color:var(--muted);font-size:12px}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
main{max-width:1400px;margin:auto;padding:8px 16px 32px;display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:16px}
@media (max-width:900px){main{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px}
#map{position:relative;width:100%;height:62vh;min-height:360px}
.dir{position:absolute;border:1px solid var(--line);border-radius:4px;overflow:hidden}
.dir>.lbl{position:absolute;left:4px;top:1px;font-size:11px;color:var(--muted);white-space:nowrap;pointer-events:none}
.f{position:absolute;border:1px solid var(--bg);border-radius:3px;cursor:pointer;overflow:hidden;font-size:11px;padding:2px 3px;
 color:#fff;white-space:nowrap;text-overflow:ellipsis}
.f.un{background:var(--grey);color:var(--grey-ink)}.f:hover,.f.sel{outline:2px solid var(--focus);z-index:2}
h2{font-size:14px;margin:0 0 8px}.side{display:flex;flex-direction:column;gap:16px;min-width:0}
pre{margin:0;max-height:48vh;overflow:auto;font:12px/1.4 ui-monospace,Menlo,monospace;white-space:pre}
.a{color:var(--add)}.d{color:var(--del)}.h{color:var(--focus)}
ul{margin:0;padding-left:18px}li{margin:2px 0;word-break:break-all}.muted{color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:12px}td{padding:3px 4px;border-top:1px solid var(--line);vertical-align:top}
button{font:inherit;background:none;border:1px solid var(--line);color:var(--ink);border-radius:6px;padding:2px 8px;cursor:pointer}
</style></head><body>
<header><h1 id="t"></h1><div class="sub" id="s"></div><div class="legend" id="lg"></div></header>
<main><section class="card"><div id="map"></div><div class="muted" style="margin-top:6px;font-size:12px">Area = file size. Grouped by top-level folder. Click a file for details.</div></section>
<aside class="side"><section class="card"><h2 id="dt">Select a file</h2><div id="dm" class="muted"></div><pre id="dd"></pre></section>
<section class="card" id="bc"><h2>Blast radius <span class="muted" style="font-weight:400">(heuristic: unchanged files that mention a changed module)</span></h2><div id="br"></div></section>
<section class="card" id="cc"><h2>Commits</h2><table id="cm"></table></section></aside></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);const hot=D.mode==='hotspots';
document.getElementById('t').textContent=`${D.repo}: ${hot?'hotspots':'change map'}`;document.getElementById('s').textContent=D.subtitle;
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
document.getElementById('lg').innerHTML=hot?'<span><i class="sw" style="background:var(--hot)"></i>changed often</span><span><i class="sw" style="background:var(--grey)"></i>rarely/never</span>'
:'<span><i class="sw" style="background:var(--add)"></i>mostly added</span><span><i class="sw" style="background:var(--del)"></i>mostly removed / deleted</span><span><i class="sw" style="background:var(--mix)"></i>mixed edit</span><span><i class="sw" style="background:var(--grey)"></i>unchanged</span><span>stronger colour = more lines</span>';
const changed=D.files.filter(f=>f.status);const maxChurn=Math.max(1,...changed.map(f=>f.add+f.del));const maxC=Math.max(1,...D.files.map(f=>f.commits||0));
function color(f){if(hot){if(!f.commits)return null;return {c:'--hot',o:.25+.75*Math.sqrt(f.commits/maxC)}}
 if(!f.status)return null;const ch=f.add+f.del,o=.35+.65*Math.sqrt(ch/maxChurn);if(f.status==='deleted')return{c:'--del',o:1};
 if(f.status==='added'||f.del===0)return{c:'--add',o};if(f.add===0)return{c:'--del',o};const r=f.add/(f.add+f.del);return{c:r>.75?'--add':r<.25?'--del':'--mix',o}}
// group by top-level dir
const groups={};for(const f of D.files){const i=f.path.indexOf('/');const g=i<0?'(root)':f.path.slice(0,i);(groups[g]=groups[g]||[]).push(f)}
function squarify(items,x,y,w,h){const out=[];let rest=items.slice().sort((a,b)=>b.v-a.v);const tot=rest.reduce((s,i)=>s+i.v,0)||1;
 const scale=w*h/tot;rest=rest.map(i=>({...i,a:i.v*scale}));
 while(rest.length){const side=Math.min(w,h);let row=[],best=Infinity;
  for(const it of rest){const r=[...row,it],s=r.reduce((t,i)=>t+i.a,0),mx=Math.max(...r.map(i=>i.a)),mn=Math.min(...r.map(i=>i.a));
   const worst=Math.max(side*side*mx/(s*s),s*s/(side*side*mn));if(worst>best)break;best=worst;row=r}
  const s=row.reduce((t,i)=>t+i.a,0);let off=0;
  if(w>=h){const rw=s/h;for(const it of row){const ih=it.a/rw;out.push({...it,x,y:y+off,w:rw,h:ih});off+=ih}x+=rw;w-=rw}
  else{const rh=s/w;for(const it of row){const iw=it.a/rh;out.push({...it,x:x+off,y,w:iw,h:rh});off+=iw}y+=rh;h-=rh}
  rest=rest.slice(row.length)}return out}
const GENERIC=/^(SKILL\.md|README\.md|index\.[jt]sx?|__init__\.py|main\.\w+|mod\.rs|package\.json|Dockerfile|pom\.xml)$/;
function label(p){const parts=p.split('/'),b=parts.pop();return GENERIC.test(b)&&parts.length?parts.pop()+'/'+b.replace(/\.md$/,''):b}
const map=document.getElementById('map');let selEl=null;
function draw(){map.innerHTML='';const W=map.clientWidth,H=map.clientHeight;
 // weight: sqrt(size) so small files stay visible; changed files get a boost so they're findable
 const gs=Object.entries(groups).map(([k,fs])=>({k,fs:fs.map(f=>({f,v:Math.sqrt(f.size)*((f.status||f.commits)?2:1)})),v:0}));gs.forEach(g=>g.v=g.fs.reduce((s,i)=>s+i.v,0));
 for(const g of squarify(gs,0,0,W,H)){const dv=document.createElement('div');dv.className='dir';Object.assign(dv.style,{left:g.x+'px',top:g.y+'px',width:g.w+'px',height:g.h+'px'});
  const lb=document.createElement('div');lb.className='lbl';lb.textContent=g.k;dv.appendChild(lb);map.appendChild(dv);
  const pad=14;for(const r of squarify(g.fs,g.x+2,g.y+pad,Math.max(g.w-4,1),Math.max(g.h-pad-2,1))){const f=r.f,el=document.createElement('div');el.className='f';
   Object.assign(el.style,{left:r.x+'px',top:r.y+'px',width:Math.max(r.w,1)+'px',height:Math.max(r.h,1)+'px'});const c=color(f);
   if(c){el.style.background=`color-mix(in srgb, var(${c.c}) ${Math.round(c.o*100)}%, var(--panel))`;el.style.color=c.o>.6?'#fff':'var(--ink)'}else el.classList.add('un');
   el.title=f.path+(f.status?` (${f.status} +${f.add} −${f.del})`:'')+(hot?` (${f.commits} commits)`:'');
   if(r.w>50&&r.h>14)el.textContent=label(f.path);el.onclick=()=>show(f,el);map.appendChild(el)}}}
function show(f,el){if(selEl)selEl.classList.remove('sel');selEl=el;el.classList.add('sel');document.getElementById('dt').textContent=f.path;
 const m=document.getElementById('dm');m.textContent=hot?`${f.commits} commits · ${f.size} bytes`:f.status?`${f.status}${f.from?' from '+f.from:''} · +${f.add} −${f.del}`:'unchanged';
 const pre=document.getElementById('dd');pre.innerHTML='';const diff=(D.diffs||{})[f.path];
 if(diff){for(const l of diff.split('\n')){const s=document.createElement('span');s.className=l[0]==='+'?'a':l[0]==='-'?'d':l.startsWith('@@')?'h':'';s.textContent=l+'\n';pre.appendChild(s)}}
 const users=(D.blast||{})[f.path];if(users&&users.length){const x=document.createElement('div');x.className='muted';x.style.margin='6px 0';x.textContent='Mentioned by: '+users.join(', ');m.appendChild(x)}}
const br=document.getElementById('br'),bl=Object.entries(D.blast||{});
if(hot){document.getElementById('bc').style.display='none'}else if(!bl.length){br.textContent='No unchanged files reference the changed modules.';br.className='muted'}
else{const ul=document.createElement('ul');for(const [k,v] of bl){const li=document.createElement('li');li.textContent=`${k} → ${v.length} file(s): ${v.slice(0,5).join(', ')}${v.length>5?' …':''}`;ul.appendChild(li)}br.appendChild(ul)}
const cm=document.getElementById('cm');if(!D.commits.length)document.getElementById('cc').style.display='none';
for(const c of D.commits){const tr=document.createElement('tr');for(const k of ['sha','date','subject']){const td=document.createElement('td');td.textContent=c[k];if(k!=='subject')td.className='muted';tr.appendChild(td)}cm.appendChild(tr)}
draw();addEventListener('resize',()=>{clearTimeout(window._r);window._r=setTimeout(draw,120)});
const first=changed.sort((a,b)=>(b.add+b.del)-(a.add+a.del))[0];if(first){const el=[...map.querySelectorAll('.f')].find(e=>e.title.startsWith(first.path+' ')||e.title===first.path);if(el)show(first,el)}
</script></body></html>
"""

if __name__ == "__main__":
    main()
