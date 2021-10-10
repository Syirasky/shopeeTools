import requests
import json
import browser_cookie3

def getHeader(url):
  cookiesString = ""
  headersDict = {}
  # get shopee cookies from browser .. chrome 
  cookies = list(browser_cookie3.chrome(domain_name='shopee.com.my'))
  cookiesLength = len(cookies)

  if(cookiesLength<0):
    print("Error > Please login to shopee.com.my by using chrome first.")
    
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

  return headersDict

def processResponseData(dataDict):
  #check for error .. 
  if dataDict['error'] == 19:
    print("Error > Please login to shopee.com.my by using chrome first.")
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

def startCalculation():


  return




def main():
  responseList = {}
  totalCalculated = 0
  nextOffset = 0
  processedData = {}
  totalCalculatedPrice = 0
  print("Calculate the damage from shopee")
  payload={}
  loop = 1
  while nextOffset >= 0:
    url = "https://shopee.com.my/api/v4/order/get_order_list?limit=5&list_type=3&offset="+str(nextOffset)
    headers = getHeader(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    responseList = response.json()
    processedData = processResponseData(responseList)
    nextOffset = processedData[1]
    totalCalculated = processedData[0] + totalCalculated
    # print("Total Calculated for now : " + str(processedData[0]) + " , iteration : " + str(loop))
    loop = loop + 1
  if totalCalculated > 0:
    totalCalculatedPrice = str(totalCalculated)[0:-2] +"."+ str(totalCalculated)[-2:]
    print('Total Spent = RM ' + str(totalCalculatedPrice))
  
if __name__ == "__main__":
    main()

