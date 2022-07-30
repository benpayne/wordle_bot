from cgitb import reset
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from sim import wordle_bot, weighted_words, expected_info
from game import result_done
import pyperclip
from text_sms import send_message

def getRowResults(driver, row_id):
    state = []
    rows = driver.find_elements(By.CLASS_NAME, "Row-module_row__dEHfN")

    #print(f"rows found: {len(rows)}")
    tiles = rows[row_id].find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")
    for t in tiles:
        state.append(t.get_attribute("data-state"))
    return state

driver = webdriver.Safari()
driver.get("https://www.nytimes.com/games/wordle/index.html")
elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Modal-module_closeIcon__b4z74')))  
action = ActionChains(driver)

if elem:
    action.move_to_element(elem).perform() 
    action.click().perform()

time.sleep(1)

sim  = expected_info()

for i in range(6):
    guess = sim.generate_guess()
    action.send_keys(guess, Keys.RETURN).perform()

    time.sleep(3)

    result = getRowResults(driver, i)
    sim.process_result(guess, result)
    if result_done(result):
        print(f"Solved in {i+1} steps")
        break
    else:
        print(result)

time.sleep(10)

button = driver.find_element(By.ID, "share-button")
button.click()
time.sleep(1)
print(pyperclip.paste())
send_message(pyperclip.paste())
driver.close()
