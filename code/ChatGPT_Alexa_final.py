import csv
import time
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


#chrome_options = Options()

#CHROME_PATH = "/home/song/Downloads/foreign_skill_testing/chromedriver"

#user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.3"
#chrome_options.add_argument(f'user-agent={user_agent}')
#driver = webdriver.Chrome(options= chrome_options, executable_path=CHROME_PATH)


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.02c2f462-19cf-41b1-b30f-0c4cfc36f90e/development/de_DE/")

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_email")))
email.send_keys("")

password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_password")))
password.send_keys("@")

password.send_keys(Keys.ENTER)

time.sleep(20)


done = ['B017OBYNZU']
with open('output.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        done.append(row[0])


#with open('output.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(['skill','invoke', 'response_alexa','user_response'])
    




def generate_response(prompt):
    response = openai.ChatCompletion.create(
                        model = "gpt-3.5-turbo", 
                        messages = [{"role": "user", "content": prompt}]
                        ).choices[0].message.content
    response = response.strip()
    time.sleep(9)
    return response


openai.api_key = ""

with open('GE_skills.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['skill'] in done:
            continue
        time.sleep(3)
        driver.refresh()
        time.sleep(3)
        Device_log = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "deviceLevel-label")))
        Device_log.click()
        response_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"react-autosuggest__input")))
        try:
            user_input = row['invoke']
            skill = row['skill']
            response_element.send_keys(user_input)
            response_element.send_keys(Keys.ENTER)
            time.sleep(9)
            response_alexa = ''
            user_response = ''
            count = 0
            while(True):
                count = count + 1
                url = driver.page_source
                time.sleep(9)
                soup = BeautifulSoup(url, 'html.parser')
                try:
                    response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                except:
                    try:
                        response_element.send_keys(user_input)
                        response_element.send_keys(Keys.ENTER)
                        url = driver.page_source
                        time.sleep(9)
                        soup = BeautifulSoup(url, 'html.parser')
                        response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                    except:
                        response_alexa = "error"
                if count<=10:
                    strings_to_check = ["?", "say", "ask", "tell", "give", "choose", "pick","guess","quote"]
                    if any(s in response_alexa.lower() for s in strings_to_check):
                        user_response = generate_response('generate a random answer for"' + response_alexa + '"and make sure the answer is very clear and less than 5 words')
                        user_response = user_response.lower()
                        if "yes" in user_response:
                            user_response = "yes"
                        elif "no" in user_response:
                            user_response = "no"
                        else:
                            user_response=user_response
                        response_element.send_keys(user_response)
                        response_element.send_keys(Keys.ENTER)
                        time.sleep(3)
                        with open('output.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([skill,row['invoke'], response_alexa,user_response])
                    else:
                        user_response = "stop"
                        url = driver.page_source
                        time.sleep(9)
                        soup = BeautifulSoup(url, 'html.parser')
                        try:
                            response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                            with open('output.csv', 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([skill,row['invoke'], response_alexa,user_response])
                        except:
                            pass
                        response_element.send_keys(user_response)
                        response_element.send_keys(Keys.ENTER)
                        time.sleep(4)     
                        try:
                            url = driver.page_source
                            time.sleep(9)
                            soup = BeautifulSoup(url, 'html.parser')
                            response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                            with open('output.csv', 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([skill,row['invoke'], response_alexa,user_response])
                        except:
                            pass 
                else:
                    user_response = "stop"
                    url = driver.page_source
                    time.sleep(9)
                    soup = BeautifulSoup(url, 'html.parser')
                    try:
                        response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                        with open('output.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([skill,row['invoke'], response_alexa,user_response])
                    except:
                        pass
                    response_element.send_keys(user_response)
                    response_element.send_keys(Keys.ENTER)
                    time.sleep(5)     
                    try:
                        url = driver.page_source
                        time.sleep(9)
                        soup = BeautifulSoup(url, 'html.parser')
                        response_alexa = soup.find(class_="askt-dialog__message askt-dialog__message--active-response").text
                        with open('output.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([skill,row['invoke'], response_alexa,user_response])
                    except:
                        pass 
                if user_response.lower() == "stop":
                    time.sleep(3)
                    response_element.send_keys("exit")
                    response_element.send_keys(Keys.ENTER)
                    time.sleep(3)
                    break
        except:
            pass

