from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import pandas as pd
import os
from GDocs_Scraper import GDocsScraper
from sheet_collector import collect_sheet
from tqdm import tqdm

class Update:
    def __init__(self,):
        #print("Updating SOPs...")
        self.df = collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")
        self.ids = [os.path.basename(link) for link in self.df["Description"].to_list()]
        for id in self.ids:
            #print(f"Updating {id}...")
            GDocsScraper(id, skip=False, local=True, Update=True)

class Search:
    
    def __init__(self, Search: str = "",):
        self.Search = Search
        self.SOP = None
        if Search != "":
            try:
                self.SOPSearch(Search)
            except Exception as e:
                print(f"Error during search: {e}")
    
    def SCorrections(self, Search: str = "",):
        if self.Search == "":
            self.Search = Search
        tokens = word_tokenize(self.Search.lower())
                
    def SOPSearch(self, Search: str = "",):
        self.SCorrections(Search)
        self.Cull()
        self.df = collect_sheet("150ygap01bZaEbxKNFHNXIee60i2AiNySWz6EijS5G4k", "lists")
        self.DeepSearch()
        if self.SOP is None:
            raise Exception("SOP not found")
    
        
    def TitleSearch(self, title) -> bool:
        if self.Search.lower() == title.lower():
            self.SOP = self.df[self.df["Title"] == title]
            return True
        return False
    
    def SimilarTS(self, Ttokens, count, search_word, title):
        if search_word.capitalize() in Ttokens:
            count += 5
        if search_word.upper() in Ttokens:
            count += 5
        if search_word.lower() in Ttokens:
            count += 5
        if search_word.capitalize() == title:
            count += 10
        if search_word.lower() == title:
            count += 10
        if search_word.upper() == title:
            count += 10
        return count
    
    def Cull(self,):
        self.SearchTokens = word_tokenize(self.Search)
        #print(pos_tag(self.SearchTokens))
        self.sentence = []
        if "``" in self.SearchTokens:
            for word in self.SearchTokens[self.SearchTokens.index('``') + 1:]:
                if "''" in word:
                    break
                else:
                    self.sentence.append(word)
        self.SearchCull = [word[0] for word in pos_tag(self.SearchTokens) if word[1] not in ["CC", "IN", "DT", "PRP", "VBP", "''", "``", "TO", "PRP$", ".", "WP", "VBZ",","] and word[0] not in ["process", "SOP", "do"]]
        if self.SearchCull == []:
            self.SearchCull = self.SearchTokens
    
    def Count(self, count, tokens, search_word):
        if search_word.lower() in tokens:
            count += tokens.count(search_word.lower())
        if search_word.capitalize() in tokens:
            count += tokens.count(search_word.capitalize())
        if search_word.upper() in tokens:
            count += tokens.count(search_word.upper())
        return count
    
    def TagSearch(self, count, search_word, tags,):
        if search_word.capitalize() in tags:
            count += 5
        return count
    
    def SortCount(self, x):
        return abs(x[0])
    
    def SentenceSearch(self, count, tokens):
        if self.sentence != []:
            if set(self.sentence).issubset(set(tokens)):
                count += 5 * len(self.sentence)
        return count
    
    def DeepSearch(self,):
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
                        #print(doc)
                        tokens = word_tokenize(doc)
                    else:
                        tokens = word_tokenize(desc)
                    for search_word in self.SearchTokens:
                        if pos_tag([search_word])[0][1] == "NNS":
                            count = self.SimilarTS(Ttokens, count, search_word[:-1], title)
                        count = self.SimilarTS(Ttokens, count, search_word, title)
                    for search_word in self.SearchCull:
                        if pos_tag([search_word])[0][1] == "NNS":
                            #print(self.SearchCull, search_word)
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
