import os
import math
from scipy import spatial



def similarityPre(pold,pnew):
	cos_sim = 1 - spatial.distance.cosine(pold, pnew)
	return cos_sim



def path_process(pathstr):
	pathstr = pathstr.replace(" ","").replace("\n","")
	path = pathstr[1:len(pathstr)-1]
	pointtmp = path.replace("[","").replace("]","").split(",")
	points =  [[0 for j in range(0, 2)] for i in range(0, int(len(pointtmp)/2))]
	for num in range(0,int(len(pointtmp)/2)):
		points[num][0] = int(pointtmp[2*num])
		points[num][1] = int(pointtmp[2*num+1])
	return points

def PathArea(points):
	area = 0
	for num in range(1, len(points)):
		if(points[num][0]== points[num-1][0]):
			area = area+(9-points[num][0])
	return area

def similarityPath(path1, path2):
	areadiff = PathArea(path1)-PathArea(path2)
	if(areadiff<0):areadiff = -areadiff
	return areadiff

def checkcomplaint(path,complaints):
#	print(complaints)
	for point in path:
		for complaint in complaints:
			if(point[0]==complaint[0] and point[1]==complaint[1]):
				return True
	return False

def updatePreference(oldPre, oldPath, complaints):
	newPre = [-1,-1,-1]
	newPath = []
	solution = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\solution.txt","r",encoding="iso-8859-1")
	
	lines = solution.readlines()
	for line in lines:
		pretmp = line.split(']',1)[0].replace(" ","").replace("[", "").replace("]","").split(',')
		pathstr = line.split(']',1)[1]
		pre = [0,0,0]
		pre[0]=round(float(pretmp[0].replace(" ","")),2)
		pre[1]=round(float(pretmp[1].replace(" ","")),2)
		pre[2]=round(1-pre[0]-pre[1],2)
		path = path_process(pathstr)
		flag = checkcomplaint(path,complaints)
		if(flag ==False and similarityPre(oldPre,pre)>similarityPre(oldPre,newPre)):
			newPre = pre
			newPath = path
		if(flag ==False and similarityPre(oldPre,pre)==similarityPre(oldPre,newPre)
			and similarityPath(path,oldPath)<similarityPath(newPath,oldPath)):
			newPre = pre
			newPath = path
#	print(newPre)
#	print(newPath)
	return newPre




def checkpathdiff(path1,gpath2):
	if(len(path1)<=len(gpath2)): 
		num= len(path1)
	else:
		num = len(gpath2)
	for tmp in range(0,num):
		if(path1[tmp][0]!=gpath2[tmp][0] or path1[tmp][1]!=gpath2[tmp][1]):
			return path1[tmp]
#	print("these paths are the same!")




def findPath(preTB):
	solution = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\solution.txt","r",encoding="iso-8859-1")
	lines = solution.readlines()
	for line in lines:
		pretmp = line.split(']',1)[0].replace(" ","").replace("[", "").replace("]","").split(',')
		pathstr = line.split(']',1)[1]
		pre = [0,0,0]
		pre[0]=round(float(pretmp[0].replace(" ","")),2)
		pre[1]=round(float(pretmp[1].replace(" ","")),2)
		pre[2]=round(1-pre[0]-pre[1],2)
		if(math.isclose(preTB[0],pre[0],rel_tol=1e-5)==True and math.isclose(preTB[1],pre[1],rel_tol=1e-5) ==True):
#			print("find path:"+str(preTB)+pathstr)
			return path_process(pathstr)
	print("I didn't find the path for"+str(preTB))
	return 


def from_old_to_groundtruth(oldpre,groundpre):
	complaintset = []
	step = 0
	while(oldpre!=groundpre):
		oldpath = findPath(oldpre)
#		print(oldpath)
		truethpath = findPath(groundpre)
#		print(truethpath)
		if(checkpathdiff(oldpath,truethpath)==None):
			break
#		print("pre:")
#		print(oldpre)
#		print(" -->")
		complaintset.append(checkpathdiff(oldpath,truethpath))
#		print(complaintset)
		oldpre = updatePreference(oldpre,oldpath,complaintset)
		step = step+1
#		print(oldpre)

#	print("truth!\n")
	return step
#print(from_old_to_groundtruth([0.9,0.05,0.05],[0.1,0.1,0.8]))


#OldPathP =   [[3, 9], [3, 8], [4, 8], [5, 8], [5, 7], [5, 6], [5, 5], [5, 4], [5, 3], [5, 2], [5, 1], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
#Complaince = [5,3]
#print(from_old_to_groundtruth(OldPreP, GroundPreP))

def numofinterference():
	i = 0.05
	j = 0.05
	solutionstep = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\resultstep.txt","w",encoding="iso-8859-1")
	while(i<1):
		while(j<1):
			k = 1-i-j
			i = round(i,2)
			j = round(j,2)
			k = round(k,2)
			if(math.isclose(k,0,rel_tol=1e-3)==True or k<=0):
				break
			step = from_old_to_groundtruth([i,j,k],GroundPreP)
			solutionstep.write("["+str(i)+","+str(j)+","+str(k)+"] "+str(step)+"\n")
			j=j+0.05
		j = 0.05
		i = i+0.05
	
	return 



#numofinterference()
#findPath([0.50,0.20,0.30])

#updatePreference(OldPreP,OldPathP,Complaince)
	
def utility_process(weights,path):
    this_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 隐私
    cost1=[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0.5, 1, 0.5, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    ]
    # 障碍物
    cost2 =[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0],
        [0, 0, 1, 1, 0.5, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    dis,obs,prav = 0.0,0.0,0.0
    for location in path:
        dis = dis + weights[1]
        prav = prav + weights[2]*cost1[location[0]][location[1]]
        obs = obs + weights[0] * cost2[location[0]][location[1]]
    dis = dis - weights[1]
#    print(dis,obs,prav)
    return 10 - (dis + obs + prav)

def from_old_to_groundtruth_pre(oldpre,groundpre,step):  #返回更新几次后的pre
	complaintset = []
	num = 0
	while(oldpre!=groundpre):
		if(num>=step):
			break
		oldpath = findPath(oldpre)
#		print(oldpath)
		truethpath = findPath(groundpre)
#		print(truethpath)
		if(checkpathdiff(oldpath,truethpath)==None):
			break
#		print("pre:")
#		print(oldpre)
#		print(" -->")
		complaintset.append(checkpathdiff(oldpath,truethpath))
#		print(complaintset)
		oldpre = updatePreference(oldpre,oldpath,complaintset)
		num = num + 1
#		print(oldpre)

#	print("truth!\n")
	return oldpre

def mappre(allmappedcase,groundtruth,numofround):
	for num in range(0, len(allmappedcase)):
#		print("what "+str(allmappedcase[num]))
		path1 = findPath(allmappedcase[num])
		truthpath1 = findPath(groundtruth)
		allmappedcase[num] = from_old_to_groundtruth_pre(allmappedcase[num], groundtruth, numofround)
	return allmappedcase


def multiple_differentiation(groundtruth,times):
#	result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\result.txt","w",encoding="iso-8859-1")
	i = 0.05
	j = 0.05
	allmappedcase = []
	result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\round"+str(0)+"_differentation.txt","w",encoding="iso-8859-1")
	while(i<1):
		while(j<1):
			k = 1-i-j
			i = round(i,2)
			j = round(j,2)
			k = round(k,2)
			if(math.isclose(0,k,rel_tol=1e-3)==True or k<=0):
				break
			allmappedcase.append([i,j,k])
			diff = similarityPre([i,j,k],groundtruth)
			result.write("["+str(i)+","+str(j)+","+str(k)+"] "+str(round(diff,5))+"\n")
			j = j+0.05
		j = 0.05
		i = i+0.05
	for num in range(0,times):
		negnum = 0
		result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\round"+str(num+1)+"_differentation.txt","w",encoding="iso-8859-1")
		allmappedcase = mappre(allmappedcase,groundtruth,num+1)
#		result.write("round!+"+str(num)+"\n")
		i = 0.05
		j = 0.05
		posit = 0
		while(i<1):
			while(j<1):
				k = 1-i-j
				i = round(i,2)
				j = round(j,2)
				k = round(k,2)
				if(math.isclose(k,0,rel_tol=1e-3)==True or k<=0 ):
					break
				diff = similarityPre(allmappedcase[posit],groundtruth)
				result.write("["+str(i)+","+str(j)+","+str(k)+"] "+str(round(diff,2))+"\n")
			#	result.write("("+str(i)+","+str(j)+","+str(utility_process(groundtruth,path1))+
			#		","+str(round(utility_process(groundtruth,newpath)))+","+
			#		str(round(delta,2))+","+str(round(base,2))+","+str(round(ratio,2))+")\n")
				j=j+0.05
				posit = posit+1
			j = 0.05
			i = i+0.05
	return


def multiple_delta(groundtruth,times):
#	result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\result.txt","w",encoding="iso-8859-1")
	i = 0.05
	j = 0.05
	allmappedcase = []
	while(i<1):
		while(j<1):
			k = 1-i-j
			i = round(i,2)
			j = round(j,2)
			k = round(k,2)
			if(math.isclose(0,k,rel_tol=1e-3)==True or k<=0):
				break
			allmappedcase.append([i,j,k])
			j = j+0.05
		j = 0.05
		i = i+0.05
	for num in range(0,times):
		negnum = 0
		result = open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\round"+str(num+1)+".txt","w",encoding="iso-8859-1")
		allmappedcase = mappre(allmappedcase,groundtruth,num+1)
#		result.write("round!+"+str(num)+"\n")
		i = 0.05
		j = 0.05
		posit = 0
		while(i<1):
			while(j<1):
				k = 1-i-j
				i = round(i,2)
				j = round(j,2)
				k = round(k,2)
				if(math.isclose(k,0,rel_tol=1e-3)==True or k<=0 ):
					break
				path1 = findPath([i,j,k])
				newpath = findPath(allmappedcase[posit])
				groundpath = findPath(groundtruth)
				delta =  utility_process(groundtruth,newpath) - utility_process(groundtruth,path1) 
				base = utility_process(groundtruth,groundpath)
				ratio = delta/base
				if(ratio<0):
					negnum = negnum+1
				result.write("("+str(i)+","+str(j)+","+str(round(ratio,2))+")\n")
			#	result.write("("+str(i)+","+str(j)+","+str(utility_process(groundtruth,path1))+
			#		","+str(round(utility_process(groundtruth,newpath)))+","+
			#		str(round(delta,2))+","+str(round(base,2))+","+str(round(ratio,2))+")\n")
				j=j+0.05
				posit = posit+1
			j = 0.05
			i = i+0.05
		print("num:"+str(negnum))
	return


#OldPreP = [0.05,0.9,0.05] #security, efficiency, privacy
GroundPreP = [0.5,0.4,0.1]
print(similarityPre([0.2,0.3,0.5],[0.25,0.2,0.55]))
#multiple_differentiation(GroundPreP,3)
#print(findPath(GroundPreP))
#print(utility_process(GroundPreP,findPath(GroundPreP)))
#multiple_delta(GroundPreP,3)
#print(similarityPre([0.4, 0.3, 0.3],[0.5,0.4,0.1]))
#print(from_old_to_groundtruth_pre([0.2,0.1,0.7],GroundPreP,1))
#numofinterference()

'''
def utility_delta():
	i = 0.05
	j = 0.05
	while(i<1):
		while(j<1):
			k = 1-i-j
			i = round(i,2)
			j = round(j,2)
			k = round(k,2)
			if(k<=0):
				break
#			print("["+str(i)+","+str(j)+","+str(k)+"] ")
			path1 = findPath([i,j,k])
			truthpath1 = findPath(GroundPreP)
			complainttmp = checkpathdiff(path1,truthpath1)
			if(complainttmp==None):
				delta = 0
			else:
				complaintsettmp = []
				complaintsettmp.append(complainttmp)
				newpre = updatePreference([i,j,k], path1, complaintsettmp)
				path2 = findPath(newpre)
				delta = utility_process(GroundPreP,path1) - utility_process(GroundPreP,path2)
				if(delta<0):
					print("oldpre:"+"["+str(i)+","+str(j)+","+str(k)+"]")
					print("oldpath: " +str(path1))
					print("newpre:"+str(newpre))
					print("newpath: "+str(path2))
					print("groundpre:"+str(GroundPreP))
					print("groundpath: " +str(truthpath1))
					print("delta:"+str(delta)+"\n\n")
#			print(str(delta))
			j=j+0.05
		j = 0.05
		i = i+0.05
	return
'''
#utility_delta()