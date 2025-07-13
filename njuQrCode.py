import requests,json

def getQrContent(login_cookie: str) -> str:
    '''
    login_cookie: The cookie "CASTGC" when logging in at authserver.nju.edu.cn
    example: login_cookie="CASTGC=ekdgjwvwlr;"

    Returns the base64 of qrcode (qrcode is an image 😅)
    '''

    if login_cookie.startswith("CASTGC="):
        login_cookie = login_cookie[7:]

    session = requests.Session()
    # session.verify = False
    session.cookies.update({"CASTGC": login_cookie})
    session.headers.update({"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4504969728)cpdaily/9.0.14  wisedu/9.0.14"})

    # Get some cookies
    # qrcode -> authserver -> qrcode
    session.get("https://qrcode.nju.edu.cn")

    ticket = session.post("https://qrcode.nju.edu.cn/api/check").text
    session.headers.update({"Ticket": ticket})

    qr_exchange_resp = session.post("https://qrcode.nju.edu.cn/code/v1/qrexchange")
    qr_exchange = qr_exchange_resp.json()
    session.headers.update({"Authorization": qr_exchange['jwt']})

    qr_data_resp = session.post(
        "https://qrcode.nju.edu.cn/code/v1/qrcode?t=1752405961085",
        json={"stuempno": None}
    )
    qr_code_data = qr_data_resp.json()['qrcode']

    return qr_code_data



if __name__=='__main__':
    # print(getQrContent("CASTGC=TGT-196633-FhxLaCBjUsdfsdscvxwwlv4eeggreregUqbpnbhpYkBELrralM91660144576435-wMv1-cas;"))
    print(getQrContent("Put your cookie here to test"))
