accountname = "myaccountname"
password = "123456"
subreddit = "wholesomememes"

from datetime import datetime
import requests
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pyautogui
from PIL import Image

def getTimeString():
    '''returns current time in %H:%M:%S Format'''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    timestring = f"Time: {current_time}"
    return(timestring)

def Reformat_Image(ImageFilePath):
    '''Takes in an image file path and formats it to 1:1 aspect ratio with white bars'''
    image = Image.open(ImageFilePath, 'r')
    image_size = image.size
    width = image_size[0]
    height = image_size[1]

    if(width != height):
        bigside = width if width > height else height
        background = Image.new('RGBA', (bigside, bigside), (0, 0, 0, 255)) #white
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2),0)))
        background.paste(image, offset)
        background.save('int.png')
        print(f"{getTimeString()} Image has been resized !")
    else:
        print("Image is already a square, it has not been resized !")

def makeTrendingHashtagString():
    '''Returns a string with current trending hashtags'''
    try:
        response = requests.get('https://api.ritekit.com/v1/search/trending?green=1&latin=1')
        print("trendingHashtagString API Call:" , response) # print response code
        jsonresponse = response.json()
        
        trendingHashtagString = ""
        for tag in jsonresponse["tags"]:
            trendingHashtagString += "#" + tag["tag"] + " "
        return trendingHashtagString

    except Exception as Exc: 
        print(Exc)

loggedIn = False

while True:
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.instagram.com")
        time.sleep(5)
        
        s = driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]") #login
        s.click()

        time.sleep(6)

        elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input') #accountname
        elem.send_keys(accountname)
        time.sleep(9)
        elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input') #password
        elem.send_keys(password)
        time.sleep(9)

        s = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button') #login
        s.click()

        loggedIn = True

    except Exception as Exc:
        print(Exc)
        loggedIn = False
        time.sleep(60)
        
    while loggedIn:
        try:
            #get meme
            response = requests.get('https://meme-api.herokuapp.com/gimme/' + subreddit)
            
            # print response code
            print(getTimeString() , " Meme Api Call: " , response)

            jsonresponse = response.json()
            url = jsonresponse["url"]
            print("Meme URL" , url)
            title = jsonresponse["title"]
            if(url[-3:] == "jpg" or url[-3:] == "png"):
        
                urllib.request.urlretrieve(url, "int.png")

                time.sleep(5)
                Reformat_Image("int.png")
                time.sleep(3)
                
                #upload new post
                time.sleep(10)
                button = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button')
                button.click()

                time.sleep(3)
                s = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div")
                s.click()
                time.sleep(8)
                pyautogui.write('int')
                time.sleep(8)
                pyautogui.press('enter')
                time.sleep(3)

                s = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button")
                s.click()
                time.sleep(3)

                s = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button")
                s.click()
                time.sleep(2)

                #caption
                s = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea")
                s.send_keys('' + title + "\n \n \n  " + makeTrendingHashtagString()) 
                time.sleep(4)

                #publish
                s = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button")
                s.click()
                print(getTimeString() , "UPLOADED IMG")
        
                #delete file
                time.sleep(15)
                os.remove("int.png")
                print(getTimeString() , " removed img")

                time.sleep(3)   
                driver.refresh()
                
                time.sleep(60*60*2) #every 2h 

        except Exception as E:
            print(E)
            break 
