import zipfile
import gzip
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO

def parse_rua(file):
    tree = ET.parse(file)
    root = tree.getroot()
    
    org_name = root.findtext('./report_metadata/org_name', default="Unknown")
    
    return pd.DataFrame([
        {
            "source_ip": r.findtext('./row/source_ip'),
            "count": r.findtext('./row/count'),
            "domain": r.findtext('./identifiers/header_from'),
            "dkim": r.findtext('./row/policy_evaluated/dkim'),
            "spf": r.findtext('./row/policy_evaluated/spf'),
            "org_name": org_name,
        }
        for r in root.findall('./record')
    ])

def extract_zip_and_parse(file_bytes):
    rows = []

    if file_bytes.startswith(b'PK'):
        with zipfile.ZipFile(BytesIO(file_bytes)) as z:
            for file_name in z.namelist():
                if file_name.endswith(".xml") and "__MACOSX" not in file_name:
                    with z.open(file_name) as f:
                        df = parse_rua(f)
                        rows.extend(df.to_dict(orient="records"))

    elif file_bytes.startswith(b'\x1f\x8b'):
        with gzip.GzipFile(fileobj=BytesIO(file_bytes)) as gz:
            file_content = BytesIO(gz.read())
            df = parse_rua(file_content)
            rows.extend(df.to_dict(orient="records"))

    else:
        raise ValueError("Unsupported file type")

    df = pd.DataFrame(rows)
    print(f"Parsed {len(df)} records with organization data." if not df.empty else "Warning: No valid data found.")
    return df
