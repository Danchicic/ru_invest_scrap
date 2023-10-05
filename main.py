import time
from time import gmtime, strftime

import fake_useragent

import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

from config import currencies

print("Coin name    1 день    1 месяц")


def generate_urls(currency: list[str]) -> dict[str, str]:
    urls = {}
    for k in currency:
        urls[k] = f"https://ru.investing.com/currencies/{k[:3]}-{k[3:]}-technical"
    return urls


def scrap_page(driver: webdriver) -> tuple[str, str]:
    # refreshing page to scrap new info
    driver.refresh()
    one_day_result = ''
    one_month_result = ''

    try:
        # clicking to '1 день' to scrap the value of 'Резюме'
        driver.find_element(By.PARTIAL_LINK_TEXT, '1 день').click()
        # finding class using name
        resume_block = driver.find_element(By.CLASS_NAME, 'summary')
        # scrapping needed result
        one_day_result: str = resume_block.find_element(By.TAG_NAME, 'span').text

        # repeat for '1 месяц'

        # clicking to '1 месяц' to scrap the value of 'Резюме'
        driver.find_element(By.PARTIAL_LINK_TEXT, '1 месяц').click()
        # finding class using name
        resume_block = driver.find_element(By.CLASS_NAME, 'summary')
        # scrapping needed result
        one_month_result: str = resume_block.find_element(By.TAG_NAME, 'span').text

    except Exception as ex:
        print(ex)
    finally:
        if one_day_result != '' and one_month_result != '':
            return one_day_result, one_month_result
        raise Exception("Some problems with scrap")


def main():
    # collecting urls
    urls = generate_urls(currency=currencies)
    print(urls)
    # generate fake useragent
    user = fake_useragent.UserAgent().random

    # collecting options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(f"user-agent={user}")

    # downloading webdriver
    chromedriver_autoinstaller.install()

    # initializing webdriver via options
    driver: webdriver = webdriver.Chrome(options=options)

    # opening all pages to scrap
    for url_name, url in urls.items():
        # getting url in new tab
        driver.get(url=url)
        # opening new tab
        driver.switch_to.new_window('tab')

    # ToDo: schedule every one minute
    # main <for> to scrap pages every one minute
    for i, url_name in enumerate(currencies):
        driver.switch_to.window(driver.window_handles[i])
        one_day, one_month = scrap_page(driver=driver)
        print(url_name, one_day, one_month, strftime("%Y-%m-%d %H:%M:%S", gmtime()), sep='    ', end='\n')


if __name__ == '__main__':
    main()
