# Import Libs
import subprocess as sb
from modules import settings_conf
import colorama
from colorama import Fore
colorama.init(autoreset=True)

# Start development server
server_ip, server_port, allowed_ip = settings_conf.init()

print(Fore.YELLOW + "\n+-- Migrate Server -------------------------+")
sb.run('python main/manage.py migrate', shell=True)

print(Fore.GREEN + "\n+-- Hosting Server -------------------------+")
sb.run(f'python main/manage.py runserver {server_ip}:{server_port}', shell=True)