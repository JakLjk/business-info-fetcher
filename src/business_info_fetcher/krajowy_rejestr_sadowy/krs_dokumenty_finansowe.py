import time
import re
import logging
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.log import setup_logger
from ..errors import (BusinessSiteNotLoaded, WebpageThrottlingError, 
                      NoDataToScrape, WebpageSessionExpired,
                      DocumentNotFound)
from .links import DOKUMENTY_FINANSOWE

class KRSDokumentyFinansowe:
    def __init__(self, job_id:str):
        load_dotenv()

        setup_logger("KRS_DF_LOG", "KRS_DF_LOG")
        self.df_log = logging.getLogger("KRS_DF_LOG")
        self.df_log.info("KRS_DF_LOG log initialised.")
        self.df_log.info(f"Initialising KRSDokumentyFinansowe object")
        self.krs = None
        self.job_id = job_id

        self.df_log.info("Loading webdriver options")
        headless_mode = bool(int(os.getenv('KRS_DOCUMENTS_SCRAPING_BROWSER_HEADLESS')))
        self.selenium_chrome_download_folder_path = os.getenv('SELENIUM_CHROME_DOWNLOADS_FOLDER')
        self.save_downloaded_documents_path = os.getenv("SAVE_DOWNLOADED_DOCUMENTS_FOLDER")

        self.ChromeOptions = webdriver.ChromeOptions()
        #TODO
        self.webdriver_standard_wait_time = None
        self.time_sleep_standard_wait_time = None
        self.df_log.debug(f"Running in headless mode: {headless_mode}")
        if headless_mode:
            self.ChromeOptions.add_argument("--headless")
        self.ChromeOptions.add_argument("--no-sandbox")
        self.ChromeOptions.add_argument("--disable-dev-shm-usage")
        self.df_log.info("Declaring folder path for downloaded files")
        os.makedirs(self.selenium_chrome_download_folder_path, exist_ok=True)
        prefs = {
            "download.default_directory": self.selenium_chrome_download_folder_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            }
        self.ChromeOptions.add_experimental_option("prefs", prefs)

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
    def session_expired_error_from_webpage(self): #TODO
        pass

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
        self.df_log.debug(f"Clearing information about available document list")
        self.document_list = None
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

        if self.throttling_error_from_webpage:
            raise WebpageThrottlingError("Throttled during loading webpage - probably too many requests")
        if not self.is_business_page_open:
            raise BusinessSiteNotLoaded("Site was not loaded properly")
        if self.information_about_no_documents_to_display_is_present:
            raise NoDataToScrape(f"There are no records to be returned for krs {self.krs}")

    def go_to_next_page(self):
        self.df_log.debug("Going to next page")
        next_button = WebDriverWait(self.driver, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-paginator-next"))
        )
        element_is_disabled = "ui-state-disabled" in next_button.get_attribute("class")
        if element_is_disabled:
            self.df_log.info("Tried clicking on button, but first page is already open")
        else:
            self.driver.execute_script("arguments[0].click();", next_button)

    def go_to_previous_page(self):
        self.df_log.debug("Going to previous page")
        previous_button = WebDriverWait(self.driver, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-paginator-prev"))
        )
        element_is_disabled = "ui-state-disabled" in previous_button.get_attribute("class")
        if element_is_disabled:
            self.df_log.info("Tried clicking on button, but first page is already open")
        else:
            self.driver.execute_script("arguments[0].click();", previous_button)

    def go_to_first_page(self):
        self.df_log.debug("Going to first page")
        first_page_button = WebDriverWait(self.driver, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-paginator-first"))
        )
        element_is_disabled = "ui-state-disabled" in first_page_button.get_attribute("class")
        if element_is_disabled:
            self.df_log.info("Tried clicking on 'go to first page button, but first page is already open")
        else:
            self.driver.execute_script("arguments[0].click();", first_page_button)

    def get_available_documents_list(self) -> list:
        self.df_log.info(f"Fetching list of available documents for krs {self.krs}")
        #TODO - session expired error checking
        if self.session_expired_error_from_webpage:
            raise WebpageSessionExpired("Web session has expired due to long inactivity")
        all_rows_data = []    
        self.go_to_first_page()  
        num_pages = self.number_of_pages_with_documents
        for i in range(num_pages):
            assert self.number_of_current_page == i+1
            self.df_log.debug(f"--Getting data from page {i+1} / {num_pages}")
            self.df_log.debug(f"--Finding table object")
            data = self.get_document_list_from_current_page()
            all_rows_data.extend(data)
            self.go_to_next_page()
        self.document_list = all_rows_data
        return all_rows_data

    def get_document_list_from_current_page(self) -> list:
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#searchForm\\:docTable_data tr")
        num_of_curr_page = self.number_of_current_page
        num_of_rows = len(rows)
        rows_data_list = []
        for y, row in enumerate(rows):
            self.df_log.debug(f"----Irerating row {y+1} / {num_of_rows}")
            cells = row.find_elements(By.CSS_SELECTOR, "td[role='gridcell']")
            row_data = {}
            row_data['numer_strony'] = num_of_curr_page
            row_data['rodzaj'] = cells[1].text.strip()
            row_data['data_od'] = cells[3].text.strip()  
            row_data['data_do'] = cells[4].text.strip() 
            row_data['status'] = cells[5].text.strip()
            rows_data_list.append(row_data)
        return rows_data_list
    
    def get_document_by_name_and_date(self, document_name:str,
                                        date_from:str,
                                        date_to:str):
        self.df_log.info(f"Fetching document {document_name} - {date_from} for krs {self.krs}")
        self.go_to_first_page()
        if self.session_expired_error_from_webpage:
            raise WebpageSessionExpired("Web session has expired due to long inactivity")
        num_pages  = self.number_of_pages_with_documents
        document_not_found = True
        page_num = 1
        while document_not_found and page_num <= num_pages:
            assert self.number_of_current_page == page_num
            self.df_log.debug(f"--Checking page {page_num} / {num_pages} for report")
            self.df_log.debug(f"--Finding table object")
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#searchForm\\:docTable_data tr")
            num_of_rows = len(rows)
            for y, row in enumerate(rows):
                self.df_log.debug(f"----Irerating row {y+1} / {num_of_rows}")
                cells = row.find_elements(By.CSS_SELECTOR, "td[role='gridcell']")
                nazwa_dokumentu = cells[1].text.strip()
                data_od = cells[3].text.strip()  
                data_do = cells[4].text.strip() 
                pokaz_szczegoly_button = cells[6]
                if (nazwa_dokumentu == document_name and
                    data_od == date_from):  
                    document_not_found = False
                    self.download_document(pokaz_szczegoly_button)     
                    time.sleep(2)
                    filename = f"{document_name} {date_from} - {date_to}"
                    saved_to_path = self.save_downloaded_documents(filename)
                    return saved_to_path
            page_num += 1
            self.go_to_next_page()

    def get_all_documents(self) -> list:
        self.df_log.info(f"Downloading all documents for krs {self.krs}")
        #TODO - session expired error checking
        if self.session_expired_error_from_webpage:
            raise WebpageSessionExpired("Web session has expired due to long inactivity")
        self.go_to_first_page()  
        num_pages = self.number_of_pages_with_documents
        saved_to_paths = []
        abs_row_number = 0
        for i in range(num_pages):
            assert self.number_of_current_page == i+1
            self.df_log.debug(f"--Downloading documents from page {i+1} / {num_pages}")
            self.df_log.debug(f"--Finding table object")
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#searchForm\\:docTable_data tr")
            num_of_rows = len(rows)
            for num_row in range(num_of_rows):
                self.df_log.debug(f"----Irerating row {num_row + abs_row_number+1} / {num_of_rows+abs_row_number+1}")
                self.df_log.debug(f"Searching for row element")
                cells = self.driver.find_element(By.CSS_SELECTOR, f"[data-ri=\"{str(num_row+abs_row_number)}\"]")
                self.df_log.debug("Searching for cells within the row")
                cells = cells.find_elements(By.CSS_SELECTOR, "td[role='gridcell']")
                nazwa_dokumentu = cells[1].text.strip()
                data_od = cells[3].text.strip()  
                data_do = cells[4].text.strip() 
                show_document_details_button = cells[6]
                filename = f"{nazwa_dokumentu} {data_od} - {data_do}"
                self.df_log.debug(f"Downloading file {filename}")
                self.download_document(show_document_details_button)
                time.sleep(2)
                self.df_log.debug(f"Saving file")
                save_path = self.save_downloaded_documents(filename)
                self.df_log.debug(f"File saved to: {save_path}")
                saved_to_paths.append(save_path)
            abs_row_number += num_of_rows 
            self.go_to_next_page()
        return saved_to_paths

    def download_document(self, show_document_details_button):
        self.df_log.info("Document has ben found proceeding to download.")
        self.df_log.debug(f"Clicking on pokaz szczegoly button'")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", show_document_details_button)
        show_document_details_button.click()
        self.df_log.debug("Searching for on download documents button")
        time.sleep(1)
        pobierz_dokumenty_button = self.driver.find_element(By.ID, "searchForm:j_idt321")
        self.df_log.debug("Clicking on download documents button")
        pobierz_dokumenty_button.click()
        self.df_log.debug("Searching for download button")
        time.sleep(1)
        akcja_pobierz_button = self.driver.find_element(By.ID, "searchForm:j_idt112")
        self.df_log.debug("Clicking on download document button")
        akcja_pobierz_button.click()
        self.df_log.debug(f"Searching for close button")
        close_btn = self.driver.find_element(By.CLASS_NAME,"ui-icon.ui-icon-closethick")
        self.df_log.debug(f"Clicking on close button")
        close_btn.click()
        self.df_log.debug(f"Searching for close button 2")
        close_btn2 = self.driver.find_element(By.ID,"searchForm:j_idt233")
        self.df_log.debug(f"Clicking on close button 2")
        close_btn2.click()

    def save_downloaded_documents(self,
                                  file_folder_name:str) ->str:
        downloaded_files_path = Path(self.selenium_chrome_download_folder_path)
        destination_folder =self.save_downloaded_documents_path
        full_destination_path = Path(destination_folder) / self.job_id / file_folder_name
        os.makedirs(full_destination_path, exist_ok=True)
        for file in downloaded_files_path.iterdir():
            shutil.move(str(file), str(full_destination_path))
        return str(full_destination_path)
    
    #TODO
    def __files_being_currently_saved(self):
        timeout = 10
        start_time = time.time()
        temp_extensions = ('.crdownload', '.part', '.tmp')
        existing_files = set(self.selenium_chrome_download_folder_path.glob('*'))
        while temp_files and (time.time() - start_time) < timeout:
            temp_files = 0
            for f in existing_files:
                if f.name.endswith(temp_extensions):
                    temp_files += 1
            

                    



        