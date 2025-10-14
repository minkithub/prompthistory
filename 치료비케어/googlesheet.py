import pandas as pd

def save_excel_data_to_txt(excel_path, output_path):
    """
    엑셀 파일 데이터를 읽어 텍스트 파일(.txt)로 저장합니다.

    Args:
        excel_path (str): 읽어올 엑셀 파일의 전체 경로.
        output_path (str): 저장할 텍스트 파일의 경로.
    """
    try:
        df = pd.read_excel(excel_path)
        records = df.to_dict('records')

        # 'w' 모드로 파일을 열고, utf-8 인코딩을 지정하여 한글 깨짐을 방지합니다.
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"'{excel_path}' 파일에서 총 {len(records)}개의 행을 찾았습니다.\n\n")

            for i, record in enumerate(records):
                f.write(f"--- 행 {i+1} 데이터 ---\n")
                for key, value in record.items():
                    display_value = "" if pd.isna(value) else value
                    f.write(f"{key} : {display_value}\n")
                f.write("-" * 20 + "\n\n")

        print(f"성공적으로 데이터를 '{output_path}' 파일에 저장했습니다.")

    except FileNotFoundError:
        print(f"[오류] 엑셀 파일을 찾을 수 없습니다: '{excel_path}'")
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    EXCEL_FILE = "/Users/minki/notevscode/치료비케어/medi.xlsx"
    OUTPUT_TXT_FILE = "output.txt"  # 저장될 텍스트 파일 이름

    save_excel_data_to_txt(EXCEL_FILE, OUTPUT_TXT_FILE)
