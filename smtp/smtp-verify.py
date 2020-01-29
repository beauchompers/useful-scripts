#!/usr/bin/python3
# check SMTP Verify for a list of ips and users
import socket 
import sys
import argparse

# args
arg_parser = argparse.ArgumentParser(description='Python SMTP VRFY Tester, enumerates SMTP for users')
arg_parser.add_argument('--ipfile', dest='ipfile', help='Name of the file containing the list of ips to hit')
arg_parser.add_argument('--userfile', dest='userfile', help='Name of the file containing the list of usernames to try')
args = arg_parser.parse_args()
   
# create list of ips and users
with open(args.ipfile) as f:
    ips = f.read().splitlines()

with open(args.userfile) as f:
    users = f.read().splitlines()
    
for i in ips:
    print(f'Attempting VRFY with users on {i}:')
    #Create a Socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connect to the Server 
    connect = s.connect((i,25)) 
    # Receive the banner 
    banner = s.recv(1024) 
    print(banner.decode('utf-8'))
    for user in users:
        # VRFY a user
        s.send(f'VRFY {user}\r\n'.encode()) 
        result = s.recv(1024) 
        print(result.decode('utf-8'))
    # Close the socket 
    s.close() 
