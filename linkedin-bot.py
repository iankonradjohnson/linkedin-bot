from random import uniform, randrange
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from config import MESSAGE, NAME_PLACEHOLDER, COMPANY_PLACEHOLDER, urls, username, password, start_page

def signin(driver, username, password):
    signin_element = driver.find_element_by_class_name("main__sign-in-link")
    signin_element.click()
    time.sleep(uniform(0.5,1.5))

    username_element = driver.find_element_by_id("username")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", username_element)
    time.sleep(uniform(0.5,1.5))
    username_element.send_keys(username)
    time.sleep(uniform(0.5,1.5))

    password_element = driver.find_element_by_id("password")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", username_element)
    time.sleep(uniform(0.5,1.5))
    password_element.send_keys(password)
    time.sleep(uniform(0.5,1.5))

    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", username_element)
    time.sleep(uniform(0.5,1.5))
    password_element.submit()
    time.sleep(uniform(0.5,1.5))


def close_active_tab(driver):
    parent = driver.window_handles[0]
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    time.sleep(uniform(0.5,1.5))
    driver.close()
    time.sleep(uniform(0.5,1.5))
    driver.switch_to.window(parent)
    time.sleep(uniform(0.5,1.5))

def has_premium(person):
    try:
        person.find_element(by=By.XPATH, value=".//*[@aria-label='Premium member']")
        return True
    except NoSuchElementException:
        return False

def element_exists(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
        return True
    except NoSuchElementException:
        return False

def random_movement():
    for i in range(randrange(3,5)):
        driver.execute_script("""
        window.scroll({
            top: document.body.scrollHeight / arguments[0],
            left: 100,
            behavior: 'smooth'
            });        
        """, uniform(0,10))
        time.sleep(uniform(1,3))


def send_message(driver, person):
    if not element_exists(driver, By.CLASS_NAME, "app-aware-link"): return
    ahref = person.find_element(by=By.CLASS_NAME, value="app-aware-link")

    link = ahref.get_attribute('href')
    time.sleep(uniform(0,1))
    driver.execute_script(f'''window.open("{link}","_blank");''')
    driver.switch_to.window(driver.window_handles[1])


    if not element_exists(driver, by=By.XPATH, value=".//div[@aria-label='Current company']"): return
    company = driver.find_element(by=By.XPATH, value=".//div[@aria-label='Current company']").text

    if not element_exists(driver, by=By.XPATH, value=".//h1"): return
    full_name = driver.find_element(by=By.XPATH, value=".//h1").text
    first_name = full_name.split(" ")[0]

    if not element_exists(driver, by=By.CLASS_NAME, value="entry-point"): return
    message_button_div = driver.find_element_by_class_name("entry-point")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", message_button_div)


    if not element_exists(driver, by=By.XPATH, value=".//a"): return
    message_button = message_button_div.find_element(by=By.XPATH, value=".//a")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", message_button)
    driver.get(message_button.get_attribute('href'))
    
    if "Free message" in driver.page_source:
        textbox = driver.find_element(by=By.XPATH, value=".//div[@aria-label='Write a message…']")
        textbox.send_keys(MESSAGE.replace(COMPANY_PLACEHOLDER, company).replace(NAME_PLACEHOLDER, first_name))
        random_movement()
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", textbox)
        textbox.submit()
        time.sleep(uniform(0.5,1.5))


driver = webdriver.Chrome()
driver.get(urls[0][0])

signin(driver, username, password)
print('Signing in...')
random_movement()

page_count = 0
profile_count = 0

for (url, pages) in urls:
        for i in range(start_page, pages+1):
            try:
                page_count+=1
                random_movement()
                print(f"On page {i}")
                driver.get(url + f'&page={i}')
                people = driver.find_elements_by_class_name("entity-result")

                for person in people:
                    if profile_count > 50: quit()
                    random_movement()
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", person)
                    if has_premium(person):
                        send_message(driver, person)
                        profile_count+=1
                        close_active_tab(driver)

                print(f"Page count = {page_count}", f"Profile count = {profile_count}")

                # scroll to bottom
                page_nums_element = driver.find_element(by=By.XPATH, value=".//button[@aria-label='Page 1']")
                random_movement()
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", page_nums_element)

            except Exception as e:
                print(e)
                continue







