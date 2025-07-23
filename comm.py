import paramiko

HOST = "192.168.1.100"  # Replace with your target IP
PORT = 22  # Default SSH port
USERNAME = "your_user"
PASSWORD = "your_password"  # Use SSH keys for better security

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto-accept unknown hosts
    client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD, timeout=5)

    print("Connected successfully!")
    
    # Run a command on the remote machine
    stdin, stdout, stderr = client.exec_command("whoami")
    print(f"Command Output: {stdout.read().decode()}")

    client.close()
except paramiko.AuthenticationException:
    print("Authentication failed. Check your username/password.")
except paramiko.SSHException as e:
    print(f"SSH error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")