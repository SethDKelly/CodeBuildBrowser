# agents/tools/web_scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

class WebScraper:
    def __init__(self, timeout: int = 10):
        """
        Initialize web scraper with configurable timeout
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; OllamaAgent/1.0)'
        })
        
    def fetch_page(self, url: str) -> str:
        """
        Fetch and return page content
        
        Args:
            url: URL to fetch
            
        Returns:
            Page content or error message
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"Error fetching page: {str(e)}"
            
    def extract_text(self, url: str, selector: str = None) -> str:
        """
        Extract text content from a webpage
        
        Args:
            url: URL to scrape
            selector: CSS selector to target specific elements
            
        Returns:
            Extracted text content
        """
        try:
            html = self.fetch_page(url)
            if html.startswith("Error"):
                return html
                
            soup = BeautifulSoup(html, 'html.parser')
            
            if selector:
                elements = soup.select(selector)
                return '\n'.join([elem.get_text(strip=True) for elem in elements])
            else:
                return soup.get_text(strip=True)
                
        except Exception as e:
            return f"Error extracting text: {str(e)}"
            
    def extract_links(self, url: str) -> str:
        """
        Extract all links from a webpage
        
        Args:
            url: URL to scrape
            
        Returns:
            JSON string of extracted links
        """
        try:
            html = self.fetch_page(url)
            if html.startswith("Error"):
                return html
                
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                absolute_url = urljoin(url, href)
                
                links.append({
                    'text': text,
                    'url': absolute_url
                })
                
            return json.dumps(links, indent=2)
            
        except Exception as e:
            return f"Error extracting links: {str(e)}"

def get_web_tool_schemas():
    """
    Get tool schemas for web scraping functions
    
    Returns:
        List of tool schemas compatible with Ollama
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "extract_text",
                "description": "Extract text content from a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the webpage to scrape"
                        },
                        "selector": {
                            "type": "string",
                            "description": "CSS selector to target specific elements (optional)"
                        }
                    },
                    "required": ["url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "extract_links",
                "description": "Extract all links from a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the webpage to scrape"
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    ]
