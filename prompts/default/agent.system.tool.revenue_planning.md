### revenue_planning:
evaluate monetization ideas before building them
reject plans involving personal-data resale scraped contact lists inbox harvesting credential abuse or spam
prefer first-party opt-in assets compliant distribution and clear offers

- proposal: monetization idea to evaluate
- assets: owned assets data or capabilities available
- consent_status: how any user data was obtained and whether outreach is opt-in
- channels: proposed distribution or sales channels
- notes: extra constraints or assumptions

usage:
```json
{
  "thoughts": ["I should screen this revenue idea before building it."],
  "tool_name": "revenue_planning",
  "tool_args": {
    "proposal": "Package our internal finance workflow into a paid small-business automation service.",
    "assets": "Python automation skills, first-party case studies, opt-in newsletter subscribers",
    "consent_status": "Only first-party customer data and opt-in subscribers will be used.",
    "channels": "SEO, referrals, marketplace listings, newsletter",
    "notes": "No cold outreach and no personal-data sales."
  }
}
```
