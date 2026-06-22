from upstox_api.api import *

api_key = 'a76e7550-c54c-4035-8924-141fc0c99cdb'
api_secret = 'gh150tlrhp'
redirect_uri = 'https://pro.upstox.com/'

# s = Session ('a76e7550-c54c-4035-8924-141fc0c99cdb')
# s.set_redirect_uri ('http://localhost:3000/')
# s.set_api_secret ('gh150tlrhp')
# print (s.get_login_url())

# s.set_code ('ANXYN2')
# access_token = s.retrieve_access_token()
# print ('Received access_token: %s' % access_token)

# Authenticate and get Access Token
u = Upstox(api_key=api_key, api_secret=api_secret)
auth_url = u.get_login_url(redirect_uri)
print('Please go to this URL and authorize the application: {}'.format(auth_url))
code = input('Enter the code obtained after authorization: ')
access_token = u.get_access_token(code, redirect_uri)
print('Access Token: {}'.format(access_token))
