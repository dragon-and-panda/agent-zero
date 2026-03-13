# Problem
Validate consent eligibility before outreach or transactional messaging.

# Solution
1. Prepare a CSV file with required columns: `email`, `contact_status`.
2. Run the instrument:
   - Outreach mode (strict opt-in):  
     `bash /workspace/instruments/financial_system/consent_audit.sh "/path/to/contacts.csv" outreach`
   - Transactional mode (`opt_in` + `transactional_only`):  
     `bash /workspace/instruments/financial_system/consent_audit.sh "/path/to/contacts.csv" transactional`
3. Read JSON output summary and ensure:
   - `rows_invalid` is `0`
   - eligible ratio matches campaign requirements
4. If the script exits with non-zero, fix data quality before proceeding.
