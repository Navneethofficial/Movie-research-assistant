from typing import Dict, Any, List
import requests
import os
from duckduckgo_search import DDGS
import googleapiclient.discovery


# -------------------------------------------------------------------
# Base class for tools
# -------------------------------------------------------------------
class SearchTool:
    def __init__(self, name: str):
        self.name = name
        
    def search(self, query: str) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement search method")


# -------------------------------------------------------------------
# GOOGLE SEARCH (NEW)
# -------------------------------------------------------------------
class GoogleSearch(SearchTool):
    def __init__(self):
        super().__init__("Google Search")
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cse_id = os.getenv("GOOGLE_CSE_ID")

        if not self.api_key or not self.cse_id:
            raise ValueError("Google API Key or CSE ID missing. Set GOOGLE_API_KEY and GOOGLE_CSE_ID.")
        
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query: str) -> Dict[str, Any]:
        try:
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": query,
                "num": 5
            }

            response = requests.get(self.base_url, params=params)
            data = response.json()

            formatted = []
            for item in data.get("items", []):
                formatted.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })

            return {
                "tool": self.name,
                "query": query,
                "results": formatted
            }

        except Exception as e:
            return {
                "tool": self.name,
                "query": query,
                "error": str(e),
                "results": []
            }


# -------------------------------------------------------------------
# DuckDuckGo Search (optional)
# -------------------------------------------------------------------
class DuckDuckGoSearch(SearchTool):
    def __init__(self):
        super().__init__("DuckDuckGo Search")

    def search(self, query: str) -> Dict[str, Any]:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(
                    f"{query} imdb rating movie details",
                    backend="api",
                    max_results=5
                )

            formatted = []
            for r in results:
                formatted.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", "") or "https://duckduckgo.com",
                    "snippet": r.get("body", "")
                })

            return {
                "tool": self.name,
                "query": query,
                "results": formatted
            }

        except Exception as e:
            return {
                "tool": self.name,
                "query": query,
                "error": str(e),
                "results": []
            }


# -------------------------------------------------------------------
# OMDB API
# -------------------------------------------------------------------
class OMDBSearch(SearchTool):
    def __init__(self):
        super().__init__("OMDB Search")
        self.api_key = os.getenv("OMDB_API_KEY")
        if not self.api_key:
            raise ValueError("OMDB API Key must be set")
        self.base_url = "http://www.omdbapi.com/"
        
    def search(self, query: str) -> Dict[str, Any]:
        try:
            params = {
                "apikey": self.api_key,
                "s": query
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            formatted_results = []
            
            if data.get("Response") == "True":
                for item in data.get("Search", [])[:3]:

                    detail_params = {
                        "apikey": self.api_key,
                        "i": item["imdbID"]
                    }
                    detail_resp = requests.get(self.base_url, params=detail_params)
                    detail = detail_resp.json()

                    if detail.get("Response") == "True":
                        formatted_results.append({
                            "title": detail.get("Title", ""),
                            "year": detail.get("Year", ""),
                            "rating": detail.get("imdbRating", "N/A"),
                            "plot": detail.get("Plot", ""),
                            "director": detail.get("Director", ""),
                            "actors": detail.get("Actors", ""),
                            "genre": detail.get("Genre", ""),
                            "poster": detail.get("Poster", ""),
                            "imdbLink": f"https://www.imdb.com/title/{detail.get('imdbID', '')}"
                        })
                        
            return {
                "tool": self.name,
                "query": query,
                "results": formatted_results
            }
            
        except Exception as e:
            return {
                "tool": self.name,
                "query": query,
                "error": str(e),
                "results": []
            }


# -------------------------------------------------------------------
# YOUTUBE SEARCH (TRAILERS)
# -------------------------------------------------------------------
class YouTubeSearch(SearchTool):
    def __init__(self):
        super().__init__("YouTube Search")
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API Key must be set")

        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key
        )
        
    def search(self, query: str) -> Dict[str, Any]:
        try:
            search_terms = query.lower()
            if "trailer" not in search_terms:
                search_terms += " official trailer movie"
            
            search_response = self.youtube.search().list(
                q=search_terms,
                part="snippet",
                maxResults=1,
                type="video"
            ).execute()
            
            formatted_results = []
            
            for item in search_response.get("items", []):
                vid = item["id"]["videoId"]
                formatted_results.append({
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "link": f"https://www.youtube.com/watch?v={vid}",
                    "videoId": vid
                })
                
            return {
                "tool": self.name,
                "query": query,
                "results": formatted_results
            }
            
        except Exception as e:
            return {
                "tool": self.name,
                "query": query,
                "error": str(e),
                "results": []
            }
