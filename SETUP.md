# Setup

## 1. Clone or Download the Project

Download the project folder and navigate into it:

```bash
cd campus-receipt-analyzer
```

---

## 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=your_key_here
```

---

## 5. Export Emails from Outlook

1. Open Outlook and navigate to your inbox or a specific folder.
2. Filter emails by a desired date range.
3. Select the emails in that range.
4. Drag and drop them into the following folder:

```
data/exported_emails/
```

This will save each email as a `.eml` file. The application will automatically filter for receipt emails during processing.

---

## 6. Run the Data Pipeline

### Step 1: Load and filter emails
```bash
python3 -m scripts.run_fetch
```

### Step 2: Parse emails using the LLM
```bash
python3 -m scripts.run_parse
```

### Step 3: Clean and categorize the data
```bash
python3 -m scripts.run_clean
```

---

## 7. Launch the Dashboard

```bash
streamlit run app.py
```

---

## Notes

- The parsing step calls the OpenAI API and may incur small costs depending on the number of emails processed.
- The rest of the pipeline (cleaning and visualization) can be run repeatedly without additional API usage.

---