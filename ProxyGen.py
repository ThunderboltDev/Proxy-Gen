import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import os
import socket

ip = requests.get("https://api.ipify.org/").text

hostname = socket.gethostname()
os.system(f"title Log In As: {hostname}")

url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

response = requests.get(url)

proxyfilename = "proxies"

if response.status_code == 200:
    proxies = response.text.split("\r\n")
    print(f"Found {len(proxies)} proxies:")
    with open(f"{proxyfilename}.txt", "w") as f:
        f.write("\n".join(proxies))
    print(f"Proxies saved to '{proxyfilename}.txt'")
else:
    print("Failed to get proxies :(")
    sys.exit()

logo = f"""
 ▐▄▄▄▄• ▄▌ ▄▄▄·▪  ▄▄▄▄▄▄▄▄ .▄▄▄       ▄▄▄·▄▄▄        ▐▄• ▄  ▄· ▄▌.▄▄ · 
  ·███▪██▌▐█ ▄███ •██  ▀▄.▀·▀▄ █·    ▐█ ▄█▀▄ █·▪      █▌█▌▪▐█▪██▌▐█ ▀. 
▪▄ ███▌▐█▌ ██▀·▐█· ▐█.▪▐▀▀▪▄▐▀▀▄      ██▀·▐▀▀▄  ▄█▀▄  ·██· ▐█▌▐█▪▄▀▀▀█▄
▐▌▐█▌▐█▄█▌▐█▪·•▐█▌ ▐█▌·▐█▄▄▌▐█•█▌    ▐█▪·•▐█•█▌▐█▌.▐▌▪▐█·█▌ ▐█▀·.▐█▄▪▐█
 ▀▀▀• ▀▀▀ .▀   ▀▀▀ ▀▀▀  ▀▀▀ .▀  ▀    .▀   .▀  ▀ ▀█▄▀▪•▀▀ ▀▀  ▀ •  ▀▀▀▀
 
  PROXIES FOUND: {len(proxies)} SAVE AS: {proxyfilename}.txt YOUR IP: {ip}

"""
CLEAR = "cls"
os.system(f"{CLEAR}")

print(logo)

proxiestxt = input("Enter Text file name to test: ")

proxiesthread = int(input("Enter Threads: "))

answer = input("Do you want to continue? (y/n): ")

if answer == "y":
    print("Testing Proxys...")
elif answer == "n":
    print("Leaving Program.")
    time.sleep(5)
    sys.exit()
else:
    print("Invalid input. Please enter Y or N.")

def check_proxy(proxy):

    proxies = {'http': proxy, 'https': proxy}
    try:
        response = requests.get('https://www.google.com/', proxies=proxies, timeout=5)
        return True
    except:
        return False

def process_proxy(proxy):

    proxy = proxy.strip()
    if check_proxy(proxy):
        with open('working_proxies.txt', 'a') as f:
            f.write(f'{proxy}\n')
        print(f'{proxy} is working and added to working_proxies.txt \n')
    else:
        print(f'{proxy} is not working \n')

def main():
    try:
        with open(f'{proxiestxt}', 'r') as f:
              proxies = f.readlines()
    except (FileNotFoundError, OSError) as e:
           print(f"Error Enter TXT file name not path! Heres the Error: {str(e)}")
           print(f"Please wait while we exit the program... REASON OF EXITING: {str(e)}")
           time.sleep(5)
           sys.exit()
           pass

    with ThreadPoolExecutor(max_workers=proxiesthread) as executor:
        results = [executor.submit(process_proxy, proxy) for proxy in proxies]

if __name__ == '__main__':
    main()
