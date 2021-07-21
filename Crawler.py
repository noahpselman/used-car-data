from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import bs4

from time import sleep


URL = "https://www.carfax.com/cars-for-sale"
ZIP = '60637'

class CarfaxCrawler():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def access_site(self, url):
        self.driver.get(url)
        sleep(2) # fix this later

    def search(self, make, model):
        make_path = '//*[@id="makeModelPanel"]/form/div[1]/div/select'
        model_path = '//*[@id="makeModelPanel"]/form/div[2]/div/select'
        zip_path = '//*[@id="makeModelPanel"]/form/div[3]/div/div[4]/div/input'
        next_button_path = '//*[@id="make-model-form-submit"]'
        show_results_button_path = '//*[@id="react-app-main"]/div/div[2]/div/div/main/div[3]/div[1]/div/div[2]/footer/div/div/button'
        
        # try:
        make_menu_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, make_path)))
        make_menu = Select(make_menu_element)
        make_menu.select_by_value(make)

        model_menu_element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, model_path)))
        model_menu = Select(model_menu_element)
        model_menu.select_by_value(model)

        zip_field_element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, zip_path)))
        zip_field_element.send_keys(ZIP)

        next_button_element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, next_button_path)))
        next_button_element.click()

        sleep(1)

        show_results_button_element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, show_results_button_path)))
        show_results_button_element.click()

    def get_html_generator(self):
        """returns generator that serves html pages 1 at a time

        Yields:
            str: html page
        """
        next_path = '//*[@id="ucl-microapp-srp-content"]/div/div[3]/div[2]/div/div/button[2]'
        next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, next_path)))
        i=0
        while next_button.get_attribute('aria-disabled') == 'false':
            print("iteration i", i)
            i += 1
            yield self.driver.page_source
            next_button.click()
            sleep(1) # find better way to do this
    





# if __name__ == '__main__':
#     crawler = Crawler()
#     crawler.access_site(URL)
#     crawler.search('Subaru', 'Outback')

