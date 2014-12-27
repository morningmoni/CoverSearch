import numpy as np
import cv2
import glob
import time

def drawMatches(img1, kp1, img2, kp2, matches):

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

##    shape1=img1.shape
##    shape2=img2.shape
##    if shape2[0]>shape1[0]:
##        img1,img2=img2,img1
##        shape1,shape2=shape2,shape1
##    height=max(shape1[0],shape2[0])
##    width=shape1[1]+shape2[1]
##
##    img=np.zeros([height,width,3], np.uint8)
##    for i in range(len(img2)):
##        img[i]=img1[i].tolist()+img2[i].tolist()+np.zeros((width-len(img1[0])-len(img2[0]),3), np.uint8).tolist()
##    for i in range(len(img2),len(img1)):
##        img[i]=img1[i].tolist()+np.zeros((width-len(img1[0]),3), np.uint8).tolist()
    img = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    img[:rows1,:cols1,:] = np.dstack([img1])
    img[:rows2,cols1:cols1+cols2,:] = np.dstack([img2])
    for mat in matches:

        img1_idx = mat[0].queryIdx
        img2_idx = mat[0].trainIdx

        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        cv2.circle(img, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(img, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)
        cv2.line(img, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)
    curtime=time.clock()
    print "runtime=",curtime-inittime
    cv2.imshow('Matched Features', img)
    while True:
        ch=cv2.waitKey(5)
        if ch==27:
            cv2.destroyAllWindows()
            break

def compare(imgname,orb,des1,bf):
    amount=0.0
    img2=cv2.imread(imgname,0)
    kp2,des2=orb.detectAndCompute(img2,None)
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
    for i in matches:
        amount+=i[0].distance

    return amount
    
    
def imgProcess(query,kpsToDraw):
    img1=cv2.imread(query,0)
    img11=cv2.imread(query)

    orb = cv2.ORB()
    kp1,des1=orb.detectAndCompute(img1,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    mim=-1
    name=''
    for filename in glob.glob("*.jpg"):
        if filename!=query:
            n=compare(filename,orb,des1,bf)
            if n<mim or mim==-1:
                mim=n
                name=filename   
            
    img2=cv2.imread(name,0)
    img22=cv2.imread(name)
    kp2,des2=orb.detectAndCompute(img2,None)
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
    matches=sorted(matches,key = lambda a : a[0].distance)

    drawMatches(img11, kp1, img22, kp2, matches[:kpsToDraw])
inittime=time.clock()
imgProcess('target.jpg',10)

