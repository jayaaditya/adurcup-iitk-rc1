from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import subprocess
import sys
from firebase import firebase

# Create your views here.
def dash(request):
	COMMAND = 'ndsctl status'
	ssh = subprocess.Popen(["ssh","root@192.168.1.1",COMMAND],
		shell=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	info = result[16].split(' ')
	refine = info[2].split('\n')
	connected_users = refine[0]
	info = result[14].split(' ')
	refine = info[4].split('\n')
	all_users = refine[0]
	info = result[12].split(' ')
	upload = info[2]
	upload_speed = info[5]
	info = result[11].split(' ')
	download = info[2]
	download_speed = info[5]
	database_var = database()
	database_var.put('/general',1,{'connected users':connected_users,'all users':all_users,'download data':download,'upload data':upload,'download speed':download_speed,'upload speed':upload_speed})
	return render(request,'Dashboard/index1.html')

def reboot(request):
	os.system("echo reboot | ssh root@192.168.1.1")
	return HttpResponseRedirect('/dashboard/dash')

def deauth(request):
	ip_client = request.GET["ip"]
	COMMAND = 'ndsctl deauth %s' %ip_client
	ssh = subprocess.Popen(["ssh","root@192.168.1.1",COMMAND],
		shell=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	print result
	return_res = "<script>alert('The user has been blocked');window.location='/dashboard/users';</script>"
	return HttpResponse(return_res)

def allusers(request):
	return render(request,'all.html')

def database():
	database_var = firebase.FirebaseApplication('https://project-9184156655217525389.firebaseio.com/',None)
	database_var.authentication = firebase.FirebaseAuthentication('APppxbcx9R3uVVPEMsuzXOsO3Kdjo8MbGHWvfrQ8','adityabvb@gmail.com')
	return database_var

def check_state(request):
	try:
		ip = request.GET['ip']
	except KeyError:
		return HttpResponse("<script>alert('IP not passed');window.location='/dashboard/dash';</script>")
	COMMAND = 'ndsctl status'
	ssh = subprocess.Popen(["ssh","root@192.168.1.1",COMMAND],
		shell=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	print result
	checkstr = "  IP: %s" %ip
	print checkstr
	for a in result:
		if a.startswith(checkstr):
			index = result.index(a)
			info = result[index+6].split('\n')
			state = info[0]
			req_str = "<script>alert('%s');window.location='/dashboard/dash';</script>" %state
			print req_str
			return HttpResponse(req_str)
	return HttpResponse("<script>alert('User not connected');window.location='/dashboard/dash';</script>")

def show_usage(request):
	try:
		ip = request.GET['ip']
	except KeyError:
		return HttpResponse("<script>alert('IP not passed');window.location='/dashboard/dash';</script>")
	COMMAND = 'ndsctl status'
	ssh = subprocess.Popen(["ssh","root@192.168.1.1",COMMAND],
		shell=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	print result
	checkstr = "  IP: %s" %ip
	print checkstr
	for a in result:
		if a.startswith(checkstr):
			index = result.index(a)
			info = result[index+7].split('\n')
			state = info[0]
			req_str = "<script>alert('%s');window.location='/dashboard/dash';</script>" %state
			print req_str
			return HttpResponse(req_str)
	return HttpResponse("<script>alert('User not connected');window.location='/dashboard/dash';</script>")

	