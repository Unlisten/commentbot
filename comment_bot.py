from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import random


# Wrapper to retry a function "func" repeatedly at 2-second intervals 
# until it succeeds to avoid runtime errors caused by trying to locate
# elements before they have loaded
def retry_find_until_success(func):
    def find(by: str, value: str):
        tries_left = 10
        while tries_left > 0:
            try:
                element = func(by, value)
                return element
            except NoSuchElementException:
                tries_left -= 1
                print(f"Failed to find element \"{value}\". retrying in 2s")
            sleep(2)
        raise TimeoutError("Max retries reached.")
    return find


# For clicking buttons called "Next" (there are a few in the login process)
def click_next(driver: webdriver.Chrome):
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()


# Login to a Google account with specified credentials
def login(
    driver: webdriver.Chrome, 
    email: str, 
    password: str, 
    already_at_page: bool=False,
) -> None:
    find_element_safe = retry_find_until_success(driver.find_element)

    # Open the Google login page
    if not already_at_page:
        driver.get('https://accounts.google.com/login')
    
    username_input: WebElement = find_element_safe(By.NAME, "identifier")
    username_input.send_keys(email)
    click_next(driver)
    sleep(3)
    pw_input = find_element_safe(By.NAME, "Passwd")
    pw_input.send_keys(password)
    click_next(driver)


# Comment on youtube video with specified URL
def comment_on_video(
    driver: webdriver.Chrome, 
    URL: str, 
    comment: str,
):
    find_element_safe = retry_find_until_success(driver.find_element)

    # Open youtube video and wait for it to load
    driver.get(URL)
    sleep(3)

    # Scroll down to comments section
    driver.execute_script("window.scrollBy(0, 700)")#document.documentElement.scrollHeight);")
    sleep(1)

    # Locate comment box and type the comment
    comment_box = find_element_safe(By.ID, "placeholder-area")
    comment_box.click()
    active_comment_box = find_element_safe(By.ID, "contenteditable-root")
    active_comment_box.send_keys(comment)

    # Locate and click "Comment" button
    comment_button = find_element_safe(By.XPATH, '//*[@id="submit-button"]')
    comment_button.click()


# Logout of a google account
def logout(driver):
    driver.get("https://accounts.google.com/Logout")


# Comments to be left on the video
COMMENTS: list[str] = [
    "This is a comment!",
    "This is also a comment!",
    # etc
]


# Usernames (username is often a gmail address) and passwords of google accounts
CREDENTIALS: dict[str, str] = {
    "example1@gmail.com": "1234",
    "example2@gmail.com": "5678",
    # etc
}


# URL of youtube video to be commented on
URL = ""


# Removes annoying "Chrome is being controlled by automated test software" message
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])


# IMPORTANT: disables automation detection so phone verification can be bypassed
# Useful link about this: https://www.blackhatworld.com/seo/evading-selenium-detection-the-ultimate-guide.1569690/#:~:text=Detection%20methods%20may%20include%3A,might%20have%20a%20specific%20navigator.
options.add_argument("--disable-blink-features=AutomationControlled")


# Creates the chrome webdriver
driver = webdriver.Chrome(options=options)


# If user has already logged in and logged out again, the display is 
# slightly different, and this must be specified to the login function
already_logged_in = False


# loop through each account and login, comment, logout for each set of creds
for username, password in CREDENTIALS.items():
    login(driver, username, password, already_logged_in)
    sleep(2)

    # The "Simplify your sign-in" text shows up when an account has not 
    # been logged into on the device before, offering you to create a 
    # passkey. Click "Not now"
    try:
        not_now_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Not now')]")
        not_now_button.click()
        sleep(4)
    except:
        pass

    # Leave a random comment from the COMMENTS list on the youtube video
    comment_on_video(driver, URL, random.choice(COMMENTS))
    sleep(3)

    # Log back out of account
    logout(driver)

    # Get the login page to login to next account
    driver.get("https://accounts.google.com/login")#servicelogin")
    driver.find_element(By.XPATH, "//*[contains(text(), 'Use another account')]").click()
    sleep(1)

    already_logged_in = True


print(f"Finished commenting on all {len(CREDENTIALS)} accounts.")
