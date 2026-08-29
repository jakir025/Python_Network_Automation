from telnetlib import Telnet

# Use input() for Python 3 (raw_input() was removed in Python 3)
cmd = input('Enter the command : ')
tn = Telnet('192.168.XX.XX')   # connect to finger port
tn.write(b'XXX\r\n')
tn.write(b'XXX\r\n')  
tn.write(b'term length 0\n')
# Fixed: removed bad backslash and added proper byte string concatenation with newline
tn.write(cmd.encode('ascii') + b'\n')
tn.write(b'exit\n')
# Fixed: removed the extra trailing closing parenthesis
print(tn.read_all().decode('ascii'))
