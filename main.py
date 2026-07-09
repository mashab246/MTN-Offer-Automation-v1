import os
import time
from modules.browser import Browser
from modules.website import Website
from modules.excel_handler import ExcelHandler
from modules.bundle_mapping import OFFER_MAPPING, EXCEL_COLUMNS
from modules.sharepoint import SharePoint
from concurrent.futures import ThreadPoolExecutor


def show_progress(processed, total, failures, start_time):

    elapsed = time.time() - start_time

    speed = (processed / elapsed) * 60 if elapsed > 0 else 0

    remaining = total - processed

    eta_seconds = (
        remaining / (processed / elapsed)
        if processed > 0 else 0
    )

    elapsed_days = int(elapsed // 86400)
    elapsed_hours = int((elapsed % 86400) // 3600)
    elapsed_minutes = int((elapsed % 3600) // 60)

    eta_days = int(eta_seconds // 86400)
    eta_hours = int((eta_seconds % 86400) // 3600)

    print("\n===================================")
    print(f"Processed : {processed:,} / {total:,}")
    print(f"Speed     : {speed:.1f} numbers/min")
    print(
        f"Elapsed   : {elapsed_days}d "
        f"{elapsed_hours}h "
        f"{elapsed_minutes}m"
    )
    print(f"Remaining : {eta_days}d {eta_hours}h")
    print(f"Failures  : {failures:,}")
    print("===================================\n")

CHECKPOINT_FILE = "checkpoint.txt"


def load_checkpoint():

    if os.path.exists(CHECKPOINT_FILE):

        with open(CHECKPOINT_FILE, "r") as f:

            content = f.read().strip()

            if content:
                return int(content)

    return 0


def save_checkpoint(index):

    with open(CHECKPOINT_FILE, "w") as f:

        f.write(str(index))

def get_data_offers(phone, data_site):

    data_site.enter_number(phone)

    data_site.click_proceed()

    offers = data_site.get_available_offers()

    data_site.reset_page(DATA_URL)

    return offers


def get_voice_offers(phone, voice_site):

    voice_site.enter_number(phone)

    voice_site.click_proceed()

    offers = voice_site.get_available_offers()

    voice_site.reset_page(VOICE_URL)

    return offers


DATA_URL = "https://www.mtn.co.ug/deal-types/daily-data-bundles/"
VOICE_URL = "https://www.mtn.co.ug/deal-types/daily-voice-bundles/"

# ----------------------------
# Download latest SharePoint workbook
# ----------------------------

SHAREPOINT_URL = "https://airtelaf-my.sharepoint.com/:x:/r/personal/13214534_airtel_africa/_layouts/15/Doc.aspx?sourcedoc=%7BA7FD07A2-4CAA-4E33-8FB8-37ED1A0EF491%7D&file=Offer%20Check%20from%20Website.xlsx&fromShare=true&action=default&mobileredirect=true"

browser = Browser()

sharepoint = SharePoint(browser.driver)

sharepoint.open_workbook(SHAREPOINT_URL)


sharepoint.download_copy()

time.sleep(10)
for _ in range(60):
    try:
        excel = ExcelHandler(
            "Offer Check from Website.xlsx"
            )
        break
    except:
        time.sleep(1)

numbers = excel.get_phone_numbers()

#numbers = excel.get_phone_numbers()

start_index = load_checkpoint()

print(f"Found {len(numbers)} phone numbers")

print(
    f"Resuming from record "
    f"{start_index:,}"
)

data_browser = Browser()
voice_browser = Browser()

data_site = Website(data_browser.driver)
voice_site = Website(voice_browser.driver)

data_browser.open(DATA_URL)
voice_browser.open(VOICE_URL)

data_site.accept_cookies()
voice_site.accept_cookies()

print("\n==============================")
print("PROCESSING DATA + VOICE")
print("==============================")

total_numbers = len(numbers)
processed = 0
failures = 0

start_time = time.time()

executor = ThreadPoolExecutor(max_workers=2)

#for row, phone in numbers:
for index, (row, phone) in enumerate(
    numbers[start_index:],
    start=start_index
):

    print(f"\nProcessing {phone}")

    try:

        data_future = executor.submit(
            get_data_offers,
            phone,
            data_site
        )

        voice_future = executor.submit(
            get_voice_offers,
            phone,
            voice_site
        )

        data_offers = data_future.result()

        voice_offers = voice_future.result()

        # ======================
        # COMBINED OFFERS
        # ======================

        all_offers = (
            data_offers +
            voice_offers
        )

        for offer in all_offers:

            if offer in OFFER_MAPPING:

                excel_name = OFFER_MAPPING[offer]

                if excel_name not in EXCEL_COLUMNS:

                    print(
                        f"EXCEL COLUMN MISSING: "
                        f"{excel_name}"
                    )

                    continue

                column = EXCEL_COLUMNS[
                    excel_name
                ]

                excel.write_offer(
                    row,
                    column,
                    1
                )

    except Exception as e:

        failures += 1

        print(
            f"Failed for {phone}"
        )

        print(
            "Refreshing browsers..."
        )

        try:
            data_browser.driver.refresh()
        except:
            pass

        try:
            voice_browser.driver.refresh()
        except:
            pass

        time.sleep(3)

        continue

    processed += 1

    if processed % 50 == 0:

        show_progress(
            processed,
            total_numbers,
            failures,
            start_time
        )

    if processed % 50 == 0:

        print(
            "Saving checkpoint..."
        )

        try:

            excel.save()

            save_checkpoint(index)

            print(
                f"Current checkpoint: {index:,}"
            )

            print(
                f"Checkpoint saved "
                f"at record "
                f"{index:,}"
            )

        except Exception as e:
            print(
                f"Save failed: {e}"
            )

# Save Excel
excel.save()

if os.path.exists(
    CHECKPOINT_FILE
):

    os.remove(
        CHECKPOINT_FILE
    )

    print(
        "Checkpoint cleared."
    )


print("\nExcel Saved Successfully.")


# Close Browser
executor.shutdown(wait=True)
#browser.close()

print("\n===================================")
print("FINAL SUMMARY")
print("===================================")

show_progress(
    processed,
    total_numbers,
    failures,
    start_time
)

"""print(
    f"Data Failures : {failures:,}"
)

print(
    f"Voice Failures: "
    f"{failures:,}"
)

print(
    f"Total Failures: "
    f"{failures + failures:,}"
)"""

print(
    f"Total Failures: {failures:,}"
)

print("===================================\n")

print("\nAutomation Finished Successfully!")