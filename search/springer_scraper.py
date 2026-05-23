from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
from dotenv import load_dotenv
import os

load_dotenv()


def find_journals(abstract_text):

    # ============================================
    # CHROME OPTIONS
    # ============================================

    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.maximize_window()

    # ============================================
    # OPEN WEBSITE
    # ============================================

    SPRINGER_URL = os.getenv("SPRINGER_URL")

    driver.get(SPRINGER_URL)

    wait = WebDriverWait(driver, 30)

    # ============================================
    # FIND ABSTRACT TEXTAREA
    # ============================================

    textarea = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "manuscript-abstract")
        )
    )

    # Scroll to textarea
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        textarea
    )

    time.sleep(2)

    # Click textarea
    driver.execute_script(
        "arguments[0].click();",
        textarea
    )

    time.sleep(1)

    # Enter abstract
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        textarea,
        abstract_text
    )

    # Trigger input event
    driver.execute_script("""
    arguments[0].dispatchEvent(
        new Event('input', { bubbles: true })
    );
    """, textarea)

    # ============================================
    # CLICK FIND JOURNALS BUTTON
    # ============================================

    find_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "search-submit")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        find_button
    )

    time.sleep(2)

    driver.execute_script(
        "arguments[0].click();",
        find_button
    )

    # ============================================
    # WAIT FOR RESULTS
    # ============================================

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.app-card-open")
        )
    )

    time.sleep(5)

    # ============================================
    # GET ALL JOURNALS
    # ============================================

    journals = driver.find_elements(
        By.CSS_SELECTOR,
        "li.app-card-open"
    )

    all_results = []

    # ============================================
    # SCRAPE EACH JOURNAL
    # ============================================

    for journal in journals:

        try:

            # ====================================
            # TITLE
            # ====================================

            try:
                title = journal.find_element(
                    By.CSS_SELECTOR,
                    "h2.app-card-open__heading a span"
                ).text.strip()

            except:
                title = ""

            # ====================================
            # LINK
            # ====================================

            try:
                link = journal.find_element(
                    By.CSS_SELECTOR,
                    "h2.app-card-open__heading a"
                ).get_attribute("href")

            except:
                link = ""

            # ====================================
            # DEFAULT VALUES
            # ====================================

            publishing_model = ""
            impact_factor = ""
            downloads = ""
            submission_to_first_decision = ""

            # ====================================
            # METADATA
            # ====================================

            metadata = journal.find_elements(
                By.CSS_SELECTOR,
                "dl.app-card-open__metadata-list div"
            )

            for item in metadata:

                try:

                    key = item.find_element(
                        By.CSS_SELECTOR,
                        "dt"
                    ).text.strip().lower()

                    value = item.find_element(
                        By.CSS_SELECTOR,
                        "dd"
                    ).text.strip()

                    # ====================================
                    # MATCH FIELDS
                    # ====================================

                    if "publishing model" in key:
                        publishing_model = value

                    elif "impact factor" in key:
                        impact_factor = value

                    elif "downloads" in key:
                        downloads = value

                    elif "submission to first decision" in key:
                        submission_to_first_decision = value

                except:
                    pass

            # ====================================
            # FINAL DATA
            # ====================================

            data = {
                "title": title,
                "link": link,
                "Publishing Model": publishing_model,
                "impact_factor": impact_factor,
                "Downloads": downloads,
                "submission_to_first_decision": submission_to_first_decision
            }

            if data not in all_results:
                all_results.append(data)

        except Exception as e:
            print("Error:", e)

    driver.quit()

    return all_results
