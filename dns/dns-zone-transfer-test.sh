#!/bin/bash
# zonetransfer test script
# This script will get the name servers for a domain, and attempt a zone transfer against each one.

# how to use the script
display_usage() { 
	echo "DNS Zone Transfer Test!" 
    echo -e "\nSupply the name of the domain"
	echo -e "\nUsage:\n$0 example.com \n" 
	} 

# if arguments supplied not equal to 1, display usage
if [ $# -ne 1 ];
then 
    display_usage
    exit 1
fi 

# zone to test
ZONE=$1

# get name servers and attempt zone transfer with dig axfr $zone @$server
for server in $(host -t ns $ZONE | cut -d " " -f 4); do
    echo "Attempting Zone Transfer against $server"
    dig axfr $ZONE @$server 
    echo " "
done
