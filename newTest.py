#coding:utf8
import re

ques = re.compile('\d+\.')
ans = re.compile('答：')

f = open('error2.txt')
state = 0
q = ''
a = ''
allQuestion = []

rightF = open('right3.txt', 'w')
errorF = open('error3.txt', 'w')


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
            print 'error', q
            errorF.write(q)
            state = 1
            q = l
            a = ''
        else:
            q += l
    elif state == 2:
        if l == '\n':
            allQuestion.append([q, a])
            state = 0
            q = ''
            a = ''
        elif ques.match(l):
            allQuestion.append([q, a])
            state = 1
            q = l
            a = ''
        else:
            a += l

            
for i in allQuestion:
    print 'problem'
    print i[0]
    print 'answer'
    print i[1]
    rightF.write(i[0])
    rightF.write(i[1])
    

rightF.close()
errorF.close()
