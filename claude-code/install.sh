#!/usr/bin/env bash
# Installs one-glance for Claude Code: output style, check hook, settings.
# Usage: ./install.sh [--lang de] [--no-default]
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
claude="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
lang="en"
make_default=1
while [ $# -gt 0 ]; do
  case "$1" in
    --lang) lang="$2"; shift 2 ;;
    --no-default) make_default=0; shift ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$claude/output-styles" "$claude/hooks/one-glance"
cp "$here/output-styles/one-glance.md" "$claude/output-styles/one-glance.md"
cp "$here/hooks/glance_check.py" "$claude/hooks/one-glance/glance_check.py"
chmod +x "$claude/hooks/one-glance/glance_check.py"

settings="$claude/settings.json"
[ -f "$settings" ] && cp "$settings" "$settings.bak-one-glance"
python3 - "$settings" "$claude/hooks/one-glance/glance_check.py" "$lang" "$make_default" <<'PY'
import json, sys
from pathlib import Path
path, script, lang, make_default = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4] == "1"
cfg = json.loads(path.read_text()) if path.exists() else {}
hooks = cfg.setdefault("hooks", {})
for event, mode in (("Stop", "stop"), ("UserPromptSubmit", "prompt")):
    groups = hooks.setdefault(event, [])
    groups[:] = [g for g in groups if not any("glance_check.py" in h.get("command", "") for h in g.get("hooks", []))]
    groups.append({"hooks": [{"type": "command", "command": f'python3 "{script}" {mode}', "timeout": 10}]})
if lang != "en":
    cfg.setdefault("env", {})["ONE_GLANCE_LANG"] = lang
if make_default:
    cfg["outputStyle"] = "one-glance"
path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
PY

echo "one-glance installed."
[ "$make_default" = 1 ] && echo "Active in new sessions. Switch off: /output-style default" \
                        || echo "Switch on: /output-style one-glance"
