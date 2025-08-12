import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GDocsScraper:
    def __init__(self, document_id, skip=False, local=False, Update=False):
        self.document_id = document_id
        self.creds = None
        self.SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
        if os.path.exists(f"files/{document_id}.txt") and local and not Update:
            self._scrape(skip, local, Update) 
            #print(f"Using local file for {document_id}")
        else:
            self._authenticate()
            if local:
                Update = True
            self._scrape(skip, local, Update)
            
    
    def _authenticate(self):
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
    
    def _scrape(self, skip, local, Update):
        if local and not Update:
            with open(f"files/{self.document_id}.txt", "r") as f:
                self.text = f.read()
        else:
            service = build("docs", "v1", credentials=self.creds)
            self.text = ""
            self.document = service.documents().get(documentId=self.document_id).execute()
            if not skip:
                for sec in self.document.get('body').get('content'):
                    if "paragraph" in sec:
                        for el in sec.get("paragraph").get("elements"):
                            if "textRun" in el:
                                spec = el.get("textRun")
                                try:
                                    if spec.get("textStyle").get("bold") == False or spec.get("textStyle").get("fontSize").get("magnitude") <= 12:
                                        self.text += spec.get("content")#.replace("○", "").replace("●", "").replace("■", "")
                                except:
                                    self.text += "\n"
            else:
                for sec in self.document.get('body').get('content'):
                    if "paragraph" in sec:
                        for el in sec.get("paragraph").get("elements"):
                            if "textRun" in el:
                                self.text += el.get("textRun").get("content")
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
