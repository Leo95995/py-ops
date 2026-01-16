# Backup Manager 

**Backup Manager** is a Python-based automation tool designed to streamline the backup process for VPS environments. It compresses source directories, uploads them to an **AWS S3** bucket, and sends real-time status alerts via **Telegram**.

##  Key Features

* **Automated Compression**: Packages source folders into `.tar.gz` archives with ISO-style timestamps.
* **Cloud Integration**: Reliable uploads to AWS S3 using `boto3`.
* **Real-time Alerts**: Instant Telegram notifications for successful uploads or failures.
* **Storage Efficiency**: Automatically removes local temporary archives after a successful cloud upload to save disk space on the host.
* **CLI Ready**: Fully controllable via command-line arguments.

##  Tech Stack

* **Language**: Python 3.10+
* **Cloud**: AWS S3 (Boto3)
* **Notifications**: Telegram Bot API
* **DevOps**: Docker ready, Environment-based configuration (`python-dotenv`).

##  Prerequisites

* Python installed on your VPS.
* An AWS IAM User with `PutObject` permissions for S3.
* A Telegram Bot (created via @BotFather).

##  Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/leo95995/py-ops.git

cd py-ops/backup-manager
```


## Set up a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure Environment Variables: Create a .env file in the root directory:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=your-aws-region
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Run the script by specifying the source folder you want to back up:

```bash
python3 backup_manager.py -s /path/to/your/app -o production_backup
```
### Arguments:

    -s, --source: (Required) Path of the directory to backup.

    -o, --output: (Optional) Custom name for the output file.

### Automation
To run backup every day at 0:00 AM, add this to your crontab -e:
Snippet di codice

```bash
0 0 * * * /path/to/backup-manager/venv/bin/python /path/to/py-ops/backup_manager.py -s /home/apps/my-target- app
```
Developed as part of my DevOps growth journey. Focused on automation, reliability, and cloud integration.

