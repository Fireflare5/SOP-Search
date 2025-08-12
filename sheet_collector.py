import os.path

import requests as re
import pandas as pd
from io import StringIO

def collect_sheet(sheet_id: str, sheet_name: str = "lists") -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    site = re.get(url)
    if site.status_code == 200:
        csv_content = site.content.decode('utf-8')
        with open(f"{sheet_name}.csv", "w") as f:
            f.write(csv_content)
        return pd.read_csv(f"{sheet_name}.csv")
    else:
        raise Exception(f"Failed to fetch the sheet: {site.status_code}")

collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")