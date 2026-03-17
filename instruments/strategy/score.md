# Problem
Rank a revenue opportunity before investing agent time in it.

# Solution
1. Score the opportunity from 0 to 10 on these dimensions:
   - revenue
   - speed
   - automation
   - resilience
   - trust
   - capital efficiency
   - legal safety
   - platform dependency
2. Run the instrument:

```bash
bash /a0/instruments/strategy/score.sh \
  --name "Autonomous Listing Concierge" \
  --revenue 8 \
  --speed 7 \
  --automation 7 \
  --resilience 7 \
  --trust 8 \
  --capital 8 \
  --legal 8 \
  --platform 5
```

3. Read the result:
   - **GO**: attractive and compliant enough to execute now
   - **HOLD**: promising but needs more validation or risk reduction
   - **REJECT**: weak economics or unacceptable legal/compliance posture

# Notes
- Higher is better for every score except `platform`, where lower dependency is better.
- The instrument hard-rejects ideas that appear to rely on personal-data resale, contact-list brokering, spam, or inbox scraping for resale.
- Use `--notes` to pass a short description if the opportunity name alone does not explain the model.
