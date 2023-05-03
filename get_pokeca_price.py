from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv

# Chromeドライバーのパス
driver_path = "/opt/homebrew/bin/chromedriver"

# スクレイピングするページのURL
url = "https://pokeca-chart.com/"

# カード番号のリスト
card_nums = ["s4a-198-190","s7r-077-067","s4-111-100","sm5s-072-066","s10d-078-067","s5r-079-070","s6a-075-069","s4a-308-190","s5a-081-070","s5a-081-070","s5a-093-070","s8b-277-184","s8b-277-184","s8b-261-184","sm12a-214-173","sm12a-177-173","sm11b-074-049","sm11b-069-049","s5r-088-070","s5r-074-070","s7d-079-067","sm7-102-096","s4a-197-190","s2-a06-096","s9a-089-067","s10b-011-071"]

# Chromeオプションの設定
options = Options()
options.headless = True

# CSVファイルに書き込み
with open("card_prices.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["カード番号", "カード名", "直近価格"])

    # Chromeドライバーを起動
    service = Service(driver_path)
    service.start()
    driver = webdriver.Chrome(service.service_url, options=options)

    # 各カード番号をループして処理
    for card_num in card_nums:
        print(card_num)


        # URLの作成
        search_url = url + card_num

        try:
            # Webページを開く
            driver.get(search_url)

            # カードのタイトルを取得
            card_title_elem = driver.find_element(By.CLASS_NAME, "entry-title")
            card_title = card_title_elem.text.strip()

            # 直近価格を取得
            card_price_tbl = driver.find_element(By.ID, "item-price-table")
            card_price_row = card_price_tbl.find_elements(By.TAG_NAME, "tr")[1]
            card_price = card_price_row.find_elements(By.TAG_NAME, "td")[1].text

        except Exception as e:
            print(e)
            card_title = None
            card_price = None

        print(f"card_num: {card_num}, card_title: {card_title}, card_price: {card_price}")
        writer.writerow([card_num, card_title, card_price])

    # Chromeドライバーを停止
    driver.quit()
    service.stop()

# 結果を表示
print("カード価格のスクレイピングが完了しました。")
