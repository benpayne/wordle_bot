from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import argparse
import pyperclip
import os

from sim import wordle_bot, weighted_words, expected_info
from game import print_result, result_done, get_pattern
from text_sms import send_message
from database import store_results, db_quit

SELENIUM_ADDR = os.getenv("SELENIUM_ADDR")
SELENIUM_PORT = os.getenv("SELENIUM_PORT")

def getRowResults(driver, row_id):
    state = []
    rows = driver.find_elements(By.CLASS_NAME, "Row-module_row__dEHfN")

    #print(f"rows found: {len(rows)}")
    tiles = rows[row_id].find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")
    for t in tiles:
        state.append(t.get_attribute("data-state"))
    return state

def wordle_bot(addr, port, local):
    if addr == None:
        addr = SELENIUM_ADDR
    if port == None:
        port = SELENIUM_PORT

    if local:
        driver = webdriver.Safari()
    else:
        options = webdriver.FirefoxOptions()
        #options = webdriver.ChromeOptions()
        driver = webdriver.Remote(
        #   command_executor='http://192.168.1.202:30525/wd/hub',
            command_executor=f"http://{addr}:{port}/wd/hub",
            options=options
        )   

    print("driver created")
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    #driver.get("https://everytimezone.com")
    #return
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Modal-module_closeIcon__b4z74')))  
    action = ActionChains(driver)

    if elem:
        action.move_to_element(elem).perform() 
        action.click().perform()

    time.sleep(1)

    sim = expected_info(print_list=True)

    answer = ""
    data = []
    word_data = []

    for i in range(6):
        guess = sim.generate_guess(i)
        action.send_keys(guess, Keys.RETURN).perform()

        time.sleep(3)

        result = getRowResults(driver, i)
        sim.process_result(guess, result)
        answer += print_result(guess, result) + "\n"
        data.append((guess, result))
        first_100 = {k: sim.word_list_data[k] for k in list(sim.word_list_data)[:100]}
        word_data.append({'total_words': len(sim.word_list_data), 'actual_info': sim.actual_info, \
            'total_info': sim.total_info, 'first_100': first_100})
        if result_done(result):
            print(f"Solved in {i+1} steps")
            break
        else:
            print(result)

    time.sleep(5)

    if local:
        button = driver.find_element(By.ID, "share-button")
        button.click()
        time.sleep(1)
        copy_data = pyperclip.paste()
        print(copy_data)

    store_results(get_pattern(data), data, word_data)
    print(answer)
    print(get_pattern(data))
    driver.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', help='address to connect to for the remote web driver')
    parser.add_argument('-p', '--port', help='port to connect to for the remote web driver')
    parser.add_argument('-l', '--local', action='store_true', help='run the with the local web driver')
    args = parser.parse_args()

    print(args)

    wordle_bot(args.addr, args.port, args.local)

    db_quit()


if __name__ == "__main__":
    main()


