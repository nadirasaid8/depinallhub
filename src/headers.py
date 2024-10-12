from src.agent import generate_random_user_agent

def headers():
    return {
        'Content-Type': 'application/json',
        'sec-ch-ua': 'Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': 'Android',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'origin': 'https://app.depinalliance.xyz',
        'referrer': 'https://app.depinalliance.xyz',
        'user-agent:': generate_random_user_agent()
    }