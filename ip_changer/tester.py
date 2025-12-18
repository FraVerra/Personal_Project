import subprocess
import sys
import textwrap
import argparse

def function_command_status(command, ok_message, failure_message, decision):
    execution = subprocess.run(command, capture_output=True, text=True, check=True)
    if execution.returncode == 0:
        print(ok_message)
        if decision:
            return execution
    else:
        print(failure_message)
        print("[*] Closing the program")
        sys.exit()

def delete_old_ip():
    old_ip = []
    ok_message = "correttamente letto ip"
    fail_message = "non letto correttamente/non presente"
    command = ["sudo","ip","a"]
    ip_informations = function_command_status(command, ok_message, fail_message, True)
    information_lines = ip_informations.stdout.split("\n")
    for lines in information_lines:
        words = lines.split(" ")
        if "secondary" in words:
            old_ip.append(words[5])
    return old_ip

def main():
    old_ip = delete_old_ip()
    print(old_ip)

if __name__ == "__main__":
    main()