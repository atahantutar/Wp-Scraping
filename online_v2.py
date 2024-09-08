import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def start():
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')
    
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )

    messages = []
    csv_file = 'messages.csv'

    while True:
        try:
            chats = driver.find_elements(By.XPATH, '//div[contains(@class, "_ahlk")]')
            
            for chat in chats:
                chat.click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "message-in")]'))
                )

                message_elements = driver.find_elements(By.XPATH, '//div[@class="copyable-text"]')
                
                for message_element in message_elements:
                  
                    pre_plain_text = message_element.get_attribute('data-pre-plain-text')
                    if pre_plain_text:
                        parts = pre_plain_text.split(']')
                        if len(parts) > 1:
                            sender = parts[1].split(':')[0].strip()
                        else:
                            sender = "Unknown"
                    else:
                        sender = "Unknown"
                    
                
                    message_text = message_element.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]').text
                    
                
                    timestamp_element = message_element.find_element(By.XPATH, './/span[contains(@class, "x1c4vz4f")]')
                    timestamp = timestamp_element.text if timestamp_element else "Unknown"
                    
                    if (sender, message_text, timestamp) not in messages:
                        messages.append((sender, message_text, timestamp))
                        print(f"Sender: {sender} | Message: {message_text} | Time: {timestamp}")

                        
                        if os.path.exists(csv_file):
                            df_existing = pd.read_csv(csv_file)
                            df_new = pd.DataFrame(messages, columns=["Sender", "Message", "Time"])
                            df_combined = pd.concat([df_existing, df_new]).drop_duplicates()
                            df_combined.to_csv(csv_file, index=False)
                        else:
                            df = pd.DataFrame(messages, columns=["Sender", "Message", "Time"])
                            df.to_csv(csv_file, index=False)

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            time.sleep(1)

start()
