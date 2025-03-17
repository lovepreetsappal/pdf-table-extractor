import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import pandas as pd
import os
from sklearn.metrics import accuracy_score, precision_score
from datetime import datetime

# Extract tables using improved settings
def extract_tables_robust(pdf_path, output_excel):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_tables = []
            for page in pdf.pages:
                # Try table extraction with better settings
                table = page.extract_table({
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "intersection_tolerance": 5,
                })
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

            if all_tables:
                final_df = pd.concat(all_tables, ignore_index=True)
                final_df.to_excel(output_excel, index=False)
                return final_df
            else:
                messagebox.showwarning("No Table Found", "No structured tables detected.\nTrying raw text extraction...")
                return extract_text_to_excel(pdf_path, output_excel)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract tables.\n{str(e)}")
        return None

# Fallback text-based extraction
def extract_text_to_excel(pdf_path, output_excel):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            lines = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines.extend(text.split("\n"))

        # Basic split by multiple spaces
        data = []
        for line in lines:
            if line.strip():
                columns = [col.strip() for col in line.split("  ") if col.strip()]
                data.append(columns)

        if not data:
            messagebox.showwarning("No Text Found", "No text could be extracted from PDF.")
            return None

        max_cols = max(len(row) for row in data)
        padded_data = [row + [""] * (max_cols - len(row)) for row in data]

        df = pd.DataFrame(padded_data)
        df.to_excel(output_excel, index=False)
        return df

    except Exception as e:
        messagebox.showerror("Error", f"Failed text extraction.\n{str(e)}")
        return None

# Accuracy check
def compute_accuracy_precision(extracted_df, ground_truth_path):
    try:
        if not os.path.exists(ground_truth_path):
            messagebox.showinfo("Accuracy Skipped", "No ground_truth.xlsx found.")
            return
        ground_truth_df = pd.read_excel(ground_truth_path)

        if extracted_df.shape[1] != ground_truth_df.shape[1]:
            messagebox.showwarning("Mismatch", "Column mismatch with ground truth. Accuracy skipped.")
            return

        extracted_flat = extracted_df.values.flatten()
        ground_truth_flat = ground_truth_df.values.flatten()
        min_len = min(len(extracted_flat), len(ground_truth_flat))

        acc = accuracy_score(ground_truth_flat[:min_len], extracted_flat[:min_len])
        prec = precision_score(ground_truth_flat[:min_len], extracted_flat[:min_len], average='macro', zero_division=0)

        messagebox.showinfo("Accuracy Results", f"Accuracy: {acc:.2f}\nPrecision: {prec:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Accuracy check failed.\n{str(e)}")

# GUI Upload
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_excel = f"extracted_{timestamp}.xlsx"

    df = extract_tables_robust(file_path, output_excel)
    if df is not None:
        messagebox.showinfo("Success", f"Saved to:\n{output_excel}")
        

# GUI Setup
root = tk.Tk()
root.title("PDF Table Extractor")
root.geometry("400x200")
root.configure(bg="#e6f2ff")

label = tk.Label(root, text="PDF Table Extractor", font=("Helvetica", 16, "bold"), bg="#e6f2ff")
label.pack(pady=20)

button = tk.Button(root, text="Upload PDF", command=upload_pdf, width=20, height=2, bg="#007acc", fg="white", font=("Helvetica", 12))
button.pack()

root.mainloop()
