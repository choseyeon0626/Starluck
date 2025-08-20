# streamlit_app.py

import streamlit as st

# --- 라이브러리 임포트 및 오류 처리 ---
# 앱에 필요한 핵심 라이브러리(부품)가 있는지 먼저 확인합니다.
try:
    import requests
    from bs4 import BeautifulSoup
# 만약 'requests'나 'bs4'가 없다는 오류(ModuleNotFoundError)가 발생하면,
# 앱 실행을 중단하고 사용자에게 해결 방법을 안내합니다.
except ModuleNotFoundError:
    st.error(
        """
        'beautifulsoup4'와 'requests' 라이브러리가 설치되지 않았습니다.
        이 앱을 실행하려면 아래 명령어를 터미널(Terminal)에 복사하여 붙여넣고 실행해주세요.
        """
    )
    st.code("pip install beautifulsoup4 requests", language="bash")
    # 라이브러리가 없으면 더 이상 진행되지 않도록 st.stop()으로 앱 실행을 중단합니다.
    st.stop()

# --- 핵심 기능 함수 ---

def get_zodiac_sign(month, day):
    """월과 일을 입력받아 해당하는 별자리를 문자열로 반환합니다."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "양자리"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "황소자리"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "쌍둥이자리"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "게자리"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "사자자리"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 23):
        return "처녀자리"
    elif (month == 9 and day >= 24) or (month == 10 and day <= 22):
        return "천칭자리"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
        return "전갈자리"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 24):
        return "사수자리"
    elif (month == 12 and day >= 25) or (month == 1 and day <= 19):
        return "염소자리"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "물병자리"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "물고기자리"
    return None

@st.cache_data(ttl=21600)  # 6시간 동안 운세 결과 캐싱
def get_todays_horoscope(zodiac_sign):
    """별자리 이름을 입력받아 오늘의 운세를 웹에서 가져옵니다."""
    try:
        url = f"https://search.naver.com/search.naver?query={zodiac_sign}+운세"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        horoscope_element = soup.select_one('div.detail > p.text')
        
        if horoscope_element:
            return horoscope_element.get_text(strip=True)
        else:
            return "운세 정보를 가져올 수 없습니다. 웹 페이지 구조가 변경되었을 수 있습니다."
    except Exception as e:
        return f"운세 정보를 가져오는 중 오류가 발생했습니다: {e}"

# --- Streamlit UI 구성 ---

st.title("✨ 별자리 운세")

birth_input = st.text_input(
    label="생년월일을 입력하세요 (월-일 형식)",
    placeholder="예시) 08-14"
)

if st.button("오늘의 운세 확인하기"):
    if birth_input:
        try:
            month, day = map(int, birth_input.split('-'))
            zodiac_sign = get_zodiac_sign(month, day)
            
            if zodiac_sign:
                st.success(f"당신의 별자리는 **'{zodiac_sign}'** 입니다.")
                with st.spinner(f"'{zodiac_sign}'의 오늘의 운세를 가져오는 중..."):
                    horoscope = get_todays_horoscope(zodiac_sign)
                    st.markdown("---")
                    st.subheader(f"오늘의 {zodiac_sign} 운세")
                    st.info(horoscope)
            else:
                st.error("유효하지 않은 날짜입니다. 다시 입력해주세요.")
        except ValueError:
            st.error("입력 형식이 잘못되었습니다. '월-일' 형식으로 입력해주세요. (예: 08-14)")
    else:
        st.warning("생년월일을 입력해주세요.")
        