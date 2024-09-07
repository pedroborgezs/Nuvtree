# Importando libs
from pathlib import Path
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
import socket
import sys
import re

# Reading settings config file
def read_settings_conf():
    # Get path
    parent = Path(__file__).resolve().parent.parent
    settings_file = parent / "settings.conf"

    # Open config file
    with open(settings_file , "r") as f:
        allowed_ip = []
        server_ip = None
        machine = False

        for line in f:
            # Get server ip
            if line.startswith("server_ip="):
                server_ip = line.split('=')[1].strip()
                allowed_ip.append(server_ip)

            # Get server port
            if line.startswith("server_port="):
                server_port = line.split('=')[1].strip()

            # Get allowed ip
            if line.startswith("allowed_ip="):
                allowed_ip.append(line.split('=')[1].strip())

            # Get email smtp
            if line.startswith("email_smtp="):
                email_smtp = line.split('=')[1].strip()

            # Get email port
            if line.startswith("email_port="):
                email_port = line.split('=')[1].strip()

            # Get email
            if line.startswith("email_address="):
                email_address = line.split('=')[1].strip()

            # Get email password
            if line.startswith("email_password="):
                email_password = line.split('=')[1].strip()

        if not server_ip:
            # Trying get machine ip
            try:
                hostname = socket.gethostname()
                server_ip = socket.gethostbyname(hostname)
                machine = True
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(0)

        allowed_ip.append(server_ip)

        if machine:
            machine = server_ip
            server_ip = '0.0.0.0'
    
    return server_ip, server_port, allowed_ip, email_smtp, email_port, email_address, email_password, machine

# Write settings on Django settings file
def write_settings_file(allowed_ip, email_smtp, email_port, email_address, email_password):
    try:
        # Django settings file
        settings_django_file = "main/main/settings.py"

        ## Read Django settings file
        with open(settings_django_file, 'r') as file:
            content = file.read()

        # Patterns for allowed hosts
        pattern_allow = r"ALLOWED_HOSTS\s*=\s*\[(.*?)\]"

        allowed_hosts_pattern = "ALLOWED_HOSTS = [" + ", ".join(f'"{ip}"' for ip in allowed_ip) + "]"

        # Patterns for email settings
        patterns_email = {
            'EMAIL_HOST': r"EMAIL_HOST\s*=\s*'.*?'",
            'EMAIL_PORT': r"EMAIL_PORT\s*=\s*\d+",
            'EMAIL_HOST_USER': r"EMAIL_HOST_USER\s*=\s*'.*?'",
            'EMAIL_HOST_PASSWORD': r"EMAIL_HOST_PASSWORD\s*=\s*'.*?'",
        }

        # New email settings
        new_email_settings = {
            'EMAIL_HOST': f"EMAIL_HOST = '{email_smtp}'",
            'EMAIL_PORT': f"EMAIL_PORT = {email_port}",
            'EMAIL_HOST_USER': f"EMAIL_HOST_USER = '{email_address}'",
            'EMAIL_HOST_PASSWORD': f"EMAIL_HOST_PASSWORD = '{email_password}'",
        }

        # Replace ALLOWED_HOSTS
        content = re.sub(pattern_allow, allowed_hosts_pattern, content)

        # Replace email settings
        for key, pattern in patterns_email.items():
            content = re.sub(pattern, new_email_settings[key], content)

        # Write new content on file
        with open(settings_django_file, 'w') as file:
            file.write(content)

        
    except Exception as e:
        print("Error: " + e)


def init():
        
    # Read config file
    server_ip, server_port, allowed_ip, email_smtp, email_port, email_address, email_password, machine = read_settings_conf()

    # Write config changes on Django settings.py
    write_settings_file(allowed_ip, email_smtp, email_port, email_address, email_password)

    print(f"{Fore.LIGHTBLUE_EX}+-- Basic Server Config To Host ------------+")
    if machine:
        print(f"{Fore.LIGHTBLUE_EX}server_ip: " + Style.RESET_ALL + machine)
    else:
        print(f"{Fore.LIGHTBLUE_EX}server_ip: " + Style.RESET_ALL + server_ip)
    print(f"{Fore.LIGHTBLUE_EX}server_port: " + Style.RESET_ALL + server_port)
    for i in allowed_ip:
        print(f"{Fore.LIGHTBLUE_EX}allowed_ip: " + Style.RESET_ALL + i)
    print(f"{Fore.LIGHTBLUE_EX}email_smtp: " + Style.RESET_ALL + email_smtp)
    print(f"{Fore.LIGHTBLUE_EX}email_port: " + Style.RESET_ALL + email_port)
    print(f"{Fore.LIGHTBLUE_EX}email: " + Style.RESET_ALL + email_address)
    print(f"{Fore.LIGHTBLUE_EX}email_password: " + Style.RESET_ALL + email_password)

    return server_ip, server_port, allowed_ip