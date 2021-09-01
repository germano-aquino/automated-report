import datetime
import pandas as pd
from APIFunctions import *
#disable proxy env variables: unset $(env | grep -i proxy | cut -d= -f1 | xargs)
#print a json object print(json.dumps(resp.json(), indent=4, sort_keys=True))

##login into zabbix##

authtoken = login('user', 'passwd')

##get hostID from FortiGate 5CTA

hostID = getHostIDbyHostName(authtoken, "FortiGate 5CTA")

##get groupID from 009 Apliances 5CTA

groupID = getGroupIDbyGroupName(authtoken, "009 Apliances 5CTA")

##get graphID by name SSL VPN

sslvpnID = getGraphID(authtoken, hostID, groupID, "SSL VPN")

##get graphItemID
currentSSLConectionsID = getItemIDbyGraphID(authtoken, sslvpnID)

##get number of VPN's connections in last week
VPN = getMaxNumberOfConnectionInLastWeek(authtoken, currentSSLConectionsID)

##get graphID by name Network Traffic port8
port8 = getGraphID(authtoken, hostID, groupID, "Network Traffic port8")

##get graphitemID
downloadID = getItemIDbyGraphID(authtoken, port8)

##get Traffic Information
report = getLastWeekTraffic(authtoken, downloadID)

##setting report Df
report["NR MÁX CONEXÕES SIMULTÂNEAS VPN"] = VPN
ldap = pd.read_csv("vpn.csv", header=None, names=["DATA", "number"], index_col=0, parse_dates=True)

date = []
enlace = []
users = []
for day in range(1,8):
	now = datetime.datetime.now()
	newDate = now - datetime.timedelta(days=day)
	date.append(newDate.strftime("%d/%m/%Y"))
	enlace.append("500 Mbps")
	users.append(int(ldap.loc[date[-1], "number"]))
users.reverse()
date.reverse()

report["DATA"] = date
report["CAPACIDADE TOTAL ENLACES INTERNET"] = enlace
report["NR DE USUÁRIOS VPN CADASTRADOS"] = users
columnsName = ["DATA", "NR DE USUÁRIOS VPN CADASTRADOS", "NR MÁX CONEXÕES SIMULTÂNEAS VPN" ,"CAPACIDADE TOTAL ENLACES INTERNET", "CONSUMO MÉDIO ENLACES INTERNET", "CONSUMO MÁX ENLACES INTERNET"]
report = pd.DataFrame(report, columns=columnsName)

##writing report in csv
report.to_csv("Novas_Estatisticas.csv", index=False)

##logout##
logout(authtoken)
