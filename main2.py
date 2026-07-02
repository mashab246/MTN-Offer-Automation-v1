import time
from modules.browser import Browser
from modules.website import Website
from modules.excel_handler2 import ExcelHandler
from modules.bundle_mapping import OFFER_MAPPING, EXCEL_COLUMNS
from modules.sharepoint import SharePoint
#from modules.profiler import PerformanceProfiler

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


DATA_URL = "https://www.mtn.co.ug/deal-types/daily-data-bundles/"
VOICE_URL = "https://www.mtn.co.ug/deal-types/daily-voice-bundles/"

# ----------------------------
# Download latest SharePoint workbook
# ----------------------------

SHAREPOINT_URL = "https://airtelaf-my.sharepoint.com/:x:/g/personal/13400403_airtel_africa/IQAnROVW_apXSJ2A0axNmhZiAcmSDh1qT8AUatkIzirW66Y?e=eJOza1&isSPOFile=1&ovuser=16c73727-979c-4d82-b3a7-eb6a2fddfe57%2C23245518%40airtel.africa&wdExp=TEAMS-TREATMENT&web=1&TeamsCID=2c21f2f2-9c46-49d3-b7a8-f0af79d561a1&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNjA1MjkwNjEyMSJ9&linkOpenTime=1782796862307"

browser = Browser()

sharepoint = SharePoint(browser.driver)

sharepoint.open_workbook(SHAREPOINT_URL)


sharepoint.download_copy()

time.sleep(10)
for _ in range(60):
    try:
        excel = ExcelHandler(
            "Offer Check from Website_Musa.xlsx"
            )
        break
    except:
        time.sleep(1)

numbers = excel.get_phone_numbers()

print(f"Found {len(numbers)} phone numbers")


browser = Browser()

website = Website(browser.driver)


print("\n==============================")
print("PROCESSING DATA BUNDLES")
print("==============================")

total_numbers = len(numbers)
processed = 0
failures = 0

start_time = time.time()


browser.open(DATA_URL)

website.accept_cookies()

#time.sleep(2)

for row, phone in numbers:

    print(f"\nProcessing DATA for {phone}")

    website.enter_number(phone)

    website.click_proceed()

    #time.sleep(3)
    try:
        data_offers = website.get_available_offers()

        for offer in data_offers:

            if offer in OFFER_MAPPING:

                excel_name = OFFER_MAPPING[offer]

                if excel_name not in EXCEL_COLUMNS:

                    print(
                        f"EXCEL COLUMN MISSING: "
                        f"{excel_name}"
                    )
                    continue

                column = EXCEL_COLUMNS[excel_name]

                print(
                    f"DATA MATCH: "
                    f"{offer} -> {column}"
                )

                excel.write_offer(
                    row,
                    column,
                    1
                )
    except Exception as e:

        failures += 1

        print(f"Failed on {phone}: {e}")

        try:
            website.reset_page(DATA_URL)
        except:
            pass

        processed += 1

        if processed % 50 == 0:
            show_progress(
                processed,
                total_numbers,
                failures,
                start_time
            )

        continue


    print(data_offers)

    processed += 1

    if processed % 50 == 0:

        show_progress(
            processed,
            total_numbers,
            failures,
            start_time
        )

        # checkpoint save every 500 numbers

        if processed % 100 == 0:

            print("Saving checkpoint...")

            try:
                excel.save()
                print("Checkpoint saved.")
            except Exception as save_error:
                print(
                    f"Checkpoint save failed: "
                    f"{save_error}"
                )

    website.reset_page(DATA_URL)

print("\n==============================")
print("PROCESSING VOICE BUNDLES")
print("==============================")

total_numbers = len(numbers)

voice_processed = 0
voice_failures = 0

voice_start_time = time.time()


browser.open(VOICE_URL)

website.accept_cookies()

#time.sleep(2)

for row, phone in numbers:

    print(f"\nProcessing VOICE for {phone}")

    try:

        website.enter_number(phone)

        website.click_proceed()

        voice_offers = website.get_available_offers()

        for offer in voice_offers:

            if offer in OFFER_MAPPING:

                excel_name = OFFER_MAPPING[offer]

                if excel_name not in EXCEL_COLUMNS:

                    print(
                        f"EXCEL COLUMN MISSING: "
                        f"{excel_name}"
                    )
                    continue

                column = EXCEL_COLUMNS[excel_name]

                print(
                    f"VOICE MATCH: "
                    f"{offer} -> {column}"
                )

                excel.write_offer(
                    row,
                    column,
                    1
                )

                print(voice_offers)

                website.reset_page(VOICE_URL)

    except Exception as e:

        voice_failures += 1

        print(
            f"Voice failed for "
            f"{phone}: {e}"
        )

        try:
            website.reset_page(VOICE_URL)
        except:
            pass

    voice_processed += 1

    if voice_processed % 50 == 0:

        show_progress(
            voice_processed,
            total_numbers,
            voice_failures,
            voice_start_time
        )

        if voice_processed % 100 == 0:

            print(
                "Saving checkpoint..."
            )

            try:
                excel.save()
                print(
                    "Checkpoint saved."
                )
            except Exception as e:
                print(
                    f"Checkpoint save failed: {e}"
                )


# Save Excel
excel.save()

print("\nExcel Saved Successfully.")


# Close Browser
browser.close()

print("\n===================================")
print("FINAL SUMMARY")
print("===================================")

show_progress(
    total_numbers,
    total_numbers,
    failures + voice_failures,
    start_time
)

print(
    f"Data Failures : {failures:,}"
)

print(
    f"Voice Failures: "
    f"{voice_failures:,}"
)

print(
    f"Total Failures: "
    f"{failures + voice_failures:,}"
)

print("===================================\n")

print("\nAutomation Finished Successfully!")