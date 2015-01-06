class artist(object):
    def __init__(self):
        self.type='artist'
        self.name=None
        self.number=None
        self.albums=None#list
        self.albumURLs=None#list
        self.pictureURL=None
        self.introduction=None
        self.place=None
    def put(self):
        print self.type
        
        print 'number',self.number
        print 'name',self.name
        print 'place',self.place
        print 'introduction',self.introduction
        print 'albums',self.albums
        print 'albumURLs',self.albumURLs
        print 'pictureURL',self.pictureURL
        
class album(object):
    def __init__(self):
        self.type='album'
        self.number=None
        self.name=None
        self.artist=None
        self.introduction=None
        self.pictureURL=None
        self.picturePATH=None
        self.songs=None
        self.songURLs=None

    def put(self):
        print self.type
        
        print 'number',self.number
        print 'name',self.name
        print 'artist',self.artist
        print 'introduction',self.introduction
        print 'pictureURL',self.pictureURL
        print 'picturePATH',self.picturePATH
        print 'songs',self.songs
        print 'songURLs',self.songURLs
        

class song(object):
    def __init__(self):
        self.type='song'
        self.number=None
        self.name=None
        self.artists=None
        self.artistURLs=None
        self.album=None
        self.albumURL=None
        self.picturePATH=None

    def put(self):
        print self.type
        
        print 'number',self.number
        print 'name',self.name
        print 'artists',self.artists
        print 'album',self.album
        print 'albumURL',self.albumURL
        print 'artistURLs',self.artistURLs
        print 'picturePATH',self.picturePATH
 

def build(path):
    if path[:12]=='texts/album/':
        tmp=path[12:-3]
        result=album()
    elif path[:13]=='texts/artist/':
        tmp=path[13:-3]
        result=artist()
    elif path[:11]=='texts/song/':
        tmp=path[11:-3]
        result=song()
    else:
        print 'path error'
        return None
    try:
        fil=open(path,'r')
    except:
        print 'faile to open file'
        return None
    if(result.type=='artist'):
        for line in fil:
            if(line[:5]=='name '):
                result.name=line[5:].strip()
            elif(line[:6]=='place '):
                result.place=line[6:].strip()
            elif(line[:7]=='number '):
                result.number=line[7:].strip()
            elif(line[:7]=='albums '):
                result.albums=line[7:].strip().split('%^&*')
                if(result.albums[-1]==''):
                    result.albums=result.albums[:-1]
                if(len(result.albums)==0):
                    result.albums=None
            elif (line[:8]=='picture '):
                result.pictureURL=line[8:].strip()
            elif(line[:10]=='albumURLs '):
                result.albumURLs=line[10:].strip().split('%^&*')
                if(result.albumURLs[-1]==''):
                    result.albumURLs=result.albumURLs[:-1]
                if(len(result.albumURLs)==0):
                    result.albumURLs=None
            elif(line[:13]=='introduction '):
                result.introduction=line[13:].strip()
    if(result.type=='album'):
        for line in fil:
            if(line[:5]=='name '):
                result.name=line[5:].strip()
            elif (line[:6]=='songs '):
                result.songs=line[6:].strip().split('%^&*')
                if(result.songs[-1]==''):
                    result.songs=result.songs[:-1]
                if(len(result.songs)==0):
                    result.songs=None
            elif(line[:7]=='number '):
                result.number=line[7:].strip()
                result.picturePATH='texts/picture/'+tmp+'jpg'
            elif(line[:7]=='artist '):
                result.artist=line[7:].strip()
            elif (line[:8]=='picture '):
                result.pictureURL=line[8:].strip()
            elif(line[:9]=='songURLs '):
                result.songURLs=line[9:].strip().split('%^&*')
                if(result.songURLs[-1]==''):
                    result.songURLs=result.songURLs[:-1]
                if(len(result.songURLs)==0):
                    result.songURLs=None
            elif(line[:13]=='introduction '):
                result.introduction=line[13:].strip()
    if(result.type=='song'):
        for line in fil:
            if(line[:5]=='name '):
                result.name=line[5:].strip()
            elif(line[:7]=='number '):
                result.number=line[7:].strip()
            elif(line[:6]=='album '):
                result.album=line[6:].strip()
            elif(line[:7]=='artist '):
                result.artists=line[7:].strip().split('%^&*')
                if(result.artists[-1]==''):
                    result.artists=result.artists[:-1]
                if(len(result.artists)==0):
                    result.artists=None
            elif(line[:9]=='albumURL '):
                result.albumURL=line[9:].strip()
                if('http://www.xiami.com/album/' in result.albumURL):
                    tmp=result.albumURL.split('/')[-1]
                    result.picturePATH='texts/picture/'+tmp+'.jpg'
            elif(line[:10]=='artistURL '):
                result.artistURLs=line[10:].strip().split('%^&*')
                if(result.artistURLs[-1]==''):
                    result.artistURLs=result.artistURLs[:-1]
                if(len(result.artistURLs)==0):
                    result.artistURLs=None

    fil.close()
    return result

##d:/Users/morning/Desktop/final_version/run/texts/album/15246.txt
if __name__ == "__main__":
    while(1):
        tmp=raw_input('path: ')
        tmp=build(tmp)
        tmp.put()
