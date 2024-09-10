# Importando libs
from pathlib import Path
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
        server_ip_machine = 'False'

        for line in f:
            # Get server ip machine value
            if line.startswith("server_ip_machine="):
                server_ip_machine = line.split('=')[1].strip()

            # Get server ip
            if line.startswith("server_ip="):
                server_ip = line.split('=')[1].strip()

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

        if server_ip_machine == 'True':
            hostname = socket.gethostname()
            server_ip_machine = socket.gethostbyname(hostname)
            allowed_ip.append(server_ip_machine)
            server_ip = '0.0.0.0'

            with open(settings_file , "r") as f:
                lines = f.readlines()

            # Write on settings_file
            with open(settings_file, 'w') as file:
                for line in lines:
                    if line.startswith("server_ip="):
                        line = "server_ip=" + server_ip_machine + '\n'
                    file.write(line)
        else:
            if not server_ip:
                print("error: server_ip has not set. define server_ip_machine on True to use ip machine to run server.")
                sys.exit(0)
            

    return server_ip, server_port, allowed_ip, email_smtp, email_port, email_address, email_password, server_ip_machine

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
    server_ip, server_port, allowed_ip, email_smtp, email_port, email_address, email_password, server_ip_machine = read_settings_conf()

    # Write config changes on Django settings.py
    write_settings_file(allowed_ip, email_smtp, email_port, email_address, email_password)

    if server_ip_machine == 'True':
        print(f"server_ip: " + server_ip_machine)
    else:
        print(f"server_ip: " + server_ip)
    print(f"server_port: " + server_port)
    for i in allowed_ip:
        print(f"allowed_ip: " + i)
    print(f"email_smtp: " + email_smtp)
    print(f"email_port: " + email_port)
    print(f"email: " + email_address)
    print(f"email_password: " + email_password)

    return server_ip, server_port, allowed_ip