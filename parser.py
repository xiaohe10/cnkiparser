# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re
import MySQLdb

class Parser():
    def __init__(self):
        self.html_dir = '/Paper'
        self.sql_host = '166.111.81.223'
        self.sql_name = 'paper'
        self.sql_user = 'root'
        self.sql_pass = 'root'
        self.count = 0

    def parse_file(self,filename):
        paper = {}
        f = open(filename,'r')
        (path,filename) = os.path.split(filename)
        id_pattern = re.compile(r'\d+')
        id = id_pattern.findall(filename)[0]
        paper['expertID'] = id
        html = f.read()
        content_pattern = re.compile(r'<table class="GridTableContent".*?</table>',re.S)
        item_pattern = re.compile(r'<TR  bgcolor.*?</TR>',re.S)
        script_pattern = re.compile(r'<script.*?</script>',re.S)
        try:
            content = content_pattern.findall(html)[0]
            for item in item_pattern.finditer(content):
                item = item.group()
                #title
                title_pattern = re.compile(r'ReplaceJiankuohao\(.*?\)',re.S)
                title = title_pattern.findall(item)[0]
                title = title.replace('ReplaceJiankuohao(\'','')
                title = title.replace('\')','')
                paper['title'] = title
                #authors
                authorlist = []
                author_pattern = re.compile(r'<a[^>]*?target="knet">.*?</a>',re.S)
                for author in author_pattern.finditer(item):
                    author =  author.group()
                    author = re.sub(r'<.*?>','',author,flags=re.S)
                    authorlist.append(author)
                paper['authorlist'] = authorlist

                #source
                source_pattern = re.compile(r'return[^<>]*?;',re.S)
                source = source_pattern.findall(item)[0]
                source = source.replace('return "','')
                source = source.replace('";','')
                paper['source'] = source
                #date
                date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                date = date_pattern.findall(item)[0]
                paper['date'] = date
            return paper
        except:
            print "parse "+ filename + "error"
        return None
    def findAllFiles(self,dir):
         os.path.walk(dir, self.processDirectory, None)
    def processDirectory (self, args, dirname, filenames ):
        for filename in filenames:
            if '.html'in filename:
                f = os.path.join(dirname,filename)
                print f
                paper = p.parse_file(f)
                if paper:
                    print 'parse '+paper['expertID']+' ok'
                    self.insert2DB(paper)
                    self.count += 1
                    if self.count > 1000:
                        self.conn.commit()
                        self.count = 0
                else:
                    print 'fail'
    def insert2DB(self,paper):
        authorlist_String = ','.join(paper['authorlist'])
        sql  = "insert into CnkiPaper (expert_ID,title,authorlist,pub_date) values({0},\"{1}\",\"{2}\",\"{3}\")".format(paper["expertID"],paper["title"],authorlist_String,paper["date"])
        self.cursor.execute(sql)
    def init_database(self):
        self.conn = MySQLdb.connect(host="166.111.81.223",user="root",passwd="root",  charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('Create database if not exists experts DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;')
        self.conn.select_db('experts')
        self.cursor = self.conn.cursor()
        self.cursor.execute('Create table if not exists CnkiPaper(expert_ID BIGINT(20),title varchar(100),authorlist varchar(100),pub_date date) ;')
        self.cursor.execute("SET NAMES utf8")
        self.cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
        self.cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
        self.conn.commit()

if __name__ == '__main__':
    p = Parser()
    p.init_database()
    p.findAllFiles('paper/0/')
    p.conn.commit()
    print "okay!!! parse success"