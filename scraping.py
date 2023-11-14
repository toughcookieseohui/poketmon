# 필요한 라이브러리
import time
import csv
import threading
import requests
from bs4 import BeautifulSoup as BS4

def scrap_one_page_in_pokedex(base_url, no_page):
    # 포켓몬 도감의 기본 URL 형에 포켓몬 상세 페이지 번호를 붙여 열람 대상 페이지의 URL 생성
    # 이 페이지를 get 하고 BS4로 파싱
    page_response = requests.get(base_url + str(no_page))
    soup = BS4(page_response.text, "html.parser")

    # 포켓몬의 이미지와 상세 정보를 담고 있는 엘리먼트는 아래와 같다
    # <div class="col-lg-6 col-12">
    
    # 상기 상기 정보로 DOM에서 find하면 두 개의 div를 찾아주는데, 첫 번째는 포켓몬 이미지
    # 해당 div에서 이미지의 경로를 구한다
    # (cont.) 다운 받아서 DB에 넣을 궁리
    img_pokemon = soup.find_all("div", "col-lg-6 col-12")[0].find("img")["src"]
    
    # 상기 div 중 두 번째는 포켓몬의 이름 외 갖가지 정보
    # 보기 좋게 별도의 변수에 할당
    detail_pokemon = soup.find_all("div", "col-lg-6 col-12")[1]
    
    # 포켓몬 도감 번호; int
    # 정수로 저장하고, 후에 'No. XXXX' 로 표기
    no_pokemon = str(int(detail_pokemon.h3.p.text[4:]))
    
    # 포켓몬 이름
    name_pokemon = detail_pokemon.h3.p.next_sibling

    # 포켓몬 설명
    description_pokemon = detail_pokemon.select_one(".para").text
    
    # 타입 외 포켓몬 특성
    info_pokemon = detail_pokemon.find("div", "bx-detail").find_all("div", "col-4")
    
    # 타입; 둘 이상 구분자 세미콜론(;)
    tmp_type = []
    for kind_of_type in info_pokemon[0].find_all("p"):
        tmp_type.append(kind_of_type.text)
    
    type_pokemon = ';'.join(tmp_type)
            
    # 키; float
    height_pokemon = info_pokemon[1].p.text.rstrip('~').rstrip('m')
    
    # 분류
    # 분류명 뒤의 '포켓몬' 제거했음. 향후 게시할 때 붙이면 됨.
    sort_pokemon = info_pokemon[2].p.text.strip().rstrip("포켓몬")
    
    # 몸무게; flaot
    # 단, ???.?kg 은 math.inf 취급
    weight_pokemon = info_pokemon[4].p.text.rstrip('~').rstrip('kg')
    if weight_pokemon.startswith('?'):
        weight_pokemon = "INF"
    
    # 특성; 둘 이상 구분자 세미콜론(;)
    tmp_ability = []
    for ability in info_pokemon[5].find_all("button"):
        tmp_ability.append(ability.previous_sibling.strip())
    
    ability_pokemon = ';'.join(tmp_ability)
    
    # 성별
    # 성별을 나타내는 이미지의 수와 이미지의 클래스를 활용하여 구분
    # 양성:: b(bi), 수컷:: m(mail), 암컷:: f(femail), 불명:: u(unkown)
    # 성별 정보는 텍스트 대신 아이콘 이미지로 표현, 이미지는 i 태그로 지칭
    tmp_sex = info_pokemon[3].find_all("i")
    # 아이콘의 수가 2이면 양성
    sex_pokemon = 'b'
    # 아이콘의 수가 0이면 불명
    if len(tmp_sex) == 0:
        sex_pokemon = 'u'
    # 아이콘의 수가 1이면 수컷/얌컷 중 하나
    elif len(tmp_sex) == 1:
        if tmp_sex[0].get("class")[0] == "icon-man":
            sex_pokemon = 'm'
        else:
            sex_pokemon = 'f'

    # 진화; 둘 이상 구분자 세미콜론(;)
    # 진화 내용이 없을 경우 NA 표기
    tmp_evolution = []
    if soup.find("div", "row per1-1") is not None:
        for info_em in soup.find("div", "row per1-1").select("h4 > p"):
            if info_em.text != '':
                tmp_evolution.append(info_em.text)
        tmp_evolution[0] = str(int(tmp_evolution[0][4:]))
        tmp_evolution[2] = str(int(tmp_evolution[2][4:]))
        if len(tmp_evolution) > 4:
            tmp_evolution[4] = str(int(tmp_evolution[4][4:]))
    if len(tmp_evolution) == 0:
        evolution_pokemon = "NA"
    else:
        evolution_pokemon = ';'.join(tmp_evolution)

    # 포켓몬 번호와 이름으로 기본키 역할을 못 하기에 포켓몬 도감 페이지 번호를 키로 활용
    return [no_page, no_pokemon, name_pokemon, type_pokemon,  height_pokemon,  sort_pokemon,   sex_pokemon,  weight_pokemon, ability_pokemon, description_pokemon, evolution_pokemon, img_pokemon]


base_url = "https://www.pokemonkorea.co.kr/pokedex/view/"
# 23. 11. 09 기준 포켓몬 도감 총 페이지
total_num_of_pokedex = 1229

# 쓰레드 별 스크레핑 결과를 인 메모리 보관하기 위한 리스트
result_p1 = []
result_p2 = []
result_p3 = []

# 스크레핑 함수를 쓰레드에 전달하기 위한 래퍼 역할 함수
def scraping_via_thread(base_url, start_n, end_n, result_list):
    for no_page in range(start_n, end_n+1):
        result_list.append(scrap_one_page_in_pokedex(base_url, no_page))
        time.sleep(0.1)

# 3개의 쓰레드로 작업
# 레이스 컨디션을 신경쓰지 않기 위해 작업 분량은 분할
scraping_thread1 = threading.Thread(target=scraping_via_thread, args=(base_url, 1, 400, result_p1))
scraping_thread2 = threading.Thread(target=scraping_via_thread, args=(base_url, 401, 800, result_p2))
scraping_thread3 = threading.Thread(target=scraping_via_thread, args=(base_url, 801, total_num_of_pokedex, result_p3))

scraping_thread1.start()
scraping_thread2.start()
scraping_thread3.start()

# 인 메모리 상태인 스크래핑 결과를 파일에 담기 위해 메인 쓰레드는 서브 쓰레드 종료까지 대기
scraping_thread1.join()
scraping_thread2.join()
scraping_thread3.join()

csv_pokedex = open("scraping_pokedex.csv", 'w+', newline='')
csv_writer = csv.writer(csv_pokedex)
# 스크래핑 항목 레이블을 CSV에 기입
csv_writer.writerow(('key', 'no', 'name', 'type',  'height',  'sort',   'sex',  'weight', 'ability', 'description', 'evolution''img_src'))

# CSV에 순서대로 기입
for info_pokemon in result_p1:
    csv_writer.writerow(info_pokemon)
for info_pokemon in result_p2:
    csv_writer.writerow(info_pokemon)
for info_pokemon in result_p3:
    csv_writer.writerow(info_pokemon)

csv_pokedex.close()
