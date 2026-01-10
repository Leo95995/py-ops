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


def get_args():
    parser = argparse.ArgumentParser(description="Docker Cleanup Utility")
    parser.add_argument("-v" , "--volumes", action="store_true", help='Include also all the volumes' )
    parser.add_argument("-a","--all", action="store_true", help="Include all the resource that are unused")
    # when used as cronjob this argument must be used.
    parser.add_argument("-f","--yes-im-really-sure", action="store_true", help="Run everything without asking permissions")

    return parser.parse_args()



def is_docker_available():
    docker_info = subprocess.run(["docker", "info"], capture_output=True)
    if docker_info.returncode != 0:
        print("Docker inattivo \n")
        return False
    else: 
        print("Docker ATTIVO \n")
        return True

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
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Success!")
        print(result.stdout)
    else:
        print("Error during prune:")
        print(result.stderr)



def main():
    args = get_args()

    # verify that docker is present
    if not is_docker_available():
        print('Error, Exit \n')
        sys.exit()

    run_prune(args)


if __name__ == "__main__":
    main()

