import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#
# res = requests.get("https://www.youtube.com/watch?v=srj7k7902Yc")
#
# # print(res.content)
#
# soup = BeautifulSoup(res.content, 'html.parser')
#
# title = soup.find('title')
#
# print(title.get_text())


### Browser- Chrome web 사용.
options = webdriver.ChromeOptions()                     # Chrome 창의 옵션을 설정할 수 있는 코드.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')                    # headless : Broswer 창을 띄우지 않고 수행 (colab에서는 필수).
# options.add_argument("window-size = 1920,1080")       # window size 설정

browser = webdriver.Chrome(options = options)           # 위 Option을 적용한 Chrome 창을 실행.
browser.maximize_window()                               # browser 창 최대화

### Youtube
YOUTUBER = "슈카월드 코믹스"      # 댓글을 가져올 유튜브
CNT = 5                   # 댓글을 가져올 동영상 개수
INTERVAL = 5              # 페이지 로딩 대기 시간

### 페이지 이동
url = "https://www.youtube.com"
browser.get(url)
time.sleep(INTERVAL)

### 유튜버 검색
elem = browser.find_element("name", "search_query")
elem.send_keys(YOUTUBER)
elem.send_keys(Keys.ENTER)
time.sleep(INTERVAL)   # 검색 완료까지 대기.

#### 유튜브 채널 입장
elem = browser.find_element("id", "main-link")
elem.click()
time.sleep(INTERVAL)

#### 유튜브 동영상 목록
# WebDriverWait(browser, n).until(): until에서 설정한 Event가 완료될때까지 n초 대기
# EC.presence_of_element_located: Element 존재여부 확인
# By.PARTIAL_LINK_TEXT: 보이는 텍스트에 검색 값이 포함된 앵커 요소를 찾으며, 여러 요소가 일치하는 경우 첫 번째 요소만 선택.
try :
    elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "동영상")))
    elem.click()
finally :  # 동작 완료 및 실패 시
    pass
time.sleep(INTERVAL)

### 현재 페이지를 한 번 더 불러와야 오류가 안남
browser.get(browser.current_url); time.sleep(INTERVAL)

### 모든 동영상을 위해 스크롤 끝까지 내리기
scroll_cnt2 = 2
now_height = browser.execute_script("return document.documentElement.scrollHeight")
while scroll_cnt2 > 0:
    browser.execute_script("window.scrollTo(0, 800)")      # 스크롤을 가장 아래로 내림
    time.sleep(INTERVAL)                                                                     # 페이지 로딩 대기

    curr_height = browser.execute_script("return document.documentElement.scrollHeight")     # 현재 문서 높이를 가져와 저장
    scroll_cnt2 -= 1

print("스크롤 종료!")

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

video_urls = soup.find_all("a", class_ = "yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media")

video_df = pd.DataFrame(columns = ["Title", "Link"])
for url_ in video_urls:
    title = url_["title"]
    link = url + url_["href"]
    temp = pd.DataFrame([title, link], index = ["Title", "Link"]).T
    video_df = pd.concat([video_df, temp], axis = 0)

video_df.reset_index(drop = True, inplace = True)
print(video_df.shape)
video_df.head(3)

# 유튜브 동영상 들어가 댓글 긁어오기
Comment_dict = {}  # 댓글을 저장할 dictionary
Comment_cnt = 0  # 긁어온 댓글 개수

for i in range(0, CNT):  # 3개의 동영상

    ######################## 유튜브 댓글 긁기위해 i번째 동영상 링크 접속 ########################
    browser.get(video_df.loc[i, "Link"])
    time.sleep(INTERVAL)
    print("==" * 25)
    print("%d번째 동영상 댓글 크롤링 시작!" % (i + 1))

    ######################## 댓글을 보기 위해 스크롤 끝까지 내리기 ########################
    # 컴퓨터 부팅 속도와 댓들과 같은 상태에따라 스크롤 높이와 시간을 조정해야하는 것 같음
    scroll_cnt = 2  # 2번 스크롤하고 정지
    now_height = browser.execute_script(
        "return document.documentElement.scrollHeight")  # now_height: 현재의 스크롤 높이로 사용  // # 네이버의 경우 documentElement 대신 body
    site_height = browser.execute_script("return document.documentElement.scrollHeight")

    # 반복 수행
    while scroll_cnt > 0:
        # browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)") # 스크롤을 가장 아래로 내림
        browser.execute_script("window.scrollTo(0, 800)")  # 스크롤을 800만큼 아래로 내림
        time.sleep(INTERVAL)  # 페이지 로딩 대기

        curr_height = browser.execute_script("return document.documentElement.scrollHeight")  # 현재 문서 높이를 가져와 저장
        scroll_cnt -= 1

    print(" -스크롤 완료! | (현재 페이지 높이 : %d)" % (curr_height))
    time.sleep(INTERVAL)  # 페이지 로딩 대기

    ######################## ID와 댓글 긁어오기 ########################
    soup = BeautifulSoup(browser.page_source, "lxml")

    # 댓글 박스 가져오기
    comment_box = soup.select("ytd-item-section-renderer#sections > div#contents")[0]

    # 댓글 리스트 길이 가져오기
    comment_len = len(comment_box.select("ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer"))
    Comment_cnt += comment_len
    print(" -이번에 수집한 댓글 수: %d개 | 누적 댓글 수: %d개" % (comment_len, Comment_cnt))

    # 반복문 작업
    for idx in range(comment_len):
        # 댓글 리스트 가져오기
        comments = comment_box.select("ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer")

        name = comments[idx].select_one("a#author-text").text.strip()
        comment = comments[idx].select_one("yt-attributed-string#content-text").text.strip()
        # try:
        #     like = comments[idx].select_one("span#vote-count-middle").attrs['aria-label']
        # except:
        #     like = ""

        Comment_dict[name] = {"Comment": comment}

    print("%d번째 동영상 댓글 크롤링 끝!" % (i + 1))

### 브라우저 종료
browser.quit()

Comment_df = pd.DataFrame.from_dict(Comment_dict, orient = 'index')
Comment_df["ID"] = Comment_df.index
Comment_df = Comment_df[["ID", "Comment"]].reset_index(drop = True)
print(Comment_df.shape)
Comment_df.head(3)

Comment_df.to_csv(YOUTUBER + "'s Youtube_comment.csv", index = False)