# Agentic Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build OAuth-based Gmail connector with explicit scope + account consent logging | Data Ops Agent | Must store token provenance and revocation handling |
| P0 | Add consent-state schema (`opt_in`, `transactional_only`, `do_not_contact`) to contact pipeline | Risk & Compliance Governor | Required before any outreach |
| P0 | Implement suppression and unsubscribe enforcement in campaign execution | Monetization Agent | Blocking requirement for outbound messaging |
| P1 | Integrate Orange workflow export/import for segment scoring | Data Ops Agent | Keep consent fields immutable through transformations |
| P1 | Create KPI dashboard for CAC, LTV, conversion, and compliance incidents | Treasury Controller | Weekly automated report |
| P1 | Add automated policy lint step before campaign launch | Risk & Compliance Governor | Fail closed on unknown consent states |
| P2 | Create paper-trading evaluation harness with drawdown alerts | Trading Research Agent | Sim-only until thresholds met |
| P2 | Build course chapter templates from mission diary entries | Content Studio Agent | Enables rapid tutorial production |

