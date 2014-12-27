import numpy as np
import cv2
import glob


m=-1
name=''
def compare(a):
    amount=0.0
    img2=cv2.imread(a,0)
    kp2,des2=orb.detectAndCompute(img2,None)
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
    for i in range(len(matches)):
        amount=amount*(float(i)/(i+1))+(matches[i][0].distance**2)/float(i+1)
    #print amount
    return amount
    
    
 



img1=cv2.imread("target.jpg",0)
orb = cv2.ORB()
#surf.upright=True
kp1,des1=orb.detectAndCompute(img1,None)

##print len(kp)
##print surf.hessianThreshold
##print surf.descriptorSize()

bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)

for filename in glob.glob("*.jpg"):
    if filename!='target.jpg':
        n=compare(filename)
        if n<m or m==-1:
            m=n
            name=filename
    #print filename,n,m
    
        
img2=cv2.imread(name,0)
kp2,des2=orb.detectAndCompute(img2,None)
matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
matches=sorted(matches,key = lambda a : a[0].distance)



rows1 = img1.shape[0]
cols1 = img1.shape[1]
rows2 = img2.shape[0]
cols2 = img2.shape[1]

out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])
out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

#print matches[:10]
for i in matches[:20]:
    img1_idx = i[0].queryIdx
    img2_idx = i[0].trainIdx
##    print i[0].queryIdx
##    print i[0].trainIdx
##    print i[1].queryIdx
##    print i[1].queryIdx
    (x1,y1) = kp1[img1_idx].pt
    (x2,y2) = kp2[img2_idx].pt
##    print (x1,y1)
##    print (x2,y2)
    color = tuple(np.random.randint(0,255,3).tolist())
    cv2.circle(out, (int(x1),int(y1)), 4, color, 1)   
    cv2.circle(out, (int(x2)+cols1,int(y2)), 4, color, 1)
    cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), color, 1)

cv2.imshow('Matched Features', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
    
