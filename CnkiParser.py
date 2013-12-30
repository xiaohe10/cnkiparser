#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: zhongxin1990@gmail.com
# CnkiParser.py parse local files to db

import os
import re
from bs4 import BeautifulSoup
import MySQLdb
import sys
from time import  time
import time

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Parser():
    def __init__(self):
        pass
    
    # parse one file !
    def parseKeyword(self,dir,filename):
        f = open(dir+filename)
        soup = BeautifulSoup(f)
        f.close()
        keywordList = []
        for keyword in  soup.find_all(href = re.compile(u'中文关键词')):
            keywordList.append((keyword.get_text()))

        return keywordList
oud3@thucloud3:~$ cd Cnk       '''
        # convert list to json and wirte json in file!
        with open('keywordReuslt','w') as outfile:
            json.dump(keywordList,outfile)
        outfile.close()
        
        # read json from file and convert to list!
        jsonfile = open('keywordReuslt')
        keywords = json.loads(jsonfile.read())
        jsonfile.close()
        return keywords
        '''
    def parsePaper(self,dir,filename):
        #print dir+ filename
	f = open(dir+filename)
        #print f.read()
	words = filename.split("_")
        expertID = words[0]
        soup = BeautifulSoup(f)
        #print 'f',f
	#print 'soup',soup
	f.close()
        #print soup.read()
        papers = []
        paperID = 0
        #print "soupfind",soup.find_all(class_='fz14')
	for title in  soup.find_all('a',text=re.compile('ReplaceJiankuohao')):
            #print title 
	    paperID += 1
            paper = Paper(expertID=expertID,paperID=paperID)
            tr = title.parent.parent
            # titles:
            text = title.get_text().split("'")
            #print "text:",text
	    paper.setTitle(text[1])

            # authors:
            '''
 	    for author in tr.find_all(target="knet"):
                paper.addAuthor(author.get_text())
            '''
            author = title.parent.next_sibling.next_sibling
	    #print author
	    #print '!!!!!!!!',len(list(author.children))
	    for a in author.children:
		if str(a).strip() !="" and str(a).strip() !=';':
		    paper.addAuthor(a.get_text().strip())
            paper.authorsList  = "|".join(paper.authors)
            # origin:
	    
            origin = tr.find(text=re.compile("IPFD,CPFD,HBRD,MTRD,SCPD,SOPD,SCSF,SCHF,SCSD,SOSD,SNAD"))
            #print origin
	    #for origin in origins:
	    #origin = author.next_sibling.next_sibling
            #print origin
            #print 'origin',origin.parent
	    #print '*'*80
	    paper.setOrigin(origin.split('"')[3].strip())
            try:
		pubtime = origin.parent.parent.next_sibling.next_sibling   
            
	    	#paper.listPaper()		
	    	#print "pubtime:",pubtime
	    # pubtime database citation:
	   
            
	    #pubtime = origins.next_sibling.next_sibling
	    
	    	paper.setPubtime(pubtime.string.strip())
            #print "pubtime",pubtime
	    	database = pubtime.next_sibling.next_sibling
            	paper.setDatabase(database.string.strip())
	    #print 'ci:',ci
	    	ci = database.next_sibling.next_sibling
	    	#print "ci:",ci
 	    	#print 'cistring',ci.string
	    	if ci.a != None:
	    		paper.setCitation(ci.a.get_text().strip())
            except Exception:
		print Exception
		#if pdc[2] != '':
             #   paper.setCitation(pdc[2])
	    #paper.listPaper()
            papers.append(paper)
        return papers
class DB():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",user="root",passwd="thusoftware",  charset='utf8')
        cursor = self.conn.cursor()
        # cursor.execute('Create database if not exists experts DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;')
        self.conn.select_db('experts')
        self.cursor = self.conn.cursor()
        self.cursor.execute('Create table if not exists GeniusExpert(Expert_ID BIGINT(20),Expert_name varchar(100),Expert_keywords varchar(2000) );')
        self.cursor.execute('Create table if not exists Paper(Expert_ID BIGINT(20),Paper_ID BIGINT(4),Paper_Title varchar(100),Paper_Authorslist varchar(100),Paper_Origin varchar(20),Paper_Pubtime varchar(10), Paper_Database varchar(5), Paper_Citation BIGINT(4)) ;')
        self.cursor.execute("SET NAMES utf8")
        self.cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
        self.cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
        self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()
    def isExpertExist(self,expert):
        sql = "select * from GeniusExpert where Expert_ID = '%s'" %(expert.expertID)
        #print sql
        count = self.cursor.execute(sql)
        if count > 0:
            return True
        else:
            return False   
    def isPaperExist(self,paper):
        sql = "select * from Paper where Expert_ID = '%s' and Paper_ID='%s' " %(paper.expertID,paper.paperID)
        #print sql
        count = self.cursor.execute(sql)
        if count > 0:
            return True
        else:
            return False 
        
        
    def insertExpert(self,expert):
        sql = "insert into GeniusExpert(Expert_ID,Expert_name,Expert_keywords) values('%s','%s','%s')" %(expert.expertID,expert.name,str(expert.keywordsList))
        try:
            print sql
            self.cursor.execute(sql)
        except Exception, e:
            f = open("ExpertError.log","a")
            f.write(str(e)+"\n")
            f.write(sql+"\n")
            f.write(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
            f.close() 
        return  True
    def insertPaper(self,paper):
        
        sql = "insert into  Paper(Expert_ID,Paper_ID,Paper_Title,Paper_Authorslist,Paper_Origin,Paper_Pubtime,Paper_Database,Paper_Citation) values('%s','%s','%s','%s','%s','%s','%s','%s')" %(paper.expertID,paper.paperID,paper.title,paper.authorsList,paper.origin,paper.pubtime,paper.database,paper.citation)
        try:
            #print sql
            self.cursor.execute(sql)
        except Exception, e:
            f = open("PaperError.log","a")
            #f.write(str(e)+"\n")
            #f.write(sql+"\n")
            f.write(time.strftime('%m-%d %H:%M:%S\n',time.localtime(time.time())))
            f.close() 
        return  True
class Paper():
    #def __init__(self,id,title,authors,origin,pubtime,database,citation，url):
    def __init__(self,expertID,paperID):
        self.expertID = expertID
        self.paperID = paperID
        self.title = ""
        self.authors = []
        self.authorsList = "" # a|b|c
        self.origin = ""
        self.pubtime = ""
        self.database = ""
        self.citation = 0
        self.url = ""
    '''
        self.title = title
        self.authors = authors
        self.origin = origin
        self.pubtime = pubtime
        self.database = database
        self.citation = citation
    '''

    def convertToDict(self):
        paper = {
            "expertID" : self.expertID,
            "paperID":self.paperID,
            "title" : self.title,
            "authors" : self.authors,
            "origin" : self.origin,
            "pubtime" : self.pubtime,
            "database" : self.database,
            "citation" : self.citation,
            "url":self.url,
        }
        return paper
    def listPaper(self):
    	
    	print "expertID:",self.expertID
        print "paperID:",self.paperID
        print "title:",self.title
        print "authorsList",self.authorsList
        '''
        print "authors:"
        for author in self.authors:
            print author,
	    print ""
        '''
        print "origin:",self.origin
        print "pubtime:",self.pubtime
        print "database:",self.database
        print "citation:",self.citation
        print "url:",self.url
    

    def setPaperID(self,paperID):
        self.paperID = paperID
    def setTitle(self,title):
        self.title = title
    def addAuthor(self,author):
        self.authors.append(author)
    def setOrigin(self,origin):
        self.origin = origin
    def setPubtime(self,pubtime):
        self.pubtime = pubtime
    def setDatabase(self,database):
        self.database = database
    def setCitation(self,citation):
        self.citation = citation
    def setUrl(self,url):
    	self.url = url
class Expert():
    def __init__(self,expertID,name,department):
        self.expertID = expertID
        self.name = name
        self.department = department
        self.keywords = []
        self.papers = []
        self.keywordsList = ""
    def ChangeKeywordsToString(self):
        self.keywordsList = " ".join(self.keywords)
    def getName(self):
        return self.name
    def getDepartment(self):
        return self.department
    def setKeyword(self,keywords):
        self.keywords = keywords
    def addPapers(self,paper):
        self.papers.append(paper)
    def setPapers(self,papers):
        self.papers = papers
    def listPerson(self):
        print "*"*80
        print 'ExpertID:',self.expertID
        print 'name:' + self.name+ 'department:' + self.department
        print "keywords:"
        for keyword in self.keywords:
            print keyword,
        print ""
        print "papers:"
        for paper in self.papers:
            paper.listPaper() 
        print "-"*80
def InsertKeyWordToDB(fromSubDir,toSubDir):
    
    db = DB()
    parser = Parser()
    
    for index in range(fromSubDir,toSubDir):
        for root,dirs,files in os.walk('Data/keyword/'+str(index)+"/"):
            #each subdir: 1000record
            start = time.time()
            for afile in files:
                if afile  == '.DS_Store':
                    continue
                words = afile.split('_')
                
                aExpert = Expert(words[0].strip(),words[1].strip(),words[2].replace(".html","").strip())
                aExpert.setKeyword(parser.parseKeyword(root,afile))
                
		aExpert.ChangeKeywordsToString()
                #print aExpert.keywordsList
		#print aExpert.keywordsList
                if not db.isExpertExist(aExpert):
                    db.insertExpert(aExpert)
		else:
		    print "Expert keyword",words[0],words[1],words[2],"is Exist!"
            end = time.time()
            db.conn.commit()
            
            print ("KeywordSubDir %d is Done!"%index),
            print time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())),"total:",end-start
            f = open("KeywordsToDB.log","a")
            f.write(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))+" keywordSubDir"+str(index)+" is Done! "+"total"+str(end-start) )
            f.close()
            
    db.close()
def InsertPaperToDB(fromSubDir,toSubDir): 
    db = DB()
    parser = Parser()
    
    for index in range(fromSubDir,toSubDir):   
        for root,dirs,files in os.walk('Data/paper/'+str(index)+"/"):
            n = 1000*index
            start = time.time()
            #print "root:",root
            for afile in files:
                
		words = afile.split('_')
		#print afile
		if afile  == '.DS_Store':
		    continue
                #print root,afile
		papers = (parser.parsePaper(root,afile))
                #print papers
		#print '~~~~~~~~'
		for eachPaper in papers:
                    #eachPaper.listPaper()
		    if not db.isPaperExist(eachPaper):
                        #print 'new paper!'
			#eachPaper.listPaper()
			db.insertPaper(eachPaper)
		    	#db.conn.commit()
		    else:
			#print 'a'
			#print "Expert Paper",words[0],words[1],words[2],"is Exist!"
			continue
                #del papers
		db.conn.commit()
		print "n:",n,
                print "Expert_ID %s is done"%words[0]
                n = n + 1 
                del papers
		#db.conn.commit()
            end = time.time()
             pers
            print ("PaperSubDir %d is Done!"%index),
            print time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())),"time:",end-start
            f = open("PaperToDB.log","a")
            f.write(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))+" paperSubDir"+str(index)+" is Done! "+"total"+str(end-start)+"\n" )
            f.close()
    db.close()      
            
    
def main():
    #print time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
    #InsertKeyWordToDB(81,82)
   
    InsertPaperToDB(9,81) 
if __name__ == '__main__':
	main()
