from fetch_emails import fetch_dmarc_reports
from parse_rua_reports import extract_zip_and_parse
from analyze_rua import save_to_csv, perform_basic_analysis
from config import load_config
import pandas as pd

def main():
    print("Step 1: Fetching RUA emails...")
    email_attachments = fetch_dmarc_reports()

    if not email_attachments:
        print("No DMARC reports fetched. Exiting.")
        return

    combined_data = pd.DataFrame()
    for i, file_bytes in enumerate(email_attachments, start=1):
        print(f"Processing attachment {i}...")

        parsed_data = extract_zip_and_parse(file_bytes)

        if parsed_data is None or parsed_data.empty:
            print(f"Attachment {i} did not contain valid data. Skipping.")
            continue

        combined_data = pd.concat([combined_data, parsed_data], ignore_index=True)

    if combined_data.empty:
        print("No valid data was parsed from the RUA reports. Exiting.")
        return

    config = load_config()
    
    print("Step 3: Saving results to CSV...")
    save_to_csv(combined_data, config["csv_output_path"])

    print("Step 4: Performing analysis...")
    perform_basic_analysis(combined_data)

if __name__ == "__main__":
    main()
