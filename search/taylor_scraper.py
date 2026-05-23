from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os

load_dotenv()

def search_taylor(abstract):

    results = []

    try:

        options = Options()

        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        wait = WebDriverWait(driver, 30)

        TAYLOR_URL = os.getenv("TAYLOR_URL")

        driver.get(TAYLOR_URL)

        textarea = wait.until(
            EC.presence_of_element_located(
                (By.ID, "journalfinder__abstract")
            )
        )

        textarea.send_keys(abstract)

        button = wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "journalfinder__search")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        driver.execute_script(
            "arguments[0].click();",
            button
        )

        wait = WebDriverWait(driver, 120)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "article.journalfinder__item--container"
                )
            )
        )

        time.sleep(2)

        articles = driver.find_elements(
            By.CSS_SELECTOR,
            "article.journalfinder__item--container"
        )

        for article in articles:

            try:

                title = article.find_element(
                    By.CSS_SELECTOR,
                    "a.journalfinder__item--title"
                ).text

                link = article.find_element(
                    By.CSS_SELECTOR,
                    "a.journalfinder__item--title"
                ).get_attribute("href")

                results.append({
                    "journal_name": title,
                    "impact_factor": "",
                    "citescore": "",
                    "publishing_model": "Unknown",
                    "submission_to_first_decision": "",
                    "publisher": "Taylor & Francis",
                    "url": link
                })

            except:
                pass

        driver.quit()

    except Exception as e:

        print("Taylor Error:", e)

    return results