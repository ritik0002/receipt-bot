# **Receipt Scanner**

This is a Python bot that automatically reads receipt images and saves the "Total" price into an Excel file.

## ⚡ What it does
1. Looks for all `.jpg` images in the `img` folder.
2. Uses **EasyOCR** (AI) to read the text on the receipt.
3. Finds the largest number (assuming it is the Total).
4. Saves everything to `Final_Receipts.xlsx`.

## 📂 The Data
You can use the official dataset or your own photos:
* **Option A (SROIE Dataset):** I used the [SROIE 2019 Dataset](https://www.kaggle.com/datasets/urbikn/sroie-datasetv2) for testing.
* **Option B (Your Own):** Just take a picture of any receipt, save it as a `.jpg`, and put it in the folder.

## 🛠️ How to use
1. Install the libraries:
   ```bash
   pip install easyocr pandas openpyxl
