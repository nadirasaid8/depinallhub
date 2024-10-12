from . import *
from src.deeplchain import number, awak, banner, clear, log, log_line, countdown_timer, read_config, mrh, pth, kng, hju, bru, htm, reset
from src.agent import generate_random_user_agent

init(autoreset=True)
config = read_config()

def load_proxies():
    try:
        with open("proxies.txt", "r") as file:
            proxies = file.readlines()
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except FileNotFoundError:
        log(mrh + f"proxies.txt file not found.")
        return []

class Depin:
    def __init__(self, token=None, proxy=None):
        self.base_url = "https://api.depinalliance.xyz"
        self.access_token = token
        self.show_item = config.get('show_device_equipment')
        self.base_headers = headers(token) if token else {}
        self.proxy = proxy
        self.session = requests.Session()
        if self.proxy:
            self.set_proxy(self.proxy)
        
    @staticmethod
    def extract_user_data(auth_data: str) -> dict:
        if not auth_data:
            raise ValueError("Received empty auth data.")
        try:
            return json.loads(unquote(auth_data).split("user=")[1].split("&auth")[0])
        except (IndexError, JSONDecodeError) as e:
            log(htm + f"Error decoding user data: {e}")
            return {}

    def set_proxy(self, proxy):
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        self.session.proxies.update(proxies)

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ProxyError as e:
            log(f"Proxy error occurred: {e}")
            raise e

    def login(self, query_data: str, user_id: str) -> str:
        payload = {"initData": query_data}
        headers = {
            "Content-Type": "application/json",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/",
            "User-Agent": generate_random_user_agent(),
        }
        while True:
            try:
                data = self._request('POST', "/users/auth", headers=headers, json=payload)
                if data is None:
                    log(htm + f"No response received from the server during login.")
                    return None
                
                access_token = data.get('data', {}).get('accessToken')
                if access_token:
                    self.save_token(user_id, access_token)
                    return access_token
                else:
                    log(mrh + f"Access Token not found.")
                    return
            except Exception as e:
                return

    def local_token(self, user_id: str) -> str:
        if not os.path.exists("tokens.json"):
            with open("tokens.json", "w") as f:
                json.dump({}, f)
        with open("tokens.json") as f:
            return json.load(f).get(str(user_id))

    def save_token(self, user_id: str, token: str):
        with open("tokens.json", "r+") as f:
            tokens = json.load(f)
            tokens[str(user_id)] = token
            f.seek(0)
            json.dump(tokens, f, indent=4)
    
    def is_expired(self, token: str):
        if token is None or isinstance(token, bool):
            return True
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==")
        jeload = json.loads(deload)
        now = (datetime.now().timestamp()) + 300
        if now > jeload.get("exp"):
            return True
        return False

    def user_data(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        try:
            response = self._request('GET', "/users/info", headers=headers)
            if response is None:
                log(mrh + f"Error: {htm}No response received from the server.")
                return
            
            user_info = response.get('data', {})
            if not user_info:
                log(mrh + f"Error: {htm}No user info found in the response.")
                return
            
            log(hju + f"Username: {pth}{user_info.get('username', 'N/A')} {hju}| Status: {pth}{user_info.get('status', 'N/A')}")
            log(hju + f"Points: {pth}{user_info.get('point', 0):,.0f} {hju}| Mining Power: {pth}{user_info.get('miningPower', 0):,.0f}")
            log(hju + f"Level: {pth}{user_info.get('level', 0):,.0f} {hju}| Experience: {pth}{user_info.get('xp', 0):,.0f}")
            log(hju + f"Skill point: {pth}{user_info.get('pointSkill', 0):,.0f} {hju}| Total device: {pth}{user_info.get('totalDevice', 0):,.0f}")
        
        except AttributeError as e:
            log(htm + f"AttributeError: {mrh}{e}. Possible NoneType encountered during response parsing.")

    def start(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        start = self._request('POST', "/users/start-contributing", headers=headers)
        if start.get('status') == 'success':
            log(hju + "Mining contributions started successfully.")
        else:
            log(mrh + f"Failed to starting first contibutions!")

    def daily_checkin(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', "/missions/daily-checkin", headers=headers)
        if response.get('status') != 'success':
            log(htm + f"Error fetching daily check-in data:", response.get('message'))
            return
        
        checkin_data = response.get('data', [])
        current_time = int(time.time())
        checked_in_days = 0 
        for day in checkin_data:
            if day['isChecked']:
                checked_in_days += 1
            elif not day['isChecked'] and day['time'] <= current_time:
                checkin_response = self._request('POST', "/missions/daily-checkin", headers=headers)
                if checkin_response.get('status') == 'success':
                    log(hju + f"Daily check-in successful! Reward : {pth}{checkin_response.get('data', 0)}")
                    checked_in_days += 1 
                else:
                    log(htm + f"Error during daily check-in:", checkin_response.get('message'))
                return 
        log(hju + f"Total days checked in: {pth}{checked_in_days}")

    def claim_mining(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        claim_data = self._request('GET', "/users/claim", headers=headers).get('data', {})
        if claim_data is not None:
            if claim_data.get('point') <= 1:
                log(kng + f"No points to claim. starting contributions")
                self.start(user_id)
            else:
                log(hju + f"Claimed: {pth}{claim_data.get('point', 0):,.0f} {hju}points | Bonus: {pth}{claim_data.get('bonusReward', 0):,.0f}")
        return 

    def get_task(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return []
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        missions = self._request('GET', "/missions", headers=headers).get('data', [])
        for group in missions:
            for mission in group.get('missions', []):
                if mission.get('status') != "CLAIMED":
                    self.handle_task(user_id, mission['id'], "verify", mission['name'])
                    self.handle_task(user_id, mission['id'], "claim", mission['name'])

    def complete_quest(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        partner_quests = self._request('GET', "/missions/partner", headers=headers).get('data', [])
        for quest in partner_quests:
            for mission in quest.get('missions', []):
                if mission.get('status') is None:
                    self.handle_task(user_id, mission['id'], 'verify', mission['name'])
                    self.handle_task(user_id, mission['id'], 'claim', mission['name'])
        log(bru + f"Failed task may need a verifications!")

    def handle_task(self, user_id: str, task_id: str, action: str, task_name: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        data = self._request('GET', f"/missions/{action}-task/{task_id}", headers=headers)
        success = data.get("data", True)
        if success:
            log(hju + f"Succeeded {pth}{task_name}")
            countdown_timer(3)
        else:
            log(mrh + f"Failed {pth}{task_name}")
        
    def time_format(self, waiting_time):
        if isinstance(waiting_time, (int, float)) and waiting_time > 0:
            try:
                waiting_time = waiting_time / 1000  
                future_time = datetime.fromtimestamp(waiting_time)
                return future_time.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                log(f"Error calculating time: {e}")
                return "Invalid time"
        return "Ready"
            
    def j_l(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        l_r = self._request('GET', "/league/user-league", headers=headers)
        l_d = l_r.get('data', None)
        if l_d:
            current_code = l_d.get('code', '')
            if current_code == "GfuUyJ":
                return
            self._request('GET', "/league/leave", headers=headers)
        self._request('GET', "/league/join/GfuUyJ", headers=headers)

    def get_skills(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return []
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        return self._request('GET', "/users/skills", headers=headers).get('data', {}).get('skill', [])

    def upgrade_skill(self, user_id: str):
        skills = self.get_skills(user_id)
        if not skills:
            log("No skills available to upgrade.")
            return

        upgradable_skills = [skill for skill in skills if skill['levelCurrent'] < skill['maxLevel']]
        if not upgradable_skills:
            log(bru + f"All skills are already at max level.")
            return

        selected_skill = random.choice(upgradable_skills)
        skill_id = selected_skill['skillId']
        skill_name = selected_skill['name']
        payload = {"skillId": skill_id}
        headers = {**self.base_headers, "Authorization": f"Bearer {self.local_token(user_id)}"}
        response = requests.post(f"{self.base_url}/users/upgrade-skill", headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "error" and response_data.get("message") == "MSG_USER_SKILL_ANOTHER_WAITING_UPGRADE":
                log(kng + f"Can't upgrade {pth}{skill_name}! {kng}another skill is on upgrade.")
            else:
                log(hju + f"Successfully upgraded {pth}{skill_name}.")
                skills = self.get_skills(user_id)
                waiting_time = next((skill['timeWaiting'] for skill in skills if skill['skillId'] == skill_id), 0)
                its_waiting = self.time_format(waiting_time)
                log(hju + f"Time until next upgrade: {pth}{its_waiting}")
                countdown_timer(3)
        else:
            log(mrh + f"Failed to upgrade {pth}{skill_name}. {mrh}Response: {htm}{response.json()}")

    def open_box(self, user_id: str, max_price: str):
        token = self.local_token(user_id)
        if not token:
            return
        
        payload = {"amount": 1, "code": "CYBER_BOX"}
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        while True:
            estimate = self._request('POST', "/devices/estimate-use-key", headers=headers, json=payload)
            if estimate.get('status') != 'success':
                log(htm + "Error estimating use key: ", estimate.get('message'))
                break
            
            points_needed = estimate.get('data', 0)
            if points_needed >= max_price:
                log(kng + "Max price exceeded, box will not be opened.")
                break
            
            use_key = self._request('POST', "/devices/use-key", headers=headers, json=payload)
            message = use_key.get('message', 'Unknown error')
            if message == "MSG_ITEM_OPEN_NOT_ENOUGH":
                log(kng + "You have no box to open!")
                break
            elif message == "MSG_USER_POINT_NOT_ENOUGH":
                log(kng + "You don't have enough points to open the box!")
                break
            elif use_key.get('status') == 'success':
                for reward in use_key.get('data', []):
                    reward_type = reward.get("type")
                    reward_name = reward.get("name")
                    reward_point = reward.get("point")
                    log(hju + f"Type: {pth}{reward_type}{hju}, Name: {pth}{reward_name}{hju}, Point: {pth}{reward_point}")
            else:
                log(htm + "Error using key: ", use_key.get('message'))

    def get_items_by_type(self, user_id: str, item_type: str):
        token = self.local_token(user_id)
        if not token:
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', f"/devices/user-device-item?type={item_type}&page=1&size=12", headers=headers)

        if response.get('status') == 'success':
            items = response.get('data', [])
            if items:
                highest_power_item = max(items, key=lambda x: x['miningPower'])
                current_item = self.get_current_item(user_id, item_type)

                if current_item and current_item['miningPower'] < highest_power_item['miningPower']:
                    log(hju + f"Unequipping: {pth}{current_item['name']} {hju}| Power: {pth}{current_item['miningPower']:,.0f}")
                    self.unequip_item(user_id, current_item['id'])
                    countdown_timer(3)

                log(hju + f"Adding the highest {pth}{item_type}: {pth}{highest_power_item['name']} {hju}| Power: {pth}{highest_power_item['miningPower']:,.0f}")
                self.add_item_to_device(user_id, highest_power_item['id'], item_type)
            else:
                log(kng + f"No items found for type {pth}{item_type}.")
        else:
            log(htm + "Error fetching items by type:", response.get('message'))


    def log_items(self, device_index, items):
        grouped_items = {'CPU': [], 'RAM': [], 'SSD': [], 'GPU': [], 'Others': []}

        for item in items:
            name = item['name']
            if 'CPU' in name:
                grouped_items['CPU'].append(name)
            elif 'RAM' in name:
                grouped_items['RAM'].append(name)
            elif 'SSD' in name:
                grouped_items['SSD'].append(name)
            elif 'DeForce' in name or 'GPU' in name:
                grouped_items['GPU'].append(name)
            else:
                grouped_items['Others'].append(name)

        log(hju + f"Equipped items for {pth}device {device_index}:")
        for group_name, group in grouped_items.items():
            if group:
                log(hju + f"{f'{pth} + {hju}'.join(group)}")


    def get_current_item(self, user_id: str, item_type: str):
        token = self.local_token(user_id)
        if not token:
            return None

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', "/devices/user-device", headers=headers)

        if response.get('status') == 'success':
            for device in response['data']:
                equipped_items = self.get_equipped_items(user_id, device_index=device['index'])
                for item in equipped_items:
                    if item['type'] == item_type:
                        return item
        else:
            log(htm + "Error fetching user devices:", response.get('message'))
        return None


    def add_item_to_device(self, user_id: str, item_id: int, item_type: str):
        token = self.local_token(user_id)
        if not token:
            return

        device_indices = self.get_device_indices(user_id)
        if not device_indices:
            log(mrh + "Error: No valid device indices found.")
            return

        for device_index in device_indices:
            headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
            response = self._request('GET', f"/devices/add-item/{device_index}/{item_id}", headers=headers)
            if response.get('status') == 'success':
                log(hju + f"Successfully added {pth}{item_id} {hju}to device {pth}{device_index}.")
                countdown_timer(3)
                return
            else:
                message = response.get('message', 'Unknown error')
                if message == "MSG_DEVICE_USER_CANNOT_ADD_MORE_ITEM":
                    log(kng + f"Can't add more {pth}{item_type} {kng}to device {pth}{device_index}.")
                else:
                    log(htm + "Error adding item to device:", message)

        if len(device_indices) <= 3:
            self.add_new_device(user_id)

    def get_device_indices(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            return []

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', "/devices/user-device", headers=headers)
        if response.get('status') == 'success':
            return [device['index'] for device in response['data']]
        else:
            log(htm + "Error fetching user devices:", response.get('message'))
            return []

    def add_new_device(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', "/devices/add-device", headers=headers)
        if response.get('status') == 'success':
            log(hju + "Successfully added a new device.")
            countdown_timer(3)

    def unequip_item(self, user_id: str, item_id: int):
        token = self.local_token(user_id)
        if not token:
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', f"/devices/remove-item/{item_id}", headers=headers)
        if response.get('status') == 'success':
            log(hju + f"Successfully unequipped item ID {pth}{item_id}.")
            countdown_timer(3)
        else:
            log(htm + "Error unequipping item:", response.get('message'))


    def get_equipped_items(self, user_id: str, device_index: int):
        token = self.local_token(user_id)
        if not token:
            return []

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', f"/devices/user-device-item?index={device_index}&page=1&size=12", headers=headers)
        
        if response and response.get('status') == 'success':
            items = response.get('data', [])
            if self.show_item:
                self.log_items(device_index, items)
            return items
        else:
            log(htm + f"Error fetching equipped items: {response.get('message')} | HTTP Status: {response.get('status')}")
            return []
        
    def contribute(self, user_id: str):
        token = self.local_token(user_id)
        if not token: return
        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', f"/devices/user-device-item-contribute?page=1&size=10", headers=headers)
        if response and response.get('status') == 'success':
            items = response.get('data', [])
            if items:
                eligible_items = [item for item in items if item['miningPower'] < 600]
                if eligible_items:
                    item_code = eligible_items[0]['code']
                    payload = {"code": item_code, "number": 1}
                    response = self._request('POST', f"/league/contribute", headers=headers, json=payload)
                    if response and response.get('status') == 'success':
                        log(hju + f"Contribute Power success: {pth}{format(item_code)}")
                        time.sleep(1)
                    else:
                        log(mrh + response.get('message'))
        
        amount = random.randint(500, 1000)
        payload = {"amount": amount}
        response = self._request('POST', f"/league/funding", headers=headers, json=payload)
        if response and response.get('status') == 'success':
            log(hju + f"Contribute Funding success: {pth}{amount}")
            time.sleep(3)
        else:
            log(htm + f"{response.get('message')}")

    def auto_buy_item(self, user_id: str, device_index: int, max_item_price: float):
        token = self.local_token(user_id)
        if not token:
            return

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        equipped_items = self.get_equipped_items(user_id, device_index)
        if not equipped_items:
            log(bru + f"No equipped items found for device {pth}{device_index}.")
            return

        equipped_powers = {item['code']: item['miningPower'] for item in equipped_items}
        page_number = 1
        purchased_items = []

        while True:
            response = self._request('GET', f"/devices/item?page={page_number}&sortBy=miningPower&sortAscending=true&size=12", headers=headers)
            if response.get('status') != 'success':
                log(htm + "Error fetching items for purchase:", response.get('message'))
                break

            items = response.get('data', [])
            if not items:
                break

            for item in items:
                should_buy = any(item['miningPower'] > equipped_powers.get(code, 0) and item['price'] <= max_item_price for code in equipped_powers)
                
                if should_buy:
                    buy_response = self._request('POST', "/devices/buy-item", headers=headers, json={"number": 1, "code": item['code']})
                    if buy_response.get('status') == 'success':
                        equipped_powers[item['code']] = item['miningPower']
                        purchased_items.append(item['code'])
                        log(hju + f"Bought {pth}{item['name']} | Price: {pth}{item['price']}.")
                        countdown_timer(3)
                    elif buy_response.get("status") == "error" and buy_response.get("message") == "MSG_USER_POINT_NOT_ENOUGH":
                        log(kng + f"Insufficient points to purchase: {pth}{item['name']} {hju}| Price: {pth}{item['price']}")
                        return
                    else:
                        log(htm + f"Error purchasing item: {item['name']} | {buy_response.get('message')}")
            
            page_number += 1

        self.update_equipped_items(user_id, device_index, purchased_items)

    def update_equipped_items(self, user_id: str, device_index: int, purchased_items: list):
        for item_code in purchased_items:
            self.get_items_by_type(user_id, item_code)

    def sell_user_items(self, user_id: str):
        token = self.local_token(user_id)
        if not token:
            log(mrh + f"Error: Token not found.")
            return None

        headers = {**self.base_headers, "Authorization": f"Bearer {token}"}
        response = self._request('GET', "/devices/user-item", headers=headers, params={
            "sortBy": "price",
            "sortAscending": "true",
            "type": "",
            "page": 1,
            "size": 12
        })

        if response.get('status') != 'success':
            log(htm + "Error fetching user items:", response.get('message'))
            return None

        for item in response['data']:
            item_name = item['name']
            item_code = item['code']
            item_type = item.get('type', None)
            item_power = item.get('miningPower', None)  
            total_item = item['totalItem']
            is_can_sell = item['isCanSell']

            if item_name == "CYBER BOX":
                log(bru + f"Skipping {item_name}, no items sold.")
                continue

            if item_power is not None:
                current_item = self.get_current_item(user_id, item_type)
                if current_item and item_power > current_item['miningPower']:
                    log(hju + f"Unequipping {pth}{current_item['name']} {hju}and equipping {pth}{item_name}.")
                    self.unequip_item(user_id, current_item['id'])
                    self.add_item_to_device(user_id, item_code, item_type)

                elif is_can_sell:
                    if total_item > 1:
                        log(hju + f"Selling {pth}{total_item - 1} {hju}of {pth}{item_name}.")
                        self._request('POST',
                            "/devices/sell-item", 
                            headers=headers, json={
                            "code": item_code,
                            "number": total_item - 1
                        })
                    else:
                        log(mrh + f"Not selling the last item of {item_name} to keep one equipped.")
                else:
                    log(mrh + f"Item {item_name} cannot be sold.")
            else:
                log(mrh + f"Item {item_name} does not have a 'miningPower' attribute.")
                if is_can_sell and total_item > 2:
                    log(hju + f"Selling {pth}{total_item - 2} {hju}of {pth}{item_name} (no miningPower attribute).")
                    self._request('POST', "/devices/sell-item", headers=headers, json={
                        "code": item_code,
                        "number": total_item - 2
                    })
                else:
                    log(mrh + f"Not selling the last few items of {item_name} to keep some equipped.")
        return True


