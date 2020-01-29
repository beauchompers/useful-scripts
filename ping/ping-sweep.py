#! /usr/bin/python3
# python3 ping sweeper, quickly sweeps a /24 subnet

import multiprocessing
import subprocess
import argparse

# args
arg_parser = argparse.ArgumentParser(description='Python Ping Sweeper, ping sweeps a /24 network')
arg_parser.add_argument('--network', dest='network', help='The /24 network to sweep, example 10.11.1', type=str, default='10.11.1')
args = arg_parser.parse_args()

host_list = []

def ping(num,ip, return_dict):
    # ping sweep
    ping = subprocess.call(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL)
    if ping == 0:
        return_dict[num] = ip

pings = []
manager = multiprocessing.Manager()
return_dict = manager.dict()

for i in range(1,255):
    ip = f'{args.network}.{i}'
    result = multiprocessing.Process(target=ping, args=(i,ip,return_dict))
    pings.append(result)
    result.start()

for p in pings:
    p.join()
    
for i in return_dict.values():  
    print(i)
