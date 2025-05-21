import os
import hashlib
import json
import pandas as pd
import numpy as np

def hash_excel_folder(folder_path, hash_file=".excel_hash.txt"):
    """Generate and store a hash of all Excel file contents."""
    hasher = hashlib.sha256()

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            with open(os.path.join(folder_path, filename), "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)

    current_hash = hasher.hexdigest()

    # If hash file exists, compare
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            previous_hash = f.read().strip()
        if current_hash == previous_hash:
            return False  # No change

    # Save current hash
    with open(hash_file, "w") as f:
        f.write(current_hash)

    return True  # Changed


def generate_json_from_excels(folder_path, output_vector_json="docs_vector.json", output_metadata_json="docs_metadata.json"):
    """Generate JSON files from Excel folder only if content changed."""
    if not hash_excel_folder(folder_path):
        print("✅ No change in Excel files — using cached data.")
        return

    print("🔄 Changes detected. Processing Excel files...")

    vector_data = []
    metadata_data = []

    uid = 0  # Unique key for mapping

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            file_path = os.path.join(folder_path, filename)
            excel_data = pd.read_excel(file_path, sheet_name=None)

            for sheet_name, df in excel_data.items():
                df = df.replace({np.nan: None})

                for row in df.to_dict(orient='records'):
                    row["__source_file__"] = filename
                    row["__sheet__"] = sheet_name

                    row_text = " ".join(str(v) for v in row.values() if v is not None)

                    key = f"doc_{uid}"
                    vector_data.append({"key": key, "text": row_text})
                    metadata_data.append({"key": key, **row})
                    uid += 1

    # Save output files
    with open(output_vector_json, "w", encoding="utf-8") as f:
        json.dump(vector_data, f, indent=2, ensure_ascii=False)

    with open(output_metadata_json, "w", encoding="utf-8") as f:
        json.dump(metadata_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Created {output_vector_json} and {output_metadata_json} with {uid} records.")


