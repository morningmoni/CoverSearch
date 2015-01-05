import numpy as np
import cv2
import glob

def compare(imgname,orb,des1,bf):
    amount=0.0
    img2=cv2.imread(imgname,0)
    kp2,des2=orb.detectAndCompute(img2,None)
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
    for i in matches:
        amount+=i[0].distance

    return amount
def myCaclHist(image):
    b=0
    g=0
    r=0  
    for x in range(len(image)):
        for y in range(len(image[0])):
           b+=image[x][y][0]
           g+=image[x][y][1]
           r+=image[x][y][2]
    total=b+g+r
    rb=float(b)/total
    rg=float(g)/total
    rr=float(r)/total
##    print b,g,r,
##    print rb,rg,rr,
    ls=[]
    for i in (rb,rg,rr):
        if i<0.3:
            ls+=[0]
        elif i>=0.3 and i<0.6:
            ls+=[1]
        else:
            ls+=[2]
##    print ls
    return ls
def caclHist(imgname):
##    print imgname
    img=cv2.imread(imgname)
    col=img.shape[1]
    row=img.shape[0]
##    print col,row
    ls=[]
    imgLT=img[:row/2,:col/2]
    ls+=myCaclHist(imgLT)
    imgLB=img[row/2:,:col/2]
    ls+=myCaclHist(imgLB)
    imgRT=img[:row/2,col/2:]
    ls+=myCaclHist(imgRT)
    imgRB=img[row/2:,col/2:]
    ls+=myCaclHist(imgRB)
##    print ls
    return ls


def create_index():
    try:
        f=open("static/texts/index",'r')
    except:
        f=open("static/texts/index",'w')
        for pic in glob.glob("static/texts/picture/*.jpg"):
            if "target" not in pic:
                print pic
                v=caclHist(pic)
                f.write(pic+'\t')
                for i in v:
                    f.write(str(i))
                f.write('\n')
        f.close()
        f=open("static/texts/index",'r')

    dic={}
    for line in f:
        line=line.strip()
        right=line.find('\t')
        name=line[:right]
        index=list(line[right+1:])
        index=[int(i) for i in index]
##        print name,index
        dic[name]=index
    f.close()
    return dic

#match
def imgProcess(query):
    dic=create_index()
    tar=caclHist(query)
    print tar
    print "Similar picture(s):"

    img1=cv2.imread(query,0)
    img11=cv2.imread(query)

    orb = cv2.ORB()
    kp1,des1=orb.detectAndCompute(img1,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    mim=-1
    name=''
    for v in dic.keys():    
        if tar==dic[v]:
            print v
            n=compare(v,orb,des1,bf)
            if n<mim or mim==-1:
                mim=n
                name=v
    loc=name.rfind("\\")
    name=name[:loc]+'/'+name[loc+1:]
    print "results=",name
    return name
##    img2=cv2.imread(name,0)
##    img22=cv2.imread(name)
##    kp2,des2=orb.detectAndCompute(img2,None)
##    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
##    matches=sorted(matches,key = lambda a : a[0].distance)
       
            
if __name__ == "__main__":
    imgProcess("static/covers/target.jpg")

