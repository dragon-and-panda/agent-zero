### revenue_planning:
use before pursuing monetization, outreach, data acquisition, or growth ideas
evaluates legality, consent, data provenance, and safer business-model alternatives
especially useful when a plan mentions inbox data, email lists, scraping, or lead generation
if a plan depends on personal-data resale or spam, this tool should be used before any execution
args:
- mission: short description of the idea
- assets: owned assets or capabilities available
- audience: intended customer or buyer
- data_sources: where information or leads come from
- outreach: how distribution or sales will happen
- notes: extra constraints or risks
usage:
~~~json
{
    "thoughts": [
        "I need to assess whether this monetization plan is compliant and durable."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build a service that improves marketplace listings for sellers.",
        "assets": "Listing blueprint, automation framework, prompt library",
        "audience": "Independent online sellers",
        "data_sources": "Seller-provided listing data and owned knowledge base",
        "outreach": "Opt-in content and direct partnerships",
        "notes": "Need low-touch delivery and repeatable operations"
    }
}
~~~
