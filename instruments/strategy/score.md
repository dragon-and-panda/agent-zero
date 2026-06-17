# Strategy Scoring Instrument

`score.sh` screens revenue lanes before they are activated.

## Inputs

Run the script with:

```bash
./instruments/strategy/score.sh <lane_name> <revenue> <speed> <defensibility> <automation_fit> <operational_ease> <legality> <consent> <provenance> <tos>
```

### Commercial scores

All commercial inputs are integers from 1 to 5.

- `revenue`: likely revenue or gross-profit impact
- `speed`: how quickly the lane can start producing value
- `defensibility`: how hard the lane is to commoditize
- `automation_fit`: how well the lane can run with limited supervision
- `operational_ease`: how simple the lane is to operate repeatedly

### Hard gates

All hard gates are `yes` or `no`.

- `legality`
- `consent`
- `provenance`
- `tos`

If any hard gate is `no`, the lane is rejected even if the commercial score is high.

## Decision Logic

- `PASS`: all hard gates pass and weighted score is at least 70
- `HOLD`: all hard gates pass but weighted score is below 70
- `REJECT`: one or more hard gates fail

## Examples

### Compliant lane

```bash
./instruments/strategy/score.sh "Inbox-to-CRM" 4 4 4 5 4 yes yes yes yes
```

### Rejected lane

```bash
./instruments/strategy/score.sh "Email list resale" 5 5 2 4 4 yes no no no
```
