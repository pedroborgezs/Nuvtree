# Import Libs
import subprocess as sb
from modules import settings_conf

# Start development server
print("provided by: nuvtree")
print("\nmodules: load settings_conf.py")
server_ip, server_port, allowed_ip = settings_conf.init()

print("\ncmd: makemigrations")
sb.run('python main/manage.py makemigrations', shell=True)
print("\ncmd: migrate")
sb.run('python main/manage.py migrate', shell=True)
print("\ncmd: runserver")
sb.run(f'python main/manage.py runserver {server_ip}:{server_port}', shell=True)