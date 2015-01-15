# -*- coding: utf-8 -*-

import sys, os, lucene, threading, time
from datetime import datetime
import urlparse,re,urllib,urllib2
from BeautifulSoup import BeautifulSoup
##import jieba   #use jieba to segment
from modal import *
import glob


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        store = lucene.SimpleFSDirectory(lucene.File(storeDir))
        writer = lucene.IndexWriter(store, analyzer, True,
                                    lucene.IndexWriter.MaxFieldLength.LIMITED)
        writer.setMaxFieldLength(1048576)
        self.indexDocs(writer)
        ticker = Ticker()
        print 'optimizing index',
        threading.Thread(target=ticker.run).start()
        writer.optimize()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, writer):
        for t in glob.glob("texts/album/*.txt"):
            try:
                a=t.rfind('\\')
                t=t[:a]+'/'+t[a+1:]
                print t
                res=build(t)              
                doc = lucene.Document()
                songs=''
                for i in res.songs:
                    songs+=i+'!@#$%'
                songURLs=''
                for i in res.songURLs:
                    songURLs+=i+'!@#$%'

##                name=" ".join(jieba.cut(res.name))
                doc.add(lucene.Field("albumnum", res.number,
                     lucene.Field.Store.YES,
                     lucene.Field.Index.ANALYZED))
                doc.add(lucene.Field("albumname", res.name,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.ANALYZED))
                doc.add(lucene.Field("albumartist",res.artist ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))

                if res.pictureURL==None:
                    a=res.introduction.find('http')
                    res.pictureURL=res.introduction[a:]
                    res.introduction="这位专辑懒得介绍自己"
                    print res.pictureURL
                doc.add(lucene.Field("albumintro",res.introduction ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("albumsongs",songs ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("albumsongURLs",songURLs ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))                          

                doc.add(lucene.Field("albumpicURL", res.pictureURL,
                             lucene.Field.Store.YES,
                             lucene.Field.Index.NOT_ANALYZED))

                writer.addDocument(doc)
            except Exception,e:
                print 'Failed in indexDocs: ',e


    

if __name__ == '__main__':
    lucene.initVM()
    i=IndexFiles("albumIndex", lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT))
    



