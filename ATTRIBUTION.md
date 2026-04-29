
---

# `ATTRIBUTION.md`

```markdown
# Attribution of AI Tool Usage

This project was developed with the assistance of a large language model (ChatGPT) as a coding support tool. The AI was used primarily to accelerate development, improve code correctness, and provide guidance on structuring components of the system.

---

## How AI Was Used

The language model was used in the following ways:

- **Syntax correction and debugging**:  
  The AI helped identify and fix common Python issues such as import errors, function definitions, and data handling bugs.

- **Code scaffolding and structure**:  
  It provided initial outlines for modules of which I was not fully capable of drafting such as the email ingestion pipeline, LLM parsing logic, and Streamlit visualization components.

- **Prompt design assistance**:  
  The AI suggested variations of prompts (zero-shot, structured, and few-shot) that were later tested and refined as part of the prompt engineering process.

- **Refinement of logic and edge cases**:  
  It assisted in improving robustness, such as handling malformed JSON outputs, normalizing evaluation comparisons, and aligning prediction results with ground truth data.

- **Documentation support**:  
  The AI helped refine README sections, evaluation explanations, and descriptions of system behavior.

---

## My Role

Despite using AI as a tool, I remained the **primary architect and decision-maker** throughout the project. Specifically, I was responsible for:

- **Defining the project idea and scope**:  
  Designing a system to analyze personal spending behavior using receipt emails.

- **Choosing the technical approach**:  
  Deciding to use an LLM for parsing unstructured email data while using rule-based methods for categorization.

- **Designing the data pipeline**:  
  Structuring the workflow from raw `.eml` files → filtering → LLM parsing → preprocessing → analysis → visualization.

- **Implementing and integrating components**:  
  Determining how each module interacts, including how parsed outputs feed into evaluation and the dashboard.

- **Guiding model evaluation and improvement**:  
  Interpreting evaluation results, identifying issues such as misalignment of ground truth data, and refining prompts accordingly.

- **Making design tradeoffs**:  
  Choosing efficient and interpretable solutions (e.g., rule-based categorization instead of additional LLM calls) to balance cost, performance, and clarity.

---

## Summary

The AI tool served as a **development assistant**, helping accelerate implementation and reduce friction in coding and debugging. However, all key decisions regarding system design, methodology, evaluation strategy, and overall direction of the project were made independently.

This project reflects my understanding of how to effectively integrate LLMs into a larger system while maintaining control over design and implementation.