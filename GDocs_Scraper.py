#Import necessary libraries
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GDocsScraper:
    def __init__(self, document_id: str, skip: bool=False, local: bool=False, Update: bool=False) -> None:
        """Gets the content of a Google Document and saves it locally.

        Args:
            document_id (str): The ID of the Google Document to scrape.
            skip (bool, optional): Skips the culling of the SOP. Defaults to False.
            local (bool, optional): Identifies if the SOPs will be local. Defaults to False.
            Update (bool, optional): Identifies if the local files should be updated. Defaults to False.
        """
        self.document_id = document_id
        self.creds = None
        self.SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
        if os.path.exists(f"files/{document_id}.txt") and local and not Update:
            self._scrape(skip, local, Update) 
        else:
            self._authenticate()
            if local:
                Update = True
            self._scrape(skip, local, Update)
            
    
    def _authenticate(self) -> None:
        """Authenticates the user to access Google Docs API.
        """
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
    
    def _scrape(self, skip: bool, local: bool, Update: bool) -> None:
        """Scraped the Google Doc for its content

        Args:
            skip (bool): Identifies if the SOP culling should be skipped.
            local (bool): Identifies if the SOPs will be local.
            Update (bool): Identifies if the local files should be updated.
        """
        if local and not Update:
            with open(f"files/{self.document_id}.txt", "r") as f:
                self.text = f.read()
        else:
            service = build("docs", "v1", credentials=self.creds)
            self.text = ""
            self.document = service.documents().get(documentId=self.document_id).execute()
            
            # Get the Important Text Only 
            if not skip:
                for sec in self.document.get('body').get('content'):
                    if "paragraph" in sec:
                        for el in sec.get("paragraph").get("elements"):
                            if "textRun" in el:
                                spec = el.get("textRun")
                                try:
                                    if spec.get("textStyle").get("bold") == False or spec.get("textStyle").get("fontSize").get("magnitude") <= 12:
                                        self.text += spec.get("content")
                                except:
                                    self.text += "\n"
            else:
                for sec in self.document.get('body').get('content'):
                    if "paragraph" in sec:
                        for el in sec.get("paragraph").get("elements"):
                            if "textRun" in el:
                                self.text += el.get("textRun").get("content")
            # Save the text locally
            if Update:
                with open(f"files/{self.document_id}.txt", "w") as f:
                    f.write(self.text)

if __name__ == "__main__":
    os.system("clear")
    document_id = "1_ND9RMbnQ9Gy5_L3fJalX2nbz4_PfN48PZDhIoRUG6A"
    scraper = GDocsScraper(document_id, skip=False, local=True, Update=False)
    print(scraper.text)
    with open("doc.txt", "w") as f:
        f.write(scraper.text)
