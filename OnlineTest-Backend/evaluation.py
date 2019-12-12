from nltk import word_tokenize,sent_tokenize,PorterStemmer
from nltk.corpus import stopwords,wordnet
import json
import nltk

ps=PorterStemmer()
sw = stopwords.words('english')
totalMarks={}
def extract(studAns):
    with open('keywords.json') as key:
        keys=json.load(key,strict=False)

    with open('keySyn.json') as key:
        kSyn=json.load(key,strict=False)
    
    with open('keyAnt.json') as key:
        kAnt=json.load(key,strict=False)

    with open('answers.json') as answers:
        facAns=json.load(answers,strict=False)

    with open('marksAlloted.json') as markAllot:
        marksAlloted=json.load(markAllot,strict=False)

    check(keys,kSyn,kAnt,facAns,studAns,marksAlloted)

def check(keys,kSyn,kAnt,facAns,studAns,marksAlloted):
    stems=[ps.stem(w) for ans in list(keys.values()) for w in list(ans.keys())]
    marks={'1':[],'2':[],'3':[],'4':[]}
    l1=[]
    for k,v in studAns.items():
        words=word_tokenize(v)
        l1=[w for w in words if w not in sw and w.isalpha()]
        m=[]
        for w in l1:
            mark=0
            x=keys[k]
            s=ps.stem(w.lower())
            if w.lower() in x.keys():
                print('1   ',w.lower())
                if words[words.index(w)-1].lower()=='not':
                    mark=float('-'+x[w.lower()])
                elif float(x[w.lower()]) not in m:
                    mark=float(x[w.lower()])
            elif s in stems:
                stem=[w1 for w1 in list(x.keys()) if ps.stem(w1)==s]
                if len(stem):
                    if words[words.index(w)-1].lower()=='not':
                        m.append(float('-'+x[stem[0].lower()]))
                    elif float(x[stem[0].lower()]) not in m:
                        m.append(float(x[stem[0].lower()]))
            elif w.lower() in [l1 for l in list(kSyn.values()) for l1 in l]:
                key=[w1 for w1 in list(kSyn.keys()) if w.lower() in kSyn[w1]]
                for k1,v1 in kSyn.items():
                    if words[words.index(w)-1].lower()=='not':
                        mark=float('-'+x[key[0].lower()])
                    elif w.lower() in v1 and key[0].lower() in x.keys():
                        if float(x[key[0].lower()]) not in m:
                            mark=float(x[key[0].lower()])
            elif w.lower() in [l1 for l in list(kAnt.values()) for l1 in l]:
                key=[w1 for w1 in list(kAnt.keys()) if w.lower() in kAnt[w1]]
                for k1,v1 in kAnt.items():
                    if words[words.index(w)-1].lower()=='not':
                        mark=float(x[key[0].lower()])
                    elif w.lower() in v1 and key[0].lower() in x.keys():
                        if float(x[key[0].lower()]) not in m:
                            mark=float('-'+x[key[0].lower()])

            if mark not in m:
                m.append(mark)
            if m not in marks[k]:
                marks[k]=m
    sim=similarity(studAns,facAns)
    grammarCheck(studAns,marks,marksAlloted,sim)

def similarity(studAns,facAns):
    sim={}
    for (k,v),(k1,v1) in zip(studAns.items(),facAns.items()):
        studWords=word_tokenize(v)
        facWords=word_tokenize(v1)
        lStud={w.lower() for w in studWords if w not in sw and w.isalpha()}
        lFac={w.lower() for w in facWords if w not in sw and w.isalpha()}
        listWords=lStud.union(lFac)
        l1=[]
        l2=[]
        for w in listWords: 
            if w in lStud: l1.append(1) 
            else: l1.append(0) 
            if w in lFac: l2.append(1) 
            else: l2.append(0)
        c=0
        for i in range(len(listWords)): 
            c+= l1[i]*l2[i]
        if not sum(l1)==0 and not sum(l2)==0:
            sim[k1] = c / float((sum(l1)*sum(l2))**0.5)
        else:
            sim[k1] = 0.0
    return sim

    
def grammarCheck(studAns,marks,marksAlloted,sim):
    flag={'1':1,'2':1,'3':1,'4':1}
    for k,v in studAns.items():
        sent=sent_tokenize(v)
        for s in sent:
            tags=nltk.pos_tag(word_tokenize(s))
            for i in range(len(tags)):
                if 'VB' in tags[i][1]:
                    if i==len(tags)-1 or i==0:
                        if not tags[i][1]=='VBG':
                            flag[k]=0
                    elif 'DT' == tags[i-1][1] or 'JJ' in tags[i-1][1]:
                        if not tags[i][1]=='VBG':
                            flag[k]=0
                elif 'NN' in tags[i][1]:
                    if not(i==len(tags)-1):
                        if 'JJ' in tags[i+1][1] or 'DT' == tags[i+1][1]:
                            flag[k]=0
    calculate(marks,flag,marksAlloted,sim)

def calculate(marks,flag,marksAlloted,sim):
    for k,v in marks.items():
        m=sum(v)
        m1=''
        if flag[k]==0:
            m1+=str(((m-0.2*(m))*int(marksAlloted[k]))/100)

        if sim[k]<0.75:
            m1+=str(((m-0.3*(m))*int(marksAlloted[k]))/100)
        else:
            totalMarks[k]=str(m*int(marksAlloted[k])/100)

        if float(m1)<0:
            totalMarks[k]='0.0'
        else:
            totalMarks[k]=m1
    print(totalMarks)