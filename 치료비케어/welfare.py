import re
import csv
import requests
from bs4 import BeautifulSoup
import time

# [복지관 데이터]를 문자열로 정의합니다.
# (전체 데이터를 여기에 복사하여 붙여넣으세요)
data = """
기관명: 가락종합사회복지관
연락처: 02-449-2341-3
홈페이지: http://www.garak.or.kr/
--------------------
기관명: 가양4종합사회복지관
연락처: 02-2668-6689
홈페이지: http://www.gayang4.or.kr/
--------------------
기관명: 가양5종합사회복지관
연락처: 02-2668-4603-4
홈페이지: http://www.gy5welfare.or.kr/
--------------------
기관명: 가양7종합사회복지관
연락처: 02-2668-8600
홈페이지: http://www.gayang7.or.kr/
--------------------
기관명: 갈월종합사회복지관
연락처: 02-752-7887
홈페이지: http://www.galwol.or.kr/
--------------------
기관명: 강감찬관악종합사회복지관
연락처: 02-886-9941-3
홈페이지: http://gaw.or.kr/
--------------------
기관명: 강남종합사회복지관
연락처: 02-451-0051-3
홈페이지: http://www.kangnamwelfare.co.kr/
--------------------
기관명: 강동종합사회복지관
연락처: 02-2041-7800
홈페이지: http://www.kdswc.or.kr/
--------------------
기관명: 공릉종합사회복지관
연락처: 02-948-0520-2
홈페이지: http://www.gongreung.or.kr/
--------------------
기관명: 광장종합사회복지관
연락처: 02-2201-1333
홈페이지: http://www.gj.or.kr/xe/
--------------------
기관명: 구로종합사회복지관
연락처: 02-852-0525
홈페이지: https://9ro.or.kr
--------------------
기관명: 구세군강북종합사회복지관
연락처: 02-984-5811~4
홈페이지: http://www.gangbuk.or.kr/
--------------------
기관명: 궁동종합사회복지관
연락처: 02-2613-9367
홈페이지: http://www.happykd.or.kr/
--------------------
기관명: 금천누리종합사회복지관
연락처: 02-868-6856
홈페이지: http://www.gcnuri.or.kr/
--------------------
기관명: 길음종합사회복지관
연락처: 02-985-0161-4
홈페이지: http://www.guswc.org/
--------------------
기관명: 까리따스방배종합사회복지관
연락처: 02-522-6004
홈페이지: http://www.cbwc.or.kr/
--------------------
기관명: 꿈의숲종합사회복지관
연락처: 02-984-6777
홈페이지: http://www.bestbun3.org
--------------------
기관명: 노원1종합사회복지관
연락처: 02-949-0700-3
홈페이지: http://www.nowon.or.kr/
--------------------
기관명: 녹번종합사회복지관
연락처: 02-388-6341-4
홈페이지: http://nokbeon.or.kr/
--------------------
기관명: 능인종합사회복지관
연락처: 02-571-2989
홈페이지: http://nungin.or.kr/index.html
--------------------
기관명: 대방종합사회복지관
연락처: 02-826-2900-3
홈페이지: http://daebangswc.org/index.html
--------------------
기관명: 대청종합사회복지관
연락처: 02-459-6332-4
홈페이지: http://www.daechung.or.kr/
--------------------
기관명: 도봉서원종합사회복지관
연락처: 02-3494-4755
홈페이지: http://www.dbsw.or.kr/
--------------------
기관명: 동대문종합사회복지관
연락처: 02-920-4500
홈페이지: http://www.communitycenter.or.kr/
--------------------
기관명: 동작이수사회복지관
연락처: 02-592-3721-2
홈페이지: http://www.isuwelfare.or.kr/
--------------------
기관명: 동작종합사회복지관
연락처: 02-814-8114
홈페이지: http://www.dongjaksw.or.kr/
--------------------
기관명: 등촌1종합사회복지관
연락처: 02-2658-1010
홈페이지: http://www.dc1welfare.or.kr/
--------------------
기관명: 등촌4종합사회복지관
연락처: 02-2658-8800
홈페이지: http://www.dc4.or.kr/
--------------------
기관명: 등촌7종합사회복지관
연락처: 02-2658-6521-4
홈페이지: http://www.dc7.or.kr/
--------------------
기관명: 등촌9종합사회복지관
연락처: 02-2658-4127~9
홈페이지: http://www.dc9.or.kr/
--------------------
기관명: 마들종합사회복지관
연락처: 02-971-8387-8
홈페이지: http://www.madeul.org/
--------------------
기관명: 마천종합사회복지관
연락처: 02-449-3141-2
홈페이지: http://macheon-welfare.or.kr
--------------------
기관명: 면목종합사회복지관
연락처: 02-436-0500
홈페이지: http://www.truem.or.kr/
--------------------
기관명: 목동종합사회복지관
연락처: 02-2651-2332
홈페이지: http://www.mokdongswc.org
--------------------
기관명: 반포종합사회복지관
연락처: 02-3477-9811
홈페이지: http://www.mybanpo.org/
--------------------
기관명: 방아골종합사회복지관
연락처: 02-3491-0500
홈페이지: http://www.bangahgol.or.kr/
--------------------
기관명: 방화11종합사회복지관
연락처: 02-2661-0670-3
홈페이지: http://banghwa11.or.kr/
--------------------
기관명: 방화2종합사회복지관
연락처: 02-2662-6661-4
홈페이지: http://banghwa2.goodneighbors.kr/
--------------------
기관명: 방화6종합사회복지관
연락처: 02-2666-6181
홈페이지: http://banghwa6.or.kr/
--------------------
기관명: 번오마을종합사회복지관
연락처: 02-981-5077
홈페이지: http://www.bun5bok.or.kr/
--------------------
기관명: 북부종합사회복지관
연락처: 02-934-7711-5
홈페이지: http://www.bookboo.or.kr/
--------------------
기관명: 북서울종합사회복지관
연락처: 02-987-5077-9
홈페이지: http://www.saeun.com/
--------------------
기관명: 사당종합사회복지관
연락처: 02-597-3710-2
홈페이지: http://www.sadangwelfare.org/new_2007/index.htm
--------------------
기관명: 사랑의전화마포종합사회복지관
연락처: 02-712-8600
홈페이지: http://www.laf.or.kr/
--------------------
기관명: 삼전종합사회복지관
연락처: 02-421-6077-8
홈페이지: http://www.samjeon.or.kr/index.php
--------------------
기관명: 상계종합사회복지관
연락처: 02-951-9930-2
홈페이지: http://www.sanggyebokji.or.kr/
--------------------
기관명: 상도종합사회복지관
연락처: 02-824-6011-3
홈페이지: http://www.happysangdo.or.kr/
--------------------
기관명: 생명의전화종합사회복지관
연락처: 02-916-9193-5
홈페이지: http://www.lifelineseoul.or.kr/
--------------------
기관명: 서대문종합사회복지관
연락처: 02-375-5040
홈페이지: http://www.sdmbokji.or.kr/
--------------------
기관명: 서울YWCA봉천종합사회복지관
연락처: 02-870-4400
홈페이지: http://www.bongchuny.or.kr/
--------------------
기관명: 서울시립대종합사회복지관
연락처: 02-3421-1988-9
홈페이지: http://uoscc.or.kr/
--------------------
기관명: 성내종합사회복지관
연락처: 02-478-2555
홈페이지: https://snwelfare.com/
--------------------
기관명: 성동종합사회복지관
연락처: 02-2290-3100
홈페이지: http://www.linksd.net/
--------------------
기관명: 성민종합사회복지관
연락처: 02-876-0900
홈페이지: http://www.smw.or.kr/
--------------------
기관명: 성산종합사회복지관
연락처: 02-374-5884-5
홈페이지: http://www.sungsan21.org/
--------------------
기관명: 성수종합사회복지관
연락처: 02-2204-9900
홈페이지: https://www.seongsuwc.or.kr
--------------------
기관명: 송파종합사회복지관
연락처: 02-401-1919
홈페이지: http://www.songpacc.or.kr/
--------------------
기관명: 수서명화종합사회복지관
연락처: 02-459-2696-7
홈페이지: http://mhwelfare.or.kr
--------------------
기관명: 수서종합사회복지관
연락처: 02-459-5504
홈페이지: https://www.suseo1993.co.kr/index.php
--------------------
기관명: 신길종합사회복지관
연락처: 02-831-2755
홈페이지: http://www.singil.org/
--------------------
기관명: 신내종합사회복지관
연락처: 02-3421-3400
홈페이지: http://www.snwc.or.kr/
--------------------
기관명: 신당종합사회복지관
연락처: 02-2231-1876-8
홈페이지: http://shindang.or.kr/
--------------------
기관명: 신림종합사회복지관
연락처: 02-851-1767-9
홈페이지: http://www.sillym.or.kr/
--------------------
기관명: 신목종합사회복지관
연락처: 02-2643-7221-3
홈페이지: http://www.shinmok.or.kr/index.php
--------------------
기관명: 신사종합사회복지관
연락처: 02-376-4141-2
홈페이지: https://www.sscc.or.kr/
--------------------
기관명: 신월종합사회복지관
연락처: 02-2605-8728
홈페이지: http://www.sinwc.org/
--------------------
기관명: 신정종합사회복지관
연락처: 02-2603-1792-3
홈페이지: http://www.shinjung.or.kr/
--------------------
기관명: 양재종합사회복지관
연락처: 02-579-4782-4
홈페이지: http://www.yangjaewc.or.kr/
--------------------
기관명: 염리종합사회복지관
연락처: 02-3276-1800
홈페이지: http://www.ynswc.or.kr
--------------------
기관명: 영등포종합사회복지관
연락처: 02-845-5331
홈페이지: http://www.childfund-ydp.or.kr/
--------------------
기관명: 영중종합사회복지관
연락처: 02-02-2679-2024
홈페이지: https://blog.naver.com/yeongjungsw
--------------------
기관명: 옥수종합사회복지관
연락처: 02-2282-1100
홈페이지: http://www.oksoocwc.or.kr/
--------------------
기관명: 우면종합사회복지관
연락처: 02-577-6321-2
홈페이지: http://www.woomyun.or.kr/
--------------------
기관명: 월계종합사회복지관
연락처: 02-999-4211-3
홈페이지: http://www.wwc.or.kr/
--------------------
기관명: 월곡종합사회복지관
연락처: 02-911-5511
홈페이지: http://www.hmwolgok.or.kr/
--------------------
기관명: 유락종합사회복지관
연락처: 02-2235-4000
홈페이지: http://www.yurak.or.kr/
--------------------
기관명: 유린원광종합사회복지관
연락처: 02-438-4011-2
홈페이지: http://www.yurin.or.kr/
--------------------
기관명: 은평종합사회복지관
연락처: 02-307-1181-3
홈페이지: http://www.eunpyeong.or.kr/
--------------------
기관명: 이대종합사회복지관
연락처: 02-3277-3190-1
홈페이지: http://www.ewhawelfare.or.kr/
--------------------
기관명: 자양종합사회복지관
연락처: 02-458-1664
홈페이지: http://www.jayang.or.kr/
--------------------
기관명: 잠실종합사회복지관
연락처: 02-423-7807-8
홈페이지: http://www.jamsilswc.or.kr/
--------------------
기관명: 장안종합사회복지관
연락처: 02-2242-7564-6
홈페이지: http://www.jang-an.or.kr/
--------------------
기관명: 장위종합사회복지관
연락처: 02-918-3073-5
홈페이지: http://www.jangwi.or.kr/
--------------------
기관명: 정릉종합사회복지관
연락처: 02-909-0434-6
홈페이지: http://www.jnwelfare.or.kr/
--------------------
기관명: 종로종합사회복지관
연락처: 02-766-8282
홈페이지: http://www.jongno.or.kr/
--------------------
기관명: 중계종합사회복지관
연락처: 02-952-0333-5
홈페이지: http://www.junggye.or.kr/
--------------------
기관명: 중곡종합사회복지관
연락처: 02-3436-4316-7
홈페이지: http://www.chunggok.org/
--------------------
기관명: 중림종합사회복지관
연락처: 02-362-3348
홈페이지: http://www.jlcwc.or.kr/
--------------------
기관명: 중앙사회복지관
연락처: 02-872-5802
홈페이지: http://www.causwc.or.kr/main/main.html
--------------------
기관명: 창동종합사회복지관
연락처: 02-993-3222
홈페이지: http://www.changdong21.or.kr/
--------------------
기관명: 청담종합사회복지관
연락처: 02-806-1376-7
홈페이지: http://www.chungdam.or.kr/
--------------------
기관명: 태화기독교사회복지관
연락처: 02-2040-1600
홈페이지: https://www.taiwha.or.kr/
--------------------
기관명: 평화종합사회복지관
연락처: 02-949-0123-4
홈페이지: http://www.pyunghwa.or.kr/
--------------------
기관명: 풍납종합사회복지관
연락처: 02-474-1201
홈페이지: http://www.pnswc.co.kr/
--------------------
기관명: 하계종합사회복지관
연락처: 02-6928-0108
홈페이지: http://www.hgwelfare.or.kr/
--------------------
기관명: 한빛종합사회복지관
연락처: 02-2690-8762-4
홈페이지: http://www.han-bit.or.kr/
--------------------
기관명: 홍은종합사회복지관
연락처: 02-395-3959
홈페이지: http://www.hwelfare.or.kr
--------------------
기관명: 화원종합사회복지관
연락처: 02-837-0761
홈페이지: https://www.hwawon.org/
--------------------
기관명: 효창종합사회복지관
연락처: 02-716-0600
홈페이지: http://www.hyochang.or.kr/
--------------------
기관명: 흑석종합사회복지관
연락처: 02-817-8052-4
홈페이지: https://hswelfare.kr/
"""

def parse_initial_data(text_data):
    """주어진 텍스트 데이터를 파싱하여 기관별 정보를 리스트로 반환합니다."""
    institutions = []
    # '----' 기준으로 각 기관 정보 분리
    blocks = text_data.strip().split('--------------------')
    for block in blocks:
        if not block.strip():
            continue
        
        inst_info = {}
        for line in block.strip().split('\n'):
            if '기관명:' in line:
                inst_info['name'] = line.split(':', 1)[1].strip()
            elif '연락처:' in line:
                inst_info['phone'] = line.split(':', 1)[1].strip()
            elif '홈페이지:' in line:
                inst_info['url'] = line.split(':', 1)[1].strip()
        institutions.append(inst_info)
    return institutions

def scrape_footer_info(url):
    """
    주어진 URL의 웹사이트에 접속하여 footer 영역의 이메일과 연락처를 수집합니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    email = "정보 없음"
    phone = "정보 없음"

    try:
        # 타임아웃 10초 설정, SSL 인증서 오류 무시
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. footer 영역 찾기 (다양한 태그와 클래스명 시도)
        footer = soup.find('footer')
        if not footer:
            footer = soup.find('div', id='footer')
        if not footer:
            footer = soup.find('div', class_='footer')
        if not footer:
            # footer를 못찾으면 body 전체를 대상으로 검색
            footer = soup.body
        
        if not footer:
            return {"email": "분석 실패", "phone": "분석 실패"}
            
        footer_text = footer.get_text(separator=' ')

        # 2. 이메일 주소 찾기 (정규표현식 사용)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, footer_text)
        if email_match:
            email = email_match.group(0)

        # 3. 연락처 찾기 (정규표현식 사용, 다양한 형식 고려)
        phone_pattern = r'(\d{2,3}[-.\s)]?\d{3,4}[-.\s]?\d{4})'
        phone_matches = re.findall(phone_pattern, footer_text)
        
        # 'Tel', 'T.', '전화' 등 키워드 근처의 번호를 우선적으로 탐색
        for keyword in ['Tel', 'T.', '전화', '대표번호', '연락처', '문의']:
            if keyword in footer_text:
                # 키워드 주변 텍스트에서 번호 다시 검색
                start_index = footer_text.find(keyword)
                search_area = footer_text[start_index:start_index+50]
                phone_match_keyword = re.search(phone_pattern, search_area)
                if phone_match_keyword:
                    phone = phone_match_keyword.group(0)
                    break # 찾으면 반복 중단
        
        if phone == "정보 없음" and phone_matches:
            phone = phone_matches[0] # 키워드 근처에서 못찾으면 첫번째로 찾은 번호 사용
            
        return {"email": email.strip(), "phone": phone.strip()}

    except requests.exceptions.RequestException as e:
        print(f"  [오류] {url} 접속 실패: {e}")
        return {"email": "접속 실패", "phone": "접속 실패"}
    except Exception as e:
        print(f"  [오류] {url} 분석 중 알 수 없는 오류: {e}")
        return {"email": "분석 오류", "phone": "분석 오류"}

def main():
    """메인 실행 함수"""
    # 1. 초기 데이터 파싱
    initial_list = parse_initial_data(data)
    
    # 2. CSV 파일 준비
    output_filename = "welfare_list.csv"
    with open(output_filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # CSV 헤더 작성
        header = ['기관명', '홈페이지주소', '전화번호', '사과', '딸기', '포도', '수박', '이메일주소']
        writer.writerow(header)
        
        print(f"총 {len(initial_list)}개의 기관 크롤링을 시작합니다.")
        
        # 3. 각 기관별로 크롤링 및 데이터 저장
        for inst in initial_list:
            print(f"[{inst['name']}] 크롤링 중... ({inst['url']})")
            
            # 홈페이지에서 푸터 정보 수집
            footer_info = scrape_footer_info(inst['url'])
            
            # 최종 전화번호 결정 (푸터에서 수집 성공 시 푸터 정보, 아니면 기존 정보)
            final_phone = footer_info['phone'] if footer_info['phone'] != "정보 없음" else inst.get('phone', '정보 없음')
            
            # CSV 행 데이터 구성
            row = [
                inst.get('name', ''),
                inst.get('url', ''),
                final_phone,
                '사과', # 고정값
                '딸기', # 고정값
                '포도', # 고정값
                '수박', # 고정값
                footer_info['email']
            ]
            
            # CSV 파일에 행 쓰기
            writer.writerow(row)
            
            # 서버에 부담을 주지 않기 위해 1초 대기
            time.sleep(1)

    print("-" * 40)
    print(f"'{output_filename}' 파일 생성이 완료되었습니다.")


# 스크립트 실행
if __name__ == "__main__":
    # requests에서 발생하는 InsecureRequestWarning 경고 비활성화
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    main()