from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
import httplib, urllib2
from bs4 import BeautifulSoup
import string
from .forms import PhNo, otp_code, authenticate
from django.shortcuts import render
from firebase import firebase
import datetime
import subprocess
import sys

no = {
	"ip": "number"
}
auth_dict = {
	'ip' : 'auth'
}

token_dict = {
	'ip' : 'token'
}

redir_dict = {
	'ip' : 'redir'
}
i = 1

class login_portal(object):
	def send_otp(self, request):
		global no
		if request.method == "POST":
			form = otp_code(request.POST)
			if form.is_valid():
				ip = get_ip(request)
				number = no[ip]
				#print form.cleaned_data['resend_otp']
				code = form.cleaned_data['otp']
				print code
				#connection = httplib.HTTPConnection("enterprise.smsgupshup.com")
				req_str = "http://enterprise.smsgupshup.com/apps/TwoFactorAuth/incoming.php?phone=%s&key=xxxxxxxxxxxxx&code=%s" %(number,code)
				html = urllib2.urlopen(req_str).read()
				soup = BeautifulSoup(html)
				otp_response = soup.get_text()
				print otp_response
				match = 'success | 200 | Code matched successfully and user has been verified'
				if otp_response == match:
					database(request)
					COMMAND = 'ndsctl auth %s' %ip
					ssh = subprocess.Popen(["ssh","root@192.168.1.1",COMMAND],
						shell=False,
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE)
					result = ssh.stdout.readlines()
					print result
					resp_str = '<script>alert("You are authenticated");window.location="http://www.google.com";</script>'
					return HttpResponse(resp_str)
				else:
					print "wrong otp"
					return HttpResponseRedirect('/login_portal/error')
			else:
				print "form not valid"
				return HttpResponseRedirect('/login_portal/login/')

		else:
			form = otp_code()
			return render(request,'front_page.html',{'form':form})

	def index(self,request):
		global no
		if request.method=='POST':
			form = PhNo(request.POST)
			if form.is_valid():
				print form.cleaned_data
				phno = form.cleaned_data['mobile_number']
				print phno
				ip = get_ip(request)
				print ip
				#no = form.mobile_number
				no[ip] = "91"+phno
				print no
				number = no[ip]
				print ('%r' %number)
				connection = httplib.HTTPConnection("enterprise.smsgupshup.com")
				req_str = "/apps/TwoFactorAuth/incoming.php?phone=%s&key=xxxxxxxxxxx" %(number)
				print req_str
				connection.request("HEAD",req_str)
				res = connection.getresponse()
				print res.status,res.reason
				return HttpResponseRedirect('/login_portal/pass/')

		else:
			form = PhNo()
			return render(request, 'index.html', {'form': form})

def home(request):
	return render(request,'index.html')

def request_otp(number):
	connection = httplib.HTTPConnection("enterprise.smsgupshup.com")
	req_str = "/apps/TwoFactorAuth/incoming.php?phone=%s&key=8e8d1a29a862c57b3ac2b795cd0de229" %number
	connection.request("HEAD",req_str)
	res = connection.getresponse()
	print res.status, res.reason


def get_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for :
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def get_parameters(request):
#	targetauth = request.GET["authtarget"]
	tokenauth = request.GET["tok"]
	redir_auth = request.GET["redir"]
	ip = get_ip(request)
	info = Modelinfo(authtarget=targetauth,token=tokenauth,redir=redir_auth,ipaddr=ip)
	info.save()
	print Modelinfo.objects.all()
	return HttpResponseRedirect('/login_portal/login/')

def get_redir(request):
	token = request.GET['tok']
	redir = request.GET['redir']
	ip = get_ip(request)
	token_dict[ip] = token
	redir_dict[ip] = redir_dict
	print token
	print redir
	return HttpResponseRedirect('/login_portal/login')

def authenticate(request):
	ip = get_ip(request)
	tokenauth = token_dict[ip]
	redir_url = "http://www.google.com"
	resp_str = '<script>alert("You are authenticated");window.location="http://192.168.1.1:2050/nodogsplash_auth/?redir=%s&tok=%s";</script>' %(redir_url, tokenauth)
	return HttpResponse(resp_str)

def database(request):
	global i
	ip = get_ip(request)
	number = no[ip]
	now = datetime.datetime.now()
	time = now.strftime("%H:%M:%S")
	date = now.strftime("%d/%m/%Y")
	database_var = firebase.FirebaseApplication('https://project-9184156655217525389.firebaseio.com/',None)
	authentication = firebase.FirebaseAuthentication('APppxbcx9R3uVVPEMsuzXOsO3Kdjo8MbGHWvfrQ8','adityabvb@gmail.com')
	database_var.authentication = authentication
	result = database_var.get('/registered', None)
	flag = 1
	count = 1
	print result
	if result==None:
		database_var.put('/registered',1,{"number":number,"ip":ip,"time":time,"date":date,"datetime":now})
		i = 2
	else:
		for x in result:
			if x==None:
				continue
			if x['number']==number and x['ip']==ip:
				result = database_var.put('/registered',count,{"number":number,"ip":ip,"time":time,"date":date,"datetime":now})
				count = count + 1
				flag = 0
				break
			count = count + 1
		if flag:
			result = database_var.put('/registered',count,{"number":number,"ip":ip,"time":time,"date":date,"datetime":now})


def wrongotp(request):
	req_str = "<script>alert('Wrong OTP. Re-enter your mobile number.');window.location='/login_portal/login';</script>"
	return HttpResponse(req_str)
