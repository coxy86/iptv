from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from string import Template
import logging
import os
import time
import json
import re


logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

SLEEP_TIME_IN_SECONDS = 6
URL_FILTERS = ["mpd", "lic"]


class ScrapeManager:
    __slots__ = ('driver', 'FOXTEL_USERNAME', 'FOXTEL_PASSWORD', 'FOXTEL_URL')

    def __init__(self):
        try:
            CHROME_PORT = os.environ.get("CHROME_PORT", "9222")
            logger.info(f"Loading chromer driver on port {CHROME_PORT}")
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_experimental_option(
                "debuggerAddress", f"127.0.0.1:{CHROME_PORT}")
            chromeOptions.set_capability(
                "goog:loggingPrefs", {"performance": "ALL"})

            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                           options=chromeOptions)

            self.FOXTEL_URL = os.environ.get(
                'FOXTEL_URL', "https://watch.foxtel.com.au/app/")
            self.FOXTEL_USERNAME = os.environ.get('FOXTEL_USERNAME')
            self.FOXTEL_PASSWORD = os.environ.get('FOXTEL_PASSWORD')
            if not self.FOXTEL_USERNAME or not self.FOXTEL_PASSWORD:
                raise Exception(
                    "FOXTEL_USERNAME and FOXTEL_PASSWORD are not set")

        except Exception as e:
            logger.error(f"Unable to initialise ScrapeManager: {type(e)} {e}")
            raise(e)

    @staticmethod
    def click_component(component):
        '''
        Static handler for when a component is clicked
        :param component:
        :return:
        '''
        component.click()
        time.sleep(SLEEP_TIME_IN_SECONDS)

    def refresh(self):
        '''
        This routine performs a web page refresh
        :return:
        '''
        self.driver.refresh()
        time.sleep(SLEEP_TIME_IN_SECONDS)

    def navigate_back(self):
        '''
        This routine navigates back to previous page
        :return:
        '''
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(SLEEP_TIME_IN_SECONDS)

    def navigate_to_url(self, url):
        '''
        This routine navigates to a provided url
        :param url:
        :return:
        '''
        self.driver.get(url)
        time.sleep(SLEEP_TIME_IN_SECONDS)

    def get_next_channel_list(self):
        '''
        This routine takes care of navigating to the next set of
        channels in the Live TV carousel section of the page
        :return:
        '''
        logger.info(f"Fetching next channels")
        try:
            live_tv = self.driver.find_element(
                By.XPATH, "//div[@title='Live TV']")
            elem = live_tv.find_element(
                By.XPATH, ".//div[@class='clicker right']")
            action = ActionChains(self.driver)
            action.click(on_element=elem)
            action.perform()
            return True
        except ElementNotInteractableException:
            logger.info("No more channels to fetch")
            return False
        except ElementClickInterceptedException:
            logger.info("No more channels to fetch")
            return False
        except Exception as e:
            logger.info(f"{e}")
            return False

    def fetch_channel_data(self, channel, urls, channel_url=None):
        '''
        Fetch channel data
        - This looks into the elements of Live TV section of the page to
            search for the specified channel
        - If channel is not found in one instance, this routine will automatically
            navigate to the next set of channels in the Live TV Carousel
        - If channel is found, this routine will navigate to the actual channel
            to begin fetching the URL information required to build m3u8
        - If channel is not found, the whole process fails
        :param channel:
        :param urls:
        :return:
        '''
        try:
            logger.info(f"fetching data for {channel}")
            if channel_url:
                self.navigate_to_url(channel_url)
                self.parse_urls_from_network_log(channel, urls)
                self.navigate_back()
                return

            self.refresh()
            b_continue = True
            live_tv = self.driver.find_element(
                By.XPATH, "//div[@title='Live TV']")
            while b_continue:
                divs = live_tv.find_elements(
                    By.XPATH, ".//div[@class='tile live playable']")
                for div in divs:
                    elements = div.text.split("\n")

                    if len(elements) > 1:
                        title = elements[1]
                        if title.endswith(channel):
                            self.click_component(div)
                            self.parse_urls_from_network_log(channel, urls)
                            self.navigate_back()
                            return

                b_continue = self.get_next_channel_list()

            raise Exception(f"Channel {channel} not found")
        except Exception as e:
            logger.error(f"Unable to parse data from Live TV section: {e}")
            raise(e)

    def deregister_chrome(self):
        try:
            logger.info("Deregister Chrome ...")
            self.open_app_settings()
            devices = self.driver.find_elements(By.XPATH, "//div[@class='device-line']")

            chrome_deregister = None
            for d in devices:
                span = d.find_element(By.XPATH, ".//span[@class='device-name']")
                if "(This device)" in span.text:
                    chrome_deregister = d.find_element(By.XPATH, ".//button[@class='settings-button']")
                    break

            if chrome_deregister:
                chrome_deregister.click()
                time.sleep(SLEEP_TIME_IN_SECONDS)
                modal = self.driver.find_element(By.XPATH, "//div[@class='modal']")
                buttons = modal.find_elements(By.XPATH, "//button[@class='settings-button']")
                for b in buttons:
                    if b.text == "Yes, do it":
                        logger.info("Chrome device is being de-registered!")
                        b.click()
                        return

        except NoSuchElementException as e:
            logger.error(f"Unable to access app settings")
            raise(e)


    def open_app_settings(self):
        try:
            logger.info("App Settings ...")
            self.driver.find_element(
                By.XPATH, "//div[@class='icon settings-icon']").click()
            self.driver.find_element(
                By.XPATH, "//span[@aria-label='App Settings']").click()
            time.sleep(SLEEP_TIME_IN_SECONDS)
        except NoSuchElementException as e:
            logger.error(f"Unable to access app settings")
            raise(e)

    def logout(self):
        '''
        Logout user automatically once automation is complete
        :return:
        '''
        try:
            logger.info("Logging out with deregistered chrome session ...")
            self.deregister_chrome()
        except NoSuchElementException as e:
            logger.error(f"Unable to logout session")
            raise(e)

    def load_and_login(self):
        '''
        Loads the FOXTEL website and automatically logs in user.
        This requires environment variables FOXTEL_USERNAME and FOXTEL_PASSWORD to be set
        :return:
        '''
        try:
            logger.info("Loading foxtel page and initiating login")
            self.driver.get(self.FOXTEL_URL)
            time.sleep(SLEEP_TIME_IN_SECONDS)

            username = self.driver.find_element(
                By.XPATH, "//input[@type='email']")
            password = self.driver.find_element(
                By.XPATH, "//input[@type='password']")
            username.send_keys(self.FOXTEL_USERNAME)
            password.send_keys(self.FOXTEL_PASSWORD)
            self.driver.find_element(By.XPATH, "//button[1]").click()
            time.sleep(SLEEP_TIME_IN_SECONDS)
        except NoSuchElementException as e:
            logger.info(f"A session appears to be active. Skipping login ....")
            try:
                self.driver.find_element(
                    By.XPATH, "//div[@class='icon settings-icon']")
            except Exception as e:
                logger.error(f"Something is not right: {e}")
                raise(e)

    def parse_urls_from_network_log(self, channel, urls):
        '''
        Parse data from network tab on chrome to fetch specific
        set of URLs as defined by URL_FILTERS
        :param urls:
        :param channel:
        :return:
        '''
        logs = self.driver.get_log("performance")

        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if "Network.responseReceived" == log["method"]:
                response = log["params"]["response"]

                if str(response["status"]) == "200":
                    if re.search(URL_FILTERS[0], str(response["url"])):
                        urls["mpd"] = str(response['url'])
                    elif re.search(URL_FILTERS[1], str(response["url"])):
                        urls["lic"] = str(response['url'])

        urls[f"{channel.lower().replace(' ', '_')}_mpd"] = urls.pop("mpd")
        urls[f"{channel.lower().replace(' ', '_')}_lic"] = urls.pop("lic")



    def build_m3u8(self, config):
        '''
        Main routine that builds m3u8
        - Loops through channels configured for each m3u8 file to be created
        - Loads a template file that is used to build the main m3u8 content
        :param config:
        :return:
        '''
        is_m3u8_created = False
        try:
            if config:
                self.load_and_login()
                for key in config:
                    channels = config[key]['channels']

                    urls = {}
                    for c in channels:
                        channel_name = c["channel_name"]
                        channel_url = c["url"] if "url" in c else None

                        self.fetch_channel_data(channel_name, urls, channel_url)

                    with open(f"templates/{key}.template") as f:
                        template = Template(f.read())
                        config[key]['m3u8'] = template.substitute(urls)
                
                is_m3u8_created = True
            else:
                logger.info("Config has not been set. No data will be parsed.")

        except Exception as e:
            logger.error(f"Unable to continue building m3u8: {e}")
        finally:
            self.logout()
            return is_m3u8_created
