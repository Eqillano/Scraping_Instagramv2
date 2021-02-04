from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import os
from pynput.keyboard import Key, Controller
import urllib
import urllib3


def instagramLogin(wd):
    user = wd.find_element_by_name('username')
    password = wd.find_element_by_name('password')
    user.clear()
    password.clear()
    instagram_u = input('Please enter your instagram username\n')
    instagram_pass = input('please enter your instagram password\n')
    user.send_keys(instagram_u)
    password.send_keys(instagram_pass)
    time.sleep(5)
    wd.find_element_by_xpath(
        '//*[@id = "loginForm"]/div/div[3]/button').click()
    # //button[@type='submit']")
    time.sleep(5)
    wd.get('https://www.instagram.com/' + instagram_u+'/')
    time.sleep(5)
    return


def makeMainDirectory(directory):
    main_directory = directory
    if not os.path.isdir(main_directory):
        os.mkdir(main_directory)
        os.chdir(main_directory)


def getInstagramAcccount(instagram_username, wd):
    time.sleep(5)
    instagram_holder = instagram_username
    wd.get('http://www.instagram.com/' + instagram_username+'/')
    scrapeInstagramAccountImages(instagram_holder, wd)

    getInspector()

    hrefActions = getInstagramActions(instagram_holder, wd)

    following = getFollowingInformation(hrefActions, wd)
    print(following)
    followers = getFollowersInformation(hrefActions, wd)
    print(followers)


def scrapeInstagramAccountImages(instagram_holder, wd):
    lenOfPage = wd.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")
    match = False
    x = 100
    while(match == False):

        # directory of instagram account
        directory = instagram_holder
        lastCount = lenOfPage
        instagram_urls = []
        time.sleep(30)
        instagram_capture = wd.find_elements_by_xpath("//img[@class='FFVAD']")

        for i in instagram_capture:
            # appending src for images to download
            instagram_urls.append(i.get_attribute('src'))

        # create directory for instagram account
        if not os.path.isdir(directory):
            os.mkdir(directory)

        for i, link in enumerate(instagram_urls):
            path = os.path.join(instagram_holder, '{:06}.jpg'.format(i+x))

            try:
                urllib.request.urlretrieve(link, path)
            except:
                print("Unable to download and place inside of folder")

        x += 100
        lenOfPage = wd.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")

        if (lastCount == lenOfPage):
            match = True


def getInstagramActions(instagram_holder, wd):
    wd.get('https://www.instagram.com/' + instagram_holder+'/')
    time.sleep(5)
    href_temp = wd.find_elements_by_xpath("//li[@class=' Y8-fY']")
    return href_temp


def getInspector():
    # MAKE SURE THAT YOU HAVE THE CHROME DRIVER CLICKED ON
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press('i')
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release('i')
    time.sleep(5)


def getFollowersInformation(actions, wd):
    followers_names = []
    followers = actions[1]
    followers.click()
    time.sleep(20)
    followers_temp = wd.page_source
    followers_data = bs(followers_temp, 'html.parser')
    followers_name = followers_data.find_all('a')
    for i in followers_name:
        followers_name.append(i.get('title'))
    clean_followers_names = [x for x in followers_name if x != None]
    return clean_followers_names


def getFollowingInformation(actions, wd):
    following_names = []
    following = actions[2]
    following.click()
    time.sleep(20)
    following_temp = wd.page_source
    following_data = bs(following_temp, 'html.parser')
    following_name = following_data.find_all('a')
    for i in following_name:
        following_names.append(i.get('title'))
    clean_following_names = [x for x in following_names if x != None]
    return clean_following_names


def main():
    wd = webdriver.Chrome()
    wd.get('https://www.instagram.com/accounts/login/')
    time.sleep(5)
    instagramLogin(wd)
    mainAccountDirectory = input(
        str('Please type a name to store your files into \n'))
    makeMainDirectory(mainAccountDirectory)
    while True:
        instagramAcccount = input(
            str('Please type instagram account for me to find "quit" to end.\n'))
        if instagramAcccount == 'quit':
            return False
        else:
            getInstagramAcccount(instagramAcccount, wd)


if __name__ == '__main__':
    main()
