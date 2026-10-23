# one-glance

**AI output has to be understood at a glance.** Any model, any tool, any use case.

If a person needs more than a few seconds to know what the AI found, the output failed.
Length, format and medium are tools. The glance is the goal.

## Before

> **Q:** Should we move our newsletter from Mailchimp to Brevo?
>
> Great question! Choosing an email marketing platform is an important decision that depends on many factors. Both Mailchimp and Brevo are popular tools with their own strengths. Mailchimp is known for its user-friendly interface and wide range of integrations, while Brevo offers competitive pricing, especially for larger contact lists. Let's look at some key considerations. First, pricing: ...
>
> *(400 more words)*

## After

> **Yes, if you send more than 20k mails a month.** Brevo costs about 40 % less at your volume.
>
> | | Mailchimp | Brevo |
> |---|---|---|
> | Price at 5k contacts | 100 € | 59 € |
> | Your 6 integrations | 6 | 5 (no Shopify sync) |
>
> **Your call:** Can you live without the Shopify sync?

## The rules

Ten rules in [RULES.md](RULES.md). The first one carries most of the weight: **the answer comes first.**

## The test

Show the output to someone for five seconds. Ask two things:

1. What is the result?
2. What do I have to do?

Two right answers: pass. Anything else: rewrite.

## Install

Claude Code, macOS or Linux, needs `git` and `python3`:

```sh
git clone https://github.com/Flow-Ryan-Hack/one-glance.git
./one-glance/claude-code/install.sh            # add --lang de for German warnings
```

Start a new session. The mode is on. Switch it off with `/output-style default`.

No git? Download the [latest release](https://github.com/Flow-Ryan-Hack/one-glance/releases/latest) as a zip, unpack it and run `claude-code/install.sh`.

## Use it

| Where | File | How |
|---|---|---|
| Visual patterns | [PATTERNS.md](PATTERNS.md) | 15 terminal diagrams, each with an HTML variant |
| HTML page | [`templates/glance-page.html`](templates/glance-page.html) | Starting point when the terminal is not enough |
| Claude Code | [`claude-code/`](claude-code/) | `./claude-code/install.sh` (add `--lang de` for German warnings) |
| CLAUDE.md, AGENTS.md | [`snippets/CLAUDE.md`](snippets/CLAUDE.md) | Paste the block |
| Cursor | [`snippets/one-glance.mdc`](snippets/one-glance.mdc) | Copy to `.cursor/rules/` |
| Claude, ChatGPT, other chat apps | [`snippets/custom-instructions.md`](snippets/custom-instructions.md) | Paste into custom instructions |

### Claude Code

The installer sets up three things:

1. **Output style `one-glance`.** Switches Claude into the mode. Toggle with `/output-style`.
2. **The glance card and visual patterns.** Every answer ends in the same shape: topic and answer, up to three findings, the one decision. See [CARD.md](CARD.md) and [PATTERNS.md](PATTERNS.md).
3. **The glance check.** A hook scores every answer: words, lines, first line, preamble, closing offers, hedging. A miss shows a one-line warning and reminds Claude before the next answer. Scores go to `~/.claude/one-glance/log.jsonl`.

Switch the check off with `ONE_GLANCE_CHECK=off`.

## Deutsch

Regeln auf Deutsch: [de/REGELN.md](de/REGELN.md).

## License

MIT
