#-*-coding:utf-8-*-
import MySQLdb,time
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, \
    SimpleFSDirectory, File,BooleanQuery, BooleanClause,\
    VERSION, initVM, Version
from flask import Flask, request,\
      redirect, url_for,render_template,flash
from werkzeug import secure_filename
import random,os
from LSH import imgProcess
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
    tmp='' 
    mark=False
    if request.method == 'POST':
        try:                        
            STORE_DIR = "index"
            initVM()       
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(directory, True)
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

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
                    return results,""
                for i in sr:
                    tmp+=i+" "
                print tmp  
                scoreDocs=run(searcher, analyzer,sr)
                for scoreDoc in scoreDocs:
                    doc = searcher.doc(scoreDoc.doc)
                    results+=[{'songname':doc.get("songname"),'songurl':\
                              doc.get('songurl'),'albumname':\
                              doc.get('albumname'),'albumcoverurl': \
                              doc.get("albumcoverurl")}]
            searcher.close()
        except Exception,e:
            print 12,e
      
#tmp为单字符highlight
    return results,tmp

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    results,sr=search()
    return render_template('search.html',results=results,sr=sr)

@app.route("/pic", methods=['GET', 'POST'])
def pic():    
    results,sr=search()
    return render_template('pic.html',results=results,sr=sr)

@app.route("/album", methods=['GET', 'POST'])
def album():    
    results,sr=search()
    return render_template('album.html',results=results,sr=sr)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    try:
        conn = MySQLdb.connect(host='localhost', user='root',passwd='1234',charset="utf8") 
        conn.select_db('coversearch');
        cursor = conn.cursor()
        cursor.execute("select * from comments ")
        data=[]
        cur=1
        while True:
            try:
                dataFromdb=cursor.fetchone()
                data+=[{'text':str(cur)+'.\n'+dataFromdb[1],'time':dataFromdb[2]}]
                cur+=1
            except:
                break
        cursor.execute("select count(*) as value from comments ")
        num=cursor.fetchone()[0]
        num=int(num)
        cm=''
        if request.method == 'POST':       
            cm=request.form['text']
            if cm!='':
                curTime=time.ctime()
                order=(num+1,cm,curTime)           
                sql = "insert into comments(id,text,time) values (%s,%s,%s)"
                cursor.execute(sql,order)
                num+=1
                data+=[{'text':str(cur)+'.\n'+cm,'time':curTime}]

        conn.commit()
        cursor.close() 
        conn.close()   
    except Exception,e:
        print e
    return render_template("comment.html",comments=data,number=num)

UPLOAD_FOLDER = 'static/covers/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
@app.route("/coversearch", methods=['GET', 'POST'])
def coversearch():
    url="#"
    if request.method == 'POST':
        try:
            imagefile=request.files["image"]
            if imagefile:
                filename="target.jpg"              
                imagefile.save(os.path.join(UPLOAD_FOLDER, filename))
                url=imgProcess(UPLOAD_FOLDER + filename)

                
        except Exception,e:
            print e
    return render_template('coversearch.html',url=url)


if __name__ == "__main__":
    
    app.run()
