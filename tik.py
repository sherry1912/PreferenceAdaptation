def process(roundnum):
    result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\round"+str(roundnum)+".txt","r",encoding="iso-8859-1")
    realresult = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\result.txt","w",encoding="iso-8859-1")
    lines = result.readlines()
    delta = [[0 for j in range(0, 100)] for i in range(0, 100)]
    for line in lines:
        tmp = line.replace(" ","").replace("(","").replace(")","").split(",")
        i = int(100*float(tmp[0]))
        j = int(100*float(tmp[1]))
        delta[i][j] = float(tmp[2])
    i = 5
    while(i<100):
        j = 5
        realresult.write("\\addplot3 [surf] coordinates{\n")
        while(j<100-i):
            realresult.write("("+str(i)+","+str(j)+","+str(round(delta[i][j],2))+")")
            if(j+5<100-i):
                realresult.write("("+str(i)+","+str(j+5)+","+str(round(delta[i][j+5],2))+")")
            if(i+5<100 and j+5<100-i):
                realresult.write("("+str(i+5)+","+str(j+5)+","+str(round(delta[i+5][j+5],2))+")")
            if(i+5<100):
                realresult.write("("+str(i+5)+","+str(j)+","+str(round(delta[i+5][j],2))+")")
            realresult.write("("+str(i)+","+str(j)+","+str(round(delta[i][j],2))+")")
            j = j+5
        realresult.write("};\n")
        i = i+5
process(3)