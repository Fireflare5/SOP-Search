# SOP-Search
A custom search engine developed for my internship
TODO: Set program up on a server.
It might need some modifications to get it running.
It uses Google's python API to access the docs and will need all the SOP's to be accessible from one main acount running it.
For information on how it works read: https://developers.google.com/workspace/docs/api/auth.
The API it uses to desplay a webpage is Dash. For information on how it works and how to use it go to https://dash.plotly.com/.
As for the search algorithm, it can be broken down into a few parts, Title Search and Deep Search. Title Search allows the user to search of the name of an SOP directly, while Deep search uses key words in a search to find the most relevent result.

Note: In order for the SOP to be accessed it has to be shared with the main acount. This should be doable by just granting everyone in the organization access and putting the link in the lists Google sheet.
Important note, the end of the link needs to be removed as https://docs.google.com/document/d/{docId}/edit?tab=t.0 will not work. The link should end with the doc id: https://docs.google.com/document/d/{docId}

It also needs a way to store common searches and their desired results to improve the accuracy. It needs to be tested with multiple people.

Example of what the SOP list should look like
<img width="1061" height="841" alt="Screenshot 2025-08-13 at 3 26 59 PM" src="https://github.com/user-attachments/assets/f5ad4389-9097-4a19-8029-b5e2cbc1e58a" />
