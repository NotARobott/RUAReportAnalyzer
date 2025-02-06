# Automated DMARC Report Processor

This project makes it easy to fetch, parse, analyze, and alert on Domain-based Message Authentication, Reporting, and Conformance (DMARC) Aggregate Reports (RUA). By leveraging the Gmail API, the script automatically downloads and processes DMARC reports from your Gmail inbox, evaluates DKIM/SPF failures, and generates CSV reports, optionally emailing alerts if issues are detected.

This guide is written to ensure compatibility with **macOS**, **Linux**, and **Windows** operating systems.

---

## Features

- **Multi-Platform Compatibility**: Works seamlessly on macOS, Linux, and Windows.
- **Automated Gmail Integration**: Fetch DMARC reports from Gmail with search filters and labels.
- **Report Parsing**: Process `.zip` and `.gz` files containing XML DMARC reports, and export parsed data as CSV.
- **Failure Analysis**: Detect DKIM and SPF failures in incoming reports and generate alerts based on detected issues.
- **Email Alerts**: Automatically email alerts with attached reports if failures occur.

---

## Prerequisites

### 1. **Python 3.6 or Later**
   - macOS: Install Python via [Homebrew](https://brew.sh) or from the [official website](https://www.python.org/downloads/).
   - Linux: Most distributions come pre-installed with Python. If outdated, install via your package manager (e.g., `sudo apt install python3` for Ubuntu/Debian).
   - Windows: Download Python from [this link](https://www.python.org/downloads/) and ensure **Add Python to PATH** is checked during installation.

### 2. **Gmail API Setup**
   - Enable the Gmail API and download your `credentials.json` file by following [this guide](https://developers.google.com/gmail/api/quickstart/python).
   - Place the `credentials.json` file in the root directory of the project.

### 3. **Install Required Python Libraries**
   - Install dependencies using `pip` after cloning the repository. Instructions are provided further below.

### 4. **Gmail Label Setup**
   - Create a Gmail label (e.g., `RUA`) to filter DMARC emails for processing. Instructions on creating labels and filters are provided in the **Gmail Label and Filter Setup** section.

---

## Setup and Installation

Follow these steps to ensure proper installation on your platform of choice:

---

### macOS Instructions

1. **Install Python via Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python
   python3 --version  # Verify installation
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/DMARC-Report-Processor.git
   cd DMARC-Report-Processor
   ```

3. **Install Required Libraries**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Place `credentials.json` in the Project Directory**:
   After enabling the Gmail API, download `credentials.json` and move it into the root directory of the project.

5. **Configure the Script**:
   Edit `config.json` to personalize settings (e.g., recipient email, output path).

6. **Run the Script**:
   ```bash
   python3 main.py
   ```

---

### Linux Instructions

1. **Ensure Python 3 is Installed**:
   Check if you already have Python installed:
   ```bash
   python3 --version
   ```
   If Python is not installed, use your package manager to install it:
   - **Debian/Ubuntu**:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```
   - **Fedora**:
     ```bash
     sudo dnf install python3 python3-pip
     ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/DMARC-Report-Processor.git
   cd DMARC-Report-Processor
   ```

3. **Install Required Libraries**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Place `credentials.json` in the Project Directory**.

5. **Run the Script**:
   ```bash
   python3 main.py
   ```

---

### Windows Instructions

1. **Install Python**:
   - Download Python from [python.org](https://www.python.org/downloads/).
   - During installation, **check the Add Python to PATH** option.

2. **Install Git** (Optional, if Git is not available):
   - Download and install Git from [git-scm.com](https://git-scm.com/).
   - Alternatively, use the **ZIP download** link on the GitHub page and extract the project manually.

3. **Install Python Libraries**:
   Open the Windows Terminal or Command Prompt:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Place `credentials.json` in the Project Directory**.

5. **Run the Script**:
   ```cmd
   python main.py
   ```

---

## Gmail Label and Filter Setup

RUA reports are typically sent to your email inbox by domains or third parties. To streamline processing with this script, you should create a Gmail label (e.g., `RUA`) and filter these emails.

1. **Log into Gmail**.
2. **Search for DMARC Report Emails**:
   In the search bar, type:
   ```plaintext
   has:attachment filename:(.zip OR .gz)
   ```
3. **Create a Filter**:
   - Click the search bar's drop-down icon.
   - In “From,” enter a known source (e.g., `dmarc-reports@example.com`), or leave it blank to catch all DMARC reports.
   - Click **Create Filter**.
4. **Apply the Label**:
   - Check **Apply the label** and create a new label (e.g., `RUA`).
   - (Optional) Check **Skip the Inbox (Archive it)** to keep your inbox clean.
   - Save the filter.

Now future DMARC emails matching your criteria will be labeled appropriately.

---

## Running the Script

1. Run the following command depending on your operating system:
   - **macOS/Linux**:
     ```bash
     python3 main.py
     ```
   - **Windows**:
     ```cmd
     python main.py
     ```

2. The script fetches emails labeled `RUA`, downloads attachments, parses and analyzes the DMARC XML reports, and saves the data in a CSV file. Alerts are sent if failures are detected.

---

## Automating the Script

You can schedule the script to run periodically:

### macOS & Linux (Cron Job)

1. Open the `crontab` editor:
   ```bash
   crontab -e
   ```

2. Add an entry to run daily at 7:00 AM:
   ```bash
   0 7 * * * /usr/bin/python3 /path/to/main.py
   ```

3. Save and exit the editor. The script now runs automatically.

### Windows (Task Scheduler)

1. Open **Task Scheduler** and create a new task.
2. Set:
   - **Trigger**: Daily at your desired time.
   - **Action**: Run a program.
     - Program/script: `python.exe`
     - Add arguments: `path\to\main.py`
     - Start in: Directory containing `main.py`.
3. Save the task. The script will now run automatically.

---

## Troubleshooting

### Common Issues

1. **Authentication Errors**:  
   - If Gmail API authentication fails, delete the `token.pickle` file and rerun the script, following the prompts to reauthenticate.

2. **No Reports Processed**:
   - Ensure your Gmail search filter matches the label specified in `config.json`.
   - Double-check that emails fitting the search criteria have `.zip` or `.gz` attachments.

3. **Permissions Error**:
   - On macOS and Linux, ensure the script file is executable:
     ```bash
     chmod +x main.py
     ```
   - On all platforms, run the script with appropriate permissions.

4. **Empty CSV**:
   - Verify that the DMARC reports include XML data and are structured properly.

---

## Directory Structure

```
DMARC-Report-Processor/
├── alert_system.py          # Handles email alerts
├── analyze_rua.py           # Processes DMARC data for failures
├── authenticate_gmail.py    # Handles Gmail API authentication
├── config.json              # Customizable script settings
├── main.py                  # Main script
├── parse_rua_reports.py     # Parses ZIP/GZIP XML reports
├── requirements.txt         # Lists required Python libraries
└── token.pickle             # OAuth2 token (auto-generated)
```

---

## Conclusion

This project simplifies the process of monitoring DMARC reports, keeping email systems secure while saving time. Compatible across macOS, Linux, and Windows, it offers an efficient, automated workflow for managing DKIM/SPF issues. Feedback and contributions are welcome!
