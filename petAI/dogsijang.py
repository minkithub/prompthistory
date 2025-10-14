import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_dog_sijang_contacts():
    """
    dogsijang.co.kr 웹사이트의 분양 게시판에서 연락처를 스크래핑하고,
    중복을 제거하여 유니크한 값만 반환합니다.
    """
    
    base_url = "https://dogsijang.co.kr/board_dog/list.php?tb=board_sale"
    page_num = 1
    all_contacts = []

    print("▶ 스크래핑을 시작합니다.")

    while True:
        url = f"{base_url}&pagenum={page_num}"
        print(f"[*] 현재 페이지 스크래핑 중: {page_num}...")

        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"오류 발생: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        list_rows = soup.select('tr[onmouseover^="this.style.backgroundColor"]')

        if not list_rows:
            print("[-] 더 이상 게시물이 없습니다. 스크래핑을 종료합니다.")
            break

        for row in list_rows:
            contact_td = row.select_one('td:nth-of-type(8)')
            if contact_td:
                contact = contact_td.get_text(strip=True)
                if contact:
                    all_contacts.append(contact)
        
        page_num += 1
        time.sleep(0.5)

    # --- ✨ 중복 제거 로직 추가 ✨ ---
    # 1. 리스트를 set으로 변환하여 중복을 제거합니다.
    # 2. 다시 list로 변환하여 순서를 유지하고 반환합니다.
    unique_contacts = list(dict.fromkeys(all_contacts))
    
    print(f"\n▶ 총 {len(all_contacts)}개의 연락처 수집 완료. 중복 제거 후 {len(unique_contacts)}개의 유니크한 연락처를 반환합니다.")
    
    return unique_contacts

if __name__ == "__main__":
    contacts = scrape_dog_sijang_contacts()
    
    if contacts:
        print("▶ 엑셀 파일로 저장을 시작합니다.")
        
        df = pd.DataFrame(contacts, columns=['연락처'])
        df.to_excel('dogsijang_contacts_unique.xlsx', index=False)
        
        print("✅ 'dogsijang_contacts_unique.xlsx' 파일로 저장이 완료되었습니다.")
    else:
        print("\n▶ 수집된 연락처가 없어 엑셀 파일을 생성하지 않았습니다.")