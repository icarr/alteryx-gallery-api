#!/usr/bin/python

from AlteryxAPI import *

URL = 'http://gallery.alteryx.com'
UID = ''
PWD = ''

APP_ID = '53a1cbb36ac90f0dd07dc56c'
ANSWERS = payload = {"appPackage":{"id":"53a1cbb36ac90f0dd07dc56c"},"appName":"2010_Census_Demographic_Report.yxwz","jobName":"","version":"","userId":"506ef1917ae24a0df09869a8","questions":[{"name":"ReportMethod","answer":"[{\"key\":\"CompareOverview\",\"value\":true}]"},{"name":"Choose from 2010 Geographies","answer":"true"},{"name":"Census Geo Tree","answer":"[\"CBSAMET:14500\"]"}]}

def _main():	
	api = AlteryxAPI(URL)
	api.login(UID, PWD)
	api.getSubscription()
	api.getApp(APP_ID)

	jobID = api.executeJob(APP_ID, ANSWERS)
	status = api.getJobStatus(jobID)

	while status in ['Queued', 'Running']:
		status = api.getJobStatus(jobID)
		print status

	print 'Job [%s] finished with status [%s]' % (jobID, status) 

	if status == "Completed":
		print 'Rendered %s' % api.getJobOutput(jobID)

	api.logout()

_main()
