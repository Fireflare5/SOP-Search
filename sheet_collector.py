import requests as re
import pandas as pd

def collect_sheet(sheet_id: str, sheet_name: str = "lists") -> pd.DataFrame:
    """Collects a Google Sheet and returns it as a Dataframe.

    Args:
        sheet_id (str): The ID of the Google Sheet.
        sheet_name (str, optional): The name of the Google Sheet. Defaults to "lists".

    Raises:
        Exception: Failed to fetch the sheet.

    Returns:
        pd.DataFrame: A Dataframe containing the Google Sheet data.
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    site = re.get(url)
    if site.status_code == 200:
        csv_content = site.content.decode('utf-8')
        with open(f"{sheet_name}.csv", "w") as f:
            f.write(csv_content)
        return pd.read_csv(f"{sheet_name}.csv")
    else:
        raise Exception(f"Failed to fetch the sheet: {site.status_code}")
if __name__ == "__main__":
    collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")