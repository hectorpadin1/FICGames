# Modules required for basic bot scripting
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from time import sleep
from datetime import datetime
from base64 import b64decode


def module(browser, by_value, argument):
    if browser is None:
        raise WebDriverException('Something unexpected happened. Bot closed unexpectedly.')
    if by_value is None:
        raise WebDriverException('No By.value was specified to find element.')
    if argument is None:
        return
    try:
        return WebDriverWait(browser, 0.05)\
            .until(EC.element_to_be_clickable((by_value, argument)))
    except TimeoutException:
        pass


def find(browser, seconds, keywords):
    t1 = datetime.now()
    result = None
    while True:
        try:
            for tuple in keywords:
                result = module(browser, tuple[0], tuple[1])
                if (result is not None):
                    return result
            if (((datetime.now()-t1).seconds) > seconds):
                raise TimeoutException('Internal error:\nThe item you were looking for could not be found after '+str(seconds)+' seconds. If yout internet is poor try adding more timeout to this functionality.')
                break
        except TimeoutException as e:
            raise TimeoutException(e)


class Bot:
    def __init__(self, username, password):
        # Decode Username and Password
        self.usr = username
        self.pwd = password
        self.url = None
        # Options for navigation
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        # Starting bot
        self.open()

    def open(self):
        self.browser = webdriver.Chrome('/usr/bin/chromedriver', options=self.options)
        self.browser.maximize_window()
        sleep(1)
        self.browser.get('https://www.instagram.com/')
        self.url = "https://www.instagram.com/"
        self.accept_cookies()

    def accept_cookies(self):
        try:
            # Press Accept cookies
            find(self.browser, 10, [(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/button[1]'),
                (By.CSS_SELECTOR, 'button.aOOlW.bIiDR'), (By.ID, None),
                (By.LINK_TEXT, None), (By.NAME, None), (By.PARTIAL_LINK_TEXT, None),
                (By.TAG_NAME, "button")]).click()
        except TimeoutException as e:
            print('Webpage did not generate any cookie ¿? wtf looks weird.\nWe might have the cookie in the browser, flush!!')
            if e is not None: print(e)

    def login(self):
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input'),
            (By.CSS_SELECTOR, 'input._2hvTZ.pexuQ.zyHYP'), (By.NAME, "username"),
            (By.TAG_NAME, "input")]).send_keys(b64decode(self.usr.encode('ascii')).decode('ascii'))
	    # Types the password (no css selector bc will find the username instead)
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input'),
		      (By.NAME, "password"), (By.TAG_NAME, "input")]).send_keys(b64decode(self.pwd.encode('ascii')).decode('ascii'))
        # Clicks log-in button
        sleep(1)
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button'),
            (By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF'), (By.TAG_NAME, "button")]).click()
        sleep(2)
        # Do not save log-in information and disable instagram notification
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'),
            (By.XPATH, '/html/body/div[1]/section/main/div/div/div/div/button'),
            (By.CSS_SELECTOR, 'button.aOOlW.HoLwm'), (By.CSS_SELECTOR, 'button.sqdOP.yWX7d.y3zKF')]).click()
        try:
            find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'),
                (By.XPATH, '/html/body/div[1]/section/main/div/div/div/div/button'),
                (By.CSS_SELECTOR, 'button.aOOlW.HoLwm'), (By.CSS_SELECTOR, 'button.sqdOP.yWX7d.y3zKF')]).click()
        except TimeoutException:
            pass

    def user_exists(self, target):
        url = 'https://www.instagram.com/'+target+'/'
        if not self.is_same_url(url):
            self.browser.get(url)
        try:
            not_found = find(self.browser, 3, [(By.CSS_SELECTOR, 'div._7UhW9.vy6Bb.MMzan.KV-D4.uL8Hv.l4b0S')])
            if not_found is not None:
                return False
        except TimeoutException:
            return True

    def is_same_url(self, url):
        if self.url == url:
            return True
        else:
            return False

    def send_direct(self, target, msg):
        url = 'https://www.instagram.com/direct/inbox'
        if not self.is_same_url(url):
            self.browser.get(url)
            sleep(1)
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button'),
            (By.CSS_SELECTOR, 'button.wpO6b.ZQScA')]).click()
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input'),
            (By.CSS_SELECTOR, 'input.j_2Hd.uMkC7.M5V28'), (By.NAME, "queryBox")]).send_keys(target)
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div[3]/button'),
            (By.CSS_SELECTOR, 'button.dCJp8')]).click()
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]/div/button'),
            (By.CSS_SELECTOR, 'button.sqdOP.yWX7d.y3zKF.cB_4K')]).click()
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')]).send_keys(msg)
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'),
            (By.CSS_SELECTOR, 'button.sqdOP.yWX7d.y3zKF')]).click()

    def follow_user(self, target):
        url = 'https://www.instagram.com/'+target+'/'
        if not self.is_same_url(url):
            self.browser.get(url)
            sleep(1)
        try:
            follow = find(self.browser, 1, [(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'),
                (By.CSS_SELECTOR, 'button._5f5mN.-fzfL._6VtSN.yZn4P')])
            if follow is not None:
                raise ValueError("Already following "+target+".")
        except TimeoutException:
            find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'),
                (By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'),
                (By.CSS_SELECTOR, 'button._5f5mN.jIbKX._6VtSN.yZn4P'),
                (By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF')]).click()

    def unfollow_user(self, target):
        url = 'https://www.instagram.com/'+target+'/'
        if not self.is_same_url(url):
            self.browser.get(url)
            sleep(1)
        try:
            follow = find(self.browser, 3, [(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'),
                (By.CSS_SELECTOR, 'button.Igw0E.rBNOH.YBx95._4EzTm')])
        except TimeoutException:
            raise ValueError("You weren't following "+target+".")
        follow.click()
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[1]'),
            (By.CSS_SELECTOR, 'button.aOOlW.-Cab_')]).click()

    def report_user(self, target, list):
        url = 'https://www.instagram.com/'+target+'/'
        if not self.is_same_url(url):
            self.browser.get(url)
            sleep(1)
        # ...
        find(self.browser, 10, [(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/button'),
            (By.CSS_SELECTOR, 'button.wpO6b')]).click()
        # report user
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div/button[3]')]).click()
        # It's inapropiate, SPAM -> /html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button[1]
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button['+str(list[0])+']')]).click()
        sleep(0.5)
        # Report account
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button['+str(list[1])+']')]).click()
        sleep(1)
        # content that should not be on instagram/pretending to be someone else
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button['+str(list[2])+']')]).click()
        sleep(0.5)
        if (list[2]==1):
            find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button['+str(list[3])+']')]).click()
            sleep(0.5)
            if (list.__len__()>=4):
                find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/fieldset/div['+str(list[4])+']/label/div/input'),
                    (By.ID, 'igCoreRadioButtontag-'+str(list[4]-1))]).click()
        elif (list[2]==2):
            # Someone i know
            find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/fieldset/div['+str(list[3])+']/label/div/input'),
                (By.ID, 'igCoreRadioButtontag-'+str(list[3]-1))]).click()
        # Submit
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[6]/button'),
            (By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF')]).click()
        # Close
        find(self.browser, 10, [(By.XPATH, '/html/body/div[4]/div/div/div/div/div/div/div[4]/button'),
            (By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF')]).click()

    def close(self):
        # Quits browser
        self.browser.quit()