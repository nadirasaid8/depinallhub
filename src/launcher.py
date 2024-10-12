from . import *
from src.deeplchain import number, awak, banner, clear, log, log_line, countdown_timer, read_config, mrh, pth, kng, hju, bru, htm, reset

config = read_config()
init(autoreset=True)

def get_status(status):
    return hju + "ON" if status else mrh + "OFF" + reset

def save_setup(setup_name, setup_data):
    with open(f'src/config/{setup_name}.json', 'w') as file:
        json.dump(setup_data, file, indent=4)
    awak()
    print(hju + f" Setup saved on {kng}setup{pth}/{setup_name}.json")
    with open(f'src/config/{setup_name}.json', 'r') as file:
        setup_content = json.load(file)
        print(f"\n{json.dumps(setup_content, indent=4)}\n")
    print(hju + f" Quick start : {pth}python main.py {htm}--setup {pth}{setup_name}")
    input(f" Press Enter to continue...")

def load_setup_from_file(setup_file):
    with open(setup_file, 'r') as file:
        setup = json.load(file)
    return setup

def show_menu(use_proxy, upgrade_skill, auto_task, auto_open_box, auto_buy_item, auto_sell_item):
    clear()
    banner()
    menu = f"""
{kng} Choose Setup :{reset}
{kng}  1.{reset} Use Proxy                  : {get_status(use_proxy)}
{kng}  2.{reset} Auto Upgrade Skill         : {get_status(upgrade_skill)}
{kng}  3.{reset} Auto Complete Tasks        : {get_status(auto_task)}
{kng}  4.{reset} Auto Open Box              : {get_status(auto_open_box)}
{kng}  5.{reset} Auto Buy Item              : {get_status(auto_buy_item)}
{kng}  6.{reset} Auto Sell Item             : {get_status(auto_sell_item)}
{kng}  7.{reset} Additional Configs         : {hju}config.json{reset}
{mrh}    {pth} --------------------------------{reset}
{kng}  8.{reset} {kng}Save Setup{reset}
{kng}  9.{reset} {mrh}Reset Setup{reset}
{kng}  0.{reset} {hju}Start Bot {kng}(default){reset}
    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4/5/6/7/8/9/0): ")
    log_line()
    return choice

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

def show_config():
    while True:
        clear()
        banner()
        config = read_config()
        
        menu = f"""
{hju} Active Menu {kng}'Change Configuration'{reset}
{htm} {'~' * 50}{reset}
{hju} Select the configuration to change:{reset}
{kng} 1. show_device_equipment (current: {hju}{config['show_device_equipment']}){reset}
{kng} 2. auto_open_box_max_price (current: {hju}{config['auto_open_box_max_price']}){reset}
{kng} 3. auto_buy_item_max_price (current: {hju}{config['auto_buy_item_max_price']}){reset}
{kng} 4. sleep_before_start (current: {hju}{config['sleep_before_start']}){reset}
{kng} 5. account_delay (current: {hju}{config['account_delay']}){reset}
{kng} 6. countdown_loop (current: {hju}{config['countdown_loop']}){reset}
{kng} 7. back to {bru}main menu{reset}

        """
        print(menu)
        
        choice = input(" Enter your choice (1/2/3/4/5/6/7): ")
        
        if choice in ['1', '2', '3', '4', '5', '6']:
            key_map = {
                '1': 'show_device_equipment',
                '2': 'auto_open_box_max_price',
                '3': 'auto_buy_item_max_price',
                '4': 'sleep_before_start',
                '5': 'account_delay',
                '6': 'countdown_loop'
            }
            
            key = key_map[choice]
            
            if choice == '1': 
                config[key] = not config[key]
            else: 
                new_value = input(f" Enter new value for {key}: ")
                try:
                    config[key] = int(new_value)
                except ValueError:
                    print(" Invalid input. Please enter a valid number.")
                    continue 

            write_config(config)
            print(f" {key} updated to {config[key]}")
        
        elif choice == '7':
            break  # Exit the loop and return to the main menu
        else:
            print(" Invalid choice. Please try again.")

def run_bot(use_proxy, upgrade_skill, auto_task, auto_open_box, auto_buy_item, auto_sell_item):
    max_price = config.get('auto_open_box_max_price', 0)
    max_item_price = config.get('auto_buy_item_max_price', 0)
    time_start = config.get('sleep_before_start', 5)
    delay = config.get('account_delay', 5)
    loop = config.get('countdown_loop', 3800)
    countdown_timer(time_start)
    proxies = load_proxies() if use_proxy else None

    try:
        with open("data.txt") as file:
            query_data_list = file.readlines()
        query_data_list = [data.strip() for data in query_data_list if data.strip()]
        if not query_data_list:
            raise ValueError("data.txt is empty or contains only empty lines.")
    except FileNotFoundError:
        log(mrh + f"data.txt file not found.")
        return

    for i, query_data in enumerate(query_data_list, start=1):
        proxy = random.choice(proxies) if proxies and use_proxy else None
        dep = Depin(proxy=proxy)
        
        log(hju + f"Processing account {pth}{i}/{len(query_data_list)}")
        if proxy:
            proxy_url = proxy
            host_port = proxy_url.split('@')[-1] if '@' in proxy_url else proxy_url.split('//')[-1]
            log(hju + f"Using proxy: {pth}{host_port}")
            log(htm + "~" * 38)

        user_data = dep.extract_user_data(query_data)
        user_id = user_data.get("id")
        if not user_id:
            log(mrh + f"User ID not found in data.")
            continue

        token = dep.local_token(user_id) or dep.login(query_data, user_id)

        while True:
            try:
                dep.user_data(user_id)
                dep.j_l(user_id)
                dep.daily_checkin(user_id)
                dep.claim_mining(user_id)
                dep.contribute(user_id)

                device_indices = dep.get_device_indices(user_id)
                if not device_indices:
                    log(bru + f"No valid device indices : {pth}{user_id}")
                    break
                device_index = device_indices[0]
                if auto_open_box:
                    dep.open_box(user_id, max_price)
                else:
                    log(bru + f"Auto open cyber box is disabled!")
                if auto_buy_item:
                    dep.auto_buy_item(user_id, device_index, max_item_price)
                else:
                    log(bru + f"Auto buy item is disabled!")
                for item_type in ["CPU", "GPU", "RAM", "STORAGE"]:
                    dep.get_items_by_type(user_id, item_type)
                if auto_task:
                    dep.get_task(user_id)
                    dep.complete_quest(user_id)
                else:
                    log(bru + f"Auto complete task is disabled!")
                if upgrade_skill:
                    dep.upgrade_skill(user_id)
                else:
                    log(bru + f"Auto upgrade skill is disabled!")
                if auto_sell_item:
                    dep.sell_user_items(user_id)
                else:
                    log(bru + f"Auto sell item is disabled!")
                break
            except requests.exceptions.ProxyError as e:
                log(mrh + f"Proxy error occurred: {e}")
                if "407" in str(e):
                    log(bru + f"Proxy authentication failed. Trying another.")
                    if proxies:
                        proxy = random.choice(proxies)
                        log(bru + f"Switching proxy: {pth}{proxy}")
                    else:
                        log(mrh + f"No more proxies available.")
                        break
                else:
                    log(htm + f"An error occurred: {htm}{e}")
                    break

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    log(bru + f"Token expired or Unauth. Attempting to login")
                    if dep.is_expired(token):
                        token = dep.login(query_data, user_id)
                    if token is False:
                        return int(datetime.now().timestamp()) + 8 * 3600
                else:
                    log(mrh + f"HTTP error occurred: {htm}{e}")
                    return

        log_line()
        countdown_timer(delay)
    countdown_timer(loop)

def main():
    parser = argparse.ArgumentParser(description="Run the bot with a specified setup.")
    parser.add_argument('--setup', type=str, help='Specify the setup file to load')
    args = parser.parse_args()

    if args.setup:
        setup_file = f'src/config/{args.setup}.json'
        setup_data = load_setup_from_file(setup_file)
        use_proxy = setup_data.get('use_proxy', False)
        upgrade_skill = setup_data.get('upgrade_skill', False)
        auto_task = setup_data.get('auto_task', False)
        auto_open_box = setup_data.get('auto_open_box', False)
        auto_buy_item = setup_data.get('auto_buy_item', False)
        auto_sell_item = setup_data.get('auto_sell_item', False)
        run_bot(use_proxy, upgrade_skill, auto_task, auto_open_box, auto_buy_item, auto_sell_item)
        
    else:
        use_proxy = False
        upgrade_skill = False
        auto_task = False
        auto_open_box = False
        auto_buy_item = False
        auto_sell_item = False

        while True:
            try:
                choice = show_menu(use_proxy, upgrade_skill, auto_task, auto_open_box, auto_buy_item, auto_sell_item)
                if choice == '1':
                    use_proxy = not use_proxy
                elif choice == '2':
                    upgrade_skill = not upgrade_skill
                elif choice == '3':
                    auto_task = not auto_task
                elif choice == '4':
                    auto_open_box = not auto_open_box
                elif choice == '5':
                    auto_buy_item = not auto_buy_item
                elif choice == '6':
                    auto_sell_item = not auto_sell_item
                elif choice == '7':
                    show_config()
                elif choice == '8':
                    setup_name = input(" Enter setup name (without space): ")
                    setup_data = {
                        'use_proxy': use_proxy,
                        'upgrade_skill': upgrade_skill,
                        'auto_task': auto_task,
                        'auto_open_box': auto_open_box,
                        'auto_buy_item': auto_buy_item,
                        'auto_sell_item': auto_sell_item
                    }
                    save_setup(setup_name, setup_data)
                elif choice == '0':
                    run_bot(use_proxy, upgrade_skill, auto_task, auto_open_box, auto_buy_item,auto_sell_item)
                elif choice == '9':
                    break
                else:
                    log(mrh + f"Invalid choice. Please try again.")
                time.sleep(1)
            except Exception as e:
                log(mrh + f"An error occurred in the main loop: {kng}{str(e)}")
                countdown_timer(10)

