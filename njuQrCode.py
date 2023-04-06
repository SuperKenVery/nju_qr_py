import requests,json

def getQrContent(login_cookie):
    '''
    login_cookie: The cookie "CASTGC" when logging in at authserver.nju.edu.cn
    example: login_cookie="CASTGC=ekdgjwvwlr;"
    '''
    if login_cookie[:7]!='CASTGC=':
        login_cookie='CASTGC='+login_cookie
    ua="Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (5511528960)cpdaily/9.0.14  wisedu/9.0.14"
    session_response_1=requests.get(
        url="https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fqrcode.nju.edu.cn%3A443%2Fapi%2Fh5",
        headers={
            'cookie':login_cookie,
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4504969728)cpdaily/9.0.14  wisedu/9.0.14'
        },
        allow_redirects=False
    )
    session_redirect_1=session_response_1.headers['Location']

    session_response_2=requests.get(url=session_redirect_1,headers={'user-agent':ua},allow_redirects=False)
    session_redirect_2=session_response_2.headers['Location']

    session_response_3=requests.get(url=session_redirect_2,headers={'user-agent':ua},cookies=session_response_2.cookies,allow_redirects=False)
    session_cookie=session_response_3.cookies

    ticket_response=requests.post(
        url="https://qrcode.nju.edu.cn/api/check",
        cookies=session_cookie,
        data=""
    )
    ticket=ticket_response.text

    bearer_token_response=requests.post(
        url="https://qrcode.nju.edu.cn/code/v1/qrexchange",
        headers={
            'ticket':ticket
        },
        data=""
    )
    bearer_token_json=bearer_token_response.text
    bearer_token=json.loads(bearer_token_json)['jwt']

    qr_content_response=requests.post(
        url="https://qrcode.nju.edu.cn/code/v1/qrcode",
        headers={
            'authorization':bearer_token
        },
        data=""
    )
    qr_content_json=qr_content_response.text
    qr_content=json.loads(qr_content_json)['qrcode']

    return qr_content

if __name__=='__main__':
    # print(getQrContent("CASTGC=TGT-196633-FhxLaCBjUsdfsdscvxwwlv4eeggreregUqbpnbhpYkBELrralM91660144576435-wMv1-cas;"))
    print(getQrContent("Put your cookie here to test"))
