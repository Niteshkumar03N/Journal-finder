# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# import time
# import csv
# import pandas as pd


# def search_cwauthors(abstract_text):

#     options = Options()

#     # Headless mode
#     options.add_argument("--headless")

#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=options
#     )

#     wait = WebDriverWait(driver, 120)

#     driver.get("https://www.cwauthors.com/journal-finder")

#     # =============================
#     # ENTER ABSTRACT
#     # =============================
#     textarea = wait.until(
#         EC.presence_of_element_located((By.TAG_NAME, "textarea"))
#     )

#     textarea.send_keys(abstract_text)

#     # =============================
#     # CLICK BUTTON
#     # =============================
#     button = wait.until(
#         EC.element_to_be_clickable((By.TAG_NAME, "button"))
#     )

#     driver.execute_script(
#         "arguments[0].click();",
#         button
#     )

#     # =============================
#     # WAIT RESULTS
#     # =============================
#     wait.until(
#         EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, "div.journalfinder_result-boxin__jwPt9")
#         )
#     )

#     all_data = []

#     page = 1

#     while True:

#         results = driver.find_elements(
#             By.CSS_SELECTOR,
#             "div.journalfinder_result-boxin__jwPt9"
#         )

#         for result in results:

#             try:

#                 title = result.find_element(
#                     By.CSS_SELECTOR,
#                     "h3.journalfinder_colmaintitle__Hp_sp"
#                 ).text.strip()

#                 link = result.find_element(
#                     By.TAG_NAME,
#                     "a"
#                 ).get_attribute("href")

#                 publisher = "N/A"
#                 citescore = "N/A"
#                 impact_factor = "N/A"

#                 fields = result.find_elements(
#                     By.CSS_SELECTOR,
#                     "div.journalfinder_journal--data__sIYJk"
#                 )

#                 for field in fields:

#                     try:

#                         label = field.find_element(
#                             By.TAG_NAME,
#                             "span"
#                         ).text.strip()

#                         value = field.find_element(
#                             By.TAG_NAME,
#                             "b"
#                         ).text.strip()

#                         if "Publisher" in label:
#                             publisher = value

#                         elif "CITE Score" in label:
#                             citescore = value

#                         elif "Impact Factors" in label:
#                             impact_factor = value

#                     except:
#                         pass

#                 data = {
#                     "Title": title,
#                     "Publisher": publisher,
#                     "CiteScore": citescore,
#                     "Impact Factor": impact_factor,
#                     "Link": link
#                 }

#                 all_data.append(data)

#             except:
#                 pass

#         # =============================
#         # NEXT PAGE
#         # =============================
#         try:

#             next_button = driver.find_element(
#                 By.CSS_SELECTOR,
#                 "li.journalfinder_next-button__mQwUu a"
#             )

#             aria_disabled = next_button.get_attribute("aria-disabled")

#             if aria_disabled == "true":
#                 break

#             driver.execute_script(
#                 "arguments[0].click();",
#                 next_button
#             )

#             page += 1

#             time.sleep(3)

#         except:
#             break

#     driver.quit()

#     # SAVE CSV
#     df = pd.DataFrame(all_data)

#     df.to_csv("journals.csv", index=False)

#     return df 


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import json


def search_cwauthors(abstract_text):

    options = Options()

    # Headless mode
    options.add_argument("--headless")

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 120)

    driver.get("https://www.cwauthors.com/journal-finder")

    # =============================
    # ENTER ABSTRACT
    # =============================
    textarea = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
    )

    textarea.send_keys(abstract_text)

    # =============================
    # CLICK BUTTON
    # =============================
    button = wait.until(
        EC.element_to_be_clickable((By.TAG_NAME, "button"))
    )

    driver.execute_script(
        "arguments[0].click();",
        button
    )

    # =============================
    # WAIT RESULTS
    # =============================
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.journalfinder_result-boxin__jwPt9")
        )
    )

    all_data = []

    page = 1

    while True:

        results = driver.find_elements(
            By.CSS_SELECTOR,
            "div.journalfinder_result-boxin__jwPt9"
        )

        for result in results:

            try:

                title = result.find_element(
                    By.CSS_SELECTOR,
                    "h3.journalfinder_colmaintitle__Hp_sp"
                ).text.strip()

                link = result.find_element(
                    By.TAG_NAME,
                    "a"
                ).get_attribute("href")

                publisher = "N/A"
                citescore = "N/A"
                impact_factor = "N/A"

                fields = result.find_elements(
                    By.CSS_SELECTOR,
                    "div.journalfinder_journal--data__sIYJk"
                )

                for field in fields:

                    try:

                        label = field.find_element(
                            By.TAG_NAME,
                            "span"
                        ).text.strip()

                        value = field.find_element(
                            By.TAG_NAME,
                            "b"
                        ).text.strip()

                        if "Publisher" in label:
                            publisher = value

                        elif "CITE Score" in label:
                            citescore = value

                        elif "Impact Factors" in label:
                            impact_factor = value

                    except:
                        pass

                data = {
                        "journal_name":
                            title,

                        "impact_factor":
                            impact_factor,

                        "citescore":
                            citescore,

                        "submission_to_first_decision":
                            "N/A",

                        "publishing_model":
                            "N/A",

                        "publisher":
                            publisher,

                        "url":
                            link
                    }

                all_data.append(data)

            except:
                pass

        # =============================
        # NEXT PAGE
        # =============================
        try:

            next_button = driver.find_element(
                By.CSS_SELECTOR,
                "li.journalfinder_next-button__mQwUu a"
            )

            aria_disabled = next_button.get_attribute("aria-disabled")

            if aria_disabled == "true":
                break

            driver.execute_script(
                "arguments[0].click();",
                next_button
            )

            page += 1

            time.sleep(3)

        except:
            break

    driver.quit()

    # =============================
    # SAVE JSON
    # =============================
    with open(
        "journals.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    # RETURN JSON-LIKE DATA
    return all_data