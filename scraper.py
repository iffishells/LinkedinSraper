"""
modules used for scraping
"""
import csv
import os
import queue
import re
import time
from datetime import datetime

from Tools.driver import *

Header = ["companyUrl","companyName", "description", "companyId",
            "regularCompanyUrl", "industry",
          "employeesCount", "employeeCountRange", "logoUrl", "isHiring","timestamp",
          "no_of_employees", "year_founded",
          "website_url", "profile_url_actual"]

# location
LOCATION_XP_1 = '(//*[@class="t-14 t-black--light t-normal break-words"])'
LOCATION_XP_2 = '(//*[@class="org-top-card-summary-info-list__info-item"])[2]'
LOCATION_XP_3 = '(//*[@class="highcharts-point highcharts-negative highcharts-color-1"])[1]'

EMAIL = 'razamehar024@gmail.com'
PASSWORD = 'mianali024'

def writing_csv(row):
    fp = 'Output.csv'
    with open(fp, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if os.path.getsize(fp) == 0:
            writer.writerow(Header)
        writer.writerow(row)


class Linkedin(Selenium):
    """
    THIS class used for scraping LinkedIn
    """

    def login(self):
        """
        Login Function which is used to log in on LinkedIn
        :return:
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
            print('Waiting')
            time.sleep(2)
            print('Start Login')
            self.find_element(By.XPATH, '//input[@id="username"]').send_keys(EMAIL)
            time.sleep(3)
            self.find_element(By.XPATH, '//input[@id="password"]').send_keys(PASSWORD)
            self.find_element(By.XPATH, '//button[@type="submit"]').click()
            print('Logined')
        except TimeoutException:
            pass

    def _scraping(self, url):
        """
        This function scrapes the whole page data
        """
        print('Start Scraping')
        #name
        print('Getting name')
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@title]')))
            nm = self.text(By.XPATH, '//h1[@title]')
        except TimeoutException:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@title]')))
                nm = self.text(By.XPATH, '//h1[@title]')
            except TimeoutException:
                nm = ''

        # current URL
        try:
            cun_url = self.driver.current_url
        except NoSuchElementException:
            cun_url = ''

        #companyId
        try:
            com_id = url.split("/")[-1]
        except NoSuchElementException:
            com_id = ''

        # About_Btn
        try:
            self.find_element(By.XPATH, '(//li[@class])[10]//a').click()
            print('clicked')
            time.sleep(5)
        except TimeoutException:
            try:
                self.find_element(By.XPATH, '//a[text()="About"]').click()
                print('clicked')
                time.sleep(5)
            except NoSuchElementException:
                pass

        # Description
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ember-view"]//section//p')))
            desc = self.text(By.XPATH, '//div[@class="ember-view"]//section//p')
        except TimeoutException:
            desc = ''

        # industry
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//h3[text()="Industry"]/../following-sibling::*')))
            ind = self.text(By.XPATH, '//h3[text()="Industry"]/../following-sibling::*')
        except NoSuchElementException:
            ind = ''

        # # Year Found
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//h3[text()="Founded"]/../following-sibling::*')))
            date = self.text(By.XPATH, '//h3[text()="Founded"]/../following-sibling::*')
        except TimeoutException:
            date = ''

        # Team_Size
        try:
            te_si = self.text(By.XPATH, '//*[@class="t-normal t-black--light '
                                        'link-without-visited-state link-without-hover-state"]')
        except NoSuchElementException:
            te_si = ''

        #members
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//h3[text()="Company size"]/../'
            #                                                           'following-sibling::*//a//span')))
            member_num = self.text(By.XPATH, '//h3[text()="Company size"]/../following-sibling::*//a//span')
            employeesCount = member_num.split(" ")[0]
            print(employeesCount)
        except NoSuchElementException:
            employeesCount = ''

        # Website
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '(//dl[@class]//a)[1]')))
            web = self.href(By.XPATH,'(//dl[@class]//a)[1]')
        except NoSuchElementException:
            web = ''

        # Logo
        try:
            log = self.find_element(By.XPATH, '(//*[@loading="lazy"])[1]').get_attribute('src')
        except NoSuchElementException:
            log = ''

        #current time
        try:
            current_time = datetime.now()
        except:
            current_time = ''

        # in Hiring
        self.find_element(By.XPATH, '//a[text()="Jobs"]').click()
        time.sleep(2)
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//h2[@class="t-18"]')))
            job_dis = self.find_element(By.XPATH,'//h2[@class="t-18"]')
            if job_dis:
                hir_t = "True"
            else:
                hir_t = 'False'
        except:
            pass
            hir_t = "False"

        # # Banner
        # try:
        #     ban = self.src(By.XPATH, '(//img[@class="pic-cropper__target-image"])[1]')
        #     print(ban)
        # except NoSuchElementException:
        #     try:
        #         banner_element1 = self.find_element(By.XPATH, '(//div[@style])[2]')
        #         banner_element = banner_element1.get_attribute("style")
        #         url_pattern = re.compile(
        #             r"https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(),]|%[0-9a-fA-F][0-9a-fA-F])+"
        #         )
        #         urls = url_pattern.findall(banner_element)
        #         ban = " ".join(urls)
        #         print(ban)
        #     except NoSuchElementException:
        #         ban = ''

        # # Location
        # try:
        #     loc = self.text(By.XPATH, '(//*[@class="t-14 t-black--light t-normal break-words"])')
        #     print(loc)
        # except NoSuchElementException:
        #     try:
        #         self.wait.until(EC.presence_of_element_located((By.XPATH, LOCATION_XP_3)))
        #         self.find_element(By.XPATH, LOCATION_XP_3).click()
        #         location_element = self.text(By.XPATH, LOCATION_XP_1)
        #         parts = location_element.split(',')
        #         loc = parts[-1].strip()
        #         print(loc)
        #     except TimeoutException:
        #         loc = ''
        #name , des, company_id, industry, emloyeescount ,employeeCountRange, logo, is hiring
        row = [url, nm, desc, com_id,
               url, ind, employeesCount,
               te_si, log, hir_t, current_time,
               te_si, date, web, url]
        print(row)
        writing_csv(row)

    q = queue.Queue()
    with open('Linkedin.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = row['urls']
            if link:  # Ensure the link is not empty
                q.put(link)

    def open_links(self):
        """
        open links
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument("--head")  # Run in headless mode
        while not self.q.empty():
            links = self.q.get()
            if isinstance(links, str):
                print(f"Opening {links}")
                try:
                    self.get(links)
                    self.login()
                    time.sleep(10)
                    self._scraping(url=links)
                except ExceptionGroup:
                    print(f"Failed to open {links}")
            self.q.task_done()
            time.sleep(1)

