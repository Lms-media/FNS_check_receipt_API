from urllib.request import urlopen
import requests
import json
from requests.auth import HTTPBasicAuth

#детальная информация по чеку
def get_info():
    fn = input("write fn number (16 digits): ")
    fd = input("write fd number (up to 10 digits): ")
    fp = input("write fp number (up to 10 digits): ")
    number = input("write your phone number: ")
    password = input("write your password: ")
    auth = HTTPBasicAuth(number, password)
    headers = {"Content-type": "application/json", "Accept": "application/json", "Device-Id": "", "Device-OS": ""}
    url_get = "https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/" + fn + "/tickets/" + fd + "?fiscalSign=" + fp + "&sendToEmail=no"
    answer = requests.get(url_get, auth=auth, headers=headers)
    if answer.status_code == 200:
        print(answer.json())
    elif answer.status_code==202:
        answer2 = requests.get(url_get, auth=auth, headers=headers)
        print(answer2.json())
    else:
        print("error: " + str(answer.status_code))
        #406 - чека нет в базе фнс, либо его не существует, либо он слишком старый
        #403 - некорректные данные пользователя
        #500 и 400 - некорректные данные чека

#регистрация
def sign_up():
    email = input("write your email: ")
    number = input("write your phone number: ")
    name = input("write your name: ")
    url_reg = "https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup"
    headers_main = {"Content-type":"application/json", "Accept":"application/json"}
    data = {"email": email, "name": name, "phone": number}
    answer = requests.post(url_reg, data=json.dumps(data), headers=headers_main)
    if answer.status_code==204:
        print("see sms with password")
    else:
        print("error: "+str(answer.status_code))
        #409 - пользователь уже существует
        #500 - номер телефона некорректный
        #400 - адрес электронной почты некорректный

#восстановления пароля
def password():
    url_pass="https://proverkacheka.nalog.ru:9999/v1/mobile/users/restore"
    number = input("write your phone number: ")
    data = {"phone":number}
    headers={"Content-type":"application/json", "Accept":"application/json"}
    answer=requests.post(url_pass, data=json.dumps(data), headers=headers)
    if answer.status_code==204:
        print("see sms with password")
    else:
        print("error: "+str(answer.status_code))
        #404 - пользователь не найден

#логин (неизвестно зачем, но есть)
def login():
    url_login="https://proverkacheka.nalog.ru:9999/v1/mobile/users/login"
    number = input("write your phone number: ")
    password = input("write your password: ")
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    auth = HTTPBasicAuth(number, password)
    answer=requests.get(url_login, auth=auth, headers=headers)
    if answer.status_code==200:
        print(answer.json())
    else:
        print("error: " + str(answer.status_code))
        #403 - некорректные данные пользователя

#проверка существования чека
def check():
    fn = input("write fn number (16 digits): ")
    fd = input("write fd number (up to 10 digits): ")
    fp = input("write fp number (up to 10 digits): ")
    year=input("write year: ")
    month=input("write month number (example: 08): ")
    day=input("write day: ")
    time=input("write time without colon (example: 1036 is 10:36): ")
    sum=input("write sum without point (example: 14590 is 145.90): ")
    number = input("write your phone number: ")
    password = input("write your password: ")
    auth = HTTPBasicAuth(number, password)
    url_check = "https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/"+fn+"/operations/1/tickets/"+fd+"?fiscalSign="+fp+"&date="+year+"-"+month+"-"+day+"T"+time+"&sum="+sum
    headers = {'Content-type': 'application/json', 'Accept': 'application/json', "Device-Id": "", "Device-OS": ""}
    answer = requests.get(url_check, headers=headers, auth=auth)
    if answer.status_code==204:
        print("check exists")
    else:
        print("error"+str(answer.status_code))
        #406 - чека нет в базе фнс, либо его не существует, либо он слишком старый, или если дата/сумма некорректная или не совпадает с датой/суммой, указанной в чеке
        #400 - не указан параметр дата/сумма
print("choose action:\n\nsign up\n\nlogin\n\nrestore password\n\nis there a check\n\ncheck info\n")
action=input()
if action=="sign up":
    sign_up()
elif action=="login":
    login()
elif action=="restore password":
    password()
elif action=="check receipt":
    check()
elif action=="check info":
    get_info()
else:
    print("incorrect input")
