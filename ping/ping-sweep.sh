#!/bin/bash
# ping sweeper
# one liner - for i in $(seq 1 255);do ping -c 1 10.11.1.$1 | tr \\n ' ' | awk '/1 received' {print $2}; done

# how to use the script
display_usage() { 
	echo "Ping sweeper!" 
    echo -e "\nSupply the first 3 octets of the range, example 10.11.1"
	echo -e "\nUsage:\n$0 10.11.1 \n" 
	} 

# if arguments supplied not equal to 1, display usage
if [ $# -ne 1 ];
then 
    display_usage
    exit 1
fi 

# subnet is first argument passed to script
SUBNET=$1

# do ping sweep
for i in $(seq 1 254); do
    ping -c 1 $SUBNET.$i | tr \\n ' ' | awk '/1 received/ {print $2}' &
done

# do ping sweep
for i in $(seq 1 254); do
    ping -c 1 $SUBNET.$i | tr \\n ' ' | awk '/1 received/ {print $2}' &
done