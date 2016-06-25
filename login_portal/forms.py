from django import forms

class authenticate(forms.Form):
	"""docstring for auth"""
	redir = forms.CharField(label="redir")
	tok = forms.CharField(label="tok")

class PhNo(forms.Form):
	"""docstring for PhNo"""
	mobile_number = forms.CharField(label="Mobile Phone",max_length=10)

class otp_code(forms.Form):
	"""docstring for otp"""
	otp = forms.CharField(label="OTP",max_length=6)