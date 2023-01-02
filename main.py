import tls_client, json, random, string, threading
from capmonster_python import HCaptchaTask
# MADE BY PR0T0N DON'T SKID LMAO (IF YOU SKID AT LEAST STAR THE REPO)
# PLEASE STAR THE REPO
# to lazy to make super property builder that's why I didn't use randomuseragent lib

class Boost:
    def __init__(self, proxy: str, serverinvite: str, capmonsterkey: str=None, sitekey: str='4c672d35-0701-42b2-88c3-78380b0db560'):
        self.serverinvite = serverinvite
        self.site_key = sitekey
        self.apikey = capmonsterkey
        self.proxy = proxy
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' # 2 lazy for random UAs
        self.super_properties = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE2NTQ4NSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        self.fingerprint_url = 'https://discord.com/api/v9/experiments'
        self.register_url = 'https://discord.com/api/v9/auth/register'
    @staticmethod
    def parse_proxy(proxy: str):
        username = proxy.split("//")[1].split(":")[0]
        password = proxy.split("@")[0].split(":")[2]
        proxy_host = proxy.split("@")[1].split(":")[0]
        proxy_port = proxy.split("@")[1].split(":")[1]
        return username, password, proxy_host, proxy_port

    def solve_captcha(self):
        try:
            print("[/]: Solving Captcha")
       #     user, passw, host, port = Boost.parse_proxy(self.proxy)
            capmonster = HCaptchaTask(self.apikey)
        #    capmonster.set_proxy('http', host, port, user, passw)
       #     capmonster.set_user_agent(self.ua)
            task_id = capmonster.create_task("http://discord.com", "4c672d35-0701-42b2-88c3-78380b0db560")
            result = capmonster.join_task_result(task_id)
            key = result.get("gRecaptchaResponse")
            print(f"[\]: Solved Captcha ({key[:30]}...)")
            return key
        except: return self.main()

    def fetch_cookies(self, session):
        try:
            
            url = 'https://discord.com/'
            headers = {'user-agent': self.ua}
            response = session.get(url, headers=headers, proxy=self.proxy)
            cookies = response.cookies.get_dict()
            cfruid = cookies.get("__cfruid")
            dcfduid = cookies.get("__dcfduid")
            sdcfduid = cookies.get("__sdcfduid")
            return cfruid, dcfduid, sdcfduid
        except: return self.main()
    def get_fingerprint(self, session):
        try: fingerprint = session.get(self.fingerprint_url, proxy=self.proxy).json()['fingerprint']; print(f"[=]: Fetched Fingerprint ({fingerprint[:15]}...)"); return fingerprint
        except Exception as err: print(err); return self.main()

    def random_chars(self, length: int, extra: str=None):
        return ''.join(random.choice(string.ascii_letters) for pr0t0n in range(length)) + extra if extra != None else ""


    def register(self, session, fingerprint, cfruid, dcfduid, sdcfduid):
        username = self.random_chars(random.randint(8, 12), extra=random.choice(string.ascii_lowercase))
        password = self.random_chars(random.randint(8, 10), extra="AfS!")
        email = self.random_chars(random.randint(6, 12), extra=random.choice(['@gmail.com', '@yahoo.com', '@outlook.com']))
        captchakey = self.solve_captcha()
        payload = {"fingerprint": fingerprint,"email": email,"username": username,"password": password,"invite": self.serverinvite,"consent": True,"date_of_birth":"1991-04-03","gift_code_sku_id": None,"captcha_key": captchakey}
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cookie": f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; __cfruid={cfruid}; __cf_bm=DFyh.5fqTsl1JGyPo1ZFMdVTupwgqC18groNZfskp4Y-1672630835-0-Aci0Zz919JihARnJlA6o9q4m5rYoulDy/8BGsdwEUE843qD8gAm4OJsbBD5KKKLTRHhpV0QZybU0MrBBtEx369QIGGjwAEOHg0cLguk2EBkWM0YSTOqE63UXBiP0xqHGmRQ5uJ7hs8TO1Ylj2QlGscA=",
            "origin": "https://discord.com",
            "referer": "https://discord.com/register",
            "user-agent": self.ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-fingerprint": fingerprint,
            "x-super-properties": self.super_properties
        }
        try:
            response = session.post(self.register_url, headers=headers, json=payload, proxy=self.proxy)
        except: return self.main()
        if int(response.status_code) == 201:
            print(f'[+]: Created Account and Joined Server (discord.gg/{self.serverinvite})')
            token = response.json()['token']
            with open('tokens.txt', 'a+') as f: f.write(f'{token}\n')
            return self.main()
        else:
            print("[-]: Error Creating Account")
            return self.main()

    def main(self):
        try:
            session = tls_client.Session(client_identifier='chrome_106')
            cfruid, dcfduid, sdcfduid = self.fetch_cookies(session)
            fingerprint = self.get_fingerprint(session)
            self.register(session, fingerprint, cfruid, dcfduid, sdcfduid)
            return self.main()
        except: return self.main()
if __name__ == "__main__":
    with open('config.json') as conf:
        content = json.load(conf)
        capmonster_api_key = content['capmonster_api_key']
        invite_code = content['invite_code']
        proxy = content['rotating_proxy']
        amount_of_threads = content['threads']
        del content
    Boost = Boost(
        proxy=proxy,
        serverinvite=invite_code,
        capmonsterkey=capmonster_api_key
    )
    for i in range(int(amount_of_threads)):
        threading.Thread(target=Boost.main).start()
    
