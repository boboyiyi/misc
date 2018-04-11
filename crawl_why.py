# -*- coding= utf-8 -*-
import codecs as cs
import StringIO
import urllib
import urllib2
import re

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
           'Connection' : 'keep-alive'}
list_pattern = re.compile('a href=\"([^\"]*html)\"')
q_pattern = re.compile('<p><strong>(.*)</p>')
a_pattern = re.compile('<[pP]>(.*)</[pP]>')
webpage_class = []
webpage_question = []
request = urllib2.Request("http://www.jianbihua.org/weishime/", None, headers)
response = urllib2.urlopen(request)
content = StringIO.StringIO(response.read())
content = content.readlines()
i = 0
while i < len(content):
    if '<UL>' == content[i].strip():
        i += 1
        while '</UL></div>' != content[i].strip():
            webpage_class.append(content[i].strip().split()[1].split('"')[1])
            i += 1
        break
    else:
        i += 1
for idx in range(len(webpage_class)):
    name = webpage_class[idx].split('/')[-2]
    print name
    request = urllib2.Request(webpage_class[idx], None, headers)
    response = urllib2.urlopen(request)
    content = StringIO.StringIO(response.read())
    content = content.readlines()
    i = 0
    while i < len(content):
        if '<ul>' == content[i].strip():
            i += 1
            while '</ul>' not in content[i]:
                webpage_question.append(content[i].strip().split()[1].split('"')[1])
                i += 1
            i += 2
            sub_pages = list_pattern.findall(content[i].strip())
            for j in range(len(sub_pages)):
                request = urllib2.Request(sub_pages[j].strip(), None, headers)
                response = urllib2.urlopen(request)
                content = StringIO.StringIO(response.read())
                content = content.readlines()
                k = 0
                while k < len(content):
                    if '<ul>' == content[k].strip():
                        k += 1
                        while '</ul>' not in content[k]:
                            webpage_question.append(content[k].strip().split()[1].split('"')[1])
                            k += 1
                        break
                    else:
                        k += 1
            break
        else:
            i += 1
    cnt = 1
    # with cs.open('QA/' + name + '.txt', 'w', 'utf-8') as fo:
    with open('QA/' + name + '.txt', 'w') as fo:
        for atom in webpage_question:
            print atom
            request = urllib2.Request(atom.strip(), None, headers)
            response = urllib2.urlopen(request)
            content = StringIO.StringIO(response.read())
            content = content.readlines()
            i = 0
            while i < len(content):
                if '<p><strong>' in content[i]:
                    q = q_pattern.findall(content[i].strip())[0].replace('</strong>', '')#.decode('gb2312')#.encode('utf-8')
                    i += 1
                    a = a_pattern.findall(content[i].strip())[0]#.decode('gb2312')#.encode('utf-8')
                    # fo.write(str(cnt) + '. ' + q + '\n')
                    # fo.write(a + '\n')
                    print >> fo, str(cnt) + '. ' + q
                    print >> fo, a
                    cnt += 1
                    break
                else:
                    i += 1
    webpage_question = []
