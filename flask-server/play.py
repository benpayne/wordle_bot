from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import argparse
import pyperclip

from sim import wordle_bot, weighted_words, expected_info
from game import print_result, result_done
from text_sms import send_message
from database import store_results, db_quit

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
        addr = "192.168.1.202"
    if port == None:
        port = 4444

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
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Modal-module_closeIcon__b4z74')))  
    action = ActionChains(driver)

    if elem:
        action.move_to_element(elem).perform() 
        action.click().perform()

    time.sleep(1)

    sim = expected_info(print_list=True)

    answer = ""
    data = []

    for i in range(6):
        guess = sim.generate_guess(i)
        action.send_keys(guess, Keys.RETURN).perform()

        time.sleep(3)

        result = getRowResults(driver, i)
        sim.process_result(guess, result)
        answer += print_result(guess, result) + "\n"
        data.append((guess, result))
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
        print(pyperclip.paste())

    store_results("", data)
    print(answer)
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
