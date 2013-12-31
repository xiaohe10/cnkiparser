# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re

class Parser():
    def __init__(self):
        self.html_dir = '/Paper'
        self.sql_host = '166.111.81.223'
        self.sql_name = 'paper'
        self.sql_user = 'root'
        self.sql_pass = 'root'

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
                    print paper['expertID']+' ok'
                else:
                    print 'fail'

if __name__ == '__main__':
    p = Parser()
    #p.parse_file('Paper/0/1.html')
    p.findAllFiles('paper/0/')