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
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    timestring = "Time = " + current_time
    return(timestring)


def Reformat_Image(ImageFilePath):
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
        print(getTimeString() , " Image has been resized !")

    else:
        print("Image is already a square, it has not been resized !")

def makeTrendingHashtagString():
    try:
        response = requests.get('https://api.ritekit.com/v1/search/trending?green=1&latin=1')

        # print response code
        print("trendingHashtagString API Call:" , response)

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
        
        #login
        s = driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
        s.click()

        time.sleep(6)

        elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        elem.send_keys(accountname)
        time.sleep(9)
        elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        elem.send_keys(password)
        time.sleep(9)

        s = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        s.click()

        loggedIn = True

    except Exception as Exc:
        print(Exc)
        loggedIn = False
        time.sleep(60)
        
    while loggedIn:
        try:
            #get meme
            response = requests.get('https://meme-api.herokuapp.com/gimme/interestingasfuck')
            
            # print response code
            print(getTimeString() , " Meme Api Call: " , response)

            jsonresponse = response.json()

            url = jsonresponse["url"]
            print("Meme URL" , url)
            title = jsonresponse["title"]
            if(url[-3:] == "jpg" or url[-3:] == "png"):
            
                urllib.request.urlretrieve(url, "int.png")

                #reformat to 1:1 aspect ratio with white bars
                time.sleep(5)
                Reformat_Image("int.png")
                time.sleep(3)

                #webupload
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
                s.send_keys('ℹ️ ' + title + ' ℹ️' + "\n \n \n #️⃣ #interesting #fact #wow #photography #facts #love #fun #didyouknow #beautiful #instagood #science #amazing #instafacts #art #dailyfacts #travel #scientist #followforfollow #likeforlike #knowledge #nature #factsdaily #allfacts #photooftheday #life #daily #cool #dailyfact #picoftheday #followforfollow #likeforlike #️⃣ \n \n \n for more: @daily.interesting.stuff" ) # add makeTrendingHashtagString() if you want
                
                time.sleep(4)

                s = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button")
                s.click()
                print(getTimeString() , "UPLOADED IMG")
        
                #delete file
                time.sleep(15)
                os.remove("int.png")
                print(getTimeString() , " removed img")

                time.sleep(3)   
                driver.refresh()
                
                time.sleep(60*30 ) 

                print("refresh")
                time.sleep(3)   
                driver.refresh()

                time.sleep(60*30) 
                
                driver.refresh()

        except Exception as E:
            print(E)
            break
