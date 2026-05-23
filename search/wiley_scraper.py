from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv

import os
import time

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# MAIN FUNCTION
# =========================================

def scrape_wiley_journals(abstract_text):

    # =========================================
    # CHROME OPTIONS
    # =========================================

    options = Options()

    options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")

    options.add_argument("--disable-software-rasterizer")

    options.add_argument("--window-size=1920,1080")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-extensions")

    options.add_argument(
        "--user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"]
    )

    # =========================================
    # OPEN DRIVER
    # =========================================

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    wait = WebDriverWait(driver, 60)

    all_results = []

    try:

        # =========================================
        # OPEN WEBSITE
        # =========================================

        WILEY_URL = os.getenv("WILEY_URL")

        driver.get(WILEY_URL)

        # =========================================
        # TITLE INPUT
        # =========================================

        title_textarea = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'textarea[name="term"]'
                )
            )
        )

        title_textarea.send_keys(
            abstract_text
        )

        # =========================================
        # ABSTRACT INPUT
        # =========================================

        abstract_textarea = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'textarea[name="abstract"]'
                )
            )
        )

        abstract_textarea.send_keys(
            abstract_text
        )

        # =========================================
        # FIND BUTTON
        # =========================================

        find_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "button-findJournals"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            find_button
        )

        # =========================================
        # WAIT FOR RESULTS
        # =========================================

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".w-journal"
                )
            )
        )

        time.sleep(5)

        page_number = 1

        # =========================================
        # PAGINATION LOOP
        # =========================================

        while True:

            print(
                f"Scraping Page {page_number}"
            )

            wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        ".w-journal"
                    )
                )
            )

            journals = driver.find_elements(
                By.CSS_SELECTOR,
                ".w-journal"
            )

            # =========================================
            # LOOP THROUGH JOURNALS
            # =========================================

            for journal in journals:

                try:

                    # =========================================
                    # SAFE TITLE + LINK
                    # =========================================

                    try:

                        title_element = journal.find_element(
                            By.CSS_SELECTOR,
                            ".w-journal__title"
                        )

                        title = (
                            title_element
                            .text
                            .strip()
                        )

                        link = (
                            title_element
                            .get_attribute("href")
                        )

                    except:

                        continue

                    # =========================================
                    # VALUES
                    # =========================================

                    values = journal.find_elements(
                        By.CSS_SELECTOR,
                        ".w-title.w-title--size-sm.w-title__w-medium"
                    )

                    submission_time = (
                        values[1].text.strip()
                        if len(values) > 1
                        else ""
                    )

                    acceptance_rate = (
                        values[2].text.strip()
                        if len(values) > 2
                        else ""
                    )

                    publication_charge = (
                        values[3].text.strip()
                        if len(values) > 3
                        else ""
                    )

                    impact_factor = (
                        values[4].text.strip()
                        if len(values) > 4
                        else ""
                    )

                    # =========================================
                    # RELEVANCE SCORE
                    # =========================================

                    try:

                        relevance = (
                            journal.find_element(
                                By.CSS_SELECTOR,
                                ".score"
                            )
                            .get_attribute(
                                "data-score"
                            )
                        )

                    except:

                        relevance = ""

                    # =========================================
                    # FINAL DATA
                    # =========================================

                    data = {

                        "Title":
                            title,

                        "Link":
                            link,

                        "Submission To First Decision":
                            submission_time,

                        "Acceptance Rate":
                            acceptance_rate,

                        "Publication Charge":
                            publication_charge,

                        "Impact Factor":
                            impact_factor,

                        "Relevance Score":
                            relevance
                    }

                    if data not in all_results:

                        all_results.append(
                            data
                        )

                except Exception as e:

                    print(
                        "Error:",
                        e
                    )

            # =========================================
            # NEXT PAGE
            # =========================================

            try:

                next_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "li.next a"
                )

                aria_disabled = (
                    next_button.get_attribute(
                        "aria-disabled"
                    )
                )

                if aria_disabled == "true":

                    break

                driver.execute_script(
                    "arguments[0].click();",
                    next_button
                )

                page_number += 1

                time.sleep(5)

            except:

                break

    except Exception as e:

        print(
            "Main Error:",
            e
        )

    finally:

        driver.quit()

    return all_results