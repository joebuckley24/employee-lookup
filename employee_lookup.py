import requests
import re
from random import randrange
from getpass import getpass

def main():

	print('NOTE: must be within Partners network for program to work properly.')
	print('If outside the network make sure you connect to VPN before using this program.')
	username = input('Enter your Partners username (e.g. John Doe may have jd89): ')
	password = getpass('Enter Partners password: ')
	user = (username, password)

	if not authenticate(user):
		return 'Unable to authenticate user credentials' 

	employee = ''
	while True:
		employee = input('Enter employee name (Last,First), blank to quit: ')
		if employee == '':
			break

		## TODO add try except block
		print(lookup(employee, user))

	return 'Goodbye'

def authenticate(credentials):
	login_url = 'https://ppd.partners.org/scripts/phsweb.swl?APP=PDPERS&ACTION=MYENTRY'
	response = requests.get(login_url, auth=credentials)
	return response.status_code == 200

def lookup(employee, credentials):
	domain = 'https://ppd.partners.org'

	search_url = domain + '/scripts/phsweb.swl?APP=PDPERS&ACTION=SEARCHRES&SRCHNM=' + employee + '&UseSearchVer=1&SEED=' + str(100 + randrange(900)) + '#top'
	search_page = requests.get(search_url, auth=credentials).content.decode('utf-8')

	## TODO need different term if employee has multiple boxes for phone number
	literal = 'Number</font></TH></TR>\r\n<TR><TD rowspan=1><FONT face=tahoma size=2><a href="(.+?)"'
	search_regex = re.search(literal, search_page).group(1)
	result_url = domain + search_regex.replace('&amp;', '&')

	result_page = requests.get(result_url, auth=credentials).content.decode('utf-8')
	email = re.search('mailto\\:(.+?)"', result_page).group(1)
	return email

if __name__ == '__main__':
	print(main())