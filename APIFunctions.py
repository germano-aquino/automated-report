import requests
import datetime
import time
import pytz

headers = {'Content-Type': 'application/json-rpc'}
url = 'http://zabbix.net/api_jsonrpc.php'

def login(user, passwd):
	data = {
	'jsonrpc': '2.0',
	'method': 'user.login',
	'params': {
		'user': user,
		'password': passwd
	},
	'id': 1,
	'auth': None
	}
	resp = requests.post(url, headers=headers, json= data)
	return (resp.json()["result"])

def getHostIDbyHostName(authToken, hostName):
	data = {
	'jsonrpc': '2.0',
	'method': 'host.get',
	'params': {
		'filter': {
			'host': hostName
		}
	},
	'id': 2,
	'auth': authToken
	}
	resp = requests.get(url, headers=headers, json= data)
	return (resp.json()["result"][0]["hostid"])

def getGroupIDbyGroupName(authToken, groupName):
	data = {
	'jsonrpc': '2.0',
	'method': 'hostgroup.get',
	'params': {
		'filter': {
			'host': groupName
		}
	},
	'id': 2,
	'auth': authToken
	}
	resp = requests.get(url, headers=headers, json= data)
	return (resp.json()["result"][0]["groupid"])

def getGraphID(authToken, hostID, groupID, graphName):
	data = {
		'jsonrpc': '2.0',
		'method': 'graph.get',
		'params': {
			'output': 'extend',
			'hostid': hostID,
			'groupid': groupID,
			'filter': {
				'name': graphName
			}
		},
		'id': 2,
		'auth': authToken
	}
	resp = requests.get(url, headers=headers, json=data)
	return (resp.json()['result'][0]['graphid'])

def getItemIDbyGraphID(authToken, graphID):
	data = {
		'jsonrpc': '2.0',
		'method': 'graphitem.get',
		'params': {
			'output': 'extend',
			'graphids': graphID
		},
		'id': 2,
		'auth': authToken
	}
	resp = requests.get(url, headers=headers, json=data)
	return (resp.json()['result'][0]['itemid'])

def getMaxNumberOfConnectionInLastWeek(authToken, itemID):
##select timestamp of consult

	vpn = []
	for day in range(1, 8):
		now = datetime.datetime.now()
		lw = now - datetime.timedelta(days=day)
		lw = (str(lw).split(" ")[0]).split("-")
		lastWeek = [int(x) for x in lw]

		dtFrom = datetime.datetime(lastWeek[0], lastWeek[1], lastWeek[2], 0, 0, tzinfo=pytz.timezone('America/Recife'))
		dtTill = datetime.datetime(lastWeek[0], lastWeek[1], lastWeek[2], 23, 59, tzinfo=pytz.timezone('America/Recife'))

		timeFrom = time.mktime(dtFrom.timetuple())
		timeTill = time.mktime(dtTill.timetuple())

	##get history of current ssl conections today
		data = {
			'jsonrpc': '2.0',
			'method': 'history.get',
			'params': {
				'output': 'extend',
				'history': 3,
				'itemids':itemID,
				'time_from': timeFrom,
				'time_till': timeTill
			},
			'id': 2,
			'auth': authToken
		}
		resp = requests.get(url, headers=headers, json=data)
		
		max = 0
		values = resp.json()["result"]
	##getting the maximum vlaue
		for val in values:
			if(max == 0 or max < int(val["value"])):
				max = int(val["value"])
		vpn.append(max)
	vpn.reverse()
	return (vpn)

def getLastWeekTraffic(authToken, itemID):
##select timestamp of consult

	maximum = []
	average = []
	for day in range(1, 8):
		now = datetime.datetime.now()
		lw = now - datetime.timedelta(days=day)
		lw = (str(lw).split(" ")[0]).split("-")
		lastWeek = [int(day) for day in lw]

		dtFrom = datetime.datetime(lastWeek[0], lastWeek[1], lastWeek[2], 9, 0, tzinfo=pytz.timezone('America/Recife'))
		dtTill = datetime.datetime(lastWeek[0], lastWeek[1], lastWeek[2], 17, 0, tzinfo=pytz.timezone('America/Recife'))

		timeFrom = time.mktime(dtFrom.timetuple())
		timeTill = time.mktime(dtTill.timetuple())

	##get history of traffic in port8
		data = {
			'jsonrpc': '2.0',
			'method': 'history.get',
			'params': {
				'output': 'extend',
				'history': 3,
				'itemids':itemID,
				'time_from': timeFrom,
				'time_till': timeTill
			},
			'id': 2,
			'auth': authToken
		}
		resp = requests.get(url, headers=headers, json=data)
		
		max = 0
		values = resp.json()["result"]
	##getting the maximum value and average value

		sum = 0
		for val in values:
			sum += int(val["value"])
			if(max == 0 or max < int(val["value"])):
				max = int(val["value"])
		avg = sum / len(values)
		maximum.append(str(round(max/1000000)) + " Mbps")
		average.append(str(round(avg/1000000)) + " Mbps")
	maximum.reverse()
	average.reverse()
	download = {"CONSUMO MÁX ENLACES INTERNET": maximum, "CONSUMO MÉDIO ENLACES INTERNET": average}
	return (download)

def logout(authToken):
	data = {
	'jsonrpc': '2.0',
	'method': 'user.logout',
	'params': [],
	'id': 2,
	'auth': authToken
	}

	requests.post(url, headers=headers, json= data)