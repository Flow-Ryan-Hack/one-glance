#!/usr/bin/env python3
"""one-glance check for Claude Code.

Stop:             scores the last answer, warns the user, remembers a miss.
UserPromptSubmit: if the last answer missed, reminds Claude before the next one.

Runs only while the output style "one-glance" is active.
Set ONE_GLANCE_CHECK=off to silence it, ONE_GLANCE_LANG=de for German warnings.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

HOME = Path.home()
STATE = HOME / ".claude" / "one-glance"
MAX_WORDS = 150
MAX_LINES = 25
MAX_FIRST_LINE = 25

TEXT = {
    "en": {
        "words": "{n} words (target ≤{max})",
        "lines": "{n} lines (target ≤{max})",
        "first": "first line too long",
        "preamble": "opens with narration, not the answer",
        "closing": "ends with an offer",
        "hedge": "hedging spread out",
    },
    "de": {
        "words": "{n} Wörter (Ziel ≤{max})",
        "lines": "{n} Zeilen (Ziel ≤{max})",
        "first": "erste Zeile zu lang",
        "preamble": "Einstieg erzählt statt antwortet",
        "closing": "Schluss bietet an statt endet",
        "hedge": "Unsicherheit verstreut",
    },
}
T = TEXT.get(os.environ.get("ONE_GLANCE_LANG", "en").lower()[:2], TEXT["en"])

PREAMBLE = re.compile(
    r"^\s*(great question|good question|gute frage|sure[,!]|okay[,!]|ok[,!]|alright|"
    r"let me|i'll|i will|i have|i've|ich habe|ich werde|lass mich|zunächst|first,)",
    re.I,
)
CLOSING = re.compile(
    r"(let me know if|if you('d)? like,? i can|feel free to|happy to help|"
    r"sag bescheid|lass mich wissen|wenn du (möchtest|willst),? (kann|könnte) ich|"
    r"falls du (noch )?(fragen|etwas))",
    re.I,
)
HEDGE = re.compile(
    r"\b(maybe|perhaps|possibly|might|could potentially|vielleicht|möglicherweise|"
    r"eventuell|unter umständen|gegebenenfalls|wahrscheinlich)\b",
    re.I,
)


def active(cwd):
    if os.environ.get("ONE_GLANCE_CHECK", "").lower() == "off":
        return False
    style = None
    files = [HOME / ".claude" / "settings.json"]
    if cwd:
        files += [Path(cwd) / ".claude" / "settings.json", Path(cwd) / ".claude" / "settings.local.json"]
    for f in files:
        try:
            style = json.loads(f.read_text()).get("outputStyle", style)
        except Exception:
            pass
    return (style or "").lower() == "one-glance"


def last_answer(data):
    text = data.get("last_assistant_message")
    if isinstance(text, str) and text.strip():
        return text
    path = data.get("transcript_path")
    if not path:
        return ""
    try:
        lines = Path(path).read_text(errors="ignore").splitlines()
    except Exception:
        return ""
    for line in reversed(lines[-400:]):
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("type") != "assistant":
            continue
        content = entry.get("message", {}).get("content", [])
        if isinstance(content, str):
            return content
        parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
        if any(p.strip() for p in parts):
            return "\n".join(parts)
    return ""


def score(text):
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    lines = [l for l in prose.splitlines() if l.strip()]
    words = len(re.findall(r"\w+", prose))
    first = lines[0] if lines else ""
    misses = []
    if words > MAX_WORDS:
        misses.append(T["words"].format(n=words, max=MAX_WORDS))
    elif len(lines) > MAX_LINES:
        misses.append(T["lines"].format(n=len(lines), max=MAX_LINES))
    if len(re.findall(r"\w+", first)) > MAX_FIRST_LINE:
        misses.append(T["first"])
    if PREAMBLE.search(first):
        misses.append(T["preamble"])
    if CLOSING.search("\n".join(lines[-2:])):
        misses.append(T["closing"])
    if len(HEDGE.findall(prose)) > 3:
        misses.append(T["hedge"])
    return {"words": words, "lines": len(lines), "misses": misses}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stop"
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if not active(data.get("cwd")):
        return
    session = data.get("session_id", "unknown")
    STATE.mkdir(parents=True, exist_ok=True)
    flag = STATE / f"miss-{session}.json"

    if mode == "prompt":
        if flag.exists():
            try:
                misses = json.loads(flag.read_text()).get("misses", [])
            finally:
                flag.unlink(missing_ok=True)
            print(
                "one-glance: Your last answer failed the five-second test ("
                + ", ".join(misses)
                + "). Keep this answer to the glance card: answer in line 1, max 150 words, "
                "decision marked, no preamble, no closing offer."
            )
        return

    text = last_answer(data)
    if not text.strip():
        return
    result = score(text)
    with open(STATE / "log.jsonl", "a") as log:
        log.write(json.dumps({"t": int(time.time()), "session": session, **result}, ensure_ascii=False) + "\n")
    if result["misses"]:
        flag.write_text(json.dumps(result))
        print(json.dumps({"systemMessage": "one-glance ⚠ " + " · ".join(result["misses"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
