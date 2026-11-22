#!/usr/bin/env python3
"""Render a project schedule as an interactive Gantt chart (HTML) and/or Mermaid gantt text.

Sources (pick one):
  --plan docs/<feature>/PLAN.md            T<n> blocks with Depends / Size / Estimate / Phase / Status / Start
  --json tasks.json                        [{"id","title","start","end"|"days","depends":[],"status","phase","owner"}]
  --github-project OWNER NUMBER            GitHub Projects (v2) items via `gh project item-list`

Output:
  --out gantt.html       interactive chart: phases, dependencies, critical path, today line, planned vs actual
  --mermaid gantt.md     Mermaid `gantt` block (renders natively in GitHub markdown, issues and PRs)

Scheduling: tasks without a start date begin the working day after their last dependency ends
(or --start). Durations are working days (Mon–Fri). Stdlib only.
"""
import argparse, datetime as dt, html, json, re, subprocess, sys

SIZE_DAYS = {"XS": 0.25, "S": 0.25, "M": 0.5, "L": 1, "XL": 2}
DONE = {"done", "closed", "complete", "completed", "merged"}
ACTIVE = {"in progress", "in-progress", "doing", "active", "in review", "review"}
BLOCKED = {"blocked", "on hold"}


def parse_date(s):
    s = (s or "").strip()
    return dt.date.fromisoformat(s[:10]) if re.match(r"\d{4}-\d{2}-\d{2}", s) else None


def next_workday(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def add_workdays(start, days):
    """End date (inclusive) of a task starting on `start` lasting `days` working days (min 1 calendar day)."""
    d, left = next_workday(start), max(1, round(days + 0.49))
    while left > 1:
        d = next_workday(d + dt.timedelta(days=1))
        left -= 1
    return d


def workdays_between(a, b):
    n, d = 0, a
    while d <= b:
        n += d.weekday() < 5
        d += dt.timedelta(days=1)
    return max(n, 1)


# ---------- sources ----------

def from_plan(path):
    text = open(path).read()
    tasks = []
    for m in re.finditer(r"^\s*(T\d+)\.\s+(.+?)\n((?:[ \t]+\S.*\n?)*)", text, re.M):
        tid, title, body = m.group(1), m.group(2).strip(), m.group(3)
        f = {k.lower(): v.strip() for k, v in re.findall(r"^\s+(\w[\w ]*?):\s*(.+)$", body, re.M)}
        deps = re.findall(r"T\d+", f.get("depends", ""))
        est = f.get("estimate", "")
        size = (re.match(r"\s*(XS|S|M|L|XL)\b", f.get("size", "")) or [None, "M"])[1]
        days = float(re.match(r"[\d.]+", est).group()) if re.match(r"[\d.]+", est) else SIZE_DAYS.get(size, 0.5)
        issue = re.search(r"#(\d+)", f.get("issue", "") + " " + title)
        tasks.append({"id": tid, "title": re.sub(r"\s*\(#\d+\)\s*$", "", title), "depends": deps, "days": days,
                      "phase": f.get("phase", ""), "status": f.get("status", "todo"), "owner": f.get("owner", ""),
                      "start": f.get("start", ""), "end": f.get("end", ""),
                      "satisfies": f.get("satisfies", ""), "issue": issue.group(1) if issue else ""})
    if not tasks:
        sys.exit(f"No T<n> tasks found in {path}")
    return tasks


def from_github(owner, number):
    r = subprocess.run(["gh", "project", "item-list", str(number), "--owner", owner, "--format", "json", "--limit", "500"],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("gh project item-list failed (is gh authenticated with the 'project' scope? "
                 "run: gh auth refresh -s project)\n" + r.stderr)
    tasks = []
    for it in json.loads(r.stdout).get("items", []):
        low = {k.lower(): v for k, v in it.items()}
        content = it.get("content") or {}
        num = content.get("number")
        start = low.get("start date") or low.get("start") or ""
        end = low.get("target date") or low.get("end date") or low.get("due date") or low.get("end") or ""
        it_field = low.get("iteration")
        if isinstance(it_field, dict) and not start:
            start = it_field.get("startDate", "")
            if it_field.get("duration") and not end and start:
                end = (parse_date(start) + dt.timedelta(days=it_field["duration"] - 1)).isoformat()
        tasks.append({"id": f"#{num}" if num else it.get("id", "")[-6:], "title": it.get("title") or content.get("title", ""),
                      "status": str(low.get("status", "todo")), "phase": str(low.get("milestone", {}).get("title", "")
                      if isinstance(low.get("milestone"), dict) else low.get("phase", "") or ""),
                      "owner": ", ".join(low.get("assignees") or []), "start": start, "end": end,
                      "days": float(low.get("estimate") or low.get("size days") or 1), "depends": [],
                      "issue": str(num or ""), "url": content.get("url", "")})
    return tasks


# ---------- scheduling ----------

def schedule(tasks, project_start):
    by_id = {t["id"]: t for t in tasks}
    for t in tasks:
        t["depends"] = [d for d in t.get("depends", []) if d in by_id]
    done, order, visiting = set(), [], set()

    def visit(t):
        if t["id"] in done:
            return
        if t["id"] in visiting:
            sys.exit(f"Dependency cycle at {t['id']}")
        visiting.add(t["id"])
        for d in t["depends"]:
            visit(by_id[d])
        visiting.discard(t["id"]); done.add(t["id"]); order.append(t)

    for t in tasks:
        visit(t)
    for t in order:
        s, e = parse_date(t.get("start")), parse_date(t.get("end"))
        if not s:
            dep_end = max((by_id[d]["_end"] for d in t["depends"]), default=None)
            s = next_workday(dep_end + dt.timedelta(days=1)) if dep_end else next_workday(project_start)
        if not e:
            e = add_workdays(s, float(t.get("days") or 1))
        t["_start"], t["_end"] = s, max(e, s)
        t["days"] = t.get("days") or workdays_between(s, e)
    # critical path: longest chain ending at the latest finish
    finish = {}
    for t in order:
        prev = max(t["depends"], key=lambda d: finish[d][0], default=None)
        finish[t["id"]] = ((t["_end"]), prev)
    tail = max(order, key=lambda t: t["_end"])["id"] if order else None
    crit = set()
    while tail:
        crit.add(tail)
        tail = finish[tail][1]
    for t in tasks:
        st = str(t.get("status", "")).lower()
        t["_state"] = "done" if st in DONE else "active" if st in ACTIVE else "blocked" if st in BLOCKED else "todo"
        t["_crit"] = t["id"] in crit
    return tasks


# ---------- output ----------

def mermaid(tasks, title):
    lines = ["```mermaid", "gantt", f"    title {title}", "    dateFormat YYYY-MM-DD", "    excludes weekends"]
    phases = {}
    for t in tasks:
        phases.setdefault(t.get("phase") or "Tasks", []).append(t)
    for ph, ts in phases.items():
        lines.append(f"    section {ph}")
        for t in ts:
            tags = [x for x in ("done" if t["_state"] == "done" else "active" if t["_state"] == "active" else "",
                                "crit" if t["_crit"] else "") if x]
            tid = re.sub(r"\W", "_", t["id"])
            label = re.sub(r"[:#;]", " ", f"{t['id']} {t['title']}").strip()
            lines.append(f"    {label} :{', '.join(tags + [tid])}, {t['_start']}, {t['_end'] + dt.timedelta(days=1)}")
    lines.append("```")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--plan"); src.add_argument("--json")
    src.add_argument("--github-project", nargs=2, metavar=("OWNER", "NUMBER"))
    p.add_argument("--start", help="project start date (default: today)")
    p.add_argument("--title", default="Project schedule")
    p.add_argument("--out"); p.add_argument("--mermaid")
    a = p.parse_args()
    if not (a.out or a.mermaid):
        a.out = "gantt.html"
    tasks = from_plan(a.plan) if a.plan else json.load(open(a.json)) if a.json else from_github(*a.github_project)
    start = parse_date(a.start) or dt.date.today()
    tasks = schedule(tasks, start)
    if a.mermaid:
        open(a.mermaid, "w").write(mermaid(tasks, a.title) + "\n"); print(f"Wrote {a.mermaid}")
    if a.out:
        data = {"title": a.title, "today": dt.date.today().isoformat(), "tasks": [
            {k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in t.items()} for t in tasks]}
        page = TEMPLATE.replace("__TITLE__", html.escape(a.title)).replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
        open(a.out, "w").write(page); print(f"Wrote {a.out}")


TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>
:root{--bg:#fbfaf8;--panel:#fff;--ink:#1d1d1b;--muted:#6b6a66;--line:#e4e2dc;--grid:#f0eee9;--wk:#f6f4f0;
 --todo:#7b8794;--active:#2b6cb0;--done:#2f8f5b;--blocked:#c8483b;--crit:#c98a1b;--today:#c8483b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161615;--panel:#1f1f1d;--ink:#ecebe7;--muted:#a19f99;--line:#34332f;
 --grid:#262624;--wk:#1b1b1a;--todo:#8d99a6;--active:#6ea8e6;--done:#4fb57e;--blocked:#e0695c;--crit:#d9a441;--today:#e0695c}}
:root[data-theme="dark"]{--bg:#161615;--panel:#1f1f1d;--ink:#ecebe7;--muted:#a19f99;--line:#34332f;--grid:#262624;--wk:#1b1b1a;
 --todo:#8d99a6;--active:#6ea8e6;--done:#4fb57e;--blocked:#e0695c;--crit:#d9a441;--today:#e0695c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
header{max-width:1400px;margin:auto;padding:20px 16px 8px}h1{font-size:20px;margin:0 0 4px}.sub{color:var(--muted)}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0 4px}.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 12px}
.stat b{display:block;font-size:18px}.stat span{color:var(--muted);font-size:12px}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:8px}.sw{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
.wrap{max-width:1400px;margin:auto;padding:8px 16px 32px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:auto}
svg text{fill:var(--ink);font-size:12px}.ph{font-weight:600}.mut{fill:var(--muted);font-size:11px}
.bar{cursor:default}.bar:hover rect.b{filter:brightness(1.12)}#tip{position:fixed;pointer-events:none;background:var(--panel);border:1px solid var(--line);
 border-radius:8px;padding:8px 10px;font-size:12px;max-width:320px;box-shadow:0 4px 14px rgba(0,0,0,.12);display:none}
</style></head><body>
<header><h1 id="t"></h1><div class="sub" id="s"></div><div class="stats" id="st"></div>
<div class="legend"><span><i class="sw" style="background:var(--done)"></i>done</span><span><i class="sw" style="background:var(--active)"></i>in progress</span>
<span><i class="sw" style="background:var(--todo)"></i>to do</span><span><i class="sw" style="background:var(--blocked)"></i>blocked</span>
<span><i class="sw" style="background:none;border:2px solid var(--crit)"></i>critical path</span><span><i class="sw" style="background:var(--today);width:2px"></i>today</span></div></header>
<div class="wrap"><div class="card"><svg id="g"></svg></div></div><div id="tip"></div>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent),T=D.tasks;const day=864e5,P=s=>new Date(s+'T00:00:00Z');
document.getElementById('t').textContent=D.title;
const min=new Date(Math.min(...T.map(t=>P(t._start))));const max=new Date(Math.max(...T.map(t=>P(t._end))));
min.setUTCDate(min.getUTCDate()-min.getUTCDay()+1-7*(min.getUTCDay()===0));const span=Math.round((max-min)/day)+3;
const n=s=>T.filter(t=>t._state===s).length;document.getElementById('s').textContent=`${T[0]._start} → ${T.reduce((a,t)=>t._end>a?t._end:a,'')} · ${T.length} tasks`;
document.getElementById('st').innerHTML=[['Done',n('done')],['In progress',n('active')],['To do',n('todo')],['Blocked',n('blocked')],['Critical path',T.filter(t=>t._crit).length+' tasks']]
 .map(([k,v])=>`<div class="stat"><b>${v}</b><span>${k}</span></div>`).join('');
const phases=[];for(const t of T){const k=t.phase||'Tasks';let p=phases.find(x=>x.k===k);if(!p)phases.push(p={k,ts:[]});p.ts.push(t)}
const svg=document.getElementById('g'),NS='http://www.w3.org/2000/svg';
function el(tag,at,parent=svg){const e=document.createElementNS(NS,tag);for(const k in at)e.setAttribute(k,at[k]);parent.appendChild(e);return e}
function draw(){svg.innerHTML='';const LW=Math.min(300,Math.max(170,innerWidth*.28)),dw=Math.max(14,Math.min(36,(Math.max(innerWidth-48,600)-LW)/span)),RH=26,TOP=58;
 const rows=phases.reduce((s,p)=>s+1+p.ts.length,0),W=LW+span*dw+20,H=TOP+rows*RH+10;svg.setAttribute('width',W);svg.setAttribute('height',H);
 const X=d=>LW+Math.round((P(d)-min)/day)*dw;
 for(let i=0;i<span;i++){const d=new Date(+min+i*day),x=LW+i*dw,wd=d.getUTCDay();if(wd===0||wd===6)el('rect',{x,y:TOP-6,width:dw,height:H-TOP,fill:'var(--wk)'});
  if(wd===1){el('line',{x1:x,x2:x,y1:TOP-16,y2:H,stroke:'var(--line)'});const tx=el('text',{x:x+3,y:TOP-22,class:'mut'});tx.textContent=d.toISOString().slice(5,10)}
  if(d.getUTCDate()===1||i===0){const tx=el('text',{x:x+3,y:14,class:'ph'});tx.textContent=d.toLocaleString('en',{month:'long',year:'numeric',timeZone:'UTC'})}}
 const pos={};let y=TOP;
 for(const p of phases){const ps=p.ts.reduce((a,t)=>t._start<a?t._start:a,'9999'),pe=p.ts.reduce((a,t)=>t._end>a?t._end:a,'');
  const tx=el('text',{x:8,y:y+17,class:'ph'});tx.textContent=p.k;el('rect',{x:X(ps),y:y+9,width:X(pe)+dw-X(ps),height:6,rx:3,fill:'var(--muted)',opacity:.5});y+=RH;
  for(const t of p.ts){const g=el('g',{class:'bar'});const lb=el('text',{x:16,y:y+17},g);const s=`${t.id} ${t.title}`;lb.textContent=s.length>LW/7?s.slice(0,LW/7-1)+'…':s;
   const x=X(t._start),w=X(t._end)+dw-x;el('rect',{class:'b',x,y:y+5,width:w,height:RH-10,rx:4,fill:`var(--${t._state==='active'?'active':t._state})`},g);
   if(t._crit)el('rect',{x:x-1,y:y+4,width:w+2,height:RH-8,rx:5,fill:'none',stroke:'var(--crit)','stroke-width':2},g);
   pos[t.id]={x1:x,x2:x+w,y:y+RH/2};g.onmousemove=e=>tip(e,t);g.onmouseleave=()=>tipEl.style.display='none';y+=RH}}
 for(const t of T)for(const d of t.depends||[]){const a=pos[d],b=pos[t.id];if(!a||!b)continue;const mx=Math.max(a.x2+6,b.x1-6);
  el('path',{d:`M${a.x2},${a.y} H${mx} V${b.y} H${b.x1-2}`,fill:'none',stroke:'var(--muted)','stroke-width':1.2,opacity:.7,'marker-end':'url(#ah)'})}
 const defs=el('defs',{});const m=el('marker',{id:'ah',viewBox:'0 0 6 6',refX:5,refY:3,markerWidth:6,markerHeight:6,orient:'auto'},defs);el('path',{d:'M0,0 L6,3 L0,6 z',fill:'var(--muted)'},m);
 if(D.today>=T.reduce((a,t)=>t._start<a?t._start:a,'9999')&&P(D.today)<=new Date(+min+span*day)){const tx=X(D.today)+dw/2;el('line',{x1:tx,x2:tx,y1:TOP-12,y2:H,stroke:'var(--today)','stroke-width':2});
  const l=el('text',{x:tx+4,y:TOP-4,class:'mut'});l.textContent='today'}}
const tipEl=document.getElementById('tip');
function tip(e,t){tipEl.style.display='block';tipEl.style.left=Math.min(e.clientX+14,innerWidth-330)+'px';tipEl.style.top=(e.clientY+14)+'px';tipEl.innerHTML='';
 const add=(k,v)=>{if(!v||(Array.isArray(v)&&!v.length))return;const d=document.createElement('div');const b=document.createElement('b');b.textContent=k+': ';d.append(b,Array.isArray(v)?v.join(', '):String(v));tipEl.appendChild(d)};
 add(t.id,t.title);add('Dates',`${t._start} → ${t._end} (${t.days} working day${t.days==1?'':'s'})`);add('Status',t.status);add('Owner',t.owner);
 add('Depends on',t.depends);add('Requirements',t.satisfies);add('Issue',t.issue&&'#'+t.issue);if(t._crit)add('Note','on the critical path: a delay here delays the end date')}
draw();addEventListener('resize',()=>{clearTimeout(window._r);window._r=setTimeout(draw,120)});
</script></body></html>
"""

if __name__ == "__main__":
    main()
