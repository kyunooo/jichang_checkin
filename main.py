import requests, json, re, os
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）

config = os.environ.get('CONFIG')
# server酱
SCKEY = os.environ.get('SCKEY')

login_url = '{}/auth/login'.format(url)
check_url = '{}/user/checkin'.format(url)

def sign(order,user,pwd):
        session = requests.session()
        global url,SCKEY
        common_header = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': url,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest',
        }
        login_header = {
        **common_header,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': f'{url}/auth/login',
        }
        checkin_header = {
        **common_header,
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': f'{url}/user/panel',
        }
        data = {
        'email': user,
        'passwd': pwd
        }
        page_header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        }
        try:
                print(f'===账号{order}进行登录...===')
                print(f'账号：{user}')
                # 先访问登录页面，获取初始Cookie
                session.get(url=login_url, headers=page_header)
                res = session.post(url=login_url,headers=login_header,data=data).text
                print(res)
                response = json.loads(res)
                print(response['msg'])
                # 登录后访问用户面板页，模拟浏览器跳转
                panel_url = f'{url}/user/panel'
                panel_header = {**page_header, 'referer': login_url, 'sec-fetch-site': 'same-origin'}
                session.get(url=panel_url, headers=panel_header)
                # 进行签到
                res2 = session.post(url=check_url,headers=checkin_header).text
                print(res2)
                result = json.loads(res2)
                print(result['msg'])
                content = result['msg']
                # 进行推送
                if SCKEY != '':
                        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
                        requests.post(url=push_url)
                        print('推送成功')
        except Exception as ex:
                content = '签到失败'
                print(content)
                print("出现如下异常%s"%ex)
                if SCKEY != '':
                        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
                        requests.post(url=push_url)
                        print('推送成功')
        print('===账号{order}签到结束===\n'.format(order=order))
if __name__ == '__main__':
        configs = config.splitlines()
        if len(configs) %2 != 0 or len(configs) == 0:
                print('配置文件格式错误')
                exit()
        user_quantity = len(configs)
        user_quantity = user_quantity // 2
        for i in range(user_quantity):
                user = configs[i*2]
                pwd = configs[i*2+1]
                sign(i,user,pwd)
        
