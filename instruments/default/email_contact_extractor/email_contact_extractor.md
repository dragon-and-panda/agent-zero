# Problem
Build a de-duplicated contact dataset from mailbox exports and related text files.

# Solution
1. Ensure your input data belongs to you or you have permission to process it.
2. Run:
   `bash /a0/instruments/default/email_contact_extractor/email_contact_extractor.sh "<input_path>" "<output_csv>" "<owner_email>"`
3. Optional: pass extra flags after the owner email:
   - `--scan-body`
   - `--min-mentions 2`
4. Import the generated CSV into Orange for filtering, scoring, and segmentation.
