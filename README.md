# D3P1N-BOT FOR D3P1N Alliance Telegram Miniapp

Full feature features as in the original D3p1n Alliance bot telegram.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [CONTACT](https://t.me/imspecials)

## REGISTER FIRST : [D3P1N ALIANCE](https://t.me/DePIN_Alliance_Bot?start=P8YJYaETWS)

## Update : 2024-10-19
  - Script base optimization
  - Add Auto Accept Member if you're Guild Owner 

# Feature 
  - Support for multiple proxy servers
  - Support for multiple telegram accounts
  - Display Menu : run the bot and set your configurations 
  - Instant Setup : save your setup and run easily 
  - Support Random User Agent 
  - Manage the items with the ability to sell items `ON` / `OFF`
  - Completion of Daily Checkin or Available Quest `ON` / `OFF`
  - Upgrade randomly selected skills `ON` / `OFF`
  - Open a cyber box that can be set to the maximum price `ON` / `OFF`
  - Purchase items in the shop that can be set to the maximum price. `ON` / `OFF`
  - Automatically use items that have higher Reward Points 
  - Show Device Equipment : bool `True/False`
  - Can run 24/7 using vps / rdp

## Requirements

- Python 3.10+

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/nadirasaid8/depinallhub.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd depinallhub
    ```

3. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `config.json` file**

    The `config.json` file should be in the root directory of the project. Here is a sample configuration:

    ```json
    {
        "show_device_equipment": false,
        "auto_open_box_max_price": 2000,
        "auto_buy_item_max_price": 2000,
        "sleep_before_start": 5,
        "account_delay": 3,
        "countdown_loop": 500
    }

    ```
    - `show_device_equipment`: set it to `true` to show device equipment 
    - `auto_open_box_max_price`: set a maximum price for the open cyber box
    - `auto_buy_item_max_price`: set a maximum price for the purchased item
    - `sleep_before_start`: the sleep time before running the bot 
    - `account_delay`: Delay between processing each account (in seconds).
    - `countdown_loop`: how long is the waiting time to return to the first account

## Usage
before starting the bot you must have your own initdata / queryid telegram!

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `D3p1n Alliance telegram bot`
3. Inspect Element or `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`D3p1n Alliance`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
```

10. **Create a `proxies.txt` file**

    The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

    Example:

    ```
    user1:pass1@ip1:port1
    user2:pass2@ip2:port2
    ```

11. **To run the bot, execute the following command:**

```bash
python main.py
```

### Instant Setup:
- **Loading setup via CLI argument:** If the `--setup` argument is provided, the script will load the corresponding `.json` file and run the bot directly without displaying the menu.
- **Menu display:** If no `--setup` argument is provided, the script will display the menu as usual.
- **Setup saving:** The option to save setups has been included in the menu as option `8`.

This will allow you to run the script directly with a predefined setup like this:

```bash
python main.py --setup mysetup
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [ https://t.me/DeeplChain ]
