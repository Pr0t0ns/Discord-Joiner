import requests, yaml
config = yaml.safe_load(open("config.yml"))
def solve_captcha(user_agent: str): # Used this to support multiple captcha services
    sitekey = "4c672d35-0701-42b2-88c3-78380b0db560"
    service = config["captcha"]["solver-service"]
    json = {
		"clientKey": "4025591aca331aabf97052f0bd0dd5b6",
		"task": {
			"type":       "HCaptchaTaskProxyless",
			"userAgent":  user_agent,
			"websiteKey": sitekey,
			"websiteURL": "https://discord.com/",
		},
	}
    
    task_id = requests.post(f"https://api.{service}/createTask",json=json).json()["taskId"]
    while True:
        r = requests.get(f"https://api.{service}/getTaskResult",json={
            "clientKey":config["captcha"]["solver-key"],"taskId":task_id
        })
        if "processing" in r.text:
            pass
        else:
            try:
                print(f'[\]: Solved Captcha ({r.json()["solution"]["gRecaptchaResponse"][:30]}...)')
                return r.json()["solution"]["gRecaptchaResponse"]
            except Exception:
                print("[-]: Failed to get task result")
                return 