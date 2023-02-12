import requests
import hashlib
import time


def send_whatsapp_message(message):
    account_sid = 'AC4426e3a608e065f77c5e074ddf6af60a'
    auth_token = '42288aeb8a6ba714864191cd1fe3415f'
    group_id = "1238432"
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    payload = {
        "From": f"whatsapp:{+14155238886}",
        "To": f"whatsapp:{+XXXXXXXXXXXX}",
        "Body": "Yeni Bir Deprem Oldu"
    }

    response = requests.post(url, auth=(account_sid, auth_token), data=payload)

    if response.status_code != 201:
        print(f"Error sending message: {response.text}")
        return False
    
    return True


def check_for_new_posts(previous_posts_hash):
   
    response = requests.get("http://www.koeri.boun.edu.tr/scripts/lst2.asp")
    html_content = response.text

    current_hash = hashlib.md5(html_content.encode()).hexdigest()

    if current_hash != previous_posts_hash:


   
       start_index = html_content.index("<pre>")
       end_index = html_content.index("</pre>")
       pre_content = html_content[start_index + 5: end_index]
       last_line = pre_content.split("\n")[-1]

    current_posts_hash = hash(last_line)
    if current_posts_hash != previous_posts_hash:
        send_whatsapp_message(last_line)
        previous_posts_hash = current_posts_hash

    return previous_posts_hash

previous_posts_hash = ""
while True:
    previous_posts_hash = check_for_new_posts(previous_posts_hash)
    time.sleep(60)  
