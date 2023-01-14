from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import csv

browser = webdriver.Chrome() # 크롬 브라우저 활용 / chromedriver 필요 
url_list = []  # 수집한 리스트를 리스트 형태로 저장
content_list = "" 
text = "성신여대미용실"  # 블로그에서 검색할 키워드

# < url 수집 >
for i in range(1, 4):  # 1~4페이지까지의 네이버 블로그 웹 사이트 페이지를 읽음
    url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo='+ str(i) + '&rangeType=ALL&orderBy=sim&keyword=' + text
    browser.get(url) # url로 이동
    time.sleep(0.5) # delay를 고려하여 0.5초 정도 기다린 뒤에 동작 

    for j in range(1, 7): # 검색된 블로그들의 url 수집
        titles = browser.find_element(By.XPATH,'/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
        title = titles.get_attribute('href') # title에서 href 태그에 나타나 있는 각 블로그 별 주소 수쥡
        url_list.append(title) # 수집된 주소를 url_list 내에 추가

# < 저장하기 >
filename = "blogtext.csv" # 저장할 csv 파일 이름
f = open(filename,"w",encoding="utf8",newline="") # encoding 형식 지정, newline="" 설정으로 한글 텍스트 외 불필요한 특수문자, 띄어쓰기 등 제거
writer = csv.writer(f)

# < text scraping > 
for url in url_list: # 수집한 url 만큼 반복
    browser.get(url) # 해당 url로 이동(블로그로 이동)
    browser.switch_to.frame('mainFrame') # html에서 iframe은 mainFrame으로 지정
    overlays = ".se-component.se-text.se-l-default" 
    contents = browser.find_elements(By.CSS_SELECTOR,overlays) # css_selector로 텍스트에 해당하는 elements를 모두 수집

    # < 토막 별 저장 > 
    data = [content.text for content in contents] # 전체 텍스트를 토막으로 나누어 리스트 형태로 변환
    writer.writerow(data) # 리스트를 저장

# selenium으로 불러온 웹 페이지가 자동으로 꺼지는 현상 방지( 없어도 됨 ) 
    # while(True):
    #     pass