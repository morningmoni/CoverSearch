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
        for t in glob.glob("texts/song/*.txt"):
            try:
                a=t.rfind('\\')
                t=t[:a]+'/'+t[a+1:]
                print t
                res=build(t)              
                doc = lucene.Document()
##                if len(res.artist[0])==1:
                artist=res.artists[0]
                artistURL=res.artistURLs[0]
##                name=" ".join(jieba.cut(res.name))
                URL='http://www.xiami.com/song/'+t[a+1:-4].strip()
##                print URL
                doc.add(lucene.Field("songname", res.name,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.ANALYZED))
                doc.add(lucene.Field("songurl", URL,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("songalbum",res.album ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("songartist",artist ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.ANALYZED))
                doc.add(lucene.Field("songalbumURL",res.albumURL ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("songartistURL",artistURL ,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))                          

                doc.add(lucene.Field("songpicURL", res.picturePATH,
                             lucene.Field.Store.YES,
                             lucene.Field.Index.NOT_ANALYZED))
                writer.addDocument(doc)
            except Exception,e:
                print 'Failed in indexDocs: ',e


    

if __name__ == '__main__':
    lucene.initVM()
    i=IndexFiles("songIndex", lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT))
    



