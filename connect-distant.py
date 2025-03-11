import subprocess

username = input("Enter the username: ")
ip_address = input("Enter the IP address: ")

ssh_çommand = f"ssh {username}@{ip_address}"
print(subprocess.run(ssh_çommand, shell=True, capture_output=True).stdout.decode())
