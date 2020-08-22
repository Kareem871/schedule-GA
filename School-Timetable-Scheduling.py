
'''
Details about the program:
    - We assumed :
        A)Hard constraint that implemented in [2], it is performed after each crossover or mutation operations.
        B)Soft constraints that implemented in [3-5], they increase some value called penalty to use it in fit operation.
        C)Fittness function is : (Fittness=1/(1+penalty)), it should be maximized

    - Some details about some functions we used:        
        1)tech_sub:contains pairs of (Teacher name, Subject name).
        2)hardconstraint(ch): ensures that a teacher can't be in different classes at the same time.
        3)soft1(ch): increase the penalty if a teacher has more than 23 , 20 lectures per week for all classes.
        4)soft2(tech_count): increase the penalty in case of there is uneven total time slot for all teachers in the same field.
        5)soft3(ch): increase the penalty if a course was held in more than 2 time-slots in a day for one class from a prededefined subjects,
                      and more than one time.
        6)GA(chromosomeNo,classNo,mx,mp,iterations) : { chromosomeNo: the number of chromosomes in the generation,
                                                        classNo     : the number of classes in the chromosome,
                                                        mx          : the probability of crossover,
                                                        mp          : the probability of mutation,
                                                        iterations  : the number of iterations }            
        
    - Chromosome structure:
        The chromosome consists of classNo classes, each class has 7 lectures daily, 5 days weekly.

    - References:
        [1] https://bit.ly/35OnnnH
'''

import math,random

tech_sub = [	#17 teacher
                ["a", "math      "],  
                ["b", "science   "],
                ["c", "phylisophy"],
                ["d", "history   "],
                ["e", "health    "],
                ["f", "culture   "],
                ["g", "english   "],
                ["h", "arabic    "],
                ["i", "chemistry "],
                ["j", "physics   "],
                ["k", "math      "],  
                ["l", "science   "],  
                ["m", "health    "],
                ["n", "english   "],  
                ["o", "history   "],  
                ["p", "culture   "],
                ["q", "arabic    "]
    ]

days = ["Sunday   ","Monday   ","Tuesday  ","Wednesday","Thursday "]


def randch():
    x=[]   
    for i in range(5):  #No. of days
        y=[]   
        for j in range(7):  #No. of subjects
            e=len(tech_sub)
            y.append(tech_sub[random.randint(0,e-1)])

        x.append([days[i],y])
    return x


def init(n):
    ch=[]
    for i in range(n):    
        ch.append(randch())
    return ch


def gen(x,y):
    gen=[]
    for i in range(x):
        gen.append(init(y))
    return gen


def fit(ch):
    penalty=soft1(ch)+soft3(ch)
    return 1/(1+penalty)


def fitAll(gen):
    fitall=[fit(ch) for ch in gen]
    tfit=sum(fitall)
    fits=[100*f/tfit for f in fitall]
    return fits


def select(fits):
    rs=0
    r=random.randint(0,100)
    for i in range(len(fits)):
        rs+=fits[i]
        if r < rs:
            return i
    return i


def crossover(p1,p2):
    print("crossover occured")
    y1=[]
    y2=[]
    for classs in range(len(p1)):   #No. of classes
        y11=[]
        y22=[]
        for day in range(len(days)):  #No. of days            
            cpx = random.randint(0,len(p1[0][0][1]))   #random from 0 to No. of subjectes (7)
            x1=p1[classs][day][1][:cpx]+p2[classs][day][1][cpx:]  #p1[classs][day][1] gives the array of subjects 
            y11.append([days[day],x1])                             #append array of [day,subject]
            #y11.append(x1)
            x2=p2[classs][day][1][:cpx]+p1[classs][day][1][cpx:]
            y22.append([days[day],x2])                             #append array of [day,subject]
            #y22.append(x2)
        y1.append(y11)
        y2.append(y22)
    t1=hardconstraint(y1)
    t2=hardconstraint(y2)
    return t1,t2

#send to hardcons
def mutation(ch):
    print("mutation occured")
    #print("ch before \n ",ch)
    for i in range(len(ch)):   #No. of classes
        for j in range(len(days)):
            mpx = random.randint(0,len(ch[i][j][1])-1)
            mpy = tech_sub[random.randint(0,len(ch[0][0][1]))]
            ch[i][j][1][mpx] = mpy
    #print("ch after \n ",ch)
    ch = hardconstraint(ch)
    return ch


#Constrain No.1 (#done)
def hardconstraint(ch):  
    for classs in range(len(ch)):    #No. of classes
        for day in range(len(days)):  #No. of days
            for subject in range(len(ch[0][0][1])):   #No. of subjects (7)
                tmp = ch[classs][day][1][subject][0]  #store teacher name in tmp
                for otherclass in range(len(ch)):     #No. of classes to compare the subject above with all subjects
                    if otherclass == classs:          #Don't compare with yourself
                        continue
                    while tmp == ch[otherclass][day][1][subject][0]:
                        random_teacher = tech_sub[random.randint(0,len(ch[0][0][1]))] #choose another random teacher
                        ch[otherclass][day][1][subject] = random_teacher
    return ch


# if teacher has more than 23 , 20 leactures (#done)
def soft1(ch):
    tech_count=[]
    penalty=0
    for teacher in range(len(tech_sub)):
        counter=0
        for classs in range(len(ch)):
            for day in range(len(days)):
                for subject in range(len(ch[0][0][1])):
                    if tech_sub[teacher] == ch[classs][day][1][subject]:
                        counter+=1
        tech_count.append([tech_sub[teacher],counter])
    for i in range(len(tech_count)):
        if tech_count[i][1] > 23:
            penalty+=15
        elif tech_count[i][1] > 20:
            penalty+=10
        else : penalty+=5     
    penalty+= soft2(tech_count)
    return penalty


# Soft 2 : uneven total time slot for all teachers in the same field    (#done)
def soft2(tech_count):
    penalty=0
    tmparr=[]   
    for teacher in range(len(tech_sub)):
        sub=tech_sub[teacher][1]
        tmp=-1
        if tech_sub[teacher][1] in tmparr:
                continue
        for techcount in range(len(tech_count)):
            if sub == tech_count[techcount][0][1]:
                if tmp == -1: 
                    tmp=tech_count[techcount][1]                
                elif tmp != tech_count[techcount][1]:
                        penalty+=1
                        break
        tmparr.append(tech_sub[teacher][1])    
    return penalty


#soft 3 each course must be held in less than 3 time-slots in a day for one class from arr[], else less than two times (#done)
def soft3(ch):
    arr = ["math      ","science   ","arabic    ","english   ","physics   ","culture   "]
    tmparr=[]
    penalty=0
    for subject in range(len(tech_sub)):
        sub=tech_sub[subject][1]         
        if sub in tmparr:
            continue
        for classs in range(len(ch)):
            for day in range(len(days)):
                counter=0
                for lecture in range(len(ch[0][0][1])):
                    if sub == ch[classs][day][1][lecture][1]:
                        counter+=1
                if sub in arr:
                    if counter >= 3:
                        penalty+= 3
                    else :
                        penalty += 6
                        
                elif counter == 2:
                    penalty+=4
            tmparr.append(sub)        
    return penalty


def report(gen,fits):  
    for i in range(len(gen)):
        ch =gen[i]
        print("chromosome : ",(i+1))
        for j in range(len(ch)):
            print("Class : ",(j+1))
            print(ch[j])    
        print(f"Fit : {fit(ch)}\nFit % :{fits[i]:5.2f}")
        print("="*100)
        
#################################################
def GA(chromosomeNo,classNo,mx,mp,iterations):
    generation = gen(chromosomeNo,classNo)
    ch1=0
    ch2=0
    fits=[]
    for j in range(iterations):
        print(f'iterations {j}')
        #print("_"*30)
        fits=fitAll(generation)
        #report(generation,fits)
        new_gen=[]
        for i in range(chromosomeNo//2):
            p1=select(fits)
            p2=select(fits)
            #print("Selection")
            #print(f"Parent 1 {p1} : fitness {fit(generation[p1])}")
            #print(f"Parent 2 {p2} : fitness {fit(generation[p2])}")
            
            if random.uniform(0,1) < mx:
                ch1,ch2=crossover(generation[p1],generation[p2])
            else:
                ch1,ch2=generation[p1],generation[p2]
            if random.uniform(0,1) < mp:
                ch1=mutation(ch1)
                print("*")
            if random.uniform(0,1) < mp:
                ch2=mutation(ch2)
                print("*")
            new_gen.append(ch1)
            new_gen.append(ch2)
            #print("Child : 1")
            #for j in range(len(ch1)):
            #    print("Class : ",(j+1))
            #    print(ch1[j])
            #print("Child : 2")
            #for d in range(len(ch1)):
            #    print("Class : ",(d+1))
            #    print(ch2[d])       
        generation=new_gen
    report(generation,fits)
        
    
def main():
    GA(10,3,0.7,0.001,100)   

    
main()