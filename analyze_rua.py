import pandas as pd
from alert_system import gmail_send_email
from config import load_config

def save_to_csv(dataframe, output_file):
    dataframe.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def perform_basic_analysis(dataframe):
    config = load_config()
    failures = dataframe[(dataframe['dkim'] != 'pass') | (dataframe['spf'] != 'pass')]
    if failures.empty:
        print("No DKIM/SPF Failures Detected.")

    if not failures.empty:
        print("Records of DKIM/SPF Failures:\n", failures)
        gmail_send_email(
            config["alert_email_subject"],
            config["alert_email_body"],
            config["recipient_email"],
            config["csv_output_path"]
        )
