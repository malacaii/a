import socketio
import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
import asyncio
from functools import cache
from datetime import datetime
import pytz
from discord import SyncWebhook, Embed
import os
import json
import traceback
from threading import Thread
import time
snd = "vergas"
webhook_url = "https://discord.com/api/webhooks/1130555491546824705/VlmmzVZZwMoJl9mDEKYr2LDRAzTeJV6A8pocYRR_vH7PYkLE5p30HIpCprX51LxzMmjw"
webhook = SyncWebhook.from_url(webhook_url)
webhook2 = SyncWebhook.from_url(webhook_url)
webhookconnect = SyncWebhook.from_url(webhook_url)
webhookconnect2 = SyncWebhook.from_url(webhook_url)
webhook_update = SyncWebhook.from_url(webhook_url)
webhook_update2 = SyncWebhook.from_url(webhook_url)
tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')
sio = socketio.AsyncServer()
app = web.Application()
connected_clients = set()
connected_bots = set()
connected_bots_buy = set()
client_ips = {}
bot_ips = {}
bot_name = {}


def update_stats():
  i = 0
  while 1:
    i += 1
    if i == 10:
      i = 0
      try:
        embed = Embed(title="isai sniper all:", color=0xb0fcff)
        embed.add_field(name="Total bots online:",
                        value=f"{len(connected_clients)}",
                        inline=False)

        webhook_update.send(embed=embed)
        webhook_update2.send(embed=embed)
      except:
        pass
    time.sleep(1)


def update_run():
  t = Thread(target=update_stats)
  t.start()


blacklist = [1375927274,13610948761,13602628266,13979169103]
update_run()

with open("limited.txt") as f:
  items = f.readlines()

@cache
class sever:
    # Configure Jinja2 template rendering
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
    
    try:
    
      @sio.event
      async def connect(sid, environ):
        datetime_VN = datetime.now(tz_VN)
        global request
        request = environ['aiohttp.request']
        client_ip = request.headers['X-Forwarded-For'].split(',')[-1].strip()
        headers = request.headers
        data = json.loads(headers.get("full", "{}"))
        if any(value is None for value in [data.get("cookie"), client_ip, data.get("checking_cookie")]): await sio.disconnect(sid)
        if "x":
            with open("database.json", "r") as f: reak = json.loads(f.read())
            reak.update({
              snd: {
                "buy_cookie": data.get(""),
                "checking_cookie": data.get("")
              }
            })
            with open("database.json", "w") as f: json.dump(reak, f, indent=1)
        if len(connected_clients) >= 500:
          sio.disconnect(sid)
        connected_clients.add(sid)
        client_ips[sid] = client_ip
        print(datetime_VN.strftime("%m/%d/%Y, %H:%M:%S"),
              ': Client connected at IP:', client_ip)
        print('Total clients online:', len(connected_clients), '\n')
        return
    
      @sio.event
      async def disconnect(sid):
        datetime_VN = datetime.now(tz_VN)
        timenow = datetime_VN.strftime("%m/%d/%Y, %H:%M:%S")
        if sid in connected_clients:
          print(timenow, ': Client disconnected IP:', client_ips[sid])
          connected_clients.remove(sid)
          client_ips.pop(sid, None)
          print('Total clients online:', len(connected_clients), '\n')
        if sid in connected_bots:
          print(timenow, f': Bot {bot_name[sid]} disconnected IP:', bot_ips[sid])
          embed = Embed(title=f"Bot {bot_name[sid]} dead please rescue",
                        color=0xb0fcff)
          embed.add_field(name=f"Bot ip: {bot_ips[sid]}", value="", inline=True)
          embed.add_field(name=f"Disconnected time: {timenow}",
                          value="",
                          inline=True)
          webhook.send(embed=embed)
          webhook2.send(embed=embed)
          connected_bots.remove(sid)
          bot_ips.pop(sid, None)
          bot_name.pop(sid, None)
          print('Total bots online:', len(connected_bots), '\n')
        if sid in connected_bots_buy:
          print(timenow, f': Bot {bot_name[sid]} disconnected IP:', bot_ips[sid])
          embed = Embed(title=f"Bot {bot_name[sid]} dead please rescue",
                        color=0xb0fcff)
          embed.add_field(name=f"Bot ip: {bot_ips[sid]}", value="", inline=True)
          embed.add_field(name=f"Disconnected time: {timenow}",
                          value="",
                          inline=True)
          webhook.send(embed=embed)
          webhook2.send(embed=embed)
          connected_bots_buy.remove(sid)
          bot_ips.pop(sid, None)
          bot_name.pop(sid, None)
          print('Total bots buy online:', len(connected_bots_buy), '\n')
    
      @sio.event
      async def bot_buy_connected(sid, name):
        connected_clients.remove(sid)
        client_ips.pop(sid, None)
        datetime_VN = datetime.now(tz_VN)
        timenow = datetime_VN.strftime("%m/%d/%Y, %H:%M:%S")
        bot_ip = None
        if 'X-Forwarded-For' in request.headers:
          bot_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
        else:
          transport = request.transport
          if transport is not None:
            bot_ip = transport.get_extra_info('peername')[0]
        print(timenow, f': Bot {name} connected at IP:', bot_ip)
        connected_bots_buy.add(sid)
        bot_ips[sid] = bot_ip
        bot_name[sid] = name
        embed = Embed(title=f"Bot {bot_name[sid]} Connected", color=0xb0fcff)
        embed.add_field(name=f"Bot ip: {bot_ips[sid]}", value="", inline=True)
        embed.add_field(name=f"Connected time: {timenow}", value="", inline=True)
        webhookconnect.send(embed=embed)
        webhookconnect2.send(embed=embed)
        print('Total bots buy online:', len(connected_bots_buy), '\n')
    
      @sio.event
      async def bot_connected(sid, name):
        connected_clients.remove(sid)
        client_ips.pop(sid, None)
        datetime_VN = datetime.now(tz_VN)
        timenow = datetime_VN.strftime("%m/%d/%Y, %H:%M:%S")
        bot_ip = None
        if 'X-Forwarded-For' in request.headers:
          bot_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
        else:
          transport = request.transport
          if transport is not None:
            bot_ip = transport.get_extra_info('peername')[0]
        print(timenow, f': Bot {name} connected at IP:', bot_ip)
        connected_bots.add(sid)
        bot_ips[sid] = bot_ip
        bot_name[sid] = name
        embed = Embed(title=f"Bot {bot_name[sid]} Connected", color=0xb0fcff)
        embed.add_field(name=f"Bot ip: {bot_ips[sid]}", value="", inline=True)
        embed.add_field(name=f"Connected time: {timenow}", value="", inline=True)
        webhook.send(embed=embed)
        webhook2.send(embed=embed)
        print('Total bots online:', len(connected_bots), '\n')
    
      @aiohttp_jinja2.template('index.html')
      async def index(request):
        return {}
    
      @sio.event
      async def new_item(sid, item_info):
        print(f"detected {item_info['name']}")
        if str(item_info['id']) + '\n' in items:
          await sio.emit('add_new_item',
                         item_info['id'],
                         room=list(connected_bots))
        else:
          items.append(str(item_info['id']) + '\n')
          with open("limited.txt", "a") as f:
            f.write(str(item_info['id']) + '\n')
          if connected_bots:
            await sio.emit('add_new_item',
                           item_info['id'],
                           room=list(connected_bots))
    
          await sio.emit('new_item_send', item_info, room=list(connected_clients))
    
      @sio.event
      async def new_item_buy(sid, item_data):
        if item_data[1]['id'] in blacklist:
          return
        print(f"new item found {item_data[1]['name']}")
        if connected_clients:
          asyncio.create_task(sio.emit('newitemfound', item_data, room=list(connected_clients)))
    
      @sio.event
      async def new_item_buyV2(sid, item_data):
        if item_data['AssetId'] in blacklist:
          return
        if item_data['PriceInRobux'] > 10:
          blacklist.append(item_data['AssetId'])
          return
        print(f"new item found {item_data['Name']} {item_data['AssetId']}")
        if connected_clients:
          asyncio.create_task(sio.emit('newitemfoundv2', item_data, room=list(connected_clients)))
    
      @sio.event
      async def new_item_buy1(sid, item_data):
        if item_data['id'] in blacklist:
          return
        print(f"new item found {item_data['name']}")
        if connected_clients:
          asyncio.create_task(sio.emit('newitemfound1', item_data, room=list(connected_clients)))
    
      @sio.event
      async def chat_message(sid, data):
        print(data)
        await sio.emit('chat_message', data)
    
      async def socketio_handler(request):
        if request.method == 'POST' or request.method == 'GET':
          data = await request.json() if request.method == 'POST' else dict(
            request.query)
          await sio.emit('chat_message', data)
          return web.Response(text='Data received and sent to clients!')
        else:
          return web.Response(status=404)

      
      async def handle(request):
        url = ""
        headers = request.headers
        fromd = headers.get("from")
        price = headers.get("price")
        serial = headers.get("serial")
        account = headers.get("account")
        item = headers.get("item")
        item_id = headers.get("item_id")
        if any(value is None for value in [item_id, fromd, price, serial, account, item]):
          return web.Response(text="One or more header values are missing.")
        embed = {
        'title': f"{account} Bought {item}",
        'url': f"https://web.roblox.com/catalog/{item_id}",
        'color': 0xb0fcff,
        'fields': [
            {'name': f"From: {fromd}", 'value': '', 'inline': False},
            {'name': f"price: {price}", 'value': '', 'inline': False},
            {'name': f"serial: {serial}", 'value': '', 'inline': False}
        ],
        'footer': {
            'text': 'Mal Sniper',
            'icon_url': 'https://cdn.discordapp.com/attachments/994101761335889930/1131243811209760848/image.png'
        }
        }
        while True:
         async with aiohttp.ClientSession() as session:
          async with session.post(url, json={'embeds': [embed]}) as response: 
            if response.status == 429: continue
            break
        return web.Response(text=str(response.status))

      async def version(request):
        vers = "vergalarga 1.01"
        print("versionvergas")
        return web.Response(text=vers)
      sio.attach(app)
      app.router.add_route('GET', '/', index)
      app.router.add_route('POST', '/web', handle)
      app.router.add_route('GET', '/vers', version)
      app.router.add_route('*', '/{path_info:.*}', socketio_handler)
      web.run_app(app, host='0.0.0.0', port=8080, ssl_context=None)
    except:
      traceback.print_exc()

sever = sever()
