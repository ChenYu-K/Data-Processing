from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support.ui import  Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()
MSuname = "d21td301@tx.osaka-cu.ac.jp"          #Microsoft email
MSpwd = ""                                      #Microsoft pwd
driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=VFDw5YxQVkCaCf9WBJjhK8qJGArJkbFAsT9pWjwdNQtUNE9KN0pGTkZITEZENUVOSVhJMEI3S1Y1SS4u') # URL
time.sleep(3)
uname = driver.find_element_by_id('i0116')
uname.send_keys(MSuname)
time.sleep(0.5)
uname.send_keys(Keys.ENTER)
time.sleep(1)
pw = driver.find_element_by_id('i0118')
time.sleep(1)
pw.send_keys(MSpwd)
time.sleep(0.5)
pw.send_keys(Keys.ENTER)
time.sleep(1)
sbutton = driver.find_element_by_id('idSIButton9')
sbutton.click()

q1 = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div/input')
q1.send_keys('c308')
q2 = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/label/input')
q2.click()
q3 = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/label/input')
q3.click()
q4 = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[4]/div/div[2]/div/div[2]/div/label/input')
q4.click()
q5 = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[5]/div/div[2]/div/div[1]/div/label/input')
q5.click()    
su = driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/button')　#提出ボタンを探す
su.click() 
time.sleep(1)
print("研活君完了")
