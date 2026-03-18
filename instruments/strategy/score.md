# Strategy Scoring Instrument

`score.sh` ranks candidate revenue tracks from `docs/strategy/incoming.md`.

## Purpose

- Give the orchestrator a repeatable way to prioritize legal and ethical revenue paths.
- Penalize ideas that are slow, risky, capital-intensive, or hard to automate.
- Block ideas that are already classified as `REJECT` in the compliance pack.

## Input format

The default input is the Markdown table in `docs/strategy/incoming.md` with these columns:

1. `id`
2. `opportunity`
3. `compliance`
4. `automation_fit`
5. `speed_to_revenue`
6. `effort`
7. `risk`
8. `capital_required`
9. `redundancy`
10. `notes`

## Scoring model

Fields use a 1-5 scale.

- Positive weights:
  - automation fit: 25
  - speed to revenue: 20
  - redundancy: 15
- Inverted weights:
  - effort: 10
  - risk: 20
  - capital required: 10

The total is normalized to a 0-100 score.

## Decision logic

- `REJECT` compliance status always returns `REJECT`.
- `HOLD` compliance status always returns `HOLD`.
- `GO` status becomes:
  - `GO` at score >= 75
  - `VALIDATE` at score >= 60
  - `HOLD` below 60

## Usage

```bash
bash instruments/strategy/score.sh
```

Optional custom file:

```bash
bash instruments/strategy/score.sh docs/strategy/incoming.md
```
