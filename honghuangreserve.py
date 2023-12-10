import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import json
from time import sleep
import sys

# arg parse
parser = argparse.ArgumentParser()
parser.add_argument('zone')
args = parser.parse_args()

# user info
EMAIL = 'yolandawww123@gmail.com'
PWD = 'lovemami511'
# EMAIL = 'arkaradet@gmail.com'
# PWD = 'Arkaradet6131!'
ROUND = '5877'
# ROUND = '5854'
# ROUND = '5800'
SEAT = 1
ZONE = args.zone
# CONCERT = 'ZHANGZHEHAN 2023 CONCERT PRIMORDIAL THEATER IN BANGKOK'
home_url = "https://www.thaiticketmajor.com/concert/"
concert_url = 'https://www.thaiticketmajor.com/concert/zhang-zhehan-2023-primordial-theater-world-tour-in-bangkok.html'
# concert_url = 'https://www.thaiticketmajor.com/concert/thailandphil-2022-23-season.html'

# load chrome
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()

def setUp():
    driver.maximize_window()
    # print('maximized.')
    driver.get(home_url)
    driver.implicitly_wait(10)
    print('got url.')
    # print('wait terminated.')

def Login():
    driver.find_element(
        By.XPATH, '//*[@class="btn-signin item d-none d-lg-inline-block"]').click()
    sleep(1)
    username = driver.find_element(By.NAME, "username")
    username.send_keys(EMAIL)
    pwd = driver.find_element(By.NAME, "password")
    pwd.send_keys(PWD)
    driver.find_element(By.XPATH, '//*[@class="btn-red btn-signin"]').click()
    sleep(2)

def selectRound():
    driver.get(concert_url)
    while driver.current_url == concert_url:
        print('grey btn')
        element = driver.find_element(By.XPATH, f"//a[@data-button='{ROUND}']")
        myClick(element)
        driver.refresh()
        sleep(1)

def selectZone():
    driver.find_element(By.XPATH, f"//area[@href='#fixed.php#{ZONE}']").click()

def selectSeat():
    availseats = 0
    while availseats == 0:
        availseats = driver.execute_script(
            "return document.getElementsByClassName('seatuncheck').length")
        print('count_loop (No. of available seats)='+str(availseats))

    found = False
    for i in range(1, availseats+1):
        print('select seat round '+str(i))
        driver.execute_script(
            f"document.getElementsByClassName('seatuncheck')[{i}].click()")
        prompt = driver.execute_script(
            "return document.getElementsByClassName('fancybox-overlay fancybox-overlay-fixed').length"
        )
        if prompt:
            element = driver.find_element(By.XPATH, '//*[@class="btn-red w-auto"]')
            element.click()
        else:
            found = True
            break

        # try:
        #     element = driver.find_element(By.XPATH, '//*[@class="fancybox-overlay fancybox-overlay-fixed"]')
        #     print("prompt window")
        #     element = driver.find_element(By.XPATH, '//*[@class="btn-red w-auto"]')
        #     element.click()
        # except NoSuchElementException:
        #     print("found seat, should book")
        #     break
    if not found:
        driver.refresh() 
        selectSeat()
    element = driver.find_element(By.ID, 'booknow')
    myClick(element)

def payment():
    driver.find_element(By.ID, 'btn_pickup').click()
    # driver.find_element(By.ID, 'wechat').click()
    driver.find_element(By.XPATH, '//strong[@class="label-txt"]').click()
    driver.find_element(By.XPATH, '//span[@class="label-txt"]').click()
    # driver.find_element(By.ID, 'btn_confirm').click()


def myClick(elm):
    actions = ActionChains(driver)
    actions.move_to_element(elm).perform()
    driver.execute_script("arguments[0].click();", elm)

setUp()
Login()
selectRound()
selectZone()
selectSeat()
payment()