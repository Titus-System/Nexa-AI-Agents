from smolagents import Tool
import requests


class SearchWikipedia(Tool):
    name = "search_wikipedia"
    description = "Fetches a summary of a Wikipedia page for a given query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The search term to look up on Wikipedia.",
        },
    }
    output_type = "string"

    def forward(self, query: str) -> str:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            title = data["title"]
            extract = data["extract"]

            return f"Summary for {title}: {extract}"

        except requests.exceptions.RequestException as e:
            return f"Error fetching Wikipedia data: {str(e)}"

    def __init__(self, *args, **kwargs):
        super().__init__()
