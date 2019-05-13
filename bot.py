# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
n=0
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

em_alive='🦠'
em_dead='⬛️'

games={}

@bot.message_handler(commands=['life'])
def life(m):
    game=creategame(m.chat.id)
    game['code']['world']['00']='alive'
    game['code']['world']['01']='alive'
    game['code']['world']['10']='alive'
    games.update(game)
    startgame(game['code'])

    
def startgame(game):
    text=''
    x=0
    y=0
    global em_alive
    global em_dead
    while y<int(game['size'][0]):
        x=0
        while x<int(game['size'][1]):
            cpoint=str(x)+str(y)
            if game['world'][cpoint]=='alive':
                text+=em_alive
            else:
                text+=em_dead
            x+=1
        y+=1
        text+='\n'
    if game['msg']==None:
        game['msg']=bot.send_message(game['id'], text)
    else:
        medit(text, game['msg'].chat.id, game['msg'].message_id)
    
    mapedit(game)
    
    
def mapedit(game):
    alive=[]
    dead=[]
    for ids in game['world']:
        x=int(ids[0])
        y=int(ids[1])
        nearalive=0
        i1=-1
        i2=-1
        while i1<=1:
            i2=-1
            while i2<=1:
                point=str(x+i1)+str(y+i2)
                try:
                    if game['world'][point]=='alive' and point!=ids:
                        nearalive+=1
                except:
                    #bot.send_message(441399484, traceback.format_exc())
                    pass
                i2+=1
            i1+=1
        if game['world'][ids]=='alive':
            if nearalive>=2 and nearalive<=3:
                alive.append(ids)
            else:
                dead.append(ids)
                
        elif game['world'][ids]=='dead':
            if nearalive==3:
                alive.append(ids)
            else:
                dead.append(ids)
    for ids in dead:
        game['world'][ids]='dead'
    for ids in alive:
        game['world'][ids]='alive'
        
    if len(alive)!=0:
        t=threading.Timer(game['speed'], startgame, args=[game])
        t.start()
    
    
def creategame(chatid, size='77', speed=1):   # x = size[0];  y = size[1];   speed в секундах.
    global n
    n+=1
    world={}
    x=0
    y=0
    while x<int(size[0]):
        y=0
        world.update({str(x)+str(y):'dead'})
        while y<int(size[1]):
            world.update({str(x)+str(y):'dead'})
            y+=1
        x+=1
    return {n:{
        'id':chatid,
        'world':world,
        'size':size,
        'speed':speed,
        'msg':None,
        'code':n
    }
           }

    
    
    
    
print('7777')
bot.polling(none_stop=True,timeout=600)

