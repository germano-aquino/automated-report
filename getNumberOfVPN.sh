#!/bin/bash
PWD=/home/aquino/Documentos/Aquino/Code/zabbixAPI/zabbix-report
PASS=$PWD/.pass.txt
VPN=$(ldapsearch -x -b "ou=Users,dc=vpn5cta,dc=eb,dc=mil,dc=br" -H ldap://10.45.1.176:389 -D "cn=admin,dc=vpn5cta,dc=eb,dc=mil,dc=br" -y $PASS | grep numResponses | cut -d' ' -f3)
VPN=$(echo "$VPN - 2" | bc)
echo -n $(date +"%d/%m/%Y")"," >> $PWD/vpn.csv
echo $VPN >> $PWD/vpn.csv
if [[ $1 = "repeat" ]]
then
	for i in 1 2; do
		echo -n $(date -d "+$i days" +"%d/%m/%Y")"," >> $PWD/vpn.csv
		echo $VPN >> $PWD/vpn.csv
	done
fi