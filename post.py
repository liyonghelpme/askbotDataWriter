#coding:utf8

import MySQLdb
import datetime
import re

ques = re.compile('\d+\.')
ans = re.compile('答：')
f = open('right3.txt')

state = 0
q = ''
a = ''
allQuestion = []

for l in f.readlines():
    if state == 0:
        res = ques.match(l)
        if res != None:
            state = 1
            q = l
            a = ''
    elif state == 1:
        if ans.match(l):
            state = 2
            a = l
        elif ques.match(l):
            state = 1
            q = l
            a = ''
        else:
            q += l[:-1]+'<br>'
    elif state == 2:
        if l == '\n':
            q = q.replace('"', '\\"')
            a = a.replace('"', '\\"')
            allQuestion.append([q, a])
            state = 0
            q = ''
            a = ''
        elif ques.match(l):
            q = q.replace('"', '\\"')
            a = a.replace('"', '\\"')
            allQuestion.append([q, a])
            state = 1
            q = l
            a = ''
        else:
            
            a += l[:-1]+'<br>'
        
con = MySQLdb.connect(host='192.30.139.242', user='root', passwd='playgame', db='askbot', charset='utf8')
#con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='askbot', charset='utf8')
cursor = con.cursor()

for i in allQuestion:

    title = i[0]
    body_text = i[0]
    tags = None
    wiki = True
    is_anonymous = True
    is_private = False
    group_id = None
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    by_email = False
    email_address = "liyonghelpme@gmail.com"
    language = "zh_CN"
    author_id = 1

    sql = ("insert into askbot_thread" 
          "          ("
          "          favourite_count,"
          "          last_activity_at,"
          "          last_activity_by_id," 
          "          title, "
          "          added_at," 
          "          approved, "
          "          language_code, "
          "          answer_count"
          '           ) values (%d, "%s", %d, "%s", "%s", %d,  "%s", 1)'  
            ) % (1, timestamp, 1,  title, timestamp, 1, language)
    print sql
    cursor.execute(sql)
    thread_id = con.insert_id()


    html = "<p>"+body_text+"<p>"
    postType = "question"

    sql = ('insert into askbot_post('
    '                author_id, '
    '                added_at,'
    '                wiki, '
    '                html, '
    '                text, '
    '                is_anonymous, '
    '                post_type, '
    '                thread_id, '
    '                approved, '
    '                summary, '
    '                language_code'
    '                ) values(%d, "%s", %d, "%s", "%s", %d, "%s", %d, %d, "%s", "%s")'
    ) % (1, timestamp, wiki, html, body_text, is_anonymous, postType, thread_id, 1, title, language)

    print sql
    con.query(sql)

    #回答问题

    text = i[1] 
    html = "<p>%s<p>" % (text)
    postType = "answer"
    summary = text
    sql = ('insert into askbot_post('
    '                author_id, '
    '                added_at,'
    '                wiki, '
    '                html, '
    '                text, '
    '                is_anonymous, '
    '                post_type, '
    '                thread_id, '
    '                approved, '
    '                summary, '
    '                language_code'
    '                ) values(%d, "%s", %d, "%s", "%s", %d, "%s", %d, %d, "%s", "%s")'
    ) % (1, timestamp, wiki, html, body_text, is_anonymous, postType, thread_id, 1, title, language)

    print sql
    cursor.execute(sql)
    postId = con.insert_id()

    sql = ('insert into askbot_postrevision('
    "               revision, "
    "               author_id, "
    "               revised_at,"
    "               summary, "
    "               text,"
    "               is_anonymous,"
    "               post_id "
    '                ) values(1, 1, "%s", "initial version", "%s", 1, %d)'
    ) % (timestamp, text, postId)
    print sql
    con.query(sql)



con.commit()








