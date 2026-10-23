# Visual patterns

A picture beats a sentence when the eye can compare, follow or locate faster than it can read.
Every pattern below works in a plain monospace terminal. Each has an HTML variant for when the
terminal is not enough.

**Read class:** *instant* is under 1 second, the eye does the work. *short* is 2–10 seconds, the
reader follows a path or scans a grid.

**Rules for all patterns**

- One diagram per answer. It replaces prose, it does not decorate it.
- Max 80 characters wide, max 20 lines. Bigger: build an HTML page and link it.
- Label every mark. A bar without a number, a box without a name, is noise.
- Use only characters that are one cell wide: box drawing `─│┌┐└┘├┤┬┴┼`, blocks `█▓▒░▏`,
  arrows `→ ← ↓ ↑`, marks `✓ ✗ ●  ○`. Keep `⚠` and emoji out of aligned layouts; some terminals
  draw them two cells wide.

| # | Pattern | Use it for | Read class |
|---|---|---|---|
| 1 | [Bar comparison](#1-bar-comparison) | amounts side by side | instant |
| 2 | [Sparkline](#2-sparkline) | a trend over time | instant |
| 3 | [Progress](#3-progress) | how far a job is | instant |
| 4 | [Status grid](#4-status-grid) | many items × few checks | instant |
| 5 | [Before / after](#5-before--after) | what changed | short |
| 6 | [Flow](#6-flow) | steps, a pipeline | short |
| 7 | [Tree](#7-tree) | hierarchy, folders, structure | short |
| 8 | [Timeline](#8-timeline) | events in order, deadlines | short |
| 9 | [Decision tree](#9-decision-tree) | if-this-then-that choices | short |
| 10 | [2×2 matrix](#10-22-matrix) | items on two criteria | short |
| 11 | [Heatmap](#11-heatmap) | intensity over two axes | instant |
| 12 | [Sequence](#12-sequence) | who talks to whom, in order | short |
| 13 | [Dependencies](#13-dependencies) | what blocks what | short |
| 14 | [Scale with reference](#14-scale-with-reference) | a size nobody can feel | instant |
| 15 | [Where am I](#15-where-am-i) | coming back to a session cold | instant |

---

## 1. Bar comparison

**Fits:** 2–8 amounts of the same unit. Costs, counts, durations.

```
Monthly cost at 5,000 contacts
Mailchimp  ████████████████████ 100 €
Brevo      ████████████          59 €
Sendy      ███                   15 €
```

Longest bar = 20 cells. Scale the rest to it, round to whole cells, number right-aligned.
**HTML:** horizontal bar chart, value label at the bar end, highlight the recommended row.

## 2. Sparkline

**Fits:** one series over time where the shape matters more than each value.

```
Signups, last 12 weeks   ▁▂▂▃▃▅▄▆▇▆▇█   212 → 488 (+130 %)
Churn                    ▅▅▄▄▄▃▃▃▂▂▂▁   4.1 % → 1.2 %
```

Eight levels: `▁▂▃▄▅▆▇█`. Always add first value, last value and the change.
**HTML:** small area chart with the last point marked and labelled.

## 3. Progress

**Fits:** a job with steps or a known total.

```
Migration   ▓▓▓▓▓▓▓░░░  7 / 10 steps   next: DNS switch
Tests       ▓▓▓▓▓▓▓▓▓▓  248 / 248 ✓
```

10 cells, one cell = 10 %. Say what comes next.
**HTML:** segmented progress bar, done segments filled, current segment outlined.

## 4. Status grid

**Fits:** several items checked against the same few criteria.

```
            build  tests  lint  deploy
web           ✓      ✓     ✓      ✓
api           ✓      ✗     ✓      ·
worker        ✓      ✓     ✗      ·
docs          ✓      ·     ✓      ✓

✗ 2 failing  · 3 not run
```

`✓` passed, `✗` failed, `·` not run. Put the summary under the grid.
**HTML:** table with coloured cells, failed cells first in sort order.

## 5. Before / after

**Fits:** a change to text, config, numbers or a plan.

```
  timeout     30 s   →  10 s
  retries      0     →   3
- cache       off
+ cache       on (5 min)
```

Arrows for changed values, `-` and `+` for removed and added lines. Only show what changed.
**HTML:** two columns side by side, changed cells highlighted.

## 6. Flow

**Fits:** steps that follow each other, a pipeline, a request path.

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Draft  │ →  │  Check  │ →  │  Clean  │ →  │  Post   │
└─────────┘    └────┬────┘    └─────────┘    └─────────┘
                    │ fails
                    ↓
               ┌─────────┐
               │ Rewrite │
               └─────────┘
```

Max 5 boxes in a row, one word per box, all boxes the same width. Label side exits.
A straight sequence without branches needs no boxes: `Draft → Check → Clean → Post`.
**HTML:** Mermaid `flowchart LR`, or an SVG with the same boxes.

## 7. Tree

**Fits:** folders, an org chart, a breakdown of a whole into parts.

```
one-glance/
├── RULES.md            the ten rules
├── PATTERNS.md         this file
├── claude-code/
│   ├── install.sh      sets everything up
│   ├── hooks/          the glance check
│   └── output-styles/  the mode
└── snippets/           for other tools
```

Comments in one column on the right. Cut deep levels to `…`.
**HTML:** collapsible list, or a treemap when sizes matter.

## 8. Timeline

**Fits:** events in order, deadlines, a history.

```
Oct ──●────────●────────────●──────────●──── Nov
     14       18           24         31
   brief    draft     review due    launch
                          ▲ today
```

Dots on one line, dates above or below, labels under. Mark today.
**HTML:** horizontal timeline with today as a vertical line.

## 9. Decision tree

**Fits:** a choice that depends on one or two conditions.

```
More than 20k mails a month?
├── yes → Brevo        saves ~40 %
└── no  → Shopify sync needed?
          ├── yes → stay on Mailchimp
          └── no  → Brevo
```

Questions end with `?`, answers end with a recommendation. Max 3 levels.
**HTML:** clickable questions that reveal the next branch.

## 10. 2×2 matrix

**Fits:** placing items on two criteria, such as effort and impact.

```
                 low effort        high effort
              ┌─────────────────┬─────────────────┐
 high impact  │ ● caching       │ ● rewrite API   │
              │ ● fix retries   │                 │
              ├─────────────────┼─────────────────┤
 low impact   │ ● rename vars   │ ● new UI kit    │
              └─────────────────┴─────────────────┘
→ start top left
```

Name both axes. Put the reading direction under the box.
**HTML:** scatter plot with labelled points and quadrant shading.

## 11. Heatmap

**Fits:** intensity across two dimensions, such as hours × days.

```
        Mo  Tu  We  Th  Fr
 9–12   ░░  ▒▒  ▓▓  ▓▓  ░░
12–15   ▒▒  ██  ██  ▓▓  ▒▒
15–18   ░░  ▒▒  ▓▓  ░░  ░░

░ low  ▒  ▓  █ high   peak: Tu–We 12–15
```

Four shades, legend in one line, name the peak.
**HTML:** colour grid with a sequential colour scale and the value on hover.

## 12. Sequence

**Fits:** messages between actors in order. Login flows, handoffs, approvals.

```
You         Claude         Hook           Log
 │  prompt     │             │             │
 │────────────→│             │             │
 │             │  answer     │             │
 │             │────────────→│             │
 │             │             │  score      │
 │             │             │────────────→│
 │  warning    │             │             │
 │←──────────────────────────│             │
```

Actors as columns, time goes down. One arrow per line.
**HTML:** Mermaid `sequenceDiagram`.

## 13. Dependencies

**Fits:** what must happen before what. Blockers, build order.

```
domain ──→ DNS ──→ SSL ──┐
                         ├──→ launch
copy ──→ review ─────────┘

blocked: SSL waits for DNS (24 h)
```

Arrows point from the thing needed to the thing that needs it. Name the blocker below.
**HTML:** directed graph, blocked nodes in the warning colour.

## 14. Scale with reference

**Fits:** a number nobody can feel. Sizes, durations, money, tokens.

```
Your prompt    ▏                            2,000 tokens
A novel        ███                        120,000 tokens
Context window ████████████████████████ 1,000,000 tokens
```

Put the unknown next to one or two things the reader knows. Linear scale, longest bar = 24 cells.
When a bar would round to zero, draw `▏` so it still shows. Ranges over 1000×: log scale, and say so.
**HTML:** bars on a log axis with the reference items in grey.

## 15. Where am I

**Fits:** the first answer after a break, or any answer in a long multi-session job.

```
Newsletter move                               session 3 of 5
──────────────────────────────────────────────────────────────
done     ✓ cost compare   ✓ export   ✓ template rebuild
now      ● DNS records for the sending domain
next     ○ test send   ○ switch list   ○ cancel Mailchimp
you      → approve the sender name "Team Hack"
```

Four fixed rows: done, now, next, you. Same order every time, so the eye knows where to look.
**HTML:** stepper with the current step highlighted and the decision as a button.
