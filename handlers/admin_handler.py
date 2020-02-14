#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers.index_handler import TornadoRequestBase
import uuid, os
import jdatetime,codecs
from user_area.smbanaie.smbanaie.userconf import *
from datetime import datetime
import tornado,pathlib

class admin_Handler(TornadoRequestBase):
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]

        # self.render('admin/admin.html', date=date)
        self.render('admin/starter.html')

    def post(self, *args, **kwargs):
        return


class add_new_post_Handler(TornadoRequestBase):
    def get(self, *args, **kwargs):
        catList = {}
        authors = []
        for clist in CATEGORIES["cat_list"] :
            catList [clist[0]] = clist[1]
        for user in AUTHORS :
            authors.append(user)
        date = str(jdatetime.datetime.now())
        fa_date_components = date[:10].split("-")
        month = fa_date_components[1]
        if  month[0]=="0":
            month = month[1]
        self.render('admin/posts/add2.html',catlist = catList,authors=authors,year=fa_date_components[0] ,month= month )

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        fa_date_components =date[:10].split("-")
        d = datetime.now()
        en_date_components ="%d-%d-%d"%(d.year,d.month,d.day)
        # ftest = open(r"F:\My GitHub Repos\WebSiteMaker\t.txt","a")
        # ftest.write(self.get("tags"))
        # ftest.close()
        article_path = USER_DIR +os.path.sep+"content"+os.path.sep+"blog"+os.path.sep+"fa"
        article_path+=os.path.sep+self.get_argument("category")+os.path.sep
        article_path+= fa_date_components[0]+os.path.sep
        if  fa_date_components[1][0]=="0":
            article_path += fa_date_components[1][1]
        else :
            article_path += fa_date_components[1]
        self.write("\n"+article_path)
        pathlib.Path(article_path).mkdir(parents=True, exist_ok=True)
        self.write("\n"+article_path+os.path.sep+self.get_argument("slug")+".md")
        f= codecs.open(article_path+os.path.sep+self.get_argument("slug")+".md", "w",encoding="utf-8")
        f.write("title:"+ self.get_argument('title')+ "\r\n")
        self.write("\n"+"title:"+ self.get_argument('title')+ "\r\n")
        f.write("date:"+ en_date_components + "\r\n")
        self.write("\n"+"date:"+ en_date_components + "\r\n")
        f.write("modified:"+ en_date_components + "\r\n")
        self.write("\n"+"modified:"+ en_date_components + "\r\n")
        f.write("icon:icon-link2\r\n")
        self.write("\n"+"icon:icon-link2\r\n")
        f.write("lang:fa\r\n")
        self.write("\n"+"lang:fa\r\n")
        f.write("category:"+self.get_argument('cat_name')+ "\r\n")
        self.write("\n"+"category:"+self.get_argument('cat_name')+ "\r\n")
        f.write("tags:"+self.get_argument('tagsvalues')+ "\r\n")
        self.write("\n"+"tags:"+self.get_argument('tagsvalues')+ "\r\n")
        f.write("Slug:"+self.get_argument('slug')+ "\r\n")
        self.write("\n"+"Slug:"+self.get_argument('slug')+ "\r\n")
        f.write("authors:"+self.get_argument('authors')+ "\r\n")
        self.write("\n"+"authors:"+self.get_argument('authors')+ "\r\n")
        f.write("summary:"+self.get_argument('summary')+ "\r\n")
        self.write("\n"+"summary:"+self.get_argument('summary')+ "\r\n")
        f.write("image: "+self.get_argument("img_adr")+self.get_argument("image")+ "\r\n\r\n")
        self.write("\n"+"image: "+self.get_argument("img_adr")+self.get_argument("image")+ "\r\n\r\n")
        f.write("!["+self.get_argument("img_desc")+" <>]({static}"+self.get_argument("img_adr")+self.get_argument("image")+")\r\n\r\n")
        self.write("\n"+"!["+self.get_argument("img_desc")+" <>]({static}"+self.get_argument("img_adr")+self.get_argument("image")+")\r\n\r\n")
        f.write(self.get_argument('article'))
        self.write("\n"+self.get_argument('article'))
        f.close()
        self.finish("\n"+article_path)


