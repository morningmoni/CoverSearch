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
        return False
    query = QueryParser(Version.LUCENE_CURRENT,"songartist",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)
    query = QueryParser(Version.LUCENE_CURRENT,"songname",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)        
    query = QueryParser(Version.LUCENE_CURRENT,"songalbum",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)

    scoreDocs = searcher.search(querys, 20).scoreDocs

    return scoreDocs
def run2(searcher, analyzer,command,num):
    querys=BooleanQuery()

    if command == '':
        return False

    query = QueryParser(Version.LUCENE_CURRENT,"albumnum",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)        
    query = QueryParser(Version.LUCENE_CURRENT,"albumname",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)
    doc=None
    scoreDocs = searcher.search(querys, num).scoreDocs
    if num>1:
        return scoreDocs
    if len(scoreDocs)==1:
        doc = searcher.doc(scoreDocs[0].doc)
        print 555,doc.get('albumname')
        if doc.get('albumname')!=command and doc.get('albumnum')!=command:
            return False
    else:
        return False

    return doc

def run3(searcher, analyzer,command):
    querys=BooleanQuery()

    if command == '':
        return False

    query = QueryParser(Version.LUCENE_CURRENT,"singername",analyzer).parse(command)
    querys.add(query,BooleanClause.Occur.SHOULD)        
    doc=None
    scoreDocs = searcher.search(querys, 1).scoreDocs
    if len(scoreDocs)==1:
        doc = searcher.doc(scoreDocs[0].doc)
        print 12345,doc.get('singername')
        if doc.get('singername')!=command:
            return False
    else:
        return False

    return doc
def search():
    results=[]
    results3=[]
    loc=[]
    sr=''
    tmp='' 
    mark=False
    if request.method == 'POST':
        try:                        
            initVM()       
            directory = SimpleFSDirectory(File("songIndex"))
            searcher = IndexSearcher(directory, True)
            directory = SimpleFSDirectory(File("artistIndex"))
            searcher3 = IndexSearcher(directory, True)
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

            if "Search" in request.form.values():
                sr=request.form['text']
                
            elif "Shuffle" in request.form.values():
                mark=True
                while len(loc)<20:
                    tmp=random.randint(0,searcher.maxDoc()-1)
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
                    results+=[{'songname':doc.get("songname"),\
                               'songurl':doc.get('songurl'),\
                               'albumname':doc.get('songalbum'),\
                               'songartist':doc.get('songartist'),\
                               'albumurl': doc.get("songalbumURL"),\
                               'picPath':doc.get('songpicURL'),\
                               }]                   
            else:
                print  request.form.values()
                print 'sr=',sr
                if sr=='':
                    return results,results3,""
                for i in sr:
                   tmp+=i+" "
##                print tmp
##                scoreDocs=run2(searcher2, analyzer,sr)
##                if len(scoreDocs)!=0:
##                    doc=searcher2.doc(scoreDocs[0].doc)
##                    results2+=[{'albumnum:', doc.get("albumnum"),\
##                               'albumname:',doc.get('albumname'),\
##                                'albumartist:',doc.get('albumartist'),\
##                               'albumintro:', doc.get("albumintro"),\
##                               'albumsongs:',doc.get('albumsongs'),\
##                               'albumsongURLs:', doc.get("albumsongURLs"),\
##                               'albumpicURL:',doc.get('albumpicURL')}]
##                else:
                scoreDocs=run3(searcher3,analyzer,sr)
                if scoreDocs == False:
                    scoreDocs=run(searcher, analyzer,sr)
                    for scoreDoc in scoreDocs:
                        doc = searcher.doc(scoreDoc.doc)
                        results+=[{'songname':doc.get("songname"),\
                                   'songurl':doc.get('songurl'),\
                                   'albumname':doc.get('songalbum'),\
                                   'songartist':doc.get('songartist'),\
                                   'albumurl': doc.get("songalbumURL"),\
                                   'picPath':doc.get('songpicURL')\
                                   }]
                else:
                    doc=scoreDocs
                    singeralbums=doc.get('singeralbums')
                    singeralbums=singeralbums.split('!@#$%')
                    singeralbumURLs=doc.get("singeralbumURLs")
                    singeralbumURLs=singeralbumURLs.split('!@#$%')
                    results3+=[{'singername': doc.get("singername"),\
                                'singerplace':doc.get('singerplace'),\
                                'singerintro':doc.get('singerintro'),\
                                'singeralbums': singeralbums,\
                               'singeralbumURLs':singeralbumURLs,\
                                'singerpicURL': doc.get("singerpicURL")\
                                }]
            searcher.close()
        except Exception,e:
            print 1,e
      
#tmp为单字符highlight
    return results,results3,tmp

def search2():
    results0=[]
    results2=[]
    loc=[]
    sr=''
    tmp='' 
    mark=False
    if request.method == 'POST':
        try:                        
            initVM()       
            directory = SimpleFSDirectory(File('albumIndex'))
            searcher2 = IndexSearcher(directory, True)
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

            if "Search" in request.form.values():
                sr=request.form['text']
                
            elif "Shuffle" in request.form.values():
                mark=True
                while len(loc)<20:
                    tmp=random.randint(0,searcher2.maxDoc()-1)
                    if tmp not in loc:
                        loc+=[tmp]
                

            if mark:
                print 'loc=',loc
                ct=0
                for i in loc:
                    doc = searcher2.doc(i)
                    songs=doc.get('albumsongs')
                    songs=songs.split('!@#$%')
                    urls=doc.get("albumsongURLs")
                    urls=urls.split('!@#$%')
                    results2+=[{'albumnum': doc.get("albumnum"),\
                               'albumname':doc.get('albumname'),\
                                'albumartist':doc.get('albumartist'),\
                               'albumintro': doc.get("albumintro"),\
                               'albumsongs':songs,\
                               'albumsongURLs': urls,\
                               'albumpicURL':doc.get('albumpicURL'),\
                                'albumartistURL':doc.get('albumartistURL'),\
                                'albumURL':doc.get('albumURL')}]                   
            else:
                print  request.form.values()
                print 'sr=',sr
                if sr=='':
                    return results0,results2,""
##                for i in sr:
##                    tmp+=i+" "
##                print tmp
                scoreDocs=run2(searcher2, analyzer,sr,1) #search exact album

                if scoreDocs!=False:
                    doc=scoreDocs
                    songs=doc.get('albumsongs')
                    songs=songs.split('!@#$%')
                    urls=doc.get("albumsongURLs")
                    urls=urls.split('!@#$%')
                    results2+=[{'albumnum': doc.get("albumnum"),\
                               'albumname':doc.get('albumname'),\
                                'albumartist':doc.get('albumartist'),\
                               'albumintro': doc.get("albumintro"),\
                               'albumsongs':songs,\
                               'albumsongURLs': urls,\
                               'albumpicURL':doc.get('albumpicURL'),\
                                'albumartistURL':doc.get('albumartistURL'),\
                                'albumURL':doc.get('albumURL')}] 
                    results0=results2
                else:
                    scoreDocs=run2(searcher2, analyzer,sr,20) #search 20 albums
                    rank=100
                    for scoreDoc in scoreDocs:
                        doc = searcher2.doc(scoreDoc.doc)
                        songs=doc.get('albumsongs')
                        songs=songs.split('!@#$%')
                        urls=doc.get("albumsongURLs")
                        urls=urls.split('!@#$%')
                        results2+=[{'albumnum': doc.get("albumnum"),\
                               'albumname':doc.get('albumname'),\
                                'albumartist':doc.get('albumartist'),\
                               'albumintro': doc.get("albumintro"),\
                               'albumsongs':songs,\
                               'albumsongURLs': urls,\
                               'albumpicURL':doc.get('albumpicURL'),\
                                'albumartistURL':doc.get('albumartistURL'),\
                                'albumURL':doc.get('albumURL'),\
                                    'rank':rank}]
                        rank-=5
            searcher2.close()
        except Exception,e:
            print 2,e
      
#tmp为单字符highlight
    conn = MySQLdb.connect(host='localhost', user='root',passwd='1234',charset="utf8") 
    conn.select_db('coversearch');
    cursor = conn.cursor()
    
    for i in results2:
        try:
            cursor.execute("select zan from albums where id="+i['albumnum'])
            zan=cursor.fetchone()[0]
##            print 'zan',zan
            i['zan']=zan
            i['rank']+=int(zan)
        except:
            i['zan']=0



    conn.commit()
    cursor.close() 
    conn.close()
##    print results2
    results2.sort(key=lambda x:x['rank'],reverse=True)
    return results0,results2,tmp



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    results,results3,sr=search()
    return render_template('search.html',results=results,sr=sr)

@app.route("/pic", methods=['GET', 'POST'])
def pic():    
    results,results3,sr=search()
    return render_template('pic.html',results=results,results3=results3,sr=sr)

@app.route("/album", methods=['GET', 'POST'])
def album():    
    results0,results2,sr=search2()
    return render_template('album.html',results0=results0,results2=results2,sr=sr)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    try:
        # conn = MySQLdb.connect(host='localhost', user='root',passwd='1234',charset="utf8")
        conn = MySQLdb.connect(host='localhost', user='ee208',passwd='ee208',charset="utf8") 
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
    url="../static/cover.jpg"
    res=[]
    if request.method == 'POST':
        try:
            imagefile=request.files["image"]
            if imagefile:
                filename="target.jpg"              
                imagefile.save(os.path.join(UPLOAD_FOLDER, filename))
                url=imgProcess(UPLOAD_FOLDER + filename)

                
        except Exception,e:
            print e
    if len(url)<4:
        url="../static/cover.jpg"
    else:
        url='../'+url
        print url
        a=url.rfind('/')
        sr=url[a+1:-4]
        print "sr=",sr
        
        try:                        
            initVM()       
            directory = SimpleFSDirectory(File('albumIndex'))
            searcher2 = IndexSearcher(directory, True)
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            scoreDocs=run2(searcher2, analyzer,sr,1)
            if scoreDocs!=False:
                doc=scoreDocs
                songs=doc.get('albumsongs')
                songs=songs.split('!@#$%')
                urls=doc.get("albumsongURLs")
                urls=urls.split('!@#$%')
                res+=[{'albumnum': doc.get("albumnum"),\
                               'albumname':doc.get('albumname'),\
                                'albumartist':doc.get('albumartist'),\
                               'albumintro': doc.get("albumintro"),\
                               'albumsongs':songs,\
                               'albumsongURLs': urls,\
                               'albumpicURL':doc.get('albumpicURL'),\
                                'albumartistURL':doc.get('albumartistURL'),\
                                'albumURL':doc.get('albumURL')}] 
        except Exception,e:
            print e

    return render_template('coversearch.html',res=res,url=url)

@app.route('/data')  
def add_numbers():  
    num = request.args.get('num', 0, type=int)  
    albumnum = request.args.get('id', 0, type=int) 
    print num ,albumnum
    try:
        conn = MySQLdb.connect(host='localhost', user='root',passwd='1234',charset="utf8") 
        conn.select_db('coversearch');
        cursor = conn.cursor()
        cursor.execute("select count(1) from albums where id="+str(albumnum))
        cur=int(cursor.fetchone()[0])
        if cur==0:
            order=(albumnum,num)           
            sql = "insert into albums(id,zan) values (%s,%s)"
            cursor.execute(sql,order)
        else:
            cursor.execute("update albums set zan="+str(num)+" where id="+str(albumnum))
            print "update albums set zan="+str(num)+" where id="+str(albumnum)
        conn.commit()
        cursor.close() 
        conn.close()
    except Exception,e:
        print e
        
    
    return False 

if __name__ == "__main__":
    
    app.run(host='0.0.0.0')
