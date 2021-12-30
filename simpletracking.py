from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}

driver = webdriver.ChromeOptions()
driver.add_argument('--no-sandbox')
driver.add_argument("--log-level=3")
driver.add_experimental_option("mobileEmulation", mobile_emulation)
bot = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=driver)
bot.set_window_size(600, 1000)
bot.get("https://www.instagram.com/accounts/login/?next=%2F&source=mobile_nav")
username=input("Enter Account UserName \n")
password=input("Enter Account Password \n")
followerlist=[]
followinglist=[]

def login():
    username_field=WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_field=WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username_field.send_keys(username)
    password_field.send_keys(password)
    button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(5)

#open and save followers
def followers():
    bot.get("https://www.instagram.com/"+username)
    totalfollowers=int((bot.find_elements(By.XPATH,'(.//span[@class="g47SY lOXF2"])')[1].text).replace(',', ''))

    followers_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/{}/followers/']".format(username)))).click()
    #Read Users as we keep scrolling
    time.sleep(2)
    k=1
    for j in range(1,round(totalfollowers/15)):
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(5)
        for i in range(k,(j+1)*10):
            singleuser=bot.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i))
            followerlist.append(""+singleuser.get_attribute('href').split("/")[3])

        k=(j*10)+1
    #print("Followers Added"+k)

def following():
    bot.get("https://www.instagram.com/"+username)
    totalfollowing=int((bot.find_elements(By.XPATH,'(.//span[@class="g47SY lOXF2"])')[2].text).replace(',', ''))
    following_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/{}/following/']".format(username)))).click()
    time.sleep(2)
    #Since the site lazy loads, we will read the users everytime we scroll
    k=1
    for j in range(1,round(totalfollowing / 15)):
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(5)
        for i in range(k,(j+1)*10):
            singleuser=bot.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i))
            followinglist.append(""+singleuser.get_attribute('href').split("/")[3])
        k=(j*10)+1
    bot.close()

#Run any logic on follower or following list , Here is an example of users not following back the Logged In User
def getunfollowerlist():
    followinglist.sort()
    followerlist.sort()

    #check who doesnt follow back
    unfollowers=[]

    for person in followinglist:
        if person not in followerlist:
            unfollowers.append(person)

    print(unfollowers)

def main():
    login()
    followers()
    following()
    getunfollowerlist()

if __name__=='__main__':
    main()
