#-*-coding:utf-8-*-

from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, \
    SimpleFSDirectory, File,BooleanQuery, BooleanClause,\
    VERSION, initVM, Version
from flask import Flask, request,\
      redirect, url_for,render_template,flash
import random
def run(searcher, analyzer,command):
    querys=BooleanQuery()

    if command == '':
        return

    query = QueryParser(Version.LUCENE_CURRENT,"songname",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)        
    query = QueryParser(Version.LUCENE_CURRENT,"albumname",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)
    scoreDocs = searcher.search(querys, 20).scoreDocs
##        print "%s total matching documents." % len(scoreDocs)    
##    for scoreDoc in scoreDocs:
##        doc = searcher.doc(scoreDoc.doc)
##        print 'songname:', doc.get("songname"), '\n','songurl:',doc.get('songurl'), '\n',\
##              'albumname:',doc.get('albumname'),'\n','albumcoverurl:', doc.get("albumcoverurl"),'\n'
    return scoreDocs
def search():
    results=[]
    loc=[]
    sr=''
    mark=False
    if request.method == 'POST':
        try:                        
            STORE_DIR = "index"
            initVM()       
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(directory, True)
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            scoreDocs=run(searcher, analyzer,sr)
            if "Search" in request.form.values():
                sr=request.form['text']
                
            elif "Shuffle" in request.form.values():
                mark=True
                while len(loc)<20:
                    tmp=random.randint(0,searcher.maxDoc())
                    if tmp not in loc:
                        loc+=[tmp]
                
##            if request.form['action']=="Search":
##                sr=request.form['text']
##            elif request.form['action']=="Shuffle":
##                sr='1'


            if mark:
                print 'loc=',loc
                for i in loc:
                    doc = searcher.doc(i)
                    results+=[{'songname':doc.get("songname"),'songurl':\
                              doc.get('songurl'),'albumname':\
                              doc.get('albumname'),'albumcoverurl': \
                              doc.get("albumcoverurl")}]                   
            else:
                print  request.form.values()
                print 'sr=',sr
                if sr=='':
                    return results
                for scoreDoc in scoreDocs:
                    doc = searcher.doc(scoreDoc.doc)
                    results+=[{'songname':doc.get("songname"),'songurl':\
                              doc.get('songurl'),'albumname':\
                              doc.get('albumname'),'albumcoverurl': \
                              doc.get("albumcoverurl")}]
            searcher.close()
        except Exception,e:
            print 12,e
        
            
    return results

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    results=search()
    return render_template('search.html',results=results)

@app.route("/pic", methods=['GET', 'POST'])
def pic():    
    results=search()
    return render_template('pic.html',results=results)

@app.route("/album", methods=['GET', 'POST'])
def album():    
    results=search()
    return render_template('album.html',results=results)


if __name__ == "__main__":
    
    app.run()
