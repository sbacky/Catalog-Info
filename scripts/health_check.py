#!/usr/bin/env python3

import shutil
import psutil
import socket
import sys
import emails

def check_cpu_constrained():
    """Returns True if the cpu is having too much usage, False otherwise"""
    return psutil.cpu_percent(1) > 80

def check_disk_space():
    """Returns True if available disk space is less than 20%, False otherwise"""
    du = shutil.disk_usage("/")
    # Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    if percent_free < 20:
        return True
    return False

def check_memory():
    '''Returns true if available memory is less than 500MB.'''
    du = shutil.disk_usage("/")
    # Calculate how many free megabytes
    megabytes_free = du.free / 2**20
    if megabytes_free < 500:
        return True
    return False

def check_no_network():
    """Returns True if it fails to resolve localhost URL, False otherwise."""
    localhost = socket.gethostbyname("localhost")
    if localhost != '127.0.0.1':
        return True
    return False

def main():
    checks=[
        (check_cpu_constrained, "Error - CPU usage is over 80%"),
        (check_disk_space, "Error - Available disk space is less than 20%"),
        (check_memory, "Error - Available memory is less than 500MB"),
        (check_no_network, "Error - localhost cannot be resolved to 127.0.0.1"),
    ]
    everything_ok = True
    for check, subject in checks:
        if check():
            sender = "automation@example.com"
            receiver = "student-03-73b7907327aa@example.com"
            body = "Please check your system and resolve the issue as soon as possible."
            attachment = ""
            message = emails.generate_email(sender, receiver, subject, body, attachment)
            emails.send_email(message)
            evrything_ok = False

    if not everything_ok:
        sys.exit(1)

    print("Everything ok.")
    sys.exit(0)

if __name__ == "__main__":
    main()
