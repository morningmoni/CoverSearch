#!/usr/bin/env python
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File,BooleanQuery, BooleanClause,\
    VERSION, initVM, Version
##import jieba

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        
        querys=BooleanQuery()       
        print
        print "Hit enter with no input to quit."
##        for i in range(searcher.maxDoc()):
##                doc=searcher.doc(i)
##                print doc.get('singername')
        
        command = raw_input("Query:")
        command = unicode(command, 'GBK')
        if command == '':
            return

        print
##        command=" ".join(jieba.cut(command))
        print "Searching for:", command
        query = QueryParser(Version.LUCENE_CURRENT,"singername",analyzer).parse(command)
        querys.add(query,BooleanClause.Occur.SHOULD)        
##        query = QueryParser(Version.LUCENE_CURRENT,"albumname",analyzer).parse(command)
##        querys.add(query,BooleanClause.Occur.SHOULD)
        scoreDocs = searcher.search(querys, 3).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print 'singername:', doc.get("singername"), '\n','singerplace:',doc.get('singerplace'), '\n',\
                  'singerintro:',doc.get('singerintro'),'\n','singeralbums:', doc.get("singeralbums"),'\n',\
                   'singeralbumURLs:',doc.get('singeralbumURLs'),'\n','singerpicURL:', doc.get("singerpicURL"),'\n'

if __name__ == '__main__':
    STORE_DIR = "artistIndex"
    initVM()
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    searcher.close()
