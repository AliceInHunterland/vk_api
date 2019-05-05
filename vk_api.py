import requests
#import json
#import sys
import datetime
import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import xml.dom.minidom as md


root = ET.Element("Root")


#задаем нужные параметвы считывания(хэштег)
ask = '#дтп'
offset = 0
all_posts = []

count = 1

#информация о записи в поиске по хэштегу
text = requests.get('https://api.vk.com/method/{METHOD_NAME}'
                     .format(METHOD_NAME='newsfeed.search'),
                    params={'q': ask,
                             'count': count,
                             'extended': 1,
                            'access_token':
                            '0d1718b5aad18a5bf2e413c7e3a582e085949d6e18981bc1e87cdd6f15a34e6a7d723c14b98e7f3ab3a54',
                             'v': 'V',
                             'offset': offset
                            }).json()


f = open('C:/Users/Ekaterina/Desktop/rehcs/q.txt', 'w', encoding="utf-8")
l = open('C:/Users/Ekaterina/Desktop/rehcs/l.txt', 'w', encoding="utf-8")
co = open('C:/Users/Ekaterina/Desktop/rehcs/co.txt', 'w', encoding="utf-8")

for i in range(1,count+1):
     
    telo = text['response'][i]['text']
    data = datetime.datetime.fromtimestamp(int(text['response'][i]['date'])).strftime('%Y-%m-%d %H:%M:%S')
    likes_count = text['response'][i]['likes']['count']
    repost_count = text['response'][i]['reposts']['count']
     
    print(telo,data,' ',likes_count,' ',repost_count)
    item_id = text['response'][i]['id']
    owner_id = text['response'][i]['owner_id']
    comments = text['response'][i]['comments']['count']
    print(owner_id)
    print(item_id)
    

    appt = ET.Element("Item")
    root.append(appt)
    
   

    #информация о лайках  
    likers = requests.get('https://api.vk.com/method/{METHOD_NAME}'.format(METHOD_NAME='likes.getList'),
                    params = {'type': 'post',
                            'owner_id': -147119129,
                            'item_id': 9129,
                            'filter': 'likers',
                            'extended' : 1,
                            'access_token':'0d1718b5aad18a5bf2e413c7e3a582e085949d6e18981bc1e87cdd6f15a34e6a7d723c14b98e7f3ab3a54',
                             'v': 'V',
                             'offset': offset
                            }).json()


    #информация о репостах 
    reposters = requests.get('https://api.vk.com/method/{METHOD_NAME}'.format(METHOD_NAME='likes.getList'),
                    params = {'type': 'post',
                            'owner_id': owner_id,
                            'item_id': item_id,
                            'filter': 'copies',
                            'extended' : 1,
                            'access_token':'0d1718b5aad18a5bf2e413c7e3a582e085949d6e18981bc1e87cdd6f15a34e6a7d723c14b98e7f3ab3a54',
                             'v': 'V',
                             'offset': offset
                            }).json()
    

    if type(owner_id) is int:
        owner_id = owner_id*(-1)

# информация о лайкнувших запись
    FIO = requests.get('https://api.vk.com/method/{METHOD_NAME}'.format(METHOD_NAME='users.get'),
                    params = {'user_ids': owner_id,
                            'fields': 'photo_50, city,sex, domain',
                            'v': 'V',
                            'access_token':'0d1718b5aad18a5bf2e413c7e3a582e085949d6e18981bc1e87cdd6f15a34e6a7d723c14b98e7f3ab3a54',
                            'offset': offset
                            }).json()
    print(FIO)
    time.sleep(1) # задержка т.к существуют ограничения вк api
    
    if FIO['response'] != []:
      first_name_post = FIO['response'][0]['first_name']
      last_name_post = FIO['response'][0]['last_name']
      domain = FIO['response'][0]['domain']
    else:
        last_name_post = ''
        first_name_post = ''
        domain = ''
   
    f.write(str(i)+"\n"+str(first_name_post)+" "+str(last_name_post)+"\n"+'https://vk.com/'+str(domain)+'\n'+str(telo)+"\n"+data+"\n"+str(likes_count)+' '+str(repost_count)+' '+str(comments)+"\n\n")
    
    print(last_name_post)
    print(first_name_post)
    print(likers)
    likes_count = likers['response']['count']
   
    Body = ET.SubElement(appt, "Body")
    Body.text = str(telo)
 

    Username = ET.SubElement(appt, "Username")
    Username.text = str(first_name_post)+' '+str(last_name_post)

    UserID = ET.SubElement(appt, "UserID")
    UserID.text = str(domain)

    Confirmed = ET.SubElement(appt, "Confirmed")
    Confirmed.text = "ne ponyatno"
    
    Date = ET.SubElement(appt, "Date")
    Date.text = str(data)
    Request = ET.SubElement(appt, "Request")
    Request = ask

    tags = ET.SubElement(appt, "Tags")
    s=list(telo)
    tag1=''
    for i in range(0, len(s)):
        if s[i] == '#':
            tag1=''
            for j in range(i+1, len(s)):
                if (s[j] != '#') and (s[j] != ' '):
                    tag1 = tag1+s[j]
                else:
                   break            
            tag = ET.SubElement(tags, "Tag")
            tag.text = str(tag1)
      
    details = ET.SubElement(appt, "Details")
    
    emotions = ET.SubElement(details, "Emotions")

    emotion_l = ET.SubElement(emotions, "Emotion")
    emotion_l.set('count', str(likes_count))
    emotion_l.set('type', 'like')
    
   

    

    if likes_count>0:
        time.sleep(0.3)

        for j in range(0,likes_count):
              name = likers['response']['items'][j]['first_name']
              last_name = likers['response']['items'][j]['last_name']
              uid = likers['response']['items'][j]['uid']
              l.write(str(i)+"\n"+str(owner_id)+"_"+str(item_id)+"\n"+name+" "+last_name+"\n")

              userID = ET.SubElement(emotion_l, "userID")
              uid.text = str(uid)
             

          


              repost = ET.SubElement(details, "Reposters")
              repost.set('count',str(repost_count))
              if (repost_count>0)and (reposters['response']['items']!=[]):
                 
                  for k in range(0,repost_count):
                    uid_r = reposters['response']['items'][k]['uid']
                    if uid == uid_r:
                       l.write('reposrer'+"\n\n")
                       
                       repost.text = str(uid_r)
           
              print(uid)


    else:
       print('no likes') 
       l.write(str(i)+"\n"+'no likes'+"\n\n")
# все комментарии к 1 посту

    comment = requests.get('https://api.vk.com/method/{METHOD_NAME}'.format(METHOD_NAME='wall.getComments'),
                    params = 
                    {'type': 'post',
                            'owner_id': owner_id,
                            'post_id': item_id,
                            'need_likes' : 1,
                            'count': 100,
                            'sort': 'abc',
                            'preview_length':0,
                            'access_token':'0d1718b5aad18a5bf2e413c7e3a582e085949d6e18981bc1e87cdd6f15a34e6a7d723c14b98e7f3ab3a54',
                            'v': 'V',
                            'offset': offset
                            }).json()

    comments = ET.SubElement(details, "Comments")

    try:

     for i in range(1, comment['response'][0]+1):
      writer = comment['response'][i]['from_id']
      data_com = datetime.datetime.fromtimestamp(int(comment[
          'response'][i]['date'])).strftime('%Y-%m-%d %H:%M:%S')
      text_com = comment['response'][i]['text']
      likes_com = comment['response'][i]['likes']['count']

      co.write(str(i)+"\n"+data_com+"\n"+str(writer) +
               "\n"+text_com+"\n"+str(likes_com)+"\n\n")
      comments.set('count', str(comment['response'][0]))
      comment = ET.SubElement(comments, "Comment")
      comment.set('№', str(i))

      username = ET.SubElement(comment, "Username")

      userid = ET.SubElement(comment, "UserID")
      userid.text = str(writer)
      text = ET.SubElement(comment, "Text")
      text.text = str(text_com)

    except KeyError:
     co.write(str(i)+"\n"+'нет доступа'+'\n')
     comments.set('no', 'true')

co.close()
f.close()
l.close()


tree = ET.ElementTree(root)
xmlstr = md.parseString(ET.tostring(root)).toprettyxml(indent="  ")
with open("appt.xml", 'w', encoding='utf-8') as f:
         f.write(xmlstr)
