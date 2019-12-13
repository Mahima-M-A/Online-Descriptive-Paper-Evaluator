from nltk import word_tokenize,sent_tokenize,PorterStemmer
from nltk.corpus import stopwords,wordnet
import json
import nltk

ps=PorterStemmer()
sw = stopwords.words('english') #to store the stopwords present in english
totalMarks={} #to store the final score

"""
#code to find synonyms and antonyms of the keywords if they exist
syn = list()
ant = list()
for synset in wordnet.synsets("detection"): #example word
   for lemma in synset.lemmas():
      syn.append(lemma.name())    #add the synonyms
      if lemma.antonyms():    #When antonyms are available, add them into the list
        ant.append(lemma.antonyms()[0].name())
"""

#to extract data present in different files
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

#to check the entered answer with respect to the faculty answer
def check(keys,kSyn,kAnt,facAns,studAns,marksAlloted):
    stems=[ps.stem(w) for ans in list(keys.values()) for w in list(ans.keys())] #to find and store the stems of the keywords
    marks={'1':[],'2':[],'3':[],'4':[]}
    l1=[]
    for k,v in studAns.items():
        words=word_tokenize(v)
        l1=[w for w in words if w not in sw and w.isalpha()] #to store the list of tokenized words without any stop words or punctuation marks
        m=[]
        for w in l1:
            mark=0
            x=keys[k]
            s=ps.stem(w.lower())
            if w.lower() in x.keys(): #to check for exact keywords
                if words[words.index(w)-1].lower()=='not':
                    mark=float('-'+x[w.lower()])
                elif float(x[w.lower()]) not in m:
                    mark=float(x[w.lower()])
            elif s in stems: #to check for stem words 
                stem=[w1 for w1 in list(x.keys()) if ps.stem(w1)==s]
                if len(stem):
                    if words[words.index(w)-1].lower()=='not':
                        m.append(float('-'+x[stem[0].lower()]))
                    elif float(x[stem[0].lower()]) not in m:
                        m.append(float(x[stem[0].lower()]))
            elif w.lower() in [l1 for l in list(kSyn.values()) for l1 in l]: #to check for synonyms
                key=[w1 for w1 in list(kSyn.keys()) if w.lower() in kSyn[w1]]
                for k1,v1 in kSyn.items():
                    if words[words.index(w)-1].lower()=='not':
                        mark=float('-'+x[key[0].lower()])
                    elif w.lower() in v1 and key[0].lower() in x.keys():
                        if float(x[key[0].lower()]) not in m:
                            mark=float(x[key[0].lower()])
            elif w.lower() in [l1 for l in list(kAnt.values()) for l1 in l]: #to check for antonyms
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

#to check the similarity between the entered and actual answers by finding the cosine ratio
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

#to check the most commonly occurring grammar errors in a descriptive answer
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

#to calculate the total marks
def calculate(marks,flag,marksAlloted,sim):
    for k,v in marks.items():
        m=sum(v)
        if m>100:
            m=m-(m-100)
        if flag[k]==0: #to check if there was a grammatical error
            m1=str(((m-0.2*(m))*int(marksAlloted[k]))/100)
            if float(m1)<0:
                totalMarks[k]='0.0'
            else:
                totalMarks[k]=m1

        if sim[k]<0.75: #to check the extent upto which the answers are similar
            m1=str(((m-0.3*(m))*int(marksAlloted[k]))/100)
            if float(m1)<0:
                totalMarks[k]='0.0'
            else:
                totalMarks[k]=m1
        else:
            totalMarks[k]=str(m*int(marksAlloted[k])/100)
        
    print(totalMarks)