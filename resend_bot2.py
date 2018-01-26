# -*- coding: utf-8 -*-
import linepy
from linepy import *
from akad.ttypes import Message
import json,sys,atexit,datetime

client = LineClient()
#client = LineClient(authToken="Input your token")
client.log("Auth Token : " + str(client.authToken))

channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))

tracer = LinePoll(client)
hello = "Saya Adalah Resend Message Bot.\n Resend Message Akan Muncul Ketika Kalian Mengurungkan Pesan\nInvite Saya Ke Grup Kalian\nTolong Jangan Spam Dengan Bot Ini\nSaya Tidak Mempunyai Command Yg Lain"
admin = "ue4e06387a5cae9fdf8cd018a41b35e98"
my_mid = client.getProfile().mid
msg_dict = {}
bl = ["ue4e06387a5cae9fdf8cd018a41b35e98"]

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("Couldn't read Log data")

#message.createdTime -> 00:00:00
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

#delete log if pass more than 24 hours
def delete_log():
    ndt = datetime.datetime.now()
    for data in msg_dict:
        if (datetime.datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > datetime.timedelta(1):
            del msg_dict[msg_id]


def RECEIVE_MESSAGE(op):
    try:
        msg = op.message
        if msg.toType == 0:
            client.log("[%s]"%(msg._from)+msg.text)
        else:
            client.log("[%s]"%(msg.to)+msg.text)
        if msg.contentType == 0:
            #Save message to dict
            msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
    except Exception as e:        print(e)
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def NOTIFIED_DESTROY_MESSAGE(op):
    try:
        at = op.param1
        msg_id = op.param2
        if msg_id in msg_dict:
            if msg_dict[msg_id]["from"] not in bl:
                client.sendMessage(at,"SentMessage Cancelled.\n\n[Pengirim Yang Mengurungkan Pesan]\n %s\n[]\n %s\n[Detail]\n %s"%(client.getContact(msg_dict[msg_id]["from"]).displayName,dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"])),msg_dict[msg_id]["text"]))
            del msg_dict[msg_id]
        else:
            client.sendMessage(at,"SentMessage Cancelled,Saya Tidak Bisa Mengirim Pesan Anda.\nKarena Anda Mengurungkan Pesan Berupa Sticker\nSorry")
    except Exception as e:
        print(e)
tracer.addOpInterrupt(65, NOTIFIED_DESTROY_MESSAGE)

def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        #Accept invitation only when from an admin
        if my_mid in op.param3:
            if op.param2 == admin:
                client.acceptGroupInvitation(op.param1)
                client.sendMessage(op.param1,hello)
            else:
                client.rejectGroupInvitation(op.param1)
    except Exception as e:
        print(e)
tracer.addOpInterrupt(13, NOTIFIED_INVITE_INTO_GROUP)

def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)

while True:
    tracer.trace()