import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.log import setup_logger
from ..errors import BusinessSiteNotLoaded

from .links import DOKUMENTY_FINANSOWE
class KRSDokumentyFinansowe:
    def __init__(self):
        setup_logger("KRS_DF_LOG", "KRS_DF_LOG")
        self.df_log = logging.getLogger("KRS_DF_LOG")
        self.df_log.info("KRS_DF_LOG log initialised.")
        self.df_log.info(f"Initialising KRSDokumentyFinansowe object")
        self.krs = None

        self.df_log.info("Loading webdriver options")
        self.ChromeOptions = webdriver.ChromeOptions()
        # self.ChromeOptions.add_argument("--headless")
        self.ChromeOptions.add_argument("--no-sandbox")
        self.ChromeOptions.add_argument("--disable-dev-shm-usage")

    @property
    def information_about_no_documents_to_display_is_present(self):
        try:
            WebDriverWait(self.driver, 1.5).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, 'span.ui-messages-info-detail'),
                    "Brak dokumentów dla KRS"
                )
            )
            return True
        except TimeoutException:
            return False

    @property
    def information_about_table_with_available_documents_is_present(self):
        try:
            WebDriverWait(self.driver, 1.5).until(
            EC.visibility_of_element_located(
                (By.ID, "searchForm:docTable:j_idt202")
                )
            )
            return True
        except TimeoutException:
            return False
        
    @property
    def throttling_error_from_webpage(self):
        try:
            WebDriverWait(self.driver, 1.5).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, 'span.ui-messages-info-detail'),
                    "Wymagane oczekiwanie pomiędzy kolejnymi wywołaniami"
                )
            )
            return True
        except TimeoutException:
            return False

    @property
    def is_business_page_open(self):
        """Checks if webdriver is opened on businees information site"""
        return (self.information_about_no_documents_to_display_is_present 
                or 
                self.information_about_table_with_available_documents_is_present)
    
    @property
    def number_of_pages_with_documents(self):
        if not self.is_business_page_open: raise BusinessSiteNotLoaded
        text = self.driver.find_element(By.CLASS_NAME, "ui-paginator-current").text
        return int(re.search(r"Strona: \d+/(\d+)", text).group(1))

    @property
    def number_of_current_page(self):
        if not self.is_business_page_open: raise BusinessSiteNotLoaded
        text = self.driver.find_element(By.CLASS_NAME, "ui-paginator-current").text
        return int(re.search(r"Strona: (\d+)/\d+", text).group(1))
    
    def initialize_driver(self) -> webdriver.Chrome:
        self.df_log.info("Initialising webdriver")
        self.driver = webdriver.Chrome(options=self.ChromeOptions)
        return self.driver

    def search_krs(self, krs: str):
        self.df_log.info(f"Searching for krs {krs} on website")
        self.krs = krs
        self.driver.get(DOKUMENTY_FINANSOWE["wyszukiwanie"])
        krs_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "unloggedForm:krs0"))
        )
        krs_input.clear()
        krs_input.send_keys(krs)

        time.sleep(0.5)

        search_button = WebDriverWait(self.driver, 1.5).until(
            EC.element_to_be_clickable((By.ID, "unloggedForm:timeDelBtn"))
        )
        ActionChains(self.driver).move_to_element(search_button).click().perform()

    def go_to_next_page(self):
        self.df_log.debug("Going to next page")
        next_button = WebDriverWait(self.driver, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-paginator-next"))
        )
        self.driver.execute_script("arguments[0].click();", next_button)

    def get_available_documents_list(self) -> list:
        self.df_log.info(f"Fetching list of available documents for krs {self.krs}")
        data = []      
        num_pages = self.number_of_pages_with_documents
        for i in range(num_pages):
            assert self.number_of_current_page == i+1
            self.df_log.debug(f"--Getting data from page {i+1} / {num_pages}")
            self.df_log.debug(f"Finding table object")
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#searchForm\\:docTable_data tr")
            num_of_rows = len(rows)
            for y, row in enumerate(rows):
                self.df_log.debug(f"----Irerating row {y+1} / {num_of_rows}")
                cells = row.find_elements(By.CSS_SELECTOR, "td[role='gridcell']")
                row_data = {}
                row_data['numer_strony'] = i+1
                row_data['rodzaj'] = cells[1].text.strip()
                row_data['data_od'] = cells[3].text.strip()  
                row_data['data_do'] = cells[4].text.strip() 
                row_data['status'] = cells[5].text.strip()
                data.append(row_data)
            self.go_to_next_page()
        return data