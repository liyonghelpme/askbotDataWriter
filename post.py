#coding:utf8

import MySQLdb
import datetime

con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='askbot', charset='utf8')

cursor = con.cursor()

title = '你好中国人民我来了哈哈哈啊哈和'
body_text = 'welcome to china hello world'
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

text = "我知道答案是什么 不告诉你哈哈" 
html = "<p>我知道答案是什么 不告诉你哈哈<p>"
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








