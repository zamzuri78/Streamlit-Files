📊 SIMPLE – Data Cleaning Station V1.1
Developed by Zamzuri © 2025

==================================================
INTRODUCTION
==================================================
SIMPLE (Structured Insights for Missing, Preprocessing, Labeling & Export) is a modular data cleaning platform built using Streamlit. It is designed to help users audit, clean, transform, and export datasets in a structured and teachable way.

This system supports both file uploads and URL-based data imports, making it flexible for various workflows including coaching, machine learning preparation, and audit-style analysis.

==================================================
FEATURES
==================================================

📥 INPUT METHODS
--------------------------------------------------
1. Upload File (.csv or .xlsx)
   - Auto separator detection for CSV
   - File name and format preview

2. Import via URL
   - Supports direct links to CSV, Excel, or Google Sheets
   - Google Sheets auto-converted to CSV format

📋 TAB 1: EDA (Exploratory Data Analysis)
--------------------------------------------------
- Data preview (head)
- Dataset dimensions (rows & columns)
- Missing value summary
- Duplicate row count
- Missing Value Status panel
- Data type summary
- Statistical summary (numerical)
- Non-numeric summary (categorical)
- Visualization tools:
  - Line chart
  - Bar chart

🧹 TAB 2: AUTO CLEANING
--------------------------------------------------
- Remove missing values (`dropna`)
- Handle missing values:
  - `fillna("Na")` for categorical
  - `interpolate()` for numerical
- Remove duplicate rows
- Download cleaned datasets after each action

🧱 TAB 3: TRANSFORMATION
--------------------------------------------------
- Drop selected columns
- Map categorical values to integers (only if < 5 unique values)
  - Manual mapping interface
  - Preview and download mapped dataset

📥 TAB 4: EXPORT & PREVIEW
--------------------------------------------------
- Select columns to preview
- Preview modes:
  - Head only
  - Tail only
  - Head & Tail
  - Paginated View (20, 50, 100 rows per page)
- Navigation buttons (Next/Previous)
- Page status indicator

==================================================
SIDEBAR BRANDING
==================================================
- Footer: Developed by Zamzuri © 2025

==================================================
REQUIREMENTS
==================================================
- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Requests (for URL import)
- OpenPyXL (for Excel support)
- Seaborn (optional for future visualizations)

==================================================
USAGE
==================================================
1. Run the app:
   > streamlit run app.py

2. Choose input method:
   - Upload file OR paste URL

3. Navigate through tabs:
   - EDA → Cleaning → Transformation → Export

4. Download cleaned or transformed datasets as needed

==================================================
NOTES
==================================================
- For Google Sheets, ensure the sheet is publicly accessible
- For CSV via GitHub, use the raw file link
- This system is designed for general-purpose datasets and audit-style workflows

==================================================
CONTACT
==================================================
Zamzuri (ZWhy)
Email: [your-email-here]
TikTok: @zamzuri7
Platform: Under development for AI-powered audit coaching

