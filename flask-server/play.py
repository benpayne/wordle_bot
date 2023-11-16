from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
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
    rows = driver.find_elements(By.CLASS_NAME, "Row-module_row__pwpBq")

    #print(f"rows found: {len(rows)}")
    tiles = rows[row_id].find_elements(By.CLASS_NAME, "Tile-module_tile__UWEHN")
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

    # <button data-testid="Play" type="button" class="Welcome-module_button__ZG0Zh">Play</button>
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Welcome-module_button__ZG0Zh')))  
        action = ActionChains(driver)

        if elem:
            action.move_to_element(elem).perform() 
            action.click().perform()
    except TimeoutException as e:
        print("Timed out waiting for page to load")
        return

    time.sleep(1)

    # <button class="Modal-module_closeIcon__TcEKb" type="button" aria-label="Close"><svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 0 24 24" width="20" class="game-icon" data-testid="icon-close"><path fill="var(--color-tone-1)" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path></svg></button>
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Modal-module_closeIcon__TcEKb')))  
        action = ActionChains(driver)

        if elem:
            action.move_to_element(elem).perform() 
            action.click().perform()
    except TimeoutException as e:
        print("Timed out waiting for page to load")
        return

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
        # <button type="button" class="Footer-module_shareButton__uYhiL"><span class="Footer-module_shareText__gb2Xs">Share</span><svg id="Footer-module_shareIcon__Pz5Am" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 0 24 24" width="20" class="game-icon" data-testid="icon-share"><path fill="var(--white)" d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92zM18 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM6 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm12 7.02c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"></path></svg></button>
        button = driver.find_element(By.CLASS_NAME, "Footer-module_shareButton__uYhiL")
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


