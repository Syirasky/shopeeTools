import requests
import json
import browser_cookie3
import os
import time
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
    print("Please select installed browser or try again")
    result['error'] = 1
    result['headersDict'] = ""
    return result

  # check for cookies length
  cookiesLength = len(cookies)
  if(cookiesLength<0):
    print("Error > Please make sure the browser installed or make sure that you logged in to shopee.com.my and wait for a few seconds try again")
    exit()
  
  for i in range(len(cookies)):
        cookiesString+= cookies[i].name+"="+cookies[i].value+"; "
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
    print("Error > Please make sure the browser installed or make sure that you logged in to shopee.com.my and wait for a few seconds try again")
    return [0,-1]
  elif dataDict['error'] != 0:
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

  if len(dataDict['data']['details_list']) == 0:
    return [itemPrice,-1]
  else:
    itemDetailsDict = dataDict['data']['details_list']
    
  for i in range(len(itemDetailsDict)):
    if itemDetailsDict[i]['status']['status_label']['text'] == 'label_order_completed':
      
      itemPrice = itemDetailsDict[i]['info_card']['final_total']
      itemPrice = int(str(itemPrice)[0:-3])
      
      totalItemPrice = totalItemPrice + itemPrice

  return [totalItemPrice,offset]


def print_menu():
  menu_options = {
    1: 'Chrome',
    2: 'Firefox',
    3: 'Edge',
    4: 'Opera',
    5: 'Brave',
    6: 'Chromium',
    0: 'Exit'
    }
  for key in menu_options.keys():
        print (key, '--', menu_options[key] )
  return

def runProcess(optionSelected):
  browserOption = optionSelected
  responseList = {}
  totalCalculated = 0
  nextOffset = 0
  processedData = {}
  totalCalculatedPrice = 0
  extraStr = ""
  print("Calculating the damage from shopee")
  payload={}
  loop = 1
  print("Process started..")
  while nextOffset >= 0:
    if loop == 1:
      print("Silo tunggu.. it might take a few seconds")
    url = "https://shopee.com.my/api/v4/order/get_order_list?limit=5&list_type=3&offset="+str(nextOffset)
    headers = getHeader(url,browserOption)['headersDict']
    response = requests.request("GET", url, headers=headers, data=payload)
    responseList = response.json()
    processedData = processResponseData(responseList)
    nextOffset = processedData[1]
    totalCalculated = processedData[0] + totalCalculated
    # print("Total Calculated for now : " + str(processedData[0]) + " , iteration : " + str(loop))
    loop = loop + 1
    # im scared shopee detect we requesting to much so i should limit to at least 1 sec
    if loop > 3:
      time.sleep(1)

  if totalCalculated > 0:
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
  else:
    print('Total Spent = RM 0.00')
    print(extraStr)
    os.system("pause")
  return

def main():
  print("Before you continue, make sure that you logged in to shopee.com.my")
  optionArray = [1,2,3,4,5,6]
  while(True):
    print_menu()
    option = int(input('Select the browser used: '))
    if option in optionArray:
      browseroption = option
      runProcess(browseroption)
    elif option == 0:
        print('Thanks for using my simple program :D')
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 6.')


if __name__ == "__main__":
    main()

