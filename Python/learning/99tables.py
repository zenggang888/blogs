m=1
while m<=9:
    i=1
    while i<=m:
        print("%d*%d"%(m,i)+"="+str(i*m),end="\t")
        i+=1
    print()
    m+=1