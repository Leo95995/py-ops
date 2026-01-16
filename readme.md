
# py-ops 

**py-ops** is a collection of personal automation and monitoring tools built in Python for VPS environments, system management, and R&D experiments.
Each tool focuses on automation, reliability, and operational efficiency.


## Projects Overview

###  1 - Backup Manager

Automates backups for VPS environments.

* Compresses source directories into `.tar.gz` archives
* Uploads to **AWS S3**
* Sends **real-time Telegram alerts**
* Efficient storage management with local cleanup

  **[Full README → backup-manager](./backup-manager/readme.md)**


### 2- Site-Checker

Lightweight uptime and SSL monitoring tool for web services.

* Monitors HTTP/S status and SSL expiration
* Sends **instant Telegram notifications**
* Maintains persistent logs for auditing
* Designed for deployment on Linux servers

  **[Full README → site-checker](./site-checker/readme.md)**


### 3- Docker Cleaner

Automates disk cleanup on production VPS without service interruption.

* Prunes unused containers, images, and optionally volumes
* Safe and auditable with explicit flags
* Provides clean operational metrics

  **[Full README → docker-cleaner](./docker-cleaner/readme.md)**


## Tech Stack

* **Languages:** Python 3.10+
* **Infrastructure & Automation:** Docker, Linux, Cron
* **Cloud & Notifications:** AWS S3, Telegram Bot API
* **DevOps R&D:** Personal experiments in automation, monitoring, and system management

---

## Usage

Each project includes a dedicated README with **installation, setup, usage, and automation instructions**.
Navigate to the respective folder to get started.

---

## Author

**Leonardo Malvolti** – Fullstack Developer | R&D & Automation
[GitHub](https://github.com/leo95995) | [LinkedIn](https://linkedin.com/in/leonardo-malvolti)


