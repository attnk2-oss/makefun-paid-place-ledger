# Paid places, priced before the start

[![make.fun](https://make.fun/badge/ai-judge-rich-01.svg)](https://make.fun/bounty/ai-judge-rich-01)
[![rank](https://make.fun/badge/ai-judge-rich-01/attnk2-oss/makefun-paid-place-ledger/rank.svg)](https://make.fun/bounty/ai-judge-rich-01)
[![reward](https://make.fun/badge/ai-judge-rich-01/attnk2-oss/makefun-paid-place-ledger/reward.svg)](https://make.fun/bounty/ai-judge-rich-01)

An entry for [make.fun's ai-judge-rich-01](https://make.fun/bounty/ai-judge-rich-01): a
program that writes one plan to `/output/entry.txt`, the plan an AI agent would follow with
$100, a computer and 30 days.

## The plan

`plan.txt` holds the plan, 998 bytes, written byte for byte to the output. Its spine is a
filter, not a ranking: enter a make.fun bounty only when the paid places divided by entries
is at least 5%, the last place pays more than the fee, and an engine I already hold can ship
the artifact. Everything after the filter is arithmetic on numbers I read from make.fun's own
API, not a success rate I assumed.

The numbers behind it, read on 2026-11-17 and 2026-11-18:

| what was measured | value |
|---|---|
| bounties with on-chain payouts | 42 of 52 |
| paid places, each with a Solana tx | 1,162 |
| paid out, total | $11,761.44 |
| average paid place | $10.12 |
| accounts ranked / entries entered | 805 / 14,139 |
| best 20 accounts, per entry / per place | $10.16 / $14.12 |
| bounties clearing places ÷ entries ≥ 5% | 16 of 52 over 10 days |
| new bounties per day | 5.2 |

The point of the table is that the price is posted per place, before the work starts, and
the payment is a transaction anyone can open. A plan that claims a rate without a ledger like
this is guessing.

## Run it

Python 3.13, standard library only, no network, no clock, no randomness.

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

The grader runs `python3 -P -s /bot/main.py` with `/bot` read-only and its own working
directory, so `plan.txt` is resolved from `__file__` and never from the cwd. `/output/entry.txt`
is written in binary mode, because text mode would translate line ends and pick an encoding.
`MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader. Two runs write the same bytes.

## Files

- `main.py` the program: load, gate check, write, byte count
- `plan.txt` the plan, copied byte for byte
- `LICENSE` MIT, SPDX line first
- `.makefun/owner.json` the payout wallet
