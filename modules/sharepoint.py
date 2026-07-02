import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SharePoint:

    def __init__(self, driver):
        self.driver = driver

    def open_workbook(self, url):
        self.driver.get(url)

    def download_copy(self):

        wait = WebDriverWait(self.driver, 30)

        wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "WacFrame_Excel_0")
            )
        )

        print("switched to excel frame")
         # Give SharePoint time to finish rendering the ribbon
        wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("step 1: looking for file")

        # File
        """file_btn = wait.until(
            EC.element_to_be_clickable(
                #(By.XPATH, "//span[text()='File']")
                (By.XPATH, "//*[normalize-space()='File']")
            )
        )
        file_btn.click
        print("step 2: file clicked")"""
        file_text = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[normalize-space()='File']")
            )
        )

        file_button = file_text.find_element(By.XPATH, "./ancestor::button[1]")

        self.driver.execute_script(
            "arguments[0].click();",
            file_button
        )

        print("File clicked")

        time.sleep(3)

        print("Current URL:", self.driver.current_url)

        print("Page title:", self.driver.title)

        print("Info elements:",
            len(self.driver.find_elements(By.XPATH, "//*[normalize-space()='Info']")))

        print("Step 3: Looking for Info")

        info_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Info']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            info_btn
        )

        #time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            info_btn
        )

        print("Info clicked")

        # Give the side panel time to open
        #time.sleep(3)

        print("Step 4: Looking for Open in Desktop")

        open_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Open in Desktop']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            open_btn
        )

        #time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            open_btn
        )

        print("Open in Desktop clicked")

        #time.sleep(2)

        print("Workbook download initiated...")

    def wait_for_download(self, folder):

        while True:

            files = os.listdir(folder)

            downloading = [
                f for f in files
                if f.endswith(".crdownload")
                or f.endswith(".tmp")
            ]

            if downloading:
                time.sleep(1)
                continue

            excel = [
                f for f in files
                if f.endswith(".xlsx")
            ]

            if excel:
                latest = max(
                    [os.path.join(folder, f) for f in excel],
                    key=os.path.getmtime
                )

                print("Downloaded:", latest)

                return latest