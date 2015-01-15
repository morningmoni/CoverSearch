def compare(a,b):
    tmp=0
    for i in range(len(a)):
        if(a[i]!=' '):
            if(a[i] in b):
                tmp+=1
    return tmp

def resortalbum(lis,keyword):
    result=[]
    gaoxiangguan=[]
    xiangguandu=[0]*len(lis)
    result1=[]
    for i in range(len(lis)):
        result.append(lis[i])


    for i in range(len(lis)):#get xiangguandu
        tmp=[compare(keyword,result[i]['albumname']),compare(keyword,result[i]['albumartist'])]
        
        xiangguandu[i]=max(1.2*(2.0*float(tmp[0])/len(keyword)+float(tmp[0])/len(result[i]['albumname'])),1.0*(2.0*float(tmp[1])/len(keyword)+float(tmp[1])/len(result[i]['albumartist'])))
        
    gao=[]
    for i in range(len(lis)):
        print result[i]['albumname'],xiangguandu[i]
        if xiangguandu[i]>=2.8:
            gaoxiangguan.append([result[i],xiangguandu[i]])
            gao.append(i)

    if(len(gaoxiangguan)==0):
        return result
    gaoxiangguan.sort(key=lambda item:item[0]['zan'])
    gaoxiangguan.sort(key=lambda item: item[1])
    for i in range(len(gaoxiangguan)):
        result1.append(gaoxiangguan[len(gaoxiangguan)-i-1][0])
    for i in range(len(lis)):
        if i not in gao:
            result1.append(result[i])
            
    
    return result1

