import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service


class Browser:

    def __init__(self):

        # Project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Edge driver path
        driver_path = os.path.join(
            project_root,
            "drivers",
            "msedgedriver.exe"
        )

        # Downloads folder
        self.download_path = os.path.join(
            project_root,
            "downloads"
        )

        os.makedirs(self.download_path, exist_ok=True)

        options = webdriver.EdgeOptions()

        options.add_argument("--start-maximized")

        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        )

        self.driver = webdriver.Edge(
            service=Service(driver_path),
            options=options
        )

    def open(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()