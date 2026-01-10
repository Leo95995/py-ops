## Docker Cleaner

Python utility for automated disk reclamation on production VPS.
Designed to handle cleanup without service interruption.

### Performance & Impact

Tested on **Ubuntu 22.04 (12.6GB RAM)**.

* **Storage Recovered:** 27.29 GB
* **System Behavior:** `dockerd` CPU peaked at ~70%. No impact on concurrent services stability.

### Implementation Details

* **Path Agnostic**: Uses `os.path.abspath(__file__)` to ensure logs are written to the script's directory regardless of the execution context (essential for crontab).
* **Process Integrity**: Implements `subprocess.run(check=True)` to map shell return codes to Python exceptions, preventing silent failures.
* **Volume Protection**: "Default Deny" policy. Deletion requires explicit `--volumes` + `--yes-im-really-sure` flags.
* **Metrics Extraction**: Output parsing for `Total reclaimed space` to provide clean operational logs instead of verbose `stdout`.

### Usage

**Check available arguments:**

```bash
python3 docker_clean.py --help 
```

**Manual Execution (Interactive):**

* `-a, --all`: Prunes all unused images (not just dangling).
* `-v, --volumes`: Prunes unused volumes (High Risk).
* `-f, --yes-im-really-sure`: Bypasses prompts for automation.

```bash
# Example: prune images and containers without volumes
python3 docker_clean.py -a

```

**Automation (Cronjob):**
Add this to `crontab -e` to run every Sunday at 03:00:

```bash
0 3 * * 0 /usr/bin/python3 /absolute/path/to/docker_clean.py --all --yes-im-really-sure
```