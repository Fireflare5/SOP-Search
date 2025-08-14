# Import necessary libraries
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os
from GDocs_Scraper import GDocsScraper
from sheet_collector import collect_sheet
from typing import List, Tuple

class Update:
    def __init__(self,) -> None:
        """Updates the local SOP files
        """
        self.df = collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")
        self.ids = [os.path.basename(link) for link in self.df["Description"].to_list()]
        for id in self.ids:
            GDocsScraper(id, skip=False, local=True, Update=True)

class Search:

    def __init__(self, Search: str = "",) -> None:
        """A search background program for SOPs.

        Args:
            Search (str, optional): The search input. Defaults to "".
        """
        self.Search = Search
        self.SOP = None
        if Search != "":
            try:
                self.SOPSearch(Search)
            except Exception as e:
                print(f"Error during search: {e}")
    
    def SCorrections(self, Search: str = "",) -> None:
        """Corrects the search string.

        Args:
            Search (str, optional): The seach input. Defaults to "".
        """
        if self.Search == "":
            self.Search = Search
                
    def SOPSearch(self, Search: str = "",) -> None:
        """The main search function.

        Args:
            Search (str, optional): The search input. Defaults to "".

        Raises:
            Exception: The SOP was not found. Meaning no SOPs matched the search or there was an error during the search.
        """
        self.SCorrections(Search)# Correct the search string
        self.Cull()# Cull the Search for keywords
        self.df = collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")# Get the list of SOPs
        self.DeepSearch()# Run the deep search
        if self.SOP is None:
            raise Exception("SOP not found")
    
        
    def TitleSearch(self, title: str) -> bool:
        """Matches the title of the SOP with the search input.

        Args:
            title (str): The title of an SOP.

        Returns:
            bool: A true of false value indicating if the title matches the search input.
        """
        if self.Search.lower() == title.lower():
            self.SOP = self.df[self.df["Title"] == title]
            return True
        return False
    
    def SimilarTS(self, Ttokens: List, count: int, search_word: str, title: str) -> int:
        """Matches the search input with a similar SOP title.

        Args:
            Ttokens (List): The tokenized title of an SOP.
            count (int): Current score of an the SOP
            search_word (str): The word to search for in the title.
            title (str): The title of an SOP.

        Returns:
            int: New score of the SOP.
        """
        if (search_word.capitalize() or search_word.upper() or search_word.lower()) in Ttokens:
            count += 10
        if title in [search_word.capitalize(),search_word.lower(),search_word.upper()]:
            count += 15
        return count
    
    def Cull(self,) -> None:
        """Culls the search input to remove unnecessary words.
        """
        self.SearchTokens = word_tokenize(self.Search)# Tokenize the search input
        self.sentence = []
        
        # Identify sentences to search for in the SOP
        if "``" in self.SearchTokens:
            for word in self.SearchTokens[self.SearchTokens.index('``') + 1:]:
                if "''" in word:
                    break
                else:
                    self.sentence.append(word)
        # Remove unnecessary words from the search input
        self.SearchCull = [word[0] for word in pos_tag(self.SearchTokens) if word[1] not in ["CC", "IN", "DT", "PRP", "VBP", "''", "``", "TO", "PRP$", ".", "WP", "VBZ",","] and word[0] not in ["process", "SOP", "do"]]
        if self.SearchCull == []:
            self.SearchCull = self.SearchTokens
    
    def Count(self, count: int, tokens: List, search_word: str) -> int:
        """Scores the SOP based on the number of times a search word appears in the description.

        Args:
            count (int): Current score of the SOP
            tokens (List): A tokenized version of the SOP
            search_word (str): Word to search for in the SOP

        Returns:
            int: New score of the SOP.
        """
        if search_word.lower() in tokens:
            count += tokens.count(search_word.lower())
        if search_word.capitalize() in tokens:
            count += tokens.count(search_word.capitalize())
        if search_word.upper() in tokens:
            count += tokens.count(search_word.upper())
        return count
    
    def TagSearch(self, count: int, search_word: str, tags: List,) -> int:
        """Scores the SOP based on if a search word is in the tags.

        Args:
            count (int): Current score of the SOP
            search_word (str): Word to search for in the tags
            tags (List): List of tags for the SOP

        Returns:
            int: The new score of the SOP
        """
        if search_word.capitalize() in tags:
            count += 5
        return count
    
    def SortCount(self, x: Tuple) -> int:
        """A function to sort the SOPs based on their score.

        Args:
            x (Tuple): A tuple containing the score and other information about the SOP.

        Returns:
            int: The absolute value of the score to be used for sorting
        """
        return abs(x[0])
    
    def SentenceSearch(self, count: int, tokens: List) -> int:
        """Scores an SOP based on specific sentences in the search input

        Args:
            count (int): Current score of the SOP
            tokens (List): Tokenized version of the SOP

        Returns:
            int: The new score of the SOP
        """
        if self.sentence != []:
            if set(self.sentence).issubset(set(tokens)):
                count += 5 * len(self.sentence)
        return count
    
    def DeepSearch(self,) -> None:
        """The Deep Search function that searches and scores the SOPs based on the search input.

        Raises:
            Exception: An SOP was not found or there was an error during the search.
        """
        descs = self.df["Description"].to_list()
        linked = self.df["Linked"].to_list()
        count_list = []
        for index, (desc, link) in enumerate(zip(descs, linked)):
            try:
                count = 0
                title = self.df["Title"].to_list()[index]
                tags = self.df["Tags"].to_list()[index]
                if self.TitleSearch(title):
                    count = 500
                else:
                    Ttokens = word_tokenize(title)
                    if link:
                        doc = GDocsScraper(os.path.basename(desc),local=True).text
                        tokens = word_tokenize(doc)
                    else:
                        tokens = word_tokenize(desc)
                    for search_word in self.SearchTokens:
                        if pos_tag([search_word])[0][1] == "NNS":
                            count = self.SimilarTS(Ttokens, count, search_word[:-1], title)
                        count = self.SimilarTS(Ttokens, count, search_word, title)
                    for search_word in self.SearchCull:
                        if pos_tag([search_word])[0][1] == "NNS":
                            count = self.Count(count,tokens, search_word[:-1])
                            count = self.TagSearch(count, search_word[:-1], tags)
                        count = self.Count(count, tokens, search_word)
                        count = self.TagSearch(count, search_word, tags)
                        count = self.SentenceSearch(count, tokens)
                    try:
                        count = count / len(self.SearchCull)
                    except:
                        raise Exception("SOP not found")
                count_list.append((count, self.df[self.df["Description"] == desc]["Title"].to_list()[0], desc))
            except Exception as e:
                print(f"Error during deep search: {e}")
                pass
        count_list.sort(key=self.SortCount, reverse=True)
        self.SOP = [SOP[1:] for SOP in count_list]
                
                        

if __name__ == "__main__":
    os.system("Clear")
    Search(input("Search or enter SOP name:\n"))
