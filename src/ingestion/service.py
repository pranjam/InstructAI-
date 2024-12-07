import requests
import xml.etree.ElementTree as ET
from fastapi import HTTPException
from common.vector_db import FaissIndexer
from common.logger import logger

class FaissIndexerService:
    """
    Service class that manages operations related to the Faiss index, such as fetching URL content
    and indexing documents in Faiss.
    """

    def __init__(self, faiss_index_file_path: str = "faiss_index_file.index"):
        """
        Initializes the FaissIndexerService class.

        Args:
            faiss_index_file_path (str): Path to the Faiss index file.
        """
        self.faiss_indexer = FaissIndexer(faiss_index_file_path)
        logger.info(f"FaissIndexerService initialized with index file at {faiss_index_file_path}")

    def is_sitemap(self, url: str) -> bool:
        """
        Determines if the given URL is a sitemap (ends with '.xml').

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is a sitemap, False otherwise.
        """
        if url.lower().endswith('.xml'):
            logger.info(f"URL {url} is identified as a sitemap.")
            return True
        logger.info(f"URL {url} is not a sitemap.")
        return False

    def get_urls_from_sitemap(self, sitemap_url: str) -> list:
        """
        Fetches all URLs from a sitemap.

        Args:
            sitemap_url (str): The URL of the sitemap.

        Returns:
            list: A list of URLs found in the sitemap.

        Raises:
            HTTPException: If the sitemap cannot be fetched or parsed.
        """
        try:
            logger.info(f"Fetching sitemap from {sitemap_url}")
            response = requests.get(sitemap_url)
            response.raise_for_status()  # Will raise an error for invalid responses
            logger.info(f"Successfully fetched sitemap from {sitemap_url}")
            
            # Check if the response is in XML format
            if "xml" not in response.headers["Content-Type"]:
                logger.error(f"The fetched content is not XML, but {response.headers['Content-Type']}")
                raise HTTPException(status_code=400, detail="Sitemap content is not in XML format.")

            # Parse the sitemap XML
            root = ET.fromstring(response.text)
            
            # Namespace dictionary to handle XML namespaces in XPath queries
            namespaces = {
                'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
            }
            
            # Extract all <loc> elements (which contain the URLs)
            urls = [url.text for url in root.findall(".//ns:loc", namespaces) if url.text]
            # Filter URLs that start with 'https://handbook.gitlab.com/handbook' ( custom for gilab we can change later only for demo)
            filtered_urls = [url for url in urls if url.startswith("https://handbook.gitlab.com/handbook")]
            logger.info(f"Extracted {len(filtered_urls)} URLs from the sitemap.")
            return filtered_urls
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching sitemap from {sitemap_url}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error fetching sitemap: {str(e)}")
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap XML from {sitemap_url}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error parsing sitemap XML: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


    def upload_url_and_index(self, url: str):
        """
        Fetches content from the given URL and indexes the documents in the Faiss index.

        If the URL is a sitemap, it fetches all URLs in the sitemap and processes them one by one.

        Args:
            url (str): URL to fetch content from.

        Returns:
            dict: A message indicating the success of the operation.
        
        Raises:
            HTTPException: If an error occurs during fetching or indexing.
        """
        try:
            logger.info(f"Processing URL: {url}")
            # If the URL is a sitemap, process all URLs in the sitemap
            if self.is_sitemap(url):
                logger.info(f"Processing sitemap: {url}")
                urls = self.get_urls_from_sitemap(url)
                for sitemap_url in urls:
                    logger.info(f"Processing URL from sitemap: {sitemap_url}")
                    # Fetch the content from each URL in the sitemap
                    documents = self.faiss_indexer.fetch_url_content(sitemap_url)
                    # Index the documents
                    self.faiss_indexer.index_documents(documents)
                logger.info(f"Successfully indexed documents from sitemap {url}")
                return {"message": f"Successfully indexed documents from sitemap {url}"}
            else:
                # If the URL is not a sitemap, process it normally
                logger.info(f"Processing regular URL: {url}")
                documents = self.faiss_indexer.fetch_url_content(url)
                self.faiss_indexer.index_documents(documents)
                logger.info(f"Successfully indexed documents from {url}")
                return {"message": f"Successfully indexed documents from {url}"}
        except HTTPException as e:
            logger.error(f"HTTP error occurred while processing URL {url}: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"An error occurred while uploading and indexing the URL {url}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred while uploading and indexing the URL: {str(e)}")
