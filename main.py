import tls_client, json, random, string, threading, yaml
from modules.utilities import get_useragent, build_xsp, get_version, get_username
from modules.hcaptcha import solve_captcha
# MADE BY PR0T0N DON'T SKID LMAO (IF YOU SKID AT LEAST STAR THE REPO)
# PLEASE STAR THE REPO
# to lazy to make super property builder that's why I didn't use randomuseragent lib

class Boost:
    def __init__(self, proxy: str, serverinvite: str, sitekey: str='4c672d35-0701-42b2-88c3-78380b0db560'):
        self.serverinvite = serverinvite
        self.site_key = sitekey
        self.proxy = proxy
        self.ua = get_useragent()
        self.super_properties = build_xsp()
        self.fingerprint_url = 'https://discord.com/api/v9/experiments'
        self.register_url = 'https://discord.com/api/v9/auth/register'
        
    def fetch_cookies(self, session):
        try:
            url = 'https://discord.com/'
            headers = {'user-agent':self.ua}
            response = session.get(url, headers=headers, proxy=self.proxy)
            cookies = response.cookies.get_dict()
            cfruid = cookies.get("__cfruid")
            dcfduid = cookies.get("__dcfduid")
            sdcfduid = cookies.get("__sdcfduid")
            return cfruid, dcfduid, sdcfduid
        except: 
            print(response.text)
            return self.main()
    def get_fingerprint(self, session):
        try: 
            fingerprint = session.get(self.fingerprint_url, proxy=self.proxy).json()['fingerprint']
            print(f"[=]: Fetched Fingerprint ({fingerprint[:15]}...)") 
            return fingerprint
        except Exception as err: 
            print(err)
            return self.main()

    def register(self, session, fingerprint, cfruid, dcfduid, sdcfduid):
        captchakey = solve_captcha(get_useragent())
        payload = {
            "fingerprint": fingerprint,
            "username": get_username(),
            "invite": self.serverinvite,
            "consent": True,
            "captcha_key": captchakey
         }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            # Gonna add __cf_bm retriever soon
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
            v,_ = get_version(get_useragent())
            session = tls_client.Session(client_identifier=f'chrome_{v}') # For updated identifier version
            cfruid, dcfduid, sdcfduid = self.fetch_cookies(session)
            fingerprint = self.get_fingerprint(session)
            self.register(session, fingerprint, cfruid, dcfduid, sdcfduid)
            return self.main()
        except: 
            return self.main()
if __name__ == "__main__":
    print("[~]: Loading config...")
    config = yaml.safe_load(open("config.yml"))["settings"]
    invite_code = config['invite_code']
    proxy = config['rotating_proxy']
    amount_of_threads = config['threads']
    if not "http://" in proxy:
        proxy = "http://"+proxy
    print("[+]: Config loaded")
    for i in range(int(amount_of_threads)):
        threading.Thread(target=Boost(proxy,invite_code).main).start()
        print(f"[+]: Started a thread ({i+1}/{amount_of_threads})")
    
