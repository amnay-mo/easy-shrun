from netmiko import ConnectHandler
from easygui import *

field_names = ("host","username")

is_valid = False
while not is_valid:
    host_info = multenterbox("Enter Connection Info", "Cisco Device Configurator", field_names)
    if host_info is None:
        print('quitting..')
        exit(0)
    is_valid = all(host_info)
    if not is_valid:
        msgbox("Missing required field", "Error")

is_valid = False
while not is_valid:
    ssh_password = passwordbox("ssh password", title="ssh password")
    if ssh_password is None:
        print('quitting..')
        exit(0)
    if ssh_password:
        is_valid = True
    else:
        msgbox("Missing required field", "Error")

is_valid = False
while not is_valid:
    enable_secret = passwordbox("enable secret", title="enable secret")
    if enable_secret is None:
        print('quitting..')
        exit(0)
    if enable_secret:
        is_valid = True
    else:
        msgbox("Missing required field", "Error")

connection_info = {
    'device_type': 'cisco_ios',
    'ip': host_info[0],
    'username': host_info[1],
    'password': ssh_password,
    'secret': enable_secret,
}
try:
    conn = ConnectHandler(**connection_info)
except Exception as e:
    msgbox(e, "Error")
    exit(-1)
conn.enable()
running_config = conn.send_command("show running-config")
running_config = "\n".join(running_config.splitlines()[4:])
device_configuration = codebox(msg="Running Config", title="Running Config", text=running_config)
if device_configuration:
    print('updating configuration..')
    configuration_commands = device_configuration.splitlines()
    conn.send_config_set(configuration_commands)
    msgbox("Configuration Done!")
else:
    print('configuration canceled')
