"""Module to check website changes
"""
import os
import pickle
import hashlib
import difflib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from textdistance import levenshtein

class WebSite:
    """Encapsulate web site retrieval and storage logic
    """
    def __init__(self, siteurl: str, pickle_folder: str):
        self.url = siteurl
        urlhash = hashlib.md5(siteurl.encode("utf-8")).hexdigest()
        self.dbpath = os.path.join(pickle_folder, f"{urlhash}.pickle")
        self.contents = []
        self.num_pages_in_db = 0
        # if the file is not present - create it
        if not os.path.exists(self.dbpath):
            os.makedirs(os.path.dirname(self.dbpath), exist_ok=True)
            with open(self.dbpath, 'wb+') as f:
                pickle.dump(self.contents, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.load_from_db()

    def load_from_db(self) -> list:
        with open(self.dbpath, 'rb') as f:
            self.contents = pickle.load(f, encoding="UTF-8")
            self.num_pages_in_db = len(self.contents)

    def get_latest_date(self) -> datetime:
        return self.contents[self.num_pages_in_db-1]['date']

    def retrieve(self):
        """Retrieves the latest version of the page
        """
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        user_agent += "AppleWebKit/537.36 (KHTML, like Gecko) "
        user_agent += "Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.198"
        header = {'user-agent': user_agent}

        # Only retrieve pages older than 3 days
        if self.num_pages_in_db > 0:
            age = (datetime.now() - self.get_latest_date()).days
            if age < 3:
                print(f"WARN: Will not retrieve age {age} for {self.url}")
                return

        response = requests.get(self.url, headers=header)

        if response.status_code == 200:
            self.contents.append({
                "date": datetime.now(),
                "content": response.content
            })
            self.save()
            self.num_pages_in_db += 1
        else:
            print("ERROR: status code was " + str(response.status_code) + " URL: " + self.url)

    def save(self):
        with open(self.dbpath, 'wb+') as f:
            pickle.dump(self.contents, f, protocol=pickle.HIGHEST_PROTOCOL)

    def get_text(self, position: int = 0) -> str:
        """Strip html from page and return the text only

        Parameters
        ----------
        position : int, optional
            which page version counting from the last to return, by default 0

        Returns
        -------
        str
            stripped html page version
        """
        html = self.contents[self.num_pages_in_db-1-position]['content'].decode("utf-8")
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text(separator="\n", strip=True)

    def check_for_changes(self) -> float:
        """Checks for changes between the last two versions of the page.

        Returns
        -------
        float
            Similarity between 0 and 1.
        """
        # do not check if only one version exists
        if self.num_pages_in_db < 2:
            return 1

        t0 = self.get_text(0)
        t1 = self.get_text(1)
        sim = levenshtein.normalized_similarity(t0, t1)
        if sim < 1:
            print(f"{self.url} has changed. Similarity is: "+str(sim))
        return sim

    def diff(self, pos1: int = 1, pos2: int = 0):
        """Compare versions at pos1 and pos2,
        counting backwards in time

        Parameters
        ----------
        pos1 : int, optional
            First version position, by default 1
        pos2 : int, optional
            Second version position, by default 0
        """
        t0 = self.get_text(pos1).splitlines(keepends=True)
        t1 = self.get_text(pos2).splitlines(keepends=True)
        diff = difflib.unified_diff(t0, t1)
        print(''.join(diff), end="")
