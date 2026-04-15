# Strategy Score Instrument

This instrument scores a proposed revenue lane and rejects ideas that fail legality or consent checks.

## Inputs

Pass six integer scores from 0 to 10:

1. legality
2. consent
3. time_to_cash
4. repeatability
5. margin
6. repo_fit

## Example

```bash
./instruments/strategy/score.sh 10 10 7 8 7 8
```

## Output

The script prints:

- raw score and normalized percentage;
- decision: GO, HOLD, or REJECT;
- short rationale.

## Gates

- legality below 8 => REJECT
- consent below 8 => REJECT

Even if other scores are high, the lane is rejected when it depends on weak legality or weak consent.
