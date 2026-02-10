import easyocr
import pandas as pd
import os
import glob

# ---SETUP PATHS ---
# We use os.path.join to safely build the path: "SROIE2019\test\img"
folder_path = os.path.join("SROIE2019", "test", "img")

# Initialize the OCR reader (English language, no GPU) (used for reading the text from the images)
reader = easyocr.Reader(['en'], gpu=False)

# - GET FILES ---
# glob finds all files ending in .jpg inside that folder
# stores a list of file paths like: ["SROIE2019/test/img/001.jpg", "SROIE2019/test/img/002.jpg",etc]
all_images = glob.glob(os.path.join(folder_path, "*.jpg"))

# Limit to first 10 images for testing (Remove [:10] to run ALL of them)
images_to_scan = all_images[:10]


# ---(Processing the images ) ---
data_rows = [] # empty list which will store the results for each receipt as a a list of dictionaries (like a row in Excel) 

for filepath in images_to_scan:
    filename = os.path.basename(filepath) # Get just "001.jpg"
    print(f"Reading {filename}...")

    try:
        # A. READ THE IMAGE
        # Returns just  a list of text without any details (like bounding boxes or confidence scores)
        text_list = reader.readtext(filepath, detail=0)

       # get the total amount from the text list
        found_numbers = []
        
        for word in text_list:
            # Clean: remove '$', 'Total', commas
            clean_word = word.lower().replace('total', '').replace('$', '').replace(',', '').strip()
            
            try:
                amount = float(clean_word)
                # Filter: Must have decimal and be realistic
                if "." in clean_word and amount < 10000:
                    found_numbers.append(amount)
            except ValueError:
                continue 

        # Heuristic: Largest number is the Total
        final_total = max(found_numbers) if found_numbers else 0.0

        # STORE RESULT
        # Create a Dictionary (The Form) for this one receipt
        single_row = {
            "File Name": filename,
            "Detected Total": final_total,
            "Raw Text Extract": str(text_list) # Save text just in case
        }
        
        # Add the Form to the Clipboard (List)
        data_rows.append(single_row)

    except Exception as e:
        print(f"Error on {filename}: {e}")

# ---  SAVE TO EXCEL ---
# Turn the List of Dictionaries into a DataFrame ( a table structure with the columns "File Name", "Detected Total", "Raw Text Extract")
df = pd.DataFrame(data_rows)

# Save as .xlsx as its required to turn into a proper Excel file (not .csv which is just text)
output_filename = "Final_Receipts.xlsx"
df.to_excel(output_filename, index=False)

print(f"\nSuccess! Saved to {output_filename}")
print(df.head())