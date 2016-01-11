#!/usr/bin/python

import requests, json, hashlib, hmac, bcrypt, base64

class AlteryxAPI:

	def __init__(self, url):
		self.url = url
		self.user = ''
		self.sessionID = ''
		self.headers = ''

	def login(self, uid, pwd):
		payload = {"scheme":"alteryx","parameters":[{"name":"email","value":uid}]}
		headers = {'content-type': 'application/json; charset=utf-8'}

		r = requests.post(self.url + "/api/auth/preauth/", data = json.dumps(payload), headers = headers).json()

		hmacKey = salt = nonce = ''
		for param in r[u'parameters']:
			if param[u'name'] == 'hmacKey':
				hmacKey = param[u'value']
			elif param[u'name'] == 'salt':
				salt = param[u'value']
			elif param[u'name'] == 'nonce':
				nonce = param[u'value']

		salt = bytes(salt).encode('utf-8')
		pwd = bytes(pwd).encode('utf-8')
		key = bytes(hmacKey).encode('utf-8')

		hashed = hmac.new(key, pwd, hashlib.sha256).hexdigest()
		hashed = bcrypt.hashpw(hashed, salt)
		hashed = hmac.new(key, nonce + '_' + hashed, hashlib.sha256).hexdigest()

		payload = {"scheme":"alteryx","parameters":[{"name":"email","value":uid},{"name":"password","value" : hashed},{"name":"nonce","value": nonce },{"name":"updateLastLoginDate","value": "true"}]}
		
		self.user = requests.post(self.url + "/api/auth/sessions/", data = json.dumps(payload), headers = headers).json()		
		self.sessionID = self.user[u'sessionId']
		self.headers = {'content-type': 'application/json; charset=utf-8', 'X-Authorization' : 'SPECIAL ' + self.sessionID }

	def logout(self):
		requests.delete(self.url + "/api/auth/sessions/%s/" % self.sessionID, headers = self.headers)

	def executeJob(self, appID, answers):		
		r = requests.post(self.url + "/api/apps/jobs/", data = json.dumps(answers), headers = self.headers).json()
		return r[u'id']

	def getApp(self, appID):
		return requests.get(self.url + "/api/apps/%s/" % appID, headers = self.headers).json()

	def getJobOutput(self, jobID):
		r = requests.get(self.url + "/api/apps/jobs/%s/output/" % jobID, headers = self.headers).json()
		return r[0][u'name']

	def getJobStatus(self, jobID):
		r = requests.get(self.url + "/api/apps/jobs/%s/" % jobID, headers = self.headers).json()
		return r[u'status']	

	def getSubscription(self):
		return requests.get(self.url + "/api/subscription/%s/" % self.user[u'user'][u'subscriptionId'], headers = self.headers).json()

	def renderJobOutput(self, jobID, outputID, format):
		return requests.get(self.url + "/api/apps/jobs/%s/output/%s/?format=%s&sessionId=%s&attachment=false" % (jobID, outputID, format), headers = self.headers)

	
