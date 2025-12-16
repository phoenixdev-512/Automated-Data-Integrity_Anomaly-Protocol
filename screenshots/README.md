# Screenshot Guidelines

This directory should contain the following screenshots for the project documentation:

## Required Screenshots

### 1. project_structure.png
- **Content:** Screenshot of the file explorer showing the complete project directory structure
- **How to capture:** Open the workspace in VS Code or File Explorer, expand all folders, and capture the tree view

### 2. data_generation.png
- **Content:** Terminal output from running `python src/generate_mock_data.py`
- **How to capture:** Run the data generator and screenshot the complete terminal output including the anomaly summary

### 3. sentinel_execution.png
- **Content:** Terminal output from running `python src/sentinel_core.py`
- **How to capture:** Run the Sentinel analysis and screenshot the full terminal output showing INFO, CRITICAL, and WARNING logs

### 4. sales_log.png
- **Content:** Open `data/sales_log.csv` in Excel or a text editor
- **How to capture:** Screenshot showing all 10 transaction records with columns: txn_id, client, billed_amount, timestamp

### 5. bank_feed.png
- **Content:** Open `data/bank_feed.csv` in Excel or a text editor
- **How to capture:** Screenshot showing all 9 transaction records (note: TXN-1005 is missing)

### 6. forensic_report.png
- **Content:** Open `audit_reports/FORENSIC_REPORT.txt` in a text editor
- **How to capture:** Screenshot the complete forensic report showing:
  - Critical Findings section
  - Warning Findings section
  - Executive Summary section

## Tips for High-Quality Screenshots

- Use high resolution (at least 1920x1080)
- Ensure text is readable and not blurry
- Use light theme for better visibility in documentation
- Crop unnecessary UI elements (taskbar, browser chrome)
- Save in PNG format for better text clarity
- Highlight important sections with red boxes if needed
