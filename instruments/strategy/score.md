# Strategy Scoring Instrument

Use `/workspace/instruments/strategy/score.sh` to classify a monetization lane as:

- `PASS`: compliant and operationally attractive enough to activate now
- `HOLD`: compliant but not attractive or mature enough yet
- `REJECT`: blocked by legality, consent, provenance, or platform-policy issues

## Inputs

The script expects ten positional arguments:

1. lane name
2. legality: `low|medium|high`
3. consent: `low|medium|high`
4. provenance: `low|medium|high`
5. tos_fit: `low|medium|high`
6. time_to_cash: `low|medium|high`
7. margin: `low|medium|high`
8. repeatability: `low|medium|high`
9. automation_fit: `low|medium|high`
10. defensibility: `low|medium|high`

## Hard gates

The lane is automatically `REJECT` when any of these are `low`:

- legality
- consent
- provenance
- tos_fit

This prevents activation of strategies involving non-consensual inbox access,
scraped contact resale, unclear data ownership, or platform terms violations.

## Soft execution factors

Operational readiness is derived from:

- time_to_cash
- margin
- repeatability
- automation_fit
- defensibility

Classification rules:

- `PASS`: all hard gates clear and none of the soft factors are `low`
- `HOLD`: all hard gates clear but at least one soft factor is `low`
- `REJECT`: any hard gate is `low`

## Example runs

```bash
bash /workspace/instruments/strategy/score.sh \
  "Opt-in niche lead magnet" high high high high high medium high high medium

bash /workspace/instruments/strategy/score.sh \
  "Client-owned inbox triage" high high high high medium low high high medium

bash /workspace/instruments/strategy/score.sh \
  "Email list brokerage" low low low low high high high high high
```
