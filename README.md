# Campus Mobile Order Receipt Analyzer

## What it Does
This project analyzes campus food spending by processing mobile order receipt emails. It ingests exported Outlook `.eml` files, filters for relevant receipt messages, and uses a large language model (GPT-4o-mini) to extract structured data such as vendor, timestamp, location, and item-level pricing. The data is then cleaned, normalized, and categorized into meaningful food groups (e.g., meals, sides, drinks). Finally, the system presents interactive visualizations in a Streamlit dashboard, including monthly spending trends, category breakdowns, and time-of-day spending patterns, enabling users to better understand their consumption habits and spending behavior while at Duke.

## Quick Start
1. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create a `.env` file in the project root and add your OpenAI API key:
   OPENAI_API_KEY=your_key_here

4. Export emails from Outlook:
   - In Outlook, navigate to your inbox or a specific folder.
   - Filter emails by a desired date range.
   - Select the emails in that range.
   - Drag and drop them into the folder:
     data/exported_emails/
   - This will save each email as a `.eml` file.

5. Load and filter receipt emails:
   python3 -m scripts.run_fetch

6. Parse emails into structured data using the LLM:
   python3 -m scripts.run_parse

7. Clean and categorize the parsed data:
   python3 -m scripts.run_clean

8. Launch the interactive dashboard:
   streamlit run app.py

## Video Links
https://youtube.com/@cdler8778?si=rtlVzbaFUs6nOXYU

## Evaluation

### Overview
I evaluated the performance of my system in extracting structured data from unstructured receipt emails and improving extraction reliability through prompt design. The evaluation focuses on how different prompt strategies affect the accuracy and consistency of the LLM outputs.

---

### Prompt Engineering

I tested three prompt designs to evaluate how prompt structure influences model performance:

| Prompt        | Vendor Accuracy | Total Accuracy | Parse Success Rate |
|---------------|----------------|----------------|---------------------|
| Zero-shot     | 0.0            | 0.0            | 1.0                 |
| Strict JSON   | 1.0            | 1.0            | 1.0                 |
| Few-shot      | 1.0            | 1.0            | 1.0                 |

- **Zero-shot prompt**: A basic extraction instruction without formatting constraints.
- **Strict JSON prompt**: Enforced a structured schema and required JSON-only output.
- **Few-shot prompt**: Included an example mapping from receipt text to structured JSON.

The results show that the zero-shot prompt failed to extract correct values despite producing valid JSON during the parsing process. In contrast, both structured and few-shot prompts achieved perfect extraction accuracy, demonstrating that prompt design plays a critical role in guiding LLM behavior.

---

### Evaluation Metrics

I evaluated model performance using six quantitative metrics to capture both correctness and structural reliability:

- **Vendor Accuracy**: Whether the correct vendor name was extracted.
- **Timestamp Accuracy**: Whether the correct transaction time was extracted and normalized.
- **Location Accuracy**: Whether the correct location was extracted.
- **Total Accuracy**: Whether the correct transaction total was extracted.
- **Exact Match Rate**: Whether all fields for a receipt were perfectly correct.
- **Parse Success Rate**: Whether the model output could be successfully parsed into valid JSON.

Example evaluation results are shown below:

| Metric                | Value |
|----------------------|-------|
| Vendor Accuracy      | 1.00  |
| Timestamp Accuracy   | 1.00  |
| Location Accuracy    | 1.00  |
| Total Accuracy       | 1.00  |
| Exact Match Rate     | 0.00  |
| Parse Success Rate   | 1.00  |

These results indicate that the model is highly reliable at extracting individual fields, achieving perfect accuracy across all core attributes. The parse success rate of 1.00 also confirms that the structured prompting approach consistently produces valid JSON outputs.

However, the exact match rate remains 0.00. This is due to minor formatting differences between predicted and ground truth values, such as variations in timestamp formatting (e.g., `"2026-01-27 11:25 AM"` vs `"2026-01-27T11:25:00"`) or location strings (e.g., `"Brodhead Center, Duke University"` vs `"Brodhead Center"`). These discrepancies highlight a limitation of highly strict equality-based evaluation rather than a failure of the model to capture the correct information.

Overall, these metrics demonstrate that the model successfully extracts the correct semantic information, even when minor formatting differences prevent a perfect exact match. This reinforces the importance of normalization when evaluating LLM outputs in real-world applications.

---

### Error Analysis

Initial evaluation revealed that the zero-shot prompt produced outputs that were structurally valid but semantically incorrect. For example, vendor names and totals were often misidentified or omitted.

Further analysis showed that:
- The model struggled with ambiguous formatting in raw HTML email content.
- Without explicit structure, the model did not consistently identify key fields.

By introducing structured prompts and examples, I eliminated these errors, achieving consistent and accurate extraction across all tested inputs.

An example error report is shown below:

| Message ID               | Error Type     | Predicted Total | Ground Truth Total | Pred Location |Ground Truth Location |
|-------------------------|----------------|-----------------|--------------------|------------------------------------------------------|
| #113640340 Receipt.eml  | total_mismatch | 12.89           | 4.29               | Brodhead Center, 416 Chapel Drive, Duke University   | Brodhead Center        |
| #115358697 Receipt.eml  | total_mismatch | 5.68            | 2.34               | McClendon Tower, 101 Wannamaker Dr, Duke University  | McClendon Tower        |
| #111442289 Receipt.eml  | total_mismatch | 4.29            | 12.78              | Brodhead Center, Duke University                    | Brodhead Center        |

#### Interpretation

At first glance, these results suggest poor model performance. However, a closer inspection reveals that the model outputs are actually **correct**, but are being compared against the wrong ground truth entries.

For example:
- A predicted total of `$12.89` is paired with a ground truth value of `$4.29`, even though both values correspond to different receipts.
- Similarly, predicted totals such as `$5.68` and `$4.29` match valid receipts but are misaligned with their corresponding labels.

This indicates that the evaluation pipeline was incorrectly matching predictions and ground truth records, rather than comparing entries based on a shared identifier. Additionally, the predicted location values contain more detailed information (full addresses), while the ground truth uses simplified labels. This results in mismatches despite the model correctly identifying the relevant location. The issue was caused by evaluating predictions across the entire parsed dataset while using a ground truth file that only contained a small subset of labeled examples. Because the evaluation did not properly filter or align records by `message_id`, predictions were compared against unrelated ground truth entries.

#### Resolution

To correct this, I modified the evaluation process to:
- Filter predictions to only include emails present in the ground truth dataset
- Align predictions and labels using `message_id` as a key

After implementing this fix, the evaluation metrics accurately reflected model performance and showed near-perfect extraction accuracy.

---

### Model Improvement Iterations

I improved model performance through iterative prompt refinement, progressively increasing the level of structure and guidance provided to the LLM:

- **Iteration 1 (Zero-shot)**:
  - Vendor Accuracy: 0.0  
  - Total Accuracy: 0.0  
  - Observed issue: lack of structure led to incorrect extraction.
  - Explanation: The initial prompt provided minimal instruction, leaving the model to infer both the task and output format. As a result, the model produced inconsistent or incorrect outputs, even though it often generated valid JSON.

- **Iteration 2 (Structured Prompt)**:
  - Vendor Accuracy: 1.0  
  - Total Accuracy: 1.0  
  - Improvement: enforcing JSON format significantly increased reliability.
  - Explanation: By explicitly defining the required fields and enforcing a strict JSON schema, I reduced ambiguity in the model’s task. This constrained the output space and ensured that the model consistently returned structured, parseable data, leading to a large improvement in accuracy.

- **Iteration 3 (Few-shot Prompt)**:
  - Vendor Accuracy: 1.0  
  - Total Accuracy: 1.0  
  - Improvement: example-based prompting further stabilized output formatting and generalization.
  - Explanation: Adding a concrete input-output example allowed the model to learn the desired transformation pattern directly within the prompt. This leveraged the model’s in-context learning ability, helping it generalize more reliably across different receipt formats and maintain consistent formatting.

Overall, these iterations demonstrate that progressively increasing the amount of guidance—moving from minimal instructions, to structured constraints, to explicit examples—significantly improves LLM performance. This process highlights how prompt engineering can serve as an effective alternative to model retraining for improving accuracy and reliability.