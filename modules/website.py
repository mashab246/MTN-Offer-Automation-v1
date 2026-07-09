from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Website:

    def __init__(self, driver):
        self.driver = driver

    def accept_cookies(self):

        #time.sleep(3)

        button = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'button[data-cc="accept-all"]')
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            button
        )

        #time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print("Cookies accepted.")

    def enter_number(self, phone):
        number_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "kz_mtn_bundle_number")
            )
        )

        number_box.clear()
        number_box.send_keys(phone)

    def click_proceed(self):

        #time.sleep(2)

        button = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, "kz_regional_bundle_number_proceed")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            button
        )

        #time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print("Proceed clicked.")
        

    def get_available_offers(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "_card-deal__title")
                )
            )
        except TimeoutException:
            print("No offers found.")
            return []

        offers = []

        cards = self.driver.find_elements(
            By.CLASS_NAME,
            "_card-deal__title"
        )

        for card in cards:
            offer = card.text.strip()

            if offer:
                offers.append(offer)

        return offers


    def reset_page(self, url):
        """
        Reload the Daily Data Bundles page so it is ready for the next number.
        """

        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "kz_mtn_bundle_number")
            )
        )
