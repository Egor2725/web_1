import requests

url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
response = requests.get(url).json()
money_list=[]

def show_money():
    
    for item in list(response):
        money= f"1 {item['Cur_Abbreviation']} = {item['Cur_OfficialRate']} BYN"
        money_list.append(money)   
    return money_list





