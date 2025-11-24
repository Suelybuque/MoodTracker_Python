# 📊 Mood & Energy Tracker: A Mini Data Pipeline

This project is a beginner-friendly, expandable mini data pipeline designed for personal self-tracking. It collects daily check-ins for mood, energy, and stress, stores the data locally, and automatically produces weekly summary reports and an optional interactive dashboard.

It's an excellent way to learn foundational Data Engineering (ETL) concepts using simple Python and modern data tools.

---

## ✨ Features

* **Extraction:** Simple command-line interface (CLI) for collecting daily mood, energy, stress (1-5 scale), and text notes.
* **Storage:** Data is stored locally in a single SQLite file via SQLAlchemy for portability and ease of setup.
* **Transformation:** Uses Pandas to calculate key insights like weekly averages, recent rolling trends, and historical aggregates.
* **Reporting:** Generates a professional, weekly PDF report using ReportLab, which includes a Matplotlib chart of your recent trends.
* **Dashboard (Optional):** A lightweight interactive dashboard built with Streamlit for real-time data visualization.
* **Cloud Ready:** Includes optional helper functions for loading artifacts (like the PDF reports) to AWS S3 or Google Cloud Storage (GCS).

---

## 🚀 Quickstart

Follow these steps to clone the repository and start tracking your data.

### 1. Setup

Clone the repository and install the required dependencies using a Python virtual environment.

```bash
# Navigate to your desired directory
git clone <YOUR-REPO-URL>
cd mood-energy-pipeline

# Create and activate a virtual environment
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Usage via CLI (`main.py`)

The pipeline is controlled using the command-line interface powered by `click`.

| Command  | Description                                                    | Example                                                                        |
| -------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `add`    | Saves today's check-in to the SQLite database.                 | `python main.py add --mood 4 --energy 3 --stress 2 --notes "Felt calm today."` |
| `report` | Generates a PDF summary for the most recent week.              | `python main.py report`                                                        |
| `seed`   | Adds 21 days of random demo data (useful for testing reports). | `python main.py seed`                                                          |

### 3. Run the Dashboard (Optional)

Visualize your data interactively using Streamlit:

```bash
streamlit run dashboard/streamlit_app.py
```

---

## ⚙️ Project Structure

```
mood-energy-pipeline/
├── data/
│   └── mood_data.db        # The self-contained SQLite database
├── pipeline/               # Core Pipeline Modules
│   ├── db.py               # Handles DB initialization and CRUD operations
│   ├── extract.py          # Collects input and seeds data
│   ├── transform.py        # Pandas logic for aggregates and trends
│   ├── report.py           # ReportLab code for PDF generation
│   └── load.py             # Optional S3/GCS upload helpers
├── dashboard/
│   └── streamlit_app.py    # Streamlit visualization code
├── main.py                 # CLI entrypoint for all commands
└── requirements.txt
```

---

## ⚠️ Note on Credentials

If you use the cloud upload functionality, ensure all credentials (for S3 or GCS) are managed via environment variables or the cloud provider's SDK configuration. **Never commit secrets to this repository.**

---

## 🤝 Contributing

Feedback and contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.
