import copy
import csv
import datetime
import glob
import json
import os
import sys
import threading
from os.path import join

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import random


##############################################Utils#################################################


def check_user_profile():
    current_path = os.path.dirname(sys.argv[0])
    usr1_path = os.path.join(current_path, 'config', 'profile1')
    usr2_path = os.path.join(current_path, 'config', 'profile2')
    profile1_path = os.path.join(usr1_path, 'Profile 1*')
    profile2_path = os.path.join(usr2_path, 'Profile 1*')

    if len(glob.glob(profile1_path)) == 0 or len(glob.glob(profile2_path)) == 0:
        login_bot(usr1_path, usr2_path)

    elif len(glob.glob(profile1_path)) == 1 and len(glob.glob(profile2_path)) != 1:
        login_bot(usr1_path, "")

    elif len(glob.glob(profile1_path)) != 1 and len(glob.glob(profile2_path)) == 1:
        login_bot("", usr2_path)

    if len(glob.glob(profile1_path)) == 1 and len(glob.glob(profile2_path)) == 1:
        output("$login$[{}] Instagram, Ameba blogで自動ログインを行いました".format(now()), "LOGIN")
        ameba = threading.Thread(target=ameba_bot)
        insta = threading.Thread(target=insta_bot)
        ameba.start()
        insta.start()


def read_file():
    current_path = os.path.dirname(sys.argv[0])
    config_path = os.path.join(current_path, 'config', 'setting.csv')

    with open(config_path) as file:
        reader = csv.reader(file)
        config_list = [row for row in reader]

    return config_list


def read_env():
    current_path = os.path.dirname(sys.argv[0])
    json_path = join(current_path, 'config', 'setting.json')

    json_open = open(json_path, 'r')
    json_load = json.load(json_open)

    return json_load


def now():
    return datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')


def output(message, sns_type):
    current_path = os.path.dirname(sys.argv[0])
    ameba_config_path = join(current_path, 'log', 'ameba_log.txt')
    insta_config_path = join(current_path, 'log', 'insta_log.txt')

    if sns_type == "ameba":
        file = open(ameba_config_path, 'a')
        file.write(message + "\n")
        file.close()

    if sns_type == "insta":
        file = open(insta_config_path, 'a')
        file.write(message + "\n")
        file.close()

    print(message)


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def scroll_down(driver):
    # ページの高さを取得
    height = driver.execute_script("return document.body.scrollHeight")
    # 最後までスクロールすると長いので、半分の長さに割る。

    # ループ処理で少しづつ移動
    for x in range(1, height, 100):
        driver.execute_script("window.scrollTo(0, " + str(x) + ");")


##############################################Login#################################################

def login_bot(ameba_profile_path, insta_profile_path):
    if ameba_profile_path != "":
        ameba_profile_option = Options()  # オプションを用意
        ameba_profile_option.add_argument("user-data-dir=" + ameba_profile_path)
        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=ameba_profile_option)
        driver.get(L_URL)
        val = input("Ameba blog用のアカウントを作り終えたら,OKと入力しEnterを押してください >>> ")

        while True:
            # User作成
            if val == "OK":
                driver.quit()
                break

        ameba_profile_option.add_argument("a-directory=Profile 1")
        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=ameba_profile_option)
        output("$login$[{}] Ameba bolgにログインしてください".format(now()), "login")
        # Ameba login tab
        driver.get(AL_URL)
        try:
            ameba_login(driver)
        except WebDriverException:
            output("$abema$[{}][AmebaError] (Error.0) login入力でエラーが発生しました．手入力してください．".format(now()), "ameba")
        val = input("ログインが完了したら,OKと入力しEnterを押してください >>> ")
        while True:
            # User作成
            if val == "OK":
                driver.quit()
                break

    if insta_profile_path != "":
        insta_profile_option = Options()  # オプションを用意
        insta_profile_option.add_argument("user-data-dir=" + insta_profile_path)
        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=insta_profile_option)
        driver.get(L_URL)
        val = input("Instagram用のアカウントを作り終えたら,OKと入力しEnterを押してください >>> ")

        while True:
            # User作成
            if val == "OK":
                driver.quit()
                break

        insta_profile_option.add_argument("a-directory=Profile 2")
        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=insta_profile_option)
        output("$login$[{}] Instagramにログインしてください".format(now()), "login")
        #Insta login tab
        driver.get(IL_URL)
        try:
            insta_login(driver)
        except WebDriverException:
            output("$insta$[{}][InstaError] (Error.0) login入力でエラーが発生しました．手入力してください．".format(now()), "insta")

        val = input("ログインが完了したら,OKと入力しEnterを押してください >>> ")
        while True:
            # User作成
            if val == "OK":
                driver.quit()
                break

    return


###########################################Abema Blog###############################################


def ameba_login(driver):
    driver.get(AL_URL)
    output("$abema$[{}] ameba blogにアクセスしました".format(now()), "ameba")
    time.sleep(1)

    # メアドと、パスワードを入力
    if len(driver.find_elements_by_name(AU_FORM)) != 0:
        driver.find_element_by_name(AU_FORM).send_keys(ameba_user_id)
        time.sleep(1)
        driver.find_element_by_name(AP_FORM).send_keys(ameba_password)
        time.sleep(1)


def ameba_tag_search(driver, ameba_tag):
    driver.get(AT_URL + ameba_tag)
    time.sleep(random.randint(4, 10))
    output("$abema$[{}] ameba blogより、tagで検索を行いました [タグ: {}]".format(now(), ameba_tag), "ameba")
    time.sleep(1)


def ameba_click_nice(driver):
    for i in range(random.randint(3, 8)):
        time.sleep(3)
        try:
            scroll_down(driver)
            docs = driver.find_elements_by_css_selector(AF_BTN)
            # このページの記事がランダム件数以下になったら次のページへ
            if len(docs) <= random.randrange(5) or random.randrange(100) % 20 == 0:
                target = driver.find_element_by_css_selector(AN_BTN)
                actions = ActionChains(driver)
                actions.move_to_element(target)
                actions.perform()
                driver.find_element_by_css_selector(AN_BTN).click()
                time.sleep(10)
                docs = driver.find_elements_by_css_selector(AF_BTN)

            docs_array = list(range(len(docs)))
            rand_num = random.randrange(0, len(docs_array))
            doc_num = docs_array[rand_num]

            # Fabをクリック
            target = driver.find_elements_by_css_selector(AF_BTN)[doc_num]
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            time.sleep(2)
            driver.find_elements_by_css_selector(AF_BTN)[doc_num].click()

            # 記事のタイトルを取得
            title = driver.find_elements_by_css_selector(AT_TXT)[doc_num].text

            output("$abema$[{}][AmebaFab] 『{}』 投稿をいいねしました".format(now(), title), "ameba")
            time.sleep(random.randint(2, 10))

        except WebDriverException:
            output("$abema$[{}][AmebaError] (Error.1) いいねでエラーが発生しました".format(now()), "ameba")

        except IndexError:
            output("$abema$[{}][AmebaError] (Error.2) いいねでエラーが発生しました".format(now()), "ameba")


def ameba_bot():
    while True:
        time.sleep(1)

        options = Options()
        current_path = os.path.dirname(sys.argv[0])
        config_path = os.path.join(current_path, 'config', 'profile1')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--remote-debugging-port=45447")
        # options.add_argument("--no-sandbox")
        options.add_argument("--user-data-dir=" + config_path)
        options.add_argument("--profile-directory=Profile 1")

        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=options)
        driver.minimize_window()

        ameba_tag_search(driver, random.choice(ameba_tag_list))
        ameba_click_nice(driver)

        driver.close()

        # 20s ~ 20min
        ameba_sleep = random.randint(random.randint(20, 100), random.randint(120, 1200))

        output("$abema$[" + str(ameba_sleep) + "秒]待機します", "ameba")
        output("$abema$=======================================================$abema$", "ameba")
        time.sleep(ameba_sleep)
        is_make_driver = False


###########################################Instagram################################################


def insta_login(driver):
    driver.get(IL_URL)
    output("$insta$[{}] Instagramにアクセスしました".format(now()), "insta")
    time.sleep(1)

    # メアドと、パスワードを入力
    driver.find_element_by_name(IU_FORM).send_keys(insta_user_id)
    time.sleep(1)
    driver.find_element_by_name(IP_FORM).send_keys(insta_password)
    time.sleep(1)


def insta_tag_search(driver, tag):
    driver.get(IT_URL + tag)
    time.sleep(random.randint(4, 10))
    output("$insta$[{}] Instagramより、tagで検索を行いました [タグ: {}]".format(now(), tag), "insta")
    time.sleep(1)


def insta_click_nice(driver):
    try:
        target = driver.find_elements_by_class_name(IP_BTN)[10]
        actions = ActionChains(driver)
        actions.move_to_element(target)
        actions.perform()
        # output("$insta$[{}] 最新の投稿まで画面を移動しました".format(now()), "insta")
        time.sleep(1)

        driver.find_elements_by_class_name(IP_BTN)[9].click()
        time.sleep(random.randint(2, 10))
        output("$insta$[{}] 投稿をクリックしました".format(now()), "insta")
        time.sleep(1)

    except WebDriverException as e:
        output("$insta$[{}][InstaError] (Error.3) いいねエラーが発生しました".format(now()), "insta")
        output("$insta$[{}][InstaError] (Error.3) {}".format(now(), e), "insta")
        return
    except IndexError as e:
        output("$insta$[{}][InstaError] (Error.4) エラーが発生しました（投稿が見つかりませんでした）".format(now()), "insta")
        output("$insta$[{}][InstaError] (Error.4) {}".format(now(), e), "insta")
        return

    count = 0
    while count < random.randint(3, 8):
        try:
            target = driver.find_element_by_css_selector(IF_BTN)
            driver.execute_script("arguments[0].click();", target)
            user = driver.find_element_by_css_selector(IT_TXT).text
            output("$insta$[{}][InstaFab] {} の投稿をいいねしました".format(now(), user), "insta")
            count += 1
            time.sleep(3)
        except WebDriverException as e:
            if len(driver.find_elements_by_css_selector(IB_BTN)) != 0:
                continue
            else:
                output("$insta$[{}][InstaError] (Error.3) いいねでエラーが発生しました".format(now()), "insta")
                output("$insta$[{}] (Error.3) {}".format(now(), e), "insta")

        try:
            target = driver.find_element_by_css_selector(IN_BTN)
            driver.execute_script("arguments[0].click();", target)
            # output("$insta$[{}] 次の投稿へ移動しました".format(now()), "insta")
        except WebDriverException as e:
            output("$insta$[{}][InstaError] (Error.5) 投稿の移動でエラーが発生しました".format(now()), "insta")
            output("$insta$[{}][InstaError] (Error.5) {}".format(now(), e), "insta")
            time.sleep(5)

        time.sleep(random.randint(random.randint(2, 5), random.randint(10, 15)))


def insta_bot():
    while True:
        time.sleep(1)
        options = Options()
        current_path = os.path.dirname(sys.argv[0])
        config_path = os.path.join(current_path, 'config', 'profile2')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--remote-debugging-port=45447")
        # options.add_argument("--no-sandbox")
        options.add_argument("--user-data-dir=" + config_path)
        options.add_argument("--profile-directory=Profile 1")

        driver = webdriver.Chrome(resource_path("./driver/chromedriver"), options=options)
        driver.minimize_window()

        insta_tag_search(driver, random.choice(insta_tag_list))
        insta_click_nice(driver)

        driver.close()

        # 20s ~ 20min
        insta_sleep = random.randint(random.randint(20, 100), random.randint(120, 1200))

        output("$insta$[" + str(insta_sleep) + "秒]待機します", "insta")
        output("$insta$=======================================================$insta$", "insta")
        time.sleep(insta_sleep)


if __name__ == '__main__':
    read_env = read_env()
    L_URL = read_env["LOGIN_URL"]
    AL_URL = read_env["AMEBA_LOGIN_URL"]
    AT_URL = read_env["AMEBA_TAG_URL"]
    AU_FORM = read_env["AMEBA_USER_FORM"]
    AP_FORM = read_env["AMEBA_PASS_FORM"]
    AL_BTN = read_env["AMEBA_LOGIN_BTN"]
    AF_BTN = read_env["AMEBA_FAB_BTN"]
    AN_BTN = read_env["AMEBA_NEXT_BTN"]
    AT_TXT = read_env["AMEBA_TITLE_TXT"]
    AF_TXT = read_env["AMEBA_FAILED_TXT"]
    IL_URL = read_env["INSTA_LOGIN_URL"]
    IT_URL = read_env["INSTA_TAG_URL"]
    IU_FORM = read_env["INSTA_USER_FORM"]
    IP_FORM = read_env["INSTA_PASS_FORM"]
    IL_BTN = read_env["INSTA_LOGIN_BTN"]
    IP_BTN = read_env["INSTA_PHOTO_BTN"]
    IN_BTN = read_env["INSTA_NEXT_BTN"]
    IF_BTN = read_env["INSTA_FAB_BTN"]
    IB_BTN = read_env["INSTA_BAD_BTN"]
    IT_TXT = read_env["INSTA_TITLE_TXT"]
    IF_TXT = read_env["INSTA_FAILED_TXT"]

    config = read_file()
    ameba_tag_list = [i for i in config[3][1:] if i != ""]
    ameba_user_id = config[1][1]
    ameba_password = config[1][3]

    insta_tag_list = [i for i in config[2][1:] if i != ""]
    insta_user_id = config[0][1]
    insta_password = config[0][3]

    check_user_profile()
