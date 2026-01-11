# Site-Checker Automated SSL & Uptime Monitor

**Site-Checker** is a lightweight, proactive monitoring tool written in Python. It is designed to track the health of web services by checking HTTP/S uptime and SSL certificate validity. When a service goes down or a certificate is nearing expiration, it sends real-time push notifications via the **Telegram Bot API** while maintaining a detailed persistent log for audit trails.

## Features

* **Uptime Monitoring**: Verifies site availability and logs HTTP status codes (e.g., 200 OK, 404 Not Found).
* **SSL Expiration Tracking**: Connects via low-level sockets to extract certificate metadata and calculate remaining validity days.
* **Smart Thresholds**: Automatically classifies SSL status as `OK`, `WARNING` (< 30 days), or `CRITICAL` (< 7 days).
* **Telegram Alerts**: Instant notifications for critical events, ensuring you can act before a service goes offline.
* **Secure Credential Management**: Uses `.env` files to keep API tokens and sensitive IDs out of the source code.
* **Operational Logging**: Maintains a persistent log file (`site_checker.log`) with timestamps for auditing and debugging.
* **DevOps Ready**: Optimized for deployment on VPS/Linux servers using Cronjobs.


## 📸 Proof of Concept

When a threshold is hit, **Site Checker** reaches out immediately:

*(To add your own: create an `images/` folder, save your screenshot as `alert.png`, and update the link in the README)*

---

## Installation & Setup

### 1. Clone the Repo

```bash
git clone https://github.com/leo95995/py-ops.git

cd py-ops/site-checker

```

### 2. Environment Setup

Create a virtual environment and install the required libraries:

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```

### 3. Configuration

1. **SITES**: Edit `sites.json` with your targets:
```json
[
  {"name": "site1", "url": "https://your-site.com"},
  {"name": "site2", "url": "https://api.your-site.com"}
]

```


2. **SECRETS**: Create a `.env` file:
```env
TELEGRAM_TOKEN=123456789:ABCDEF...
TELEGRAM_CHAT_ID=987654321
```

3. **Telegram Bot Setup**

To receive real-time alerts, you need to set up a Telegram Bot:

- Create the Bot: Search for @BotFather on Telegram and send the command /newbot. Follow the instructions to get your API Token.

- Get your **Chat ID**:

- Search for @IDBot and send /getid to get your personal numeric Chat ID.

- Alternatively, start a chat with your new bot and visit https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates to find your ID in the JSON response.

- Activate the Bot: Send a "Hello" message or click Start in the chat with your new bot. 

**Note: This is because the bot cannot message you first due to Telegram's anti-spam policy.**

## Usage

### Manual Execution

Run the full check for all sites in the JSON file:

```bash
python site_checker.py
```

Or check a single URL on the fly:

```bash
python site_checker.py --url https://google.com

```

### Automated Deployment (VPS)

you can also schedule it using `crontab`on your target server: 

Run `crontab -e` and add the following line to check your sites for example every morning at 9:00 AM:

```bash
0 9 * * * absolute/path/to/py-ops/site-checker/venv/bin/python absolute/path/to/py-ops/site-checker/site_checker.py >> /path/to/cron_debug.log 2>&1
```


## Logging & Observability

Site-checker produces clean, scannable logs. You can monitor them in real-time on your server:

```bash
# watch the sentinel work in real-time
tail -f site_checker.log

# search for critical issues only
grep "CRITICAL" site_checker.log

# or you can use less to search detailed
less site_checker.log
```

## Author

**Leonardo Malvolti** *Fullstack Developer* [GitHub Profile](http://github.com/leo95995) | [LinkedIn](https://linkedin.com/in/leonardo-malvolti)