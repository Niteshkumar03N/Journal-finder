<div align="center">

<br/>

# Journal Finder

**A multi-publisher journal recommendation engine for academic researchers.**

Paste your research abstract. Get ranked journal suggestions — with impact factors, CiteScores, submission timelines, APC charges, and direct links — from five major publishers, all in one place.

## Overview

Identifying the right journal is one of the most time-intensive steps in academic publishing. Researchers typically visit each publisher's website individually, enter their abstract multiple times, and manually compare results.

**Journal Finder eliminates that workflow.** It submits your abstract to all five publishers simultaneously using headless browser automation, normalizes the results into a unified schema, and surfaces everything in a single clean interface.

No API keys required. No manual cross-referencing. One abstract, one click.

---

## Supported Publishers

| Publisher | Data Extracted |
|-----------|----------------|
| **Springer** | Title · Impact Factor · Publishing Model · Annual Downloads · Submission-to-First-Decision |
| **Elsevier** | Title · Impact Factor · CiteScore · APC · Open Access Status · Acceptance-to-Publication |
| **Taylor & Francis** | Title · Journal URL |
| **CW Authors** | Title · Publisher · CiteScore · Impact Factor |
| **Wiley** | Title · Impact Factor · Submission Time · Acceptance Rate · Publication Charge |


---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Chrome installed on your system

> `webdriver-manager` handles ChromeDriver automatically — no manual driver installation needed.

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/journal-finder.git
cd journal-finder
```

### 2. Set up a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Usage

<div align="left">

1. Paste your research abstract into the text area.
2. Select one or more publishers using the checkboxes.
3. Click **Find Journals**.
4. Browse results grouped by publisher — each card shows title, metadata badges, and a direct link.
5. Download all results as a JSON file using the export button.

</div>

---

## Architecture

Each scraper operates a **headless Chrome instance** via Selenium. It navigates to the publisher's official journal-finder page, submits the abstract as a real user would, waits for results to load, then extracts structured data from the DOM.

```
Abstract (user input)
        │
        ▼
  ┌─────────────────┐
  │   app.py        │  Streamlit UI — orchestrates scraper calls
  └────────┬────────┘
           │
     ┌─────┴──────────────────────────────────┐
     ▼        ▼          ▼         ▼          ▼
 Springer  Elsevier  Taylor &  CW Authors  Wiley
 Scraper   Scraper   Francis   Scraper     Scraper
                     Scraper
     │        │          │         │          │
     └─────┬──┴──────────┴─────────┴──────────┘
           │
           ▼
   Unified results array
           │
    ┌──────┴──────┐
    ▼             ▼
 Cards UI     JSON export
 (by pub.)       ⬇
```

---

## Output Schema

All scrapers normalize their output to a common format:

```json
{
  "journal_name": "Nature Communications",
  "publisher": "Springer",
  "impact_factor": "16.6",
  "citescore": "19.7",
  "publishing_model": "Open Access",
  "submission_to_first_decision": "7 days",
  "acceptance_to_publication": "4 days",
  "publication_charge": "$4,990",
  "url": "https://www.nature.com/ncomms/",
  "downloads": "10.2M"
}
```

Fields not available for a given publisher are returned as `null`.

---

## Dependencies

```
streamlit
selenium
webdriver-manager
pandas
python-dotenv
```

---

## Known Limitations

| | |
|---|---|
| **Speed** | Each scraper runs a real browser session. Expect 15–60 seconds per publisher depending on network conditions. |
| **Fragility** | Scrapers depend on the publisher's current HTML structure. If a publisher updates their frontend, selectors may need updating. |
| **Taylor & Francis** | Currently extracts title and URL only. Additional metadata fields are not yet parsed. |
| **Rate sensitivity** | Avoid sending repeated requests in rapid succession to prevent temporary blocks. |

---


## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built for researchers. Open to contributions.

</div>
