import win32com.client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import re
import pyperclip as ppc
from math import ceil
from threading import Thread, Lock
import pythoncom


DRIVER_PATH = 'C:\python\chromedriver.exe'
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')


def Deeptrans(t, driver):
    global translated_texts
    stextarea = driver.find_element_by_css_selector(
        '.lmt__textarea.lmt__source_textarea.lmt__textarea_base_style')
    ttextarea = driver.find_element_by_css_selector(
        '.lmt__textarea.lmt__target_textarea.lmt__textarea_base_style')
    for i in range(t * unit, min((t + 1) * unit, length)):
        sourse_text = sourse_texts[i]
        if re.search(r"[\x00-\x1F\x7F]",
                     sourse_text.strip()) or len(sourse_text.strip()) < 5:
            continue
        lock.acquire()
        ppc.copy(sourse_text)
        stextarea.send_keys(Keys.CONTROL, "v")
        lock.release()
        translated_text = ""
        while not translated_text:
            time.sleep(5)
            translated_text = ttextarea.get_property("value")
        stextarea.send_keys(Keys.CONTROL, "a")
        stextarea.send_keys(Keys.BACKSPACE)
        translated_texts[str(i + 1)] = translated_text


def runDriver(t):
    driver = webdriver.Chrome(DRIVER_PATH)
    url = 'https://www.deepl.com/ja/translator'
    driver.get(url)
    Deeptrans(t, driver)
    driver.quit()


def multiThreadTranslate(file_path, font):
    global lock, length, unit, sourse_texts, translated_texts
    app = win32com.client.Dispatch("Word.Application")
    app.Visible = True #コメントアウトでWord非表示
    doc = app.Documents.Open(file_path)
    try:
        doc.Paragraphs(1).Range.Font.Name = font
    except:
        print('指定されたフォントは存在しません')
        doc.Close(SaveChanges=0)
        app.Quit()
        return
    length = doc.Paragraphs.Count
    n = 9 #Chromeを9つ開いて同時実行
    unit = ceil(length / n)
    lock = Lock()
    clipboard = ppc.paste()
    sourse_texts = [doc.Paragraphs(i + 1).Range.Text for i in range(length)]
    translated_texts = {}
    threads = []
    for t in range(n):
        thread = Thread(target=runDriver, args=(t, ))
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    for k, v in translated_texts.items():
        doc.Paragraphs(int(k)).Range.Text = v.replace('\n', '\r')
        doc.Paragraphs(int(k)).Range.Font.Name = font
    doc.SaveAs2(FileName=re.sub("(.+)(\.pdf)", r"\1_jp.pdf", file_path),
                FileFormat=17)
    doc.Close(SaveChanges=0)
    app.Quit()
    print('Process is completed.')
    ppc.copy(clipboard)


if __name__ == '__main__':
    file_path = input('PDFの絶対パスを入力してください:     ')
    print('フォントを選択してください')
    fonts = {'1': '游明朝', '2': 'メイリオ', '3': 'BIZ UDP明朝 Medium', '4': 'その他'}
    font = fonts[input('   '.join(
        [", ".join(list(fonts.items())[i])
         for i in range(len(fonts))]) + ":     ")]
    if font == 'その他': font = input('フォント名を入力してください:     ')
    multiThreadTranslate(file_path, font=font)
