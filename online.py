from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def start():

    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')
    
   
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )

    while True:
        try:
            chats = driver.find_elements(By.XPATH, '//div[contains(@class, "_ahlk")]')
            
            for chat in chats:
            
                chat.click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "message-in")]'))
                )

                messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
                
                if messages:
                  
                    first_message = messages[-1]
                    print(first_message.text)
                
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
        
        time.sleep(30)  

start()
