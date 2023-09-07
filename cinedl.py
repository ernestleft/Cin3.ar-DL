import base64
import os
import requests
import subprocess
import re

# LOGIN

loginurl = "https://id.cine.ar/v1.5/auth/login"
logintoken = ""
email = ""
password = ""
userid = ""
dlid = ""
dltitle = ""
dltype = ""

if os.path.exists("tkn.txt"):
    f = open("tkn.txt", "r")
    logintoken = f.read()
    print("Already logged in.")
else:
    print("Welcome to cine.ar downloader.")
    email = input("Please enter your email: ")
    password = input("Please enter your cine.ar password: ")
    payload = "{{\"email\":\"{}\",\"password\":\"{}\"}}".format(email, password)
    headers = {
        'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'id.cine.ar'
    }
    response = requests.request("POST", loginurl, headers=headers, data=payload)
    #print(response.text)
    regex = r"\"token\":\"(.*?)\""
    matches = re.finditer(regex, response.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        logintoken = match.group(1)
    f = open("tkn.txt", "w")
    f.write(logintoken)
    
    #print(logintoken)
    print("Logged in successfully.")

# get profile id

userurl = "https://play.cine.ar/api/v1.7/user"

userpayload = {}
userheaders = {
  'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
  'Accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'Authorization': 'Bearer {}'.format(logintoken),
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'play.cine.ar'
}
#print(userheaders)

userresponse = requests.request("GET", userurl, headers=userheaders, data=userpayload)

userregex = r"\"id\":\"(.*?)\""
matches = re.finditer(userregex, userresponse.text, re.MULTILINE)
for matchNum, match in enumerate(matches, start=1):
    userid = match.group(1)

print("Enter url of the content you want to download.")
dlurl = input("URL: ")
dlregex = r"cine.ar\/INCAA\/produccion\/(\d{3,5})"
matches = re.finditer(dlregex, dlurl, re.MULTILINE)
for matchNum, match in enumerate(matches, start=1):
    dlid = match.group(1)

print("Downloading element with id {}.".format(dlid))

# is Series or movie?

reqtitle = ""
reqtempo = ""
reqcapi = ""
reqid = ""
reqyear = ""

requrl = "https://play.cine.ar/api/v1.7/INCAA/prod/{}?perfil={}".format(dlid, userid)

reqpayload = {}
reqheaders = {
  'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
  'Accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'Authorization': 'Bearer {}'.format(logintoken),
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty'
}

reqresponse = requests.request("GET", requrl, headers=reqheaders, data=reqpayload)
reqregex = r"\"tipos\":\[{\"text\":\"(.*?)\","

matches = re.finditer(reqregex, reqresponse.text, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    dltype = match.group(1)

if dltype == "Series":
    seriestitle = ""
    print("This is a series. Collecting chapters...")
    yearregex = r"\"an\":\"(\d{3,5})\""
    matches = re.finditer(yearregex, reqresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        reqyear = match.group(1)
    serietitleregex = r"\"fotos\":\[\"\w{24,27}\"\],\"tit\":\"(.*?)\","
    matches = re.finditer(serietitleregex, reqresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        seriestitle = match.group(1)
    chapterregex = r"\"tags\":\[\"\w{3,7}\"\],\"tit\":\"(.*?)\",\"tempo\":(\d{1,3}),\"capi\":(\d{1,3}),\"sid\":(\d{2,5})}"
    matches = re.finditer(chapterregex, reqresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        reqtitle = match.group(1)
        reqtempo = match.group(2)
        reqcapi = match.group(3)
        reqid = match.group(4)
        dlurl = "https://player.cine.ar/odeon/?i={}&p={}&s=INCAA&t={}".format(reqid, userid, logintoken)
        dlbaseurl = "https://player.cine.ar/odeon/"
        dlblockurl = ""

        dlpayload = {}
        dlheaders = {
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'iframe',
            'host': 'player.cine.ar',
            'Referer': 'https://play.cine.ar/'
        }
        dlresponse = requests.request("GET", dlurl, headers=dlheaders, data=dlpayload)
        dlregex1 = r"window.arsatPlayer.prodUrlEncoded = '(.*?)'"
        matches = re.finditer(dlregex1, dlresponse.text, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            dlblockurl = match.group(1)
        dwnlurl = "https://player.cine.ar/odeon/{}".format(dlblockurl)
        downlurl = ""
        dwnlpayload = {}
        dwnlheaders = {
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'host': 'player.cine.ar'
        }

        dwnlresponse = requests.request("GET", dwnlurl, headers=dwnlheaders, data=dwnlpayload)
        #print(dwnlresponse.text)
        dwnlregex = (r"RESOLUTION=\d{3,5}x720,CLOSED-CAPTIONS=NONE\n"
            r"data:application\/x-mpegurl;base64,([\s\S]+)")
        matches = re.finditer(dwnlregex, dwnlresponse.text, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            downlurl = match.group(1)
        #print(downlurl)

        # Decode the base64 string
        decoded_data = base64.b64decode(downlurl)

        # Write the file

        with open('decoded_file.m3u8', 'wb') as f:
            f.write(decoded_data)
            f.close()

        print("{}. {} - Season {} - Episode {}".format(matchNum, reqtitle, reqtempo, reqcapi))
        command = r'"N_m3u8DL" "decoded_file.m3u8" --workDir "C:\Downloads" --saveName "{}-{}-{}-S{}-E{}-720p" --headers "Accept:*%2f*|Accept-Language:en%2ces-ES%3bq%3d0.9%2ces%3bq%3d0.8|Connection:keep-alive|Origin:https%3a%2f%2fplayer.cine.ar|Referer:https%3a%2f%2fplayer.cine.ar%2f|Sec-Fetch-Dest:empty|Sec-Fetch-Mode:cors|Sec-Fetch-Site:cross-site|User-Agent:Mozilla%2f5.0%20%28Windows%20NT%2010.0%3b%20Win64%3b%20x64%29%20AppleWebKit%2f537.36%20%28KHTML%2c%20like%20Gecko%29%20Chrome%2f114.0.0.0%20Safari%2f537.36|sec-ch-ua:%22Not.A%2fBrand%22%3bv%3d%228%22%2c+%22Chromium%22%3bv%3d%22114%22%2c+%22Google%20Chrome%22%3bv%3d%22114%22|sec-ch-ua-mobile:%3f0|sec-ch-ua-platform:%22Windows%22" --enableDelAfterDone --disableDateInfo --enableMuxFastStart'.format(seriestitle, reqtitle, reqyear, reqtempo, reqcapi)
        subprocess.run(command, shell=True)
        #delete file decoded_file.m3u8
        os.remove("decoded_file.m3u8")
        

else:
    print("This is a movie.")
    yearregex = r"\"an\":\"(\d{3,5})\""
    matches = re.finditer(yearregex, reqresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        reqyear = match.group(1)
    # get video

    dlurl = "https://player.cine.ar/odeon/?i={}&p={}&s=INCAA&t={}".format(dlid, userid, logintoken)
    dlbaseurl = "https://player.cine.ar/odeon/"
    dlblockurl = ""

    dlpayload = {}
    dlheaders = {
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'iframe',
    'host': 'player.cine.ar',
    'Referer': 'https://play.cine.ar/'
    }

    dlresponse = requests.request("GET", dlurl, headers=dlheaders, data=dlpayload)
    #print(dlresponse.text)

    dlregex1 = r"window.arsatPlayer.prodUrlEncoded = '(.*?)'"
    matches = re.finditer(dlregex1, dlresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        dlblockurl = match.group(1)
    #print(dlblockurl)
    titleregex = r"window.arsatPlayer.prodTitle = '(.*?)'"
    matches = re.finditer(titleregex, dlresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        dltitle = match.group(1)

    dwnlurl = "https://player.cine.ar/odeon/{}".format(dlblockurl)
    downlurl = ""
    dwnlpayload = {}
    dwnlheaders = {
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'host': 'player.cine.ar'
    }

    dwnlresponse = requests.request("GET", dwnlurl, headers=dwnlheaders, data=dwnlpayload)
    #print(dwnlresponse.text)
    dwnlregex = (r"RESOLUTION=\d{3,5}x720,CLOSED-CAPTIONS=NONE\n"
        r"data:application\/x-mpegurl;base64,([\s\S]+)")
    matches = re.finditer(dwnlregex, dwnlresponse.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        downlurl = match.group(1)
    #print(downlurl)

    # Decode the base64 string
    decoded_data = base64.b64decode(downlurl)

    # Write the file

    with open('decoded_file.m3u8', 'wb') as f:
        f.write(decoded_data)
        f.close()

    command = r'"N_m3u8DL" "decoded_file.m3u8" --workDir "C:\Downloads" --saveName "{}-{}-720p" --headers "Accept:*%2f*|Accept-Language:en%2ces-ES%3bq%3d0.9%2ces%3bq%3d0.8|Connection:keep-alive|Origin:https%3a%2f%2fplayer.cine.ar|Referer:https%3a%2f%2fplayer.cine.ar%2f|Sec-Fetch-Dest:empty|Sec-Fetch-Mode:cors|Sec-Fetch-Site:cross-site|User-Agent:Mozilla%2f5.0%20%28Windows%20NT%2010.0%3b%20Win64%3b%20x64%29%20AppleWebKit%2f537.36%20%28KHTML%2c%20like%20Gecko%29%20Chrome%2f114.0.0.0%20Safari%2f537.36|sec-ch-ua:%22Not.A%2fBrand%22%3bv%3d%228%22%2c+%22Chromium%22%3bv%3d%22114%22%2c+%22Google%20Chrome%22%3bv%3d%22114%22|sec-ch-ua-mobile:%3f0|sec-ch-ua-platform:%22Windows%22" --enableDelAfterDone --disableDateInfo --enableMuxFastStart'.format(dltitle, reqyear)
    subprocess.run(command, shell=True)
    #delete file decoded_file.m3u8
    os.remove("decoded_file.m3u8")

print("Done.")
