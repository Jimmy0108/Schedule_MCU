import time
import os
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import random
import logging

# --- 導入 selenium-stealth ---
from selenium_stealth import stealth

# --- 設定日誌 ---
logging.basicConfig(filename='course_scraper.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

# --- 全域設定 ---
ENTRY_URL = "https://stu.mcu.edu.tw/appx/qry/Qs01.aspx"
GRADES_TO_FETCH = ['1', '2', '3', '4']
DEPARTMENT_LIST = {
    "01": "英語教學中心", "02": "體育室", "09": "數位媒體設計學系", "11": "企業管理學系",
    "13": "資訊管理學系", "14": "觀光事業學系", "15": "影音新聞暨社群傳播學系",
    "17": "應用統計與資料科學學系", "18": "休閒遊憩管理學系", "19": "餐旅管理學系",
    "21": "商業設計學系", "23": "商品設計學系", "24": "建築學系", "26": "廣告暨策略行銷學系",
    "27": "新聞與大眾傳播學士學位學程", "30": "傳播學院", "31": "新媒體暨傳播管理學系",
    "32": "廣播電視學系", "36": "資訊工程學系", "38": "犯罪防治學系", "39": "生物科技學系",
    "40": "醫療資訊與管理學系", "41": "法律學系", "42": "應用英語學系", "44": "應用日語學系",
    "46": "金融科技應用學士學位學程", "48": "旅遊與觀光學士學位學程", "52": "會計學系",
    "53": "資訊應用與金融保險學系", "54": "財務金融學系", "57": "國際企業學系",
    "59": "國際事務與外交學士學位學程", "60": "諮商臨床與工商心理學系",
    "61": "諮商臨床與工商心理學系碩士班諮商心理學組", "62": "諮商臨床與工商心理學系碩士班臨床心理學組",
    "64": "金融學系", "65": "財金法律學系", "67": "生物醫學工程學系", "68": "公共事務與行政管理學系",
    "70": "高階經理碩士在職學位學程", "74": "都市設計與永續發展學系", "75": "人工智慧應用學系",
    "76": "半導體應用學士學位學程", "79": "應用中文與華語文教學系", "83": "教育研究所", "84": "電機工程學系",
    "86": "金融科技應用學系", "88": "時尚與創新管理學士學位學程",
    "89": "資訊科技應用與管理學士學位學程", "90": "國際事務碩士學位學程",
    "91": "國際企業與貿易學士學位學程", "96": "金融科技碩士學位學程",
    "98": "國防行政管理進修學士學位學程", "99": "國際班", "KM": "金門校區(不分系所)"
}
LOCATION_LIST = {
    "1": "台北",
    "2": "桃園",
    "3": "金門",
    "4": "連江",
    "5": "基河",
    "6": "美國",
    "7": "泰國",
    "8": "馬來西亞"
}

def setup_driver():
    """初始化並返回一個配置好的 Selenium WebDriver 實例"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except TypeError:
        logging.warning("偵測到舊版 Selenium 語法，切換至 executable_path。")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    stealth(driver, languages=["zh-TW", "zh"], vendor="Google Inc.", platform="Win32",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    return driver

def get_data_from_page(driver):
    """從當前頁面解析課表 DataFrame"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#printlist table")))
        page_source = driver.page_source
        df_list = pd.read_html(StringIO(page_source))
        course_df = df_list[-1]
        course_df.dropna(how='all', inplace=True)
        return course_df
    except TimeoutException:
        logging.warning("在頁面中找不到課表 (等待超時)。")
        print("  > 在頁面中找不到課表 (等待超時)。")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"解析表格時發生錯誤: {e}")
        print(f"  > 解析表格時發生錯誤: {e}")
        return pd.DataFrame()

def scrape_department_based_courses(link_text):
    """爬取需要選擇系所和年級的課程 (必修/選修)"""
    print(f"\n--- 開始爬取【{link_text}】 ---")
    driver = setup_driver()
    all_dfs = []
    try:
        driver.get(ENTRY_URL)
        wait = WebDriverWait(driver, 15)
        
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text))).click()
        print(f"> 已進入【{link_text}】查詢頁面。")
        
        for dept_id, dept_name in DEPARTMENT_LIST.items():
            for grade in GRADES_TO_FETCH:
                try:
                    print(f"  正在查詢: {dept_name} - {grade}年級")
                    wait.until(EC.element_to_be_clickable((By.ID, 'MainContent_drpDepartment')))
                    Select(driver.find_element(By.ID, 'MainContent_drpDepartment')).select_by_value(dept_id)
                    Select(driver.find_element(By.ID, 'MainContent_drpGrade')).select_by_value(grade)
                    driver.find_element(By.ID, 'MainContent_btnSend').click()
                    
                    df = get_data_from_page(driver)
                    if not df.empty:
                        df['系所名稱'] = dept_name
                        df['年級'] = grade
                        all_dfs.append(df)
                    time.sleep(random.uniform(0.5, 1.0))
                except Exception as e:
                    logging.error(f"爬取 {dept_name}-{grade}年級 時失敗: {e}")
                    print(f"  > 爬取 {dept_name}-{grade}年級 時失敗，跳過。")
                    driver.refresh()
                    continue
    finally:
        driver.quit()
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

def scrape_location_based_courses(link_text):
    """爬取需要選擇校區的課程 (通識/教育學程)"""
    print(f"\n--- 開始爬取【{link_text}】 ---")
    driver = setup_driver()
    all_dfs = []
    try:
        driver.get(ENTRY_URL)
        wait = WebDriverWait(driver, 15)
        
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text))).click()
        print(f"> 已進入【{link_text}】查詢頁面。")
        
        location_dropdown_id = 'MainContent_drpCampus' 
        
        for loc_id, loc_name in LOCATION_LIST.items():
            try:
                print(f"  正在查詢: {loc_name}")
                wait.until(EC.element_to_be_clickable((By.ID, location_dropdown_id)))
                Select(driver.find_element(By.ID, location_dropdown_id)).select_by_value(loc_id)
                
                driver.find_element(By.ID, 'MainContent_btnSend').click()
                
                df = get_data_from_page(driver)
                if not df.empty:
                    df['查詢校區'] = loc_name
                    all_dfs.append(df)
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                logging.error(f"爬取 {loc_name} 時失敗: {e}")
                print(f"  > 爬取 {loc_name} 時失敗，跳過。")
                driver.refresh()
                continue
    finally:
        driver.quit()
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

def main():
    """主函式，提供互動選單讓使用者選擇爬取項目"""
    output_dir = "course_data"
    os.makedirs(output_dir, exist_ok=True)
    
    tasks = {
        "1": ("必修課程", scrape_department_based_courses),
        "2": ("選修課程", scrape_department_based_courses),
        "3": ("通識課程", scrape_location_based_courses),
        "4": ("教育學程課程", scrape_location_based_courses),
    }

    while True:
        print("\n======================================")
        print("  銘傳大學課程爬蟲")
        print("======================================")
        print("請選擇要爬取的課程類別：")
        print("1. 必修課程")
        print("2. 選修課程")
        print("3. 通識課程")
        print("4. 教育學程課程")
        print("5. 全部爬取")
        print("0. 離開")
        print("--------------------------------------")
        choice = input("請輸入選項 (0-5): ")

        if choice == '0':
            print("感謝使用，程式結束。")
            break
        
        selected_tasks = []
        if choice in tasks:
            selected_tasks.append(tasks[choice])
        elif choice == '5':
            selected_tasks = list(tasks.values())
        else:
            print("無效的選項，請重新輸入。")
            continue

        for task_name, scrape_function in selected_tasks:
            try:
                result_df = scrape_function(task_name)
                
                if not result_df.empty:
                    output_filename = os.path.join(output_dir, f"{task_name}.json")
                    # to_json 會直接覆蓋已存在的檔案
                    result_df.to_json(output_filename, orient='records', force_ascii=False, indent=4)
                    print(f"✅ 【{task_name}】爬取完成，共 {len(result_df)} 筆資料已儲存至 {output_filename}")
                else:
                    print(f"⚠️ 【{task_name}】未爬取到任何資料。")
            except Exception as e:
                print(f"❌ 執行【{task_name}】任務時發生嚴重錯誤: {e}")
                logging.error(f"執行【{task_name}】任務時發生嚴重錯誤: {e}")

        print("\n操作完成。")

if __name__ == "__main__":
    main()
