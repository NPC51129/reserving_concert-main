from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import json
from time import sleep
import sys
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()
# driver = webdriver.Chrome(ChromeDriverManager().install())
print('chrome loaded')
base_url = "https://www.thaiticketmajor.com/concert/"
userdetail_file = "userdetail.json"
count = 0
with open(userdetail_file, 'r') as f:
    user = json.load(f)
email = user["email"]
password = user["pwd"]
zone = user["zone"]
concert = user["concert"]
seat = int(user["seats"])
zone_cnt = 0
show = int(user["show"]) # 用不上
next_zone_index = 1
zone_list = []


def setUp():
    driver.maximize_window()
    print('maximized.')
    driver.get(base_url)
    print('got url.')
    driver.implicitly_wait(100)
    print('wait terminated.')


# 注意 sleep 耗时
def Login():
    driver.find_element(
        By.XPATH, '//*[@class="btn-signin item d-none d-lg-inline-block"]').click()
    sleep(1)
    username = driver.find_element(By.NAME, "username")
    username.send_keys(email)
    pwd = driver.find_element(By.NAME, "password")
    pwd.send_keys(password)
    driver.find_element(By.XPATH, '//*[@class="btn-red btn-signin"]').click()
    sleep(2)
    cur_url = driver.current_url
    print('cur_url: '+ cur_url)
    while cur_url == base_url:
        # 本页若展示了洪荒剧场演唱会才会 be found，否则失败
        # 需要去 “检查” 查看 item 的名字
        element = driver.find_element(By.PARTIAL_LINK_TEXT, concert)

        myClick(element)
        cur_url = driver.current_url
    print('current url: '+driver.current_url)


def SelectShow():
    element = driver.find_element(
        By.XPATH, '//*[@class="btn-red btn-buynow btn-item"]')
    myClick(element)

    # 1. verify condition 页面不是总出现
    # 2. 如果有多个场次，可能会找到错误的 button
    print('in SelectShow, current_url: '+ driver.current_url)
    result = findUrl("verify_condition", driver.current_url)
    print(result)

    if result:
        element = driver.find_element(By.ID, "rdagree")
        myClick(element)
        # btn-solid-round5-blue w-auto
        driver.find_element(
            By.ID, 'btn_verify').click()


def findUrl(msg, link):
    if (link.find(msg) > 0):
        return True
    else:
        return False


def SelectZone(zone=zone):

    global zone_cnt
    while zone_cnt == 0:
        zone_cnt = driver.execute_script(
            "return document.getElementsByTagName('area').length")
        print('count_zone'+str(zone_cnt))
        sleep(1)

    index = 0
    for i in range(1, zone_cnt+1):
        print('round '+str(i))
        seat = driver.find_element(
            By.XPATH, f'//*[@name="uMap2"]/area[{i}]').get_attribute("href")
        print('seat'+seat)
        result = finZone(zone, seat)
        if result:
            index = i
            break
    print('index='+str(index))
    driver.find_element(
        By.XPATH, f'//*[@name="uMap2"]/area[{index}]').click()


def finZone(msg, link):
    get_zone = link.split('#')
    if msg == get_zone[2]:
        return True
    else:
        return False


def SelectSeat(number=seat):

    global count
    availseats = 0
    # 这里要改成 找到的全是 unavailable seats
    loop = 0
    while availseats == 0:
        availseats = driver.execute_script(
            "return document.getElementsByClassName('seatuncheck').length")
        print('count_loop (No. of available seats)='+str(availseats))
        sleep(1)
        loop += 1
        if loop > 1:
            return

    for i in range(1, availseats+1):
        print('select seat round '+str(i))
        driver.execute_script(
            f"document.getElementsByClassName('seatuncheck')[{i}].click()")
        result = driver.execute_script(
            "return document.getElementsByClassName('seatchecked').length")
        print('result='+str(result))
        if result == number:
            # driver.find_element(
            #     By.XPATH, 
            #     '//*[@class="btn-red btn-main-action w-auto right"]').click()
            # driver.find_element(By.ID, 'booknow').click()
            element = driver.find_element(By.ID, 'booknow')
            myClick(element)
            count = result
            break
    
    exit()
    # sleep(100)
    # 此函数未改变 count


def go_to_next_zone():
    print('going to next zone...')
    global next_zone_index
    while next_zone_index <= zone_cnt:
        print('go back')
        driver.find_element(By.XPATH, '//*[@class="btn-red linear"]').click()
        # driver.find_element_by_partial_link_text("ย้อนกลับ / Back").click()
        driver.implicitly_wait(40)
        print("seats available? ")
        # driver.find_element_by_partial_link_text(
        #     "ที่นั่งว่าง / Seats Available").click()
        element = driver.find_element(By.ID, 'popup-avail')
        myClick(element)
        driver.implicitly_wait(30)
        # for j in range(2, zone_cnt+1):
        while True:
            # txt-link txt-green
            # amount = driver.find_element_by_xpath(
            #     f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[2]").text
            # print('table amount=' + str(amount))\
            try:
                # driver.find_element(By.XPATH, '//*[@class="txt-link txt-green"]').click()
                # driver.find_element(By.XPATH, '//*[@class="txt-link txt-blue"]').click()
                element = driver.find_element(By.XPATH, '//*[@class="txt-link txt-green"]')
                element.click()
                SelectSeat()
            except NoSuchElementException:
                print('no green btn')
                # sleep(1)
                # refresh
                # btn-red linear w-auto
                driver.find_element(By.XPATH,
                    '//*[@class="btn-red linear w-auto"]').click()
                continue
            exit()
            i = driver.find_element_by_xpath(
                f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[1]").text
            if amount != "0" or amount == "Available":
                SelectZone(i)
                SelectSeat()
            next_zone_index += 1
    if count == 0:
        print(f"Sorry, this concert don't have any seat for you.")
        sys.exit()


def confirm_ticketprotect():
    driver.find_element_by_partial_link_text(
        "ยืนยันที่นั่ง / Book Now").click()
    driver.implicitly_wait(50)
    driver.find_element_by_partial_link_text("Continue").click()
    driver.implicitly_wait(40)


def myClick(elm):
    actions = ActionChains(driver)
    actions.move_to_element(elm).perform()
    driver.execute_script("arguments[0].click();", elm)


setUp()
Login()
SelectShow()
SelectZone(zone)
SelectSeat()
if count==0:
    go_to_next_zone()
