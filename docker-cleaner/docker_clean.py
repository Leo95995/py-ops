#!/usr/bin/env python3 
"""
Docker Cleanup Utility
Developed by Leo
Automates the removal of unused Docker resources while ensuring volume safety.
"""

# library used to launch shell commands
import subprocess
# sue
import sys
# working with argparse and path lib
import argparse
# added datetime
import datetime

# define CLI arguments for targeted cleanup and automation 
def get_args():
    parser = argparse.ArgumentParser(description="Docker Cleanup Utility")
    parser.add_argument("-v" , "--volumes", action="store_true", help='Include also all the volumes' )
    parser.add_argument("-a","--all", action="store_true", help="Include all the resource that are unused")
    # when used as cronjob this argument must be used.
    parser.add_argument("-f","--yes-im-really-sure", action="store_true", help="Run everything without asking permissions")
    #  return the final results of arguments
    return parser.parse_args()

# function that checks if docker is currently present
def is_docker_available():
    docker_info = subprocess.run(["docker", "info"], capture_output=True)
    if docker_info.returncode != 0:
        log_event("Docker daemon unrechable: exiting \n", "ERROR")
        return False
    else: 
        return True


# Function used to log events
def log_event(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{level}] {message}"

    # print logs on screen
    print(formatted_message)
    
    # persistent logging for operational audit and disk usage tracking
    with open("./docker_cleanup.log", "a") as f:
        f.write(formatted_message + "\n")


# The function that run docker system prune
def run_prune(args):

    command = ["docker", "system", "prune"]

    if args.volumes:
        if not args.yes_im_really_sure:
            confirmation= input("You are about to remove all the volumes, are you sure?  Y/N \n")
            if confirmation.lower() != "y":
             print('Operazione annullata')
             return
        command.append("--volumes")
    if args.all:
        print("Pulizia totale attivata")     
        command.append("-a")    

    if "-f" not in command:
        command.append("-f")

    print("Running command:", " ".join(command))
    # text as true to return the output as readable text
    try:
        # check as true exit with subprocess.calledprocesserror if error code is != 0
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        reclaimed = "0B"
        for line in result.stdout.splitlines():
            if "Total reclaimed space:" in line:
                    reclaimed = line.split(":")[1].strip()

        log_event(f"SUCCESS: Cleanup completed. Space recovered: {reclaimed}")
    except subprocess.CalledProcessError as e:
        # logging stderr also
        log_event(f"ERROR: Command failed. Details: {e.stderr}", level="ERROR")        

# The main functin to be executed
def main():
    args = get_args()

    # verify that docker is present
    if not is_docker_available():
        print('Error, Exit \n')
        sys.exit()
    run_prune(args)


if __name__ == "__main__":
    main()

