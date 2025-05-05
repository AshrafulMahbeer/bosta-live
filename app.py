import requests, json, os

host = os.environ['AYNA_HOST']
proxy = json.loads(os.environ['BDPROXY'])

login_url = f"{host}api/authorization/login"
login_data = json.loads(os.environ['LOGIN_DATA'])
login_header = {"Content-Type": "application/json", "Referer": f"{host}authorization"}
login_response = requests.post(login_url, json=login_data, headers=login_header).json()
user_id = login_response.get("user_id","")
operatorId = login_response.get("operatorId","")
access_token = login_response.get("content",{}).get("token",{}).get("access_token","")
device_id = os.environ['DEVICE_ID']

channels_url = f"{host}api/player/channels?language=en&operator_id={operatorId}&device_id={device_id}&density=1&client=browser&platform=web&os=windows"
authorized_header = {"authorization": f"Bearer {access_token}"}
channels_response = requests.get(channels_url, headers=authorized_header).json()
data = []
m3u = "#EXTM3U \n\n## Made with Love By Pr4nto Bhai => https://t.me/pranto_bhai\n\n"
if channels_response["message"]== "Success":
    for channel in channels_response["content"]["data"]:
        channel_info = {"id": channel.get("keyCode",""), "name": channel.get("title",""), "logo": channel.get("image","")}
        stream_url = f'{host}api/player/streams?language=en&operator_id={operatorId}&device_id={device_id}&density=1&client=browser&platform=web&os=windows&media_id={channel.get("id","")}'
        stream_response = requests.get(stream_url, headers=authorized_header).json()
        if stream_response["message"]=="Success":
            channel_info["link"] = stream_response["content"][0]["src"]["url"]
        else:
            channel_info["link"] = ""
        data.append(channel_info)
        print(f'added {channel_info["name"]}')
        m3u += f'#EXTINF:-1 tvg-id="{channel.get("keyCode","")}" tvg-logo="{channel.get("image","")}", {channel.get("title","")}\n{channel_info["link"]}\n\n'
    with open("aynaott.m3u","w") as m3ufile:
        m3ufile.write(m3u)
    with open("aynaott_channel_data.json","w") as channeldata:
        json.dump(data,channeldata,indent=2)
else:
    print("Something is wrong!")
