#!/usr/bin/env python3
"""PreToolUse hook: block destructive git commands and direct pushes to protected branches.
Exit code 2 blocks the command and shows the reason to the agent, which must then ask the user."""
import json, re, sys

# Exact branch names, plus prefixes ending in "/" that protect a whole namespace.
PROTECTED = ("main", "master", "develop", "dev", "release/")
_exact = [re.escape(p) for p in PROTECTED if not p.endswith("/")]
_prefix = [re.escape(p) + r"[\w./-]+" for p in PROTECTED if p.endswith("/")]
# A push target is a whole word: optional "src:" (e.g. HEAD:main) and optional refs/heads/,
# then the branch, then whitespace or the end of the command. So "dev" is protected but
# "dev-tools", "maintenance-fix" and "feat/dev" are not.
PROTECTED_REF = (r"\s(?:\S*:)?(?:refs/heads/)?(?:" + "|".join(_exact + _prefix) + r")(?=\s|$|[;&|])")
RULES = [
    (r"\bgit\s+push\b[^;&|]*\s(--force(?!-with-lease)|-f\b)", "force push (use --force-with-lease, and only with user approval)"),
    (r"\bgit\s+reset\s+[^;&|]*--hard", "git reset --hard discards work"),
    (r"\bgit\s+clean\s+[^;&|]*-[a-z]*f", "git clean -f deletes untracked files"),
    (r"\bgit\s+branch\s+[^;&|]*-D\b", "git branch -D deletes unmerged work"),
    (r"\bgit\s+checkout\s+[^;&|]*--\s+\.", "git checkout -- . discards all local changes"),
    (r"\bgit\s+restore\s+[^;&|]*(\s\.|--staged\s+\.)", "git restore . discards all local changes"),
    (r"\bgit\s+push\b[^;&|]*?" + PROTECTED_REF, "direct push to a protected branch (open a PR instead)"),
    (r"\bgh\s+pr\s+merge\b", "merging a PR needs explicit user approval"),
    (r"\bgh\s+api\b[^;&|]*branches/[^;&|]*/protection[^;&|]*(-X|--method)\s*(PUT|DELETE|PATCH)", "changing branch protection"),
]

try:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)
for pattern, why in RULES:
    if re.search(pattern, cmd):
        print(f"Blocked by total-skills git guard: {why}. Ask the user for explicit approval; "
              "if they approve, they can run it themselves or temporarily disable the hook.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
