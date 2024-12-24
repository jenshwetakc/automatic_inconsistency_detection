
'''
# november 13
## update the logic to check whether the button is clicked and whether the theme is switched or not?


'''






'''
November 11
Adding test cases for alxea's rank application that support both light and dark mode
Here A- means Alexa

Single Click
1. Application: https://www.w3schools.com/ - Case A-1.1
2. Application: https://mega.io/ Case A-1.2
3. Application: Applicaiton: https://www.tutorialspoint.com/index.htm Case A-1.3
3. Application: https://www.op.gg/     - Case A-1.2
4. Application: https://www.biobiochile.cl/ - Case A-1.4 added on november15 2024  todoo...
5. Application: https://www.geeksforgeeks.org/ - Case A-1.5 
7. Application: https://www.kakaocorp.com/page/ - Case A-1.7 
8. Application:
9. Application: https://www.newegg.com/  - Case A-1.9 (run on light mode first) -- hold todo
10. Applicaiton: https://design.uzone.id/target-vs-walmart-home-goods-apparel-smackdown/?utm_source=campaign&utm_medium=boost    Case A-1.10(runs on light mode) 
11. Applicaiton: https://www.binance.com/en - Case A-1.11, first runs on dark mode -- hold we are not able to find the menu button and click on it for mobile application 
12. Application: https://www.hesport.com/ - Case A-1.12, application first runs on light mode,  runs on light mode 


november 25 
13. Application: https://www.espncricinfo.com/, - Case A-1.13, application start in light mode, when we perform action while changing into the dark mode we have to go back to the main page




Application from dataforseo

1.
2.
3. Application: https://langeek.co/, Case D-1.3, application first runs on light mode 
4. Appplication: https://globalnews.ca/, Case D-1.4, application first runs on dark mode 

application: https://www.resetera.com/ Case D-1.8 application first runs on light mode ---- todo hold application doesnot change body or html tag for dark mode
application: https://www.androidauthority.com/ Case D-1.9 application first runs on dark mode, done for mobile application 
'''

import logging
import os
import shutil
import time
import random
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



USRPROFILE = '~/Library/Application Support/Google/Chrome/'

# application setup ............


url = "application url"
extension_path = "path/to/Dark Mode - Night Eye - Chrome Web Store 5.2.2.0.crx"
webdriver_path = "path/tp/Selenium/projectOne/chromedriver"


def setup_driver(extension_path=None):
    option = Options()
    option.add_argument('--disable-popup-blocking')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument("--disable-notifications")

    ## mobile emulator
    mobile_emulation = {
        # "deviceName": "iPhone X"  # Corrected device name
        "deviceName": "iPhone 12 Pro"  # Corrected device name
    }

    option.add_experimental_option('mobileEmulation', mobile_emulation)


    service = Service(webdriver_path)

    if extension_path:
        option.add_extension(extension_path)
    driver = webdriver.Chrome(service=service, options=option)

    # driver.set_window_size(1280, 1024)

    return driver

def start_web_application(driver):
    """Launches the web application."""
    driver.get(url)
    time.sleep(2)


# theme checker logic ......

def is_dark_theme(driver):
    """
    Check if the application is using a dark theme.
    """
    try:
        # Case A-1.1
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_theme_enabled = body_tag.get_attribute('class')
        #
        # if 'darktheme' in dark_theme_enabled:
        #     print(dark_theme_enabled)
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False

        # Case A-1.2 start

        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = body_tag.get_attribute('class')
        #
        # if 'theme-dark' in dark_class_enabled:
        #     print(dark_class_enabled)
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = body_tag.get_attribute('class')
        #
        # if dark_class_enabled == 'theme-dark':
        #     print(dark_class_enabled)
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # Case A-1.2 end

        # Case A-1.3
        # html tag
        # html_tag = driver.find_element(By.TAG_NAME, 'html')
        # dark_theme_enabled = html_tag.get_attribute('class')
        #
        # if 'opgg-kit-dark' in dark_theme_enabled:
        #     print('Application is in dark mode.')
        #     return True
        # else:
        #     print('Application is in light mode.')
        #     return False
        # Case A-1.3 end

        # ## Case A-1.3 - tutorial points
        # # html tag
        # for web
        # html_tag = driver.find_element(By.TAG_NAME, 'html')
        # dark_theme_enabled = html_tag.get_attribute('class')
        #
        # if 'dark' in dark_theme_enabled:
        #     print('Application is in dark mode.')
        #     return True
        # else:
        #     print('Application is in light mode.')
        #     return False
        # ## Case A-1.3 end

        #
        # ##Case A-1.4 start
        # ## for web
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = body_tag.get_attribute('class')
        #
        # if 'dark-mode' in dark_class_enabled:
        #     print('dark_class_enabled', dark_class_enabled)
        #     return True
        # else:
        #     print('Application is in light mode')
        #     return False
        # ##Case A-1.4 end

        # Case A-1.5 start
        # by using css_selector
        ###  Find the <div> element with class "root"

        # dynamic cases for dark theme enabled so...
        # root_div = driver.find_element(By.CSS_SELECTOR, 'div.root')
        #
        # # Get the 'data-dark-mode' attribute value
        # dark_mode_enabled = root_div.get_attribute('data-dark-mode')
        # print(dark_mode_enabled)
        #
        # # Check if dark mode is enabled
        # if dark_mode_enabled == 'true':
        #     print("Dark mode is enabled")
        #     return True
        # else:
        #     print("Light mode is enabled")
        #     return False

        # html_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = html_tag.get_attribute('class')
        # print(dark_class_enabled)
        #
        # if dark_class_enabled == 'dark':
        #     print('Application is in dark mode')
        #     return True
        # else:
        #     print('Application is in light mode')
        #     return False

        #### web
        # toggle_button = driver.find_element(By.CLASS_NAME, 'darkMode-wrap-desktop')
        # Case A-1.5 end


        # # Case A-1.7 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_theme_enabled = body_tag.get_attribute('class')
        # print(dark_theme_enabled)
        #
        # # mobile
        # # if 'dark mo' in dark_theme_enabled:
        # #     print('dark_class_enabled')
        # #     return True
        # # else:
        # #     print('application is in light mode')
        # #     return False
        #
        # # web
        # if 'dark pc' in dark_theme_enabled:
        #     print('dark_class_enabled')
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        #
        # # Case A-1.7 end


        # Case A-1.8 start
        # html_tag = driver.find_element(By.TAG_NAME, 'html')
        # dark_class_enabled = html_tag.get_attribute('class')
        # print(dark_class_enabled)
        #
        # if dark_class_enabled == 'dark':
        #     print('Application is in dark mode')
        #     return True
        # else:
        #     print('Application is in light mode')
        #     return False

        # Case A-1.8 end


        # Case A-1.9 start
        # html_tag = driver.find_element(By.TAG_NAME, 'html')
        # dark_theme_enabled = html_tag.find_element('class')
        # print('dark_theme_enabled', dark_theme_enabled)
        #
        # if dark_theme_enabled == 'dark-mode':
        #     print('dark mode enabled')
        #     return True
        # else:
        #     print('Application is in light mode')
        #     return False
        # Case A-1.9 end


        # # Case A-1.10 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_theme_enabled = body_tag.get_attribute('class')
        # print(dark_theme_enabled)
        #
        # ##mobile - web
        # if 'dark-theme' in dark_theme_enabled:
        #     print('dark_class_enabled')
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # # Case A-1.10 end

        # # Case A-1.11 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_theme_enabled = body_tag.get_attribute('class')
        # print(dark_theme_enabled)
        #
        # ##mobile
        # if 'dark' in dark_theme_enabled:
        #     print('dark_class_enabled', dark_theme_enabled)
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # # Case A-1.11 end

        # # Case A-1.12 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_theme_enabled = body_tag.get_attribute('class')
        # print(dark_theme_enabled)
        #
        # ##
        # if 'night-mode' in dark_theme_enabled:
        #     print('dark_class_enabled')
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # # Case A-1.12 end

        print('Case A-1.13')

       #  ##Case A-1.13 start
       #  body_tag = driver.find_element(By.TAG_NAME, 'body')
       #  # element = body_tag.find_element(By.CSS_SELECTOR, '[data-color-theme]')
       #  # print(element)
       #  print('body_tag', body_tag)
       #  dark_theme_enabled = body_tag.get_attribute('data-color-theme')
       #  print('dark_theme_enabled', dark_theme_enabled)
       #
       #  if 'dark' in dark_theme_enabled:
       #      print('Application is in dark mode')
       #      return True
       #  else:
       #      print('Application is in light mode')
       #      return False
       # ## Case A-1.13 start

        print('Case A-1.14')

         ##Case A-1.13 start
        body_tag = driver.find_element(By.TAG_NAME, 'body')
        # element = body_tag.find_element(By.CSS_SELECTOR, '[data-color-theme]')
        # print(element)
        print('body_tag', body_tag)
        dark_theme_enabled = body_tag.get_attribute('data-md-color-scheme')
        print('dark_theme_enabled', dark_theme_enabled)

        if 'slate' in dark_theme_enabled:
            print('Application is in dark mode')
            return True
        else:
            print('Application is in light mode')
            return False
        ## Case A-1.13 start




        # # # Case D-1.3 start
        # element = driver.find_element("css selector", '[data-mode]')
        #
        # # Get the value of the `data-mode` attribute
        # data_mode = element.get_attribute("data-mode")
        #
        # if 'dark' in data_mode:
        #     print('Application is in dark mode')
        #     return True
        # else:
        #     print('Application is in light mode')
        #     return False
        # #
        # # # Case D-1.3 end

        print('Case D-1.4 ')
        # ##Case D-1.4 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = body_tag.get_attribute('class')
        # print(dark_class_enabled)
        # dark_class_enabled = driver.find_element(By.CLASS_NAME, 'dark-theme')
        #
        # if dark_class_enabled:
        #     print('dark mode enabled')
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # ##Case D-1.4 end

        print('d-1.9')
        # ##Case D-1.9 start
        # body_tag = driver.find_element(By.TAG_NAME, 'body')
        # dark_class_enabled = body_tag.get_attribute('class')
        # print('dark enabled', dark_class_enabled)
        #
        #
        # if 'd_a' in dark_class_enabled:
        #     print('dark mode enabled')
        #     return True
        # else:
        #     print('application is in light mode')
        #     return False
        # ##Case D-1.4 end

    except Exception as e:
        print(f"An error occurred while checking dark mode: {str(e)}")
        return False



def is_toggle_theme_button(driver):
    """
    Check if the toggle button for changing themes exists.
    """
    try:
        # Case A-1.1
        # mobile
        # theme_toggle_button = driver.find_element(By.ID, 'tnb-dark-mode-toggle-btn')

        # web
        # theme_toggle_button = driver.find_element(By.ID, 'tnb-dark-mode-toggle-wrapper')
        # Case A-1.1 end


        # Case A-1.2 start
        # mobile
        # menu_button = driver.find_element(By.CLASS_NAME, 'mobile-menu-btn')
        # menu_button.click()
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-box')

        # web
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-button')
        # Case A-1.2 end


        ## Case A-1.3 start
        ## For mobile
        # menu_button = driver.find_element(By.CLASS_NAME, 'MobileGNB-module_sub__cwRSw')
        # print(menu_button)
        # menu_button.click()
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'Switch-module_switch__9-NOR')
        # print('toggle_button', theme_toggle_button)

        ## for web
        #     theme_toggle_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Change Theme' and @value='dark']"))
        # )
        #     print(theme_toggle_button)
        ## Case A-1.3 end

        # # Case A-1.3 start tutorial point
        # # For mobile
        # # not available
        # # for web
        # theme_toggle_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "accent-nav__button"))
        # )
        # print(theme_toggle_button)
        # # Case A-1.3 end



        # Case A-1.4
        # theme_toggle_button =driver.find_element(By.CLASS_NAME, 'nav-btn')
        # print(theme_toggle_button)
        # Case A-1.4


        # Case A-1.5 start
        # mobile-case
        # time.sleep(2)
        # hamburger_menu = driver.find_element(By.CLASS_NAME, 'hamburgerMenu')
        # print('hamburger menu', hamburger_menu)
        # hamburger_menu.click()
        # time.sleep(2)
        # # Scroll down to the bottom, theme change button is located there
        # modal_container = driver.find_element(By.CLASS_NAME, 'headerSidebarWrapperOpen')
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_container)
        # time.sleep(2)
        # theme_toggle_button = driver.find_element(By.CSS_SELECTOR, 'button[data-gfg-action="toggleGFGTheme"]')
        # print('theme_toggle_button', theme_toggle_button)

        # web-case
        # toggle_button = driver.find_element(By.CLASS_NAME, 'darkMode-wrap-desktop')
        # Case A-1.5 end

        # Case A-1.7 start


        # mobile

        # hamburger_button = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.CLASS_NAME, 'btn_hamburger'))
        # )
        # time.sleep(5)
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hamburger_button)
        # print('hamburger_button', hamburger_button)
        # driver.execute_script("arguments[0].click();", hamburger_button)
        # print(f"Hamburger button found: {hamburger_button}")
        # time.sleep(2)
        # modal_container = driver.find_element(By.CLASS_NAME, 'slide_on')
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal_container)
        #
        # #  Locate and Scroll to Theme Toggle Button
        # theme_toggle_button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'btn_mode'))
        # )
        # print(theme_toggle_button)


        # web

        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'btn_mode')
        # print(theme_toggle_button)

        # Case A-1.7 end

        # Case A-1.8 start
        # toggle_button = driver.find_element(By.CLASS_NAME, 'mode-toggle')
        # Case A-1.8 end

        # Case A-1.9 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'toggle-m')
        # print(theme_toggle_button)
        # Case A-1.9 end


        # Case A-1.10 start

        # # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'darkmode-button')
        # # Case A-1.10 end
        #
        # # Case A-1.11 start
        # menu_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, 'bn-svg'))
        # )
        # print('menu_button', menu_button)

        # not working for mobile

        # for web

        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'theme-icon')
        # print(theme_toggle_button)


        # Case A-1.11 end



        # Case A-1.12 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'switch-mode')
        # print(theme_toggle_button)
        # Case A-1.12 end


        #Case A-1.13 start
        # menu_button = driver.find_element(By.CLASS_NAME, 'icon-settings-outlined')
        # print(menu_button)
        # time.sleep(2)
        # driver.execute_script("arguments[0].click();", menu_button)
        # menu_button.click()
        #
        # # not working second part
        # time.sleep(15)
        # print(menu_button)
        # theme_toggle_button = driver.find_element((By.XPATH, "//i[contains(@class, 'icon-wb_sunny-outlined')]"))
        #
        #
        # print("Popup container is visible.", theme_toggle_button)
        #try 2

        # menu_button = driver.find_element(By.CLASS_NAME, 'icon-settings-outlined')
        #
        # # Scroll to the button if necessary (optional, for visibility issues)
        # ActionChains(driver).move_to_element(menu_button).perform()
        #
        # # Click the button
        # menu_button.click()
        #
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'ds-mr-2')
        # print('theme_toggle_button', theme_toggle_button)


        # web
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-dark_mode-filled')
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'md-icon')

        #Case A-1.13 end

        # Case A-1.14 start

        # web
        theme_toggle_button = driver.find_element(By.CLASS_NAME, 'md-header__button')
        print(theme_toggle_button)
        # Case A-1.14 end




        # # Case D-1.3 start
        # menu_button = driver.find_element(By.ID, 'menuButton')
        # menu_button.click()
        #
        # print(menu_button)
        # time.sleep(2)
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'tw-bg-gray-84')
        # print(theme_toggle_button)
        # # Case D-1.3 end

        # # # Case D-1.4 start
        # theme_toggle_button = driver.find_element(By.ID, 'theme-toggle-desktop')
        #
        # # # Case D-1.4 end
        #
        # ## Case D-1.8 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'p-nav-menuTrigger')
        #
        # ## Case D-1.8 end


        # ## Case D-1.9 start
        #
        # # try 2
        # # Locate using aria-label
        # menu_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Show menu"]')
        #
        # # Scroll to the button if necessary (optional, for visibility issues)
        # ActionChains(driver).move_to_element(menu_button).perform()
        #
        # # Click the button
        # menu_button.click()
        #
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'd_Am')
        # print('theme_toggle_button', theme_toggle_button)
        #
        # # close = driver.find_element(By.CLASS_NAME, 'd_im')
        # # close.click()
        #
        #
        # ## Case D-1.9 end

        if theme_toggle_button:
            return True
        else:
            return False



    except:
        return False

def toggle_to_dark(driver):
    """
    Toggle the theme of the application.
    """
    try:
        ''' By Id '''
        # Case A-1.1
        # mobile
        # toggle_button = driver.find_element(By.ID, 'tnb-dark-mode-toggle-wrapper')
        # toggle_button.click()

        # web
        # toggle_button = driver.find_element(By.ID, 'tnb-dark-mode-toggle-wrapper')
        # toggle_button.click()

        # Case A-1.1 end

        ## Case A-1.2 start
        # mobile
        # menu_button = driver.find_element(By.CLASS_NAME, 'mobile-menu-btn')
        # menu_button.click()
        # container_toggle = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "mobile-modals"))
        # )
        #
        # theme_toggle_button = container_toggle.find_element(By.CLASS_NAME, 'theme-btn')
        # theme_toggle_button.click()

        # web
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-button')
        # theme_toggle_button.click()



        ## Case A-1.2 end

        # #Case A-1.3 start
        #
        # ## for mobile
        # # driver.execute_script("window.scrollTo(0, 0);")
        # # menu_button = driver.find_element(By.CLASS_NAME, 'MobileGNB-module_sub__cwRSw')
        # # print(menu_button)
        # # menu_button.click()
        # # container = WebDriverWait(driver, 10).until(
        # #     EC.visibility_of_element_located((By.CLASS_NAME, "MobileNavMenu-module_mobile-nav-menu__-aSK3"))
        # # )
        # # print("Container is visible.")
        # #
        # # # Step 2: Scroll to the button (Dark Mode Toggle)
        # # button = WebDriverWait(driver, 10).until(
        # #     EC.element_to_be_clickable((By.XPATH, "//label[@for='darkMode']"))
        # # )
        # # driver.execute_script("arguments[0].scrollIntoView(true);", button)
        # # button.click()
        # # menu_close = driver.find_element(By.CLASS_NAME, 'MobileNavMenu-module_close-btn__dwksY')
        # # menu_close.click()
        #
        # ## For web
        # theme_toggle_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Change Theme' and @value='light']"))
        # )
        # theme_toggle_button.click()
        # #Case A-1.3 end


        # # Case A-1.3  start tutorial-point
        # theme_toggle_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "accent-nav__button"))
        # )
        # # toggle_button = driver.find_element(By.CLASS_NAME, 'accent-nav__button')
        # driver.execute_script("arguments[0].scrollIntoView();", theme_toggle_button)
        # time.sleep(2)
        # theme_toggle_button.click()
        # # Case A-1.3  end tutorial-point


        # # Case A-1.4 start
        # theme_toggle_button =driver.find_element(By.CLASS_NAME, 'nav-btn')
        # driver.execute_script("arguments[0].scrollIntoView();", theme_toggle_button)
        # theme_toggle_button.click()
        #
        # # Case A-1.4 end


        # # Case A-1.5
        # # mobile
        # icon_button = driver.find_element(By.CLASS_NAME, 'hamburgerMenu')
        # time.sleep(2)
        # print('humburger menu', icon_button)
        # icon_button.click()
        # time.sleep(2)
        # icon_button.click()  ## add two click as the first click is not able to click on the button
        #
        # ##### **** to check whether the button is clicked or not ****
        #
        # # # Get initial class name or attribute value
        # # initial_class = icon_button.get_attribute("class")
        # #
        # # # Attempt to click the hamburger menu
        # # icon_button.click()
        # # time.sleep(2)  # Wait for the potential change in state
        # #
        # # # Check if the class name has changed
        # # updated_class = icon_button.get_attribute("class")
        # # if initial_class != updated_class:
        # #     print("Hamburger menu has been clicked; class changed.")
        # # else:
        # #     print("Hamburger menu click did not change the class.")
        #
        # ###### Scroll down to the bottom, theme change button is located there
        # modal_container = driver.find_element(By.CLASS_NAME, 'headerSidebarWrapperOpen')
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_container)
        # time.sleep(2)
        # toggle_theme_button = driver.find_element(By.CSS_SELECTOR, 'button[data-gfg-action="toggleGFGTheme"]')
        # print('toggle_button', toggle_theme_button)
        # toggle_theme_button.click()
        #
        # # web
        # # toggle_button = driver.find_element(By.CLASS_NAME, 'darkMode-wrap-desktop')
        #
        # # check if the theme switched to dark mode
        # if is_dark_theme(driver):
        #     print('Switched to dark mode.')
        #     return True
        # else:
        #     print('Theme button clicked but mode did not changed.')
        #     return False
        # # Case A-1.5 end

        print()

        # Case A-1.7 start
        ## mobile

        # modal_container = driver.find_element(By.CLASS_NAME, 'slide_on')
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal_container)
        #
        # #  Locate and Scroll to Theme Toggle Button
        # theme_toggle_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, 'btn_mode'))
        # )
        # print(theme_toggle_button)
        # driver.execute_script("arguments[0].click();", theme_toggle_button)
        # close_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_close')))
        # driver.execute_script("arguments[0].click();", close_button)
        # time.sleep(2)

        ## web
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'btn_mode')
        # driver.execute_script("arguments[0].click();", theme_toggle_button)

        # Case A-1.7 end


        # Case A-1.9 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'toggle-m')
        # print(theme_toggle_button)
        # driver.execute_script("arguments[0].click();", theme_toggle_button)
        # Case A-1.9 end


        # # Case A-1.8 start
        # toggle_button = driver.find_element(By.CLASS_NAME, 'darkmode-button')
        # toggle_button.click()
        # # Case A-1.8 start



        # Case A-1.8 started
        # mobile application
        # icon_button = driver.find_element(By.CSS_SELECTOR, "div.fly-mobile-on i.fas.fa-bars")
        # actions = ActionChains(driver)
        # actions.move_to_element(icon_button).click().perform()
        # dark_mode_button = driver.find_element(By.CLASS_NAME, 'dark-mode')
        # print('light mode button', dark_mode_button)
        # driver.execute_script("arguments[0].click();", dark_mode_button)
        # time.sleep(2)

        # case web
        # toggle_button = driver.find_element(By.CLASS_NAME, 'mode-toggle')
        # print(toggle_button)
        # toggle_button.click()

        # if is_dark_theme(driver):
        #     print('Switched to dark mode.')
        #     return True
        # else:
        #     print('Theme button clicked but mode did not changed.')
        #     return False
        # case A-1.8 started  end

        # # Case A-1.11 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'theme-icon')
        # theme_toggle_button.click()
        # # Case A-1.11 end

        # Case A-1.12 start
        # theme_toggle_button = driver.find_element(By.ID, 'nightMode')
        # theme_toggle_button.click()
        # Case A-1.12 end

        print('a-1.12')

        # # Case A-1.13 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-dark_mode-filled')
        # ActionChains(driver).move_to_element(theme_toggle_button).perform()
        # theme_toggle_button.click()
        # # Case A-1.13 end


        # Case A-1.13 start
        theme_toggle_button = driver.find_element(By.CLASS_NAME, 'md-header__button')
        driver.execute_script("arguments[0].click();", theme_toggle_button)
        theme_toggle_button.click()
        # Case A-1.13 end




        ####Dataforceo

        # ## Case D-1.3 start
        # menu_button = driver.find_element(By.ID, 'menuButton')
        # menu_button.click()
        #
        # print(menu_button)
        # time.sleep(2)
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'tw-bg-gray-84')
        # theme_toggle_button.click()
        # print(theme_toggle_button)
        # ## Case D-1.3 end

        # # ## Case D-1.4 start
        # toggle_button = driver.find_element(By.ID, 'theme-toggle-desktop')
        # print(toggle_button)
        # driver.execute_script("arguments[0].click();", toggle_button)
        # # ## Case D-1.4 start

        print('d-1.9')

        # ## Case D-1.9 start
        #
        # # try 2
        # # Locate using aria-label
        # menu_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Show menu"]')
        #
        # # Scroll to the button if necessary (optional, for visibility issues)
        # ActionChains(driver).move_to_element(menu_button).perform()
        #
        # # Click the button
        # menu_button.click()
        # parent_div = driver.find_element(By.CSS_SELECTOR, 'div[data-popup="true"][role="button"]')
        #
        # # Locate the button within the parent div using aria-label
        # theme_toggle_button = parent_div.find_element(By.CSS_SELECTOR, 'button[aria-label="Switch theme"]')
        #
        # # Scroll to the button if necessary
        # ActionChains(driver).move_to_element(theme_toggle_button).perform()
        # theme_toggle_button.click()
        #
        # close_popup = driver.find_element(By.CLASS_NAME, 'd_im')
        # ActionChains(driver).move_to_element(close_popup).perform()
        # close_popup.click()
        #
        # ## Case D-1.9 end


        ## check for all cases
        print(is_dark_theme)
        if is_dark_theme(driver):
            print('Switched to dark mode.')
            return True
        else:
            print('Theme button clicked but mode did not changed.')
            return False


    # except TimeoutException:
    #     print("Theme-changing button not found.")
    #     return False
    except Exception as e:
        print(f"An error occurred while toggling the theme: {str(e)}")
        return False

def toggle_to_light(driver):
    """
    Click the button to change the theme of the application to light mode,
    if the application is in dark mode
    """
    try:

        ## Case A-1.2 start
        # mobile
        # container_toggle = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "mobile-modals"))
        # )
        #
        # theme_toggle_button = container_toggle.find_element(By.CLASS_NAME, 'theme-btn')
        # theme_toggle_button.click()

        # web
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'icon-button')
        # theme_toggle_button.click()

        ## Case A-1.2 end


        # # Case A-1.3 start
        #
        # ## for mobile
        # #
        # # container = WebDriverWait(driver, 10).until(
        # #     EC.visibility_of_element_located((By.CLASS_NAME, "MobileNavMenu-module_mobile-nav-menu__-aSK3"))
        # # )
        # # print("Container is visible.")
        # #
        # # # Step 2: Scroll to the button (Dark Mode Toggle)
        # # button = WebDriverWait(driver, 10).until(
        # #     EC.element_to_be_clickable((By.XPATH, "//label[@for='darkMode']"))
        # # )
        # # driver.execute_script("arguments[0].scrollIntoView(true);", button)
        # # button.click()
        # # menu_close = driver.find_element(By.CLASS_NAME, 'MobileNavMenu-module_close-btn__dwksY')
        # # menu_close.click()
        #
        #
        # ## for web
        #
        # theme_toggle_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Change Theme' and @value='dark']"))
        # )
        # theme_toggle_button.click()
        # # Case A-1.3 end

        # Case A-1.8 start
        # mobile application
        # icon_button = driver.find_element(By.CSS_SELECTOR, "div.fly-mobile-on i.fas.fa-bars")
        # actions = ActionChains(driver)
        # actions.move_to_element(icon_button).click().perform()
        # light_mode_button = driver.find_element(By.CLASS_NAME, 'light-mode')
        # print('light mode button', light_mode_button)
        # driver.execute_script("arguments[0].click();", light_mode_button)
        # time.sleep(2)

        # web case
        # toggle_button = driver.find_element(By.CLASS_NAME, 'mode-toggle')
        # print(toggle_button)
        # toggle_button.click()

        # Case A-1.8 end

        # # ## Case D-1.4 start
        # toggle_button = driver.find_element(By.ID, 'theme-toggle-desktop')
        # print(toggle_button)
        # driver.execute_script("arguments[0].click();", toggle_button)
        # # ## Case D-1.4 start

        # ## Case D-1.9 start
        # parent_div = driver.find_element(By.CSS_SELECTOR, 'div[data-popup="true"][role="button"]')
        #
        # # Locate the button within the parent div using aria-label
        # theme_toggle_button = parent_div.find_element(By.CSS_SELECTOR, 'button[aria-label="Switch theme"]')
        #
        # # Scroll to the button if necessary
        # ActionChains(driver).move_to_element(theme_toggle_button).perform()
        # theme_toggle_button.click()
        #
        # close_popup = driver.find_element(By.CLASS_NAME, 'd_im')
        # ActionChains(driver).move_to_element(close_popup).perform()
        # close_popup.click()
        #
        #
        # ## Case D-1.9 end

        # # Case A-1.11 start
        # theme_toggle_button = driver.find_element(By.CLASS_NAME, 'theme-icon')
        # theme_toggle_button.click()
        # # Case A-1.11 end

        print('test', is_dark_theme(driver))

        if not is_dark_theme(driver):
            print('Switched to light mode.')
            return True
        else:
            print('Theme button clicked but mode did not changed.')
            return False
    # except TimeoutException:
    #     print("Theme-changing button not found.")
    #     return False
    except Exception as e:
        print(f"An error occurred while toggling the theme: {str(e)}")
        return False

# screenshots

def create_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)
    return folder_name
def take_screenshot(driver, folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)
    # driver.save_screenshot(file_path)
    screenshot_binary = driver.get_screenshot_as_png()

    # Save the binary data to an image file
    with open(file_path, 'wb') as file:
        file.write(screenshot_binary)
    print(f'Screenshot taken: {file_path}')

# MENU BAR

def get_menubar_element(driver):
    try:
        nav_elements = driver.find_elements(By.TAG_NAME, 'nav')
        print('len of nav tag ',len(nav_elements))
        visible_nav = None

        for nav in nav_elements:
            if nav.is_displayed():
                visible_nav = nav
                break

        if not visible_nav:
            header_element = driver.find_elements(By.TAG_NAME, 'header')
            for header in header_element:
                if header.is_displayed():
                    visible_nav = header
                    break

        if not visible_nav:
            logging.error('No visible element found')
            return

        logging.info('found visible element')

        nav_items = visible_nav.find_elements(By.XPATH, './/span | .//a | .//button | .//li')
        time.sleep(2)
        print('nav item length',len(nav_items))

        visible_nav_items = [item for item in nav_items if item.is_displayed()]
        print('visible_nav_items length', len(visible_nav_items))
        return visible_nav_items

    except Exception as e:
        print(e)

def get_selected_element(load_from_list, visible_nav_items):
    global selected_element_positions
    if load_from_list and selected_element_positions:
        selected_elements = [visible_nav_items[pos] for pos in selected_element_positions]
    else:
        selected_element = random.sample(range(len(visible_nav_items)), 3)
        selected_element_positions = selected_element
        selected_elements = [visible_nav_items[pos] for pos in selected_element_positions]
    return selected_elements


def hover_over_nav_elements(driver, folder, load_from_list=False):
    wait = WebDriverWait(driver, 10)
    global selected_element_positions

    try:


        visible_nav_items = get_menubar_element(driver)


        selected_elements = get_selected_element(load_from_list, visible_nav_items)

        actions = ActionChains(driver)
        for index, item in enumerate(selected_elements):
            try:
                wait.until(EC.visibility_of(item))
                wait.until(EC.element_to_be_clickable(item))
                scroll_to_button(driver, item)
                actions.move_to_element(item).perform()
                print(f"Hovered over item {index + 1}/{len(selected_elements)}: {item.text or item.get_attribute('href')}")
                take_screenshot(driver, folder, f'hover_item_{index + 1}.png')
                time.sleep(2)
            except Exception as e:
                print(f"Failed to interact with item {index + 1}/{len(selected_elements)}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



# BUTTON
def scroll_to_button(driver, button):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)


def get_button(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        print('len of button tag', len(buttons))
        visible_buttons = [button for button in buttons if button.is_displayed()]
        print('len of visible button', len(visible_buttons))
        return visible_buttons

    except Exception as e:
        print('get button function exception:',e)

def selected_button(load_from_list, visible_buttons):
    global selected_button_index

    if load_from_list and selected_button_index:
        selected_buttons = [visible_buttons[btn] for btn in selected_button_index]
    else:
        selected_buttons = random.sample(range(len(visible_buttons)), 1)
        selected_button_index = selected_buttons
        selected_buttons = [visible_buttons[btn] for btn in selected_button_index]
    return selected_buttons

def check_redirect(driver, wait, current_url, new_url):
    if current_url != new_url:
        print(f'Redirected to the new URL {new_url}')
        driver.back()
        wait.until(EC.url_to_be(current_url))
        time.sleep(2)
        return True
    else:
        print('Same page')

def button_click(driver, folder_name, button_list=False):
    wait = WebDriverWait(driver, 10)

    try:

        visible_buttons = get_button(driver)


        selected_buttons = selected_button(button_list, visible_buttons)


        for index, button in enumerate(selected_buttons):
            try:
                current_url = driver.current_url
                wait.until(EC.visibility_of(button))
                wait.until(EC.element_to_be_clickable(button))
                scroll_to_button(driver, button)
                button.click()
                time.sleep(2)
                print(f'{button.text} has been clicked')
                take_screenshot(driver, folder_name, f'btn{index+1}.png')

                new_url = driver.current_url

                check_redirect(driver, wait, current_url, new_url)

                check_popup(driver)
                time.sleep(2)
            except Exception as e:
                print(f"Failed to interact with button {index + 1}/{len(selected_buttons)}: {e}")
    except Exception as e:
        print(e)

def check_popup(driver):
    popups = driver.find_elements(By.CSS_SELECTOR, '.model, .popup,  .dialog, [role="dialog"], [role="alertdialog"], [aria-modal="true"]')
    if popups:
        close_popup(driver)

def close_popup(driver):
    close_selectors = [
        'button.close',
        'button[aria-label="Close"]',
        '.modal .close',
        '.modal-footer button.btn-secondary'
        #added
        'button[aria-label="close"]'
    ]

    for selector in close_selectors:
        close_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
        for button in close_buttons:
            button.click()
            time.sleep(1)
            return

    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()
    time.sleep(1)




#NAVIGATE THE PAGES

def get_internal_links(driver, domain):
    links = driver.find_elements(By.TAG_NAME, 'a')
    internal_links = []
    for link in links:
        href = link.get_attribute('href')
        if href and (urlparse(href).netloc == domain or urlparse(href).netloc == ''):
            internal_links.append(href)
    print('len of internal link', len(internal_links))
    return internal_links

def save_visited_urls(visited_urls, file_path):
    """Save the visited URLs to a file."""
    with open(file_path, 'w') as f:
        for url in visited_urls:
            f.write(f"{url}\n")


def crawl_browser(driver, steps, folder,  previously_visited_urls=None):
    """Crawl through pages and capture screenshots."""
    visited_urls = []
    domain = urlparse(url).netloc
    driver.get(url)
    file_path = '/Users/shwetakc/Embracing_dark/Alexa/screenshots/visited_urls.txt'

    try:
        for step in range(1, steps + 1):
            if previously_visited_urls and step - 1 < len(previously_visited_urls):
                link = previously_visited_urls[step - 1]
            else:
                time.sleep(random.uniform(1, 3))
                internal_links = get_internal_links(driver, domain)
                if not internal_links:
                    logging.info("No internal links found, skipping this step.")
                    continue
                link = random.choice(internal_links)

            driver.get(link)
            visited_urls.append(link)
            print(f"Visiting: {link}")
            scroll_page(driver, folder, step)
            save_visited_urls(visited_urls, file_path)
        return visited_urls

    except Exception as e:
        logging.error(f"An error occurred in crawl_browser: {e}")

def normalize_styles(driver):
    """
    Normalize styles for consistent rendering across themes.
    """
    driver.execute_script("""
        document.body.style.margin = '0';
        document.body.style.padding = '0';
        document.body.style.boxSizing = 'border-box';
        document.documentElement.style.margin = '0';
        document.documentElement.style.padding = '0';
        document.documentElement.style.boxSizing = 'border-box';
    """)
    print("Styles normalized for consistent scrolling.")
def scroll_page(driver, folder, step):
    normalize_styles(driver)

    scroll_intervals = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    total_height = driver.execute_script("return document.body.scrollHeight")
    for scroll_percentage in scroll_intervals:
        scroll_position = (total_height * scroll_percentage) / 100
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(2)
        file_name = (f'page_{step}_scroll_{scroll_percentage}.png')
        take_screenshot(driver, folder, file_name)


## to debug
def perform_action(driver, action_name):
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        screenshot_path = f'{action_name}_screenshot.png'
        driver.save_screenshot(screenshot_path)

        print(f'Screenshot saved to {screenshot_path}')
    except Exception as e:
        print(f"An error occurred while performing the action: {str(e)}")


def theme_checker(extension_path = None):
    try:
        if USRPROFILE == '':
            raise Exception('Please fill Google Chrome\'s user profile location')
    except:
        raise Exception('Please fill Google Chrome\'s user profile location in USRPROFILE global variable')

    # create folder for screenshots
    main_folder = create_folder('screenshots')
    dark_mode_folder = create_folder(os.path.join(main_folder, 'dark'))
    light_mode_folder = create_folder(os.path.join(main_folder, 'light'))

    step = 1


    driver = setup_driver()
    start_web_application(driver)

    if is_dark_theme(driver):
        print('Dark theme is active.')

        if is_toggle_theme_button(driver):
            print('Theme toggle button found. Toggling to light mode')
            time.sleep(2)
            if toggle_to_light(driver):
                hover_over_nav_elements(driver, light_mode_folder)
                button_click(driver, light_mode_folder)
                previously_visited_urls = crawl_browser(driver, folder=light_mode_folder, steps=step)
                print('Switching back to dark mode.')
                start_web_application(driver)

                #dark mode
                time.sleep(2)
                if toggle_to_dark(driver):
                    print('Toggling back to dark mode')

                    hover_over_nav_elements(driver, dark_mode_folder, load_from_list=True)
                    button_click(driver, dark_mode_folder, button_list=True)
                    crawl_browser(driver, folder=dark_mode_folder, steps=step, previously_visited_urls=previously_visited_urls)
                else:
                    print('Failed to return to dark mode. Exiting...')
                    driver.quit()
            else:
                print('Failed to switch to light mode. Exiting...')
                driver.quit()
        else:
            print('No toggle button found, the web-application have no default mode.Quiting the application.')
            driver.quit()

    else:
        print('The application is in light mode.')
        hover_over_nav_elements(driver, light_mode_folder)
        button_click(driver, light_mode_folder)
        previously_visited_urls = crawl_browser(driver, folder=light_mode_folder, steps=step)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)


    #dark mode
        if is_toggle_theme_button(driver):
            if toggle_to_dark(driver):
                print('Switch to dark mode... ')
                hover_over_nav_elements(driver, dark_mode_folder, load_from_list=True)
                button_click(driver, dark_mode_folder, button_list=True)
                crawl_browser(driver, folder=dark_mode_folder, steps=step, previously_visited_urls=previously_visited_urls)
                driver.quit()
            else:
                print('Failed to switch to dark mode. Exiting...')

    # with extension

        else:
            print('Application does not support dark mode, applying the dark mode extension...')
            driver_ex = setup_driver(extension_path)
            start_web_application(driver_ex)

            hover_over_nav_elements(driver_ex, dark_mode_folder, load_from_list=True)
            button_click(driver_ex, dark_mode_folder, button_list=True)
            crawl_browser(driver_ex, folder=dark_mode_folder, steps=3, previously_visited_urls=previously_visited_urls)
            crawl_browser(driver_ex, folder=dark_mode_folder, steps=step, previously_visited_urls=previously_visited_urls)

            driver_ex.quit()

if __name__ == '__main__':
    theme_checker(extension_path)