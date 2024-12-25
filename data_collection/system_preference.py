
'''

1. application: https://www.reddit.com/
2. application: https://www.uptodown.com/
3. application: https://www.jw.org/en/
4. application: https://www.urbandictionary.com/
5. application: https://www.t-online.de/
6. application: https://www.howtogeek.com/
7. application: https://www.narcity.com/
8. application: https://www.xda-developers.com/
9. application: https://www.makeuseof.com/
10. application: https://gamerant.com/


datainforseo
1. application: https://www.cbr.com/
2. application: https://www.thegamer.com/
3. application: https://www.letras.com/
4. application: https://movieweb.com/
5. application: https://www.sofascore.com/
6. application: https://www.ndtv.com/


random
1. application: https://www.spiegel.de/
2. application: https://www.sapo.pt/
3. application: https://www.xing.com/



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
extension_path = "path/to/automatic_inconsistency_detection/data_collection/extension/Dark Mode - Night Eye - Chrome Web Store 5.2.2.0.crx"  # night eye extension to convert into the dark mode
google_translate_path = "path/to/automatic_inconsistency_detection/data_collection/extension/Google Translate - Chrome Web Store 2.0.16.0.crx"
add_blocker_path = "path/to/automatic_inconsistency_detection/data_collection/extension/AdBlock — block ads across the web - Chrome Web Store 6.11.1.0.crx"
webdriver_path = "path/to/automatic_inconsistency_detection/data_collection/chromedriver"



def setup_driver(extension_path=None):
    option = Options()
    option.add_argument('--ignore-certificate-errors')
    option.add_argument("--disable-notifications")

    # mobile emulator

    mobile_emulation = {
        "deviceName": "iPhone 12 Pro"  # Corrected device name
    }

    option.add_experimental_option('mobileEmulation', mobile_emulation)


    service = Service(webdriver_path)
    option.add_extension(google_translate_path)
    option.add_extension(add_blocker_path)

    if extension_path:
        option.add_extension(extension_path)
    driver = webdriver.Chrome(service=service, options=option)

    # driver.set_window_size(1280, 1024)

    return driver

def start_web_application(driver):
    """Launches the web application."""
    driver.get(url)
    time.sleep(2)

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
    # popups = driver.find_elements(By.CSS_SELECTOR, '.model, .popup,  .dialog, [role="dialog"], [role="alertdialog"]')
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
    file_path = 'path/to/data_collection/screenshots_s/visited_urls.txt'

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
    print(folder)
    # scroll_intervals = [0, 25, 50, 75, 100]
    # scroll_intervals = [0, 100]
    scroll_intervals = [0, 10,  20, 30, 40, 50, 60, 70, 80, 90, 100]
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
    main_folder = create_folder('screenshots_s')
    dark_mode_folder = create_folder(os.path.join(main_folder, 'dark'))
    light_mode_folder = create_folder(os.path.join(main_folder, 'light'))
    # extension_folder = create_folder(os.path.join(main_folder, 'extension'))

    step = 5


    driver = setup_driver()
    start_web_application(driver)

    hover_over_nav_elements(driver, light_mode_folder)
    button_click(driver, light_mode_folder)
    previously_visited_urls = crawl_browser(driver, folder=light_mode_folder, steps=step)

    print('Switching mode')
    print('Switching mode')
    print('Switching mode')
    print('Switching mode')
    time.sleep(15)

    start_web_application(driver)

    hover_over_nav_elements(driver, dark_mode_folder, load_from_list=True)
    button_click(driver, dark_mode_folder, button_list=True)
    crawl_browser(driver, folder=dark_mode_folder, steps=step, previously_visited_urls=previously_visited_urls)

    driver.quit()



if __name__ == '__main__':
    theme_checker(extension_path)