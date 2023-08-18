import os, json, time, random, string, logging, threading, ctypes, sys, concurrent.futures

try:
    import tls_client
    import colorama
    import pystyle
    import httpx
    import datetime
    import account_generator_helper
    import requests
    import uuid
except ModuleNotFoundError:
    os.system("pip install tls_client")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install httpx")
    os.system("pip install datetime")
    os.system("pip install account_generator_helper")
    os.system("pip install requests")
    os.system("pip install uuid")

from colorama import Fore, Style, init
from tls_client import Session
from datetime import datetime
from pystyle import Write, System, Colors, Colorate
from account_generator_helper import GmailNator
from uuid import uuid4
from json import dumps

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

generated = 0
failed = 0
total = 0
joined = 0

config = json.loads(open('config.json', 'r').read())
proxies = open('proxies.txt', "r", encoding="utf-8").read().splitlines()
output_lock = threading.Lock()
init()

def get_time_rn():
    date = datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def proxy_scraper():
    if config["auto_proxy_scraper"] == "y":
        with open(f"proxies.txt", "w", encoding='utf-8') as f:
            f.write("")
        def save_proxies(proxies):
            with open("proxies.txt", "w") as file:
                file.write("\n".join(proxies))

        def get_proxies():
            with open('proxies.txt', 'r', encoding='utf-8') as f:
                proxies = f.read().splitlines()
            if not proxies:
                proxy_log = {}
            else:
                proxy = random.choice(proxies)
                proxy_log = {
                    "http://": f"http://{proxy}", "https://": f"http://{proxy}"
                }
            try:
                url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
                response = httpx.get(url, proxies=proxy_log, timeout=60)

                if response.status_code == 200:
                    proxies = response.text.splitlines()
                    save_proxies(proxies)
                else:
                    time.sleep(1)
                    get_proxies()
            except httpx.ProxyError:
                get_proxies()
            except httpx.ReadError:
                get_proxies()
            except httpx.ConnectTimeout:
                get_proxies()
            except httpx.ReadTimeout:
                get_proxies()
            except httpx.ConnectError:
                get_proxies()
            except httpx.ProtocolError:
                get_proxies()

        def check_proxies_file():
            file_path = "proxies.txt"
            if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                get_proxies()

        check_proxies_file()
    else:
        pass

proxy_scraper()

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Guilded Account Generator 』 ~ By H4cK3dR4Du#1337 | .gg/radutool')
time.sleep(1.5)

def update_title():
    global generated, failed, total, joined
    current_time = time.time()
    elapsed_time = current_time - start_time
    accounts_per_minute = generated / (elapsed_time / 60)
    accounts_per_hour = generated / (elapsed_time / 3600)
    accounts_per_day = generated / (elapsed_time / 86400)
    elapsed_days = int(elapsed_time // 86400)
    elapsed_hours = int((elapsed_time % 86400) // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_seconds = int(elapsed_time % 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Guilded Account Generator 』 ~ By H4cK3dR4Du#1337 | Joined : {joined} | Created : {generated} @ Elapsed: {elapsed_days}d {elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s % Speed : {int(accounts_per_minute)}/m | .gg/radutool')

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def guilded_generator():
    global generated, failed, total, joined
    def format_cookies(items: dict):
        cookies_text = str()
        for cookie in items: cookies_text += f'{cookie[0]}={cookie[1]}; '
        return cookies_text[:len(cookies_text)-2]
    proxies = []
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        for line in f:
            proxies.append(line.strip())

    session = Session(
        client_identifier='chrome_113'
    )

    random_proxy = random.choice(proxies)
    proxy_parts = random_proxy.split(':')

    if len(proxy_parts) >= 4:
        ip, port, username, password = proxy_parts[:4]
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
    else:
        ip, port = proxy_parts[:2]
        proxy_url = f"http://{ip}:{port}"

    proxy = proxy_url
    session.proxies = {
        "http": proxy,
        "https": proxy
    }
    
    url = 'https://www.guilded.gg/api/me?isLogin=false&v2=true'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "DNT": "1",
        "Guilded-Client-ID": str(uuid4()),
        "Guilded-Viewer-Platform": "desktop",
        "Referer": "https://www.guilded.gg/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = session.get(url=url, headers=headers)
    formatted_cookies = format_cookies(r.cookies.items()),r.cookies.get('guilded_mid')
    str_cookies = formatted_cookies[0]
    client_id = formatted_cookies[1]
    password = "".join(random.choices(string.ascii_letters+string.digits,k=12))
    email = "".join(random.choices(string.ascii_letters+string.digits,k=20)) + "@gmail.com"
    url = "https://raw.githubusercontent.com/TahaGorme/100k-usernames/main/usernames.txt"
    response = requests.get(url)
    names = response.text.splitlines()
    username = random.choice(names)

    payload = {
        "extraInfo": {
            "platform": "desktop"
        },
        "name": username,
        "email": email,
        "password": password,
        "fullName": username
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "Content-Length": str(len(json.dumps(payload))),
        "Content-Type": "application/json",
        "Cookie": str_cookies,
        "Guilded-Client-ID": client_id,
        "Guilded-Stag": "".join(random.choices('0123456789abcdef', k=32)),
        "Guilded-Viewer-Platform": "desktop",
        "Origin": "https://www.guilded.gg",
        "Referer": "https://www.guilded.gg/",
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    while True:
        try:
            r = session.post(f'https://www.guilded.gg/api/users?type=email', headers=headers, json=payload)
            break
        except:
            continue
    
    headers["cookie"] = str_cookies + "; " + format_cookies(r.cookies.items())
    token = r.cookies.get('hmac_signed_session')

    if r.status_code == 200:
        with output_lock:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Created Account {gray}| ", end='')
            sys.stdout.flush()
            Write.Print(email + f":" + password + f"\n", Colors.red_to_blue, interval=0.000)
            generated += 1
            total += 1
            update_title()
            headers['content-length'] = "19"
            invite_code = config['invite']
            r2 = session.put(url=f'https://www.guilded.gg/api/invites/{invite_code}', data=json.dumps({
                "type":"consume"
            }))
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({magenta}~{gray}) {pretty}Joined Server {gray}| ", end='')
            sys.stdout.flush()
            Write.Print(token[:60] + "******\n", Colors.red_to_blue, interval=0.000)
            joined += 1
            update_title()
            url1 = "https://raw.githubusercontent.com/squeazzyy/Discord-Scraped-Usernames-Bios-Avatars-Realistic/main/bio.txt"
            response1 = requests.get(url1)
            bios = response1.text.splitlines()
            bio = random.choice(bios)
            tagline = [".gg/radutool | Best Tools", "github.com/H4cK3dR4Du"]
            id = r.json()['user']['id']
            payload = {
                "userId": id,
                "aboutInfo": {
                    "bio": bio,
                    "tagLine": tagline
                }
            }
            headers["content-length"] = str(len(json.dumps(payload)))
            session.put(f'https://www.guilded.gg/api/users/{id}/profilev2', data=json.dumps(payload))
            pfps_list = ["https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/6e30a4fc068204762c300b1311a3cbea-Large.png?w=450&h=450", "https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/800a0c61ae30d972ef2a99be9447d298-Large.png?w=450&h=450", "https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/e31f7c5699cb49678c0c812ce225cbaa-Large.png?w=450&h=450", "https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/dd843aeb5150f46c984d2cf386e6c659-Large.png?w=450&h=450", "https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/c40262696603d83f6f010314db51847d-Large.png?w=450&h=450", "https://s3-us-west-2.amazonaws.com/www.guilded.gg/UserAvatar/de30a4417e710011c9baae4f96eb7040-Large.png?w=450&h=450"]
            headers["content-length"] = str(len(json.dumps({
                "imageUrl": random.choice(pfps_list)
            })))
            session.post(f'https://www.guilded.gg/api/users/me/profile/images', data=json.dumps({
                "imageUrl": random.choice(pfps_list)
            }))
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pretty}Humanized [Bio, Tagline, PFP] {gray}| ", end='')
            sys.stdout.flush()
            Write.Print(token[:60] + "******\n", Colors.red_to_blue, interval=0.000)
            open('accounts.txt', 'a').write(f'Email : {email} | Password : {password} | Token : {token}\n')
    else:
        pass

def generate():
    while True:
        try:
            guilded_generator()
        except Exception as e:
            generate()

def check_titles():
    while True:
        update_title()

if __name__ == "__main__":
    os.system("cls")
    Write.Print(f"""
\t\t  /$$$$$$            /$$ /$$       /$$                 /$$                        
\t\t /$$__  $$          |__/| $$      | $$                | $$                        
\t\t| $$  \__/ /$$   /$$ /$$| $$  /$$$$$$$  /$$$$$$   /$$$$$$$      /$$$$$$   /$$$$$$ 
\t\t| $$ /$$$$| $$  | $$| $$| $$ /$$__  $$ /$$__  $$ /$$__  $$     /$$__  $$ /$$__  $$
\t\t| $$|_  $$| $$  | $$| $$| $$| $$  | $$| $$$$$$$$| $$  | $$    | $$  \ $$| $$  \ $$
\t\t| $$  \ $$| $$  | $$| $$| $$| $$  | $$| $$_____/| $$  | $$    | $$  | $$| $$  | $$
\t\t|  $$$$$$/|  $$$$$$/| $$| $$|  $$$$$$$|  $$$$$$$|  $$$$$$$ /$$|  $$$$$$$|  $$$$$$$
\t\t \______/  \______/ |__/|__/ \_______/ \_______/ \_______/|__/ \____  $$ \____  $$
\t\t                                                               /$$  \ $$ /$$  \ $$
\t\t                                                              |  $$$$$$/|  $$$$$$/
\t\t                                                               \______/  \______/ 

                            \t\t( ~ discord.gg/radutool ~ )   
\n\n""", Colors.yellow_to_red, interval=0.000)
    for i in range(int(config['threads'])):
        threading.Thread(target=generate).start()
    threading.Thread(target=check_titles).start()