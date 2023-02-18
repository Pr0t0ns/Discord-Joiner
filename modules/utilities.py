import requests,re,base64,json,yaml

def get_useragent(): # Experimental
    r = requests.get("https://jnrbsn.github.io/user-agents/user-agents.json")
    return r.json()[0]

def get_version(user_agent): # Just splits user agent
    chrome_version = user_agent.split("/")[3].split(".")[0]
    full_chrome_version = user_agent.split("/")[3].split(" ")[0]
    return chrome_version, full_chrome_version

def get_buildnumber(): # Todo: make it permanently work
    r = requests.get('https://discord.com/app', headers={'User-Agent': 'Mozilla/5.0'})
    asset = re.findall(r'([a-zA-z0-9]+)\.js', r.text)[-2]
    assetFileRequest = requests.get(f'https://discord.com/assets/{asset}.js', headers={'User-Agent': 'Mozilla/5.0'}).text
    try:
        build_info_regex = re.compile('buildNumber:"[0-9]+"')
        build_info_strings = build_info_regex.findall(assetFileRequest)[0].replace(' ', '').split(',')
    except:
        print("[-]: Failed to get build number")
        pass
    dbm = build_info_strings[0].split(':')[-1]
    return int(dbm.replace('"', ""))

def build_xsp():
    ua = get_useragent()
    _,fv = get_version(ua)
    data = json.dumps({
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": ua,
        "browser_version": fv,
        "os_version": "10",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": get_buildnumber(),
        "client_event_source": None
    }, separators=(",",":"))
    return base64.b64encode(data.encode()).decode()

def get_username():
    config = yaml.safe_load(open("config.yml"))["token"]
    c_username = config["username"] # Stands for "custom username"
    if len(c_username) == 0: 
        username = requests.get("https://story-shack-cdn-v2.glitch.me/generators/username-generator").json()["data"]["name"]
    else:
        if len(c_username) >= 2:
            username = c_username
        else:
            print("Custom username must be atleast 2 characters long.")
    return username