import os
import re
import requests
from bs4 import BeautifulSoup
from time import sleep

class LoadDocuments():
    def __init__(self, data_path: str, url_file: str) -> None:
        self.url_file = url_file
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)

    def load_documents(self) -> None:
        with open(self.url_file, 'r') as file:
            for line in file:
                url = line.strip()
                self.load_document_from_url(url)


    def load_document_from_url(self, url: str) -> None:
        def sanitize_filename(name: str) -> str:
            return re.sub(r'[\\/*?:"<>|]', "", name)
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            
            title_tag = soup.find("title")
            title_text = title_tag.get_text() if title_tag else "untitled"

            main_content = soup.find(id="bodyContent") or soup.find("body")
            
            main_content_html = main_content.prettify() if main_content else soup.prettify()

            file_name = os.path.join(self.data_path, f"{sanitize_filename(title_text)}.html")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(main_content_html)
            print(f"Saved content to {file_name}")
            sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")