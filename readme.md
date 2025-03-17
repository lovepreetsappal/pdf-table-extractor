# 📄 PDF Table Extractor Tool
A Python-based tool to extract tables from any PDF document (with or without borders), convert them to Excel files, and optionally compare them to a ground truth for accuracy and precision evaluation.

# 🚀 Features
Detects and extracts tables from system-generated PDFs.
Works with tables that have borders, no borders, or irregular shapes.
Saves output as Excel file with optional multiple sheets (for multipage PDFs).
Allows accuracy/precision testing against a ground_truth.xlsx file.
Simple GUI for file selection using tkinter.
# 🛠️ Requirements
Install required libraries via pip:

bash
Copy
Edit
pip install PyMuPDF pandas openpyxl scikit-learn tkinter
Note: tkinter is pre-installed with Python on most systems.

# 📂 File Structure
File	Description
main.py	Main script to run the tool (PDF ➜ Excel + Accuracy).
README.md	Project documentation.
# 📥 How to Use
1. Run the Tool
In your terminal or command prompt:

bash
Copy
Edit
python main.py
2. Upload PDF
A file dialog will appear. Select your PDF file.
The tool will process the PDF and save an Excel file (with a timestamp).
3. Accuracy Check (Optional)
If ground_truth.xlsx exists, the tool will ask if you want to perform an accuracy test.
It compares the extracted data with the ground truth file.
# 📊 Accuracy & Precision Metrics
Metric	Definition
Accuracy	% of correctly extracted data vs total ground truth data.
Precision	% of relevant (correct) data among all extracted data.
# ⚠️ Known Limitations
Multi-line and merged cells may require manual formatting.
Irregular tables might need manual cleanup for perfect structure.
Accuracy check requires aligned data in the ground truth file.
# 🤝 Contribution
Feel free to fork this repo and contribute improvements, especially for:

Auto-detecting headers.
Enhanced multi-line row handling.
Exporting to CSV or JSON formats.
# 📄 License
MIT License – use freely with attribution