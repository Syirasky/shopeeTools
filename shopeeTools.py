import requests
import json
import browser_cookie3
import os
import time
import itertools
import threading
import time
import sys

def animatedLoading():
    chars = "/—\|" 
    for char in chars:
        sys.stdout.write('\r'+'Calculating...'+char)
        time.sleep(.1)
        sys.stdout.flush() 


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def getHeader(url,browserOption):
  cookiesString = ""
  result = {'error':0,'headersDict':""}
  headersDict = {}
  # get shopee cookies from browser .. 
  try:
    if browserOption == 1:
      cookies = list(browser_cookie3.chrome(domain_name='shopee.com.my'))
    elif browserOption == 2:
      cookies = list(browser_cookie3.firefox(domain_name='shopee.com.my'))
    elif browserOption == 3:
      cookies = list(browser_cookie3.edge(domain_name='shopee.com.my'))
    elif browserOption == 4:
      cookies = list(browser_cookie3.opera(domain_name='shopee.com.my'))
    elif browserOption == 5:
      cookies = list(browser_cookie3.brave(domain_name='shopee.com.my'))
    elif browserOption == 6:
      cookies = list(browser_cookie3.chromium(domain_name='shopee.com.my'))
  except:
    print("Error> Cannot use selected browser. Try another browser")
    result['error'] = 1
    result['headersDict'] = ""
    return result
  # dont want this cookies 
  rejectCookies = ["AMP_TOKEN","G_AUTHUSER_H","G_ENABLED_IDPS"]
  # check for cookies length
  cookiesLength = len(cookies)
  if(cookiesLength<0):
    print("Error > (Cookies)")
    exit()
  
  for i in range(len(cookies)):
    if not cookies[i].name in rejectCookies:
      cookiesString+= cookies[i].name+"="+cookies[i].value+"; "
  # print("cookiesString below")      
  # print(cookiesString)
  #process header here .. set the header 
  headersDict['authority'] = 'shopee.com.my'
  headersDict['method'] = 'GET'
  headersDict['path'] = url
  headersDict['scheme'] = 'https'
  headersDict['accept'] =  '*/*'
  headersDict['accept-encoding'] = 'gzip, deflate, br'
  headersDict['accept-language'] = 'en-GB,en-US;q=0.9,en;q=0.8,fil;q=0.7'
  headersDict['cookie'] = cookiesString
  headersDict['if-none-match-'] = ''
  headersDict['referer'] = 'https://shopee.com.my/user/purchase/?type=3'
  headersDict['sec-ch-ua'] ='"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
  headersDict['sec-ch-ua-mobile'] = '?0'
  headersDict['sec-fetch-dest'] = 'empty'
  headersDict['sec-fetch-mode'] = 'cors'
  headersDict['sec-fetch-site'] = 'same-origin'
  headersDict['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
  headersDict['x-api-source'] = 'pc'
  headersDict['x-requested-with'] = 'XMLHttpRequest'
  headersDict['x-shopee-language'] = 'en'

  result['error']= 0
  result['headersDict']= headersDict
  
  return result

def processResponseData(dataDict):
  #check for error .. 
  if dataDict['error'] == 19:
    cls()
    print("Error > Problem with browser or the login. Hurm not sure ..")
    return [0,-1]
  elif dataDict['error'] != 0:
    cls()
    print("Error > Unknown error")
    return [0,-1]
  # processedData ['totalPaid','offset']
  processedData = {} 
  #check for the next offset  .. the server send -1 if no more items 
  offset = dataDict['data']['next_offset']
  #set the empty data item
  itemDetailsDict = {}
  #set item price by default 0 
  totalItemPrice = 0
  itemPrice = 0
  if(offset == -1):
    return [itemPrice,-1]

  #process for the items details 
  # print(dataDict)
  if len(dataDict['data']['order_data']['details_list']) == 0:
    return [itemPrice,-1]
  else:
    itemDetailsDict = dataDict['data']['order_data']['details_list']
    
  for i in range(len(itemDetailsDict)):
    if itemDetailsDict[i]['status']['status_label']['text'] == 'label_order_completed':
      
      itemPrice = itemDetailsDict[i]['info_card']['final_total']
      itemPrice = int(str(itemPrice)[0:-3])
      
      totalItemPrice = totalItemPrice + itemPrice

  return [totalItemPrice,offset]

def print_menu():
  menu_options = {
    1: 'Chrome (not sure if it works now)',
    2: 'Firefox',
    3: 'Edge',
    4: 'Opera',
    5: 'Brave',
    6: 'Chromium',
    0: 'Exit'
    }
    
  print("---------------ShopeeTools---------------")
  print("Before you continue, make sure that you logged in to shopee.com.my")
  print()
  for key in menu_options.keys():
        print (key, '--', menu_options[key] )
  return

def runProcess(optionSelected):
  cls()
  browserOption = optionSelected
  responseList = {}
  totalCalculated = 0
  nextOffset = 0
  processedData = {}
  totalCalculatedPrice = 0
  extraStr = ""
  # print("Calculating the damage from shopee")
  payload={}
  loop = 1
  print("Process started..")
  
  while nextOffset >= 0:
    if loop == 1:
      print("Silo tunggu.. just a few seconds")
    url = "https://shopee.com.my/api/v4/order/get_all_order_and_checkout_list?limit=5&offset="+str(nextOffset)
    headers = getHeader(url,browserOption)['headersDict']
    response = requests.request("GET", url, headers=headers, data=payload)
    responseList = response.json()
    processedData = processResponseData(responseList)
    nextOffset = processedData[1]
    totalCalculated = processedData[0] + totalCalculated
    # print("Total Calculated for now : " + str(processedData[0]) + " , iteration : " + str(loop))
    loop = loop + 1
    # im scared shopee detect we requesting to much so i should limit to at least 1 sec
    if loop > 20:
      time.sleep(1)
  
  return totalCalculated

def testFunction(optionSelected):
  time.sleep(2)
  i = 0
  while i == 2:
    i = i + 1

  return 100.00

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return
    
    def is_alive(self):
        return threading.Thread.is_alive(self)

def main():
  optionArray = [1,2,3,4,5,6]
  totalCalculated = 0;
  while(True):
    cls()
    print_menu()
    
    try : 
      option = int(input('Select the browser used: '))
    except ValueError:
       print("Not a number! Try again.")
       continue
    


    if option in optionArray:
      browseroption = option
      
      # define the thread ..
      threadProcess = ThreadWithReturnValue(name='runProcess', target=runProcess, args=(browseroption,))
      threadProcess.start()
      
      # check if thread still running .. if not then exit and get the result 
      while threadProcess.is_alive():
        animatedLoading()
      cls()

      totalCalculated = threadProcess.join()
      
      if totalCalculated > 1000000 and totalCalculated < 2000000:
        extraStr = "Beli gapo banyok tu"
      elif totalCalculated > 2000000:
        extraStr = "banyak weh pitih. tolong bank in ko ambo"
      elif totalCalculated > 100000 and totalCalculated < 1000000:
        extraStr = "Okay la tu"
      elif totalCalculated < 100000:
        extraStr = "ANDA ADALAH INSAN TERPILIH. Pandai berjimat"
      totalCalculatedPrice = str(totalCalculated)[0:-2] +"."+ str(totalCalculated)[-2:]
      print('Total Spent = RM ' + str(totalCalculatedPrice))
      print(extraStr)
      os.system("pause")

    elif option == 0:
        print('Thanks for using my simple program :D')
        os.system("pause")
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 6.')
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
