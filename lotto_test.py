# 패키지 불러오기
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import telegram
import time
from datetime import datetime
import sign_info
import asyncio


chrome_options = Options()
# ChromeDriver 경로 설정
# driver_path = r"C:\dev\lotto\chromedriver-win64\chromedriver.exe"

# 동행복권 사이트 접속
url = 'https://www.dhlottery.co.kr/user.do?method=login&returnUrl='
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(driver_path)
driver.get(url)
driver.maximize_window()
time.sleep(1)

# 로그인
driver.find_element(By.XPATH, value = '//*[@id="userId"]').send_keys(sign_info.id)
time.sleep(1)
driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/input[2]').send_keys(sign_info.pw)
time.sleep(1)
driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/a').click()
time.sleep(1)

# 텔레그램 정보
telegram_TOKEN = sign_info.tel_token
telegram_chat_id = sign_info.telegram_chat_id
bot = telegram.Bot(telegram_TOKEN)

# 마이페이지 접속
driver.get('https://www.dhlottery.co.kr/userSsl.do?method=myPage')
time.sleep(1)

# 잔액 확인
deposit = driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/div[1]/div[2]/p[1]/strong').text
deposit = deposit.replace(',', '')

# 최근 구매 바코드 수집후 공백 제거
blank_num = driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]').text
num = blank_num.replace(" ", "")

async def send_message_and_photo():
    # 최근 구매 바코드 스크린샷 저장 후 텔레그램 전송
    driver.get('https://dhlottery.co.kr/myPage.do?method=lotto645Detail&orderNo=2023070900359696140&barcode='+num+'&issueNo=1')
    el = driver.find_element(By.XPATH, '//*[@id="popup645paper"]')
    el.screenshot('./lotto.png')

    await bot.send_message(telegram_chat_id, '이번주 추첨결과')
    await bot.send_photo(telegram_chat_id, open('./lotto.png', 'rb'))

# 이벤트 루프를 생성하고, 비동기 함수를 실행합니다.
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message_and_photo())

# 로또 구매하기

# 로또 구매하기

if int(deposit) <= 5000 :  #예치금이 5000원 보다 작을시
    bot.sendMessage(telegram_chat_id, f'잔고 : {deposit}원'+ "\n 충전이 필요합니다" + "\n https://dhlottery.co.kr/payment.do?method=payment")       #예치금 텔레그램 보내기

else :
    
    # 로또 구매 페이지 이동
    driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')
    time.sleep(1)

    # 프레임 변경
    iframe = driver.find_element(By.XPATH, value = '//*[@id="ifrm_tab"]')
    driver.switch_to.frame(iframe)

    # 첫번째 수동번호
    nums1 = (7, 15, 23, 24, 35, 41)
    for n in nums1:
        driver.find_element(By.XPATH, f'//label[@for="check645num{str(n)}"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # 두번째 수동번호
    nums2 = (8, 14, 15, 22, 33, 45)
    for n in nums2:
        driver.find_element(By.XPATH, f'//label[@for="check645num{str(n)}"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # 세번째 수동번호
    nums3 = (13, 16, 23, 34, 38, 44)
    for n in nums3:
        driver.find_element(By.XPATH, f'//label[@for="check645num{str(n)}"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # 네번째 반자동 (7)
    driver.find_element(By.XPATH, value = '//label[@for="check645num7"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="checkNumGroup"]/div[1]/label/span').click()
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # 다섯번째 반자동 (18)
    driver.find_element(By.XPATH, value = '//label[@for="check645num18"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="checkNumGroup"]/div[1]/label/span').click()
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # # 자동선택
    # driver.find_element(By.XPATH, value = '//*[@id="checkNumGroup"]/div[1]/label/span').click()
    # # 수량선택
    # driver.find_element(By.XPATH, value = '//*[@id="amoundApply"]/option[2]').click()
    # # 확인
    # driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()

    # 구매확정
    driver.find_element(By.XPATH, value = '//*[@id="btnBuy"]').click()
    driver.find_element(By.XPATH, value = '//*[@id="popupLayerConfirm"]/div/div[2]/input[1]').click()
    time.sleep(2)

    # 구매내역 스크린샷 저장 후 텔레그램 전송
    el = driver.find_element(By.XPATH, '//*[@id="popReceipt"]')
    el.screenshot('./lotto1.png')

    # iframe에서 기본 창으로 다시 변경
    driver.switch_to.default_content()

    # 마이페이지 접속
    driver.get('https://www.dhlottery.co.kr/userSsl.do?method=myPage')
    time.sleep(2)

    # 구매 후 잔액
    deposit2 = driver.find_element(By.XPATH, value = '/html/body/div[1]/header/div[2]/div[2]/form/div/ul[1]/li[2]/a[1]/strong').text

    # 날짜 텔레그램 전송
    dt = datetime.today().strftime('%Y-%m-%d')

    bot.send_message(telegram_chat_id, dt + '구매내역')
    bot.send_photo(telegram_chat_id, open('./lotto1.png', 'rb'))
    bot.send_message(telegram_chat_id, '남은 잔액 : ' + deposit2)


# 접속 종료
driver.quit()

    # # 자동선택
    # driver.find_element(By.XPATH, value = '//*[@id="checkNumGroup"]/div[1]/label/span').click()
    # # 수량선택
    # driver.find_element(By.XPATH, value = '//*[@id="amoundApply"]/option[2]').click()
    # # 확인
    # driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click()