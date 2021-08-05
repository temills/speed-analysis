#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import random
import pandas as pd


#TODO
#combine response time/num responses into single metric signifying ease of response
#perform speed analysis on other categories
#and then concat data (descriptor corr. w coming to mind, and ease of response to descriptor) to get overall corr

#speed data
#correlation of descriptor with coming to mind, as calculated from rating data
#genCorr = {'large': 0.3443250488940599, 'cool': 0.2786921485840363, 'striking': 0.35164786386252667, 'dangerous': 0.3241003513545623, 'lifespan': 0.31874309221991487, 'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}


with open('/Users/traceymills/consideration/speed-analysis/data.csv.json') as f:
  data = json.load(f)
#descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan", "cute", "normal", "land", "think", "awake", "type, mammal", "tropics", "diet, carnivore"]
descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
descriptors = descriptors1 + descriptors2
genCorr = {'type, mammal': 0.18894731849701007, 'diet, carnivore': 0.2038779167838987, 'large': 0.3458998251843229, 'cute': 0.05406309013621359, 'cool': 0.2777483689929533, 'normal': -0.18053805054990885, 'striking': 0.3521983036172046, 'dangerous': 0.3271850392200191, 'tropics': 0.04016115026339956, 'land': 0.12875489519410027, 'lifespan': 0.317285976201681, 'think': 0.10311812598072409, 'awake': 0.06481348622086591,'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}


#with open('/Users/traceymills/consideration/speed-analysis/vegetables.json') as f:
#  data = json.load(f)
#descriptors = ["dishes", "popular", "available", "crunchy", "think", "warm", "heavy", "calories", "fragrant", "sweet"]
#genCorr = {'think': 0.47655677204291835, 'dishes': 0.5705715245609457, 'popular': 0.5414066993921484, 'available': 0.7111093760951049, 'fragrant': -0.11504084613286147, 'warm': -0.05142553559714049, 'sweet': 0.16918140757029312, 'crunchy': 0.4246094506168629, 'heavy': 0.03928128161072006, 'calories': -0.09369407427843358}

#with open('/Users/traceymills/consideration/speed-analysis/restaurants.json') as f:#
#  data = json.load(f)
#descriptors = ["interesting side dishes", "soft food", "cold food", "desserts", "healthy", "popular", "many locations", "casual", "quick", "brightly colored logo"]
#genCorr = {'interesting side dishes': 0.05797794277449986, 'soft food': 0.11357816033282128, 'cold food': -0.0679028961223725, 'desserts': 0.052718285665607136, 'popular': 0.4220453392935601, 'many locations': 0.5335387989116023, 'is unique': -0.2925555800029079, 'healthy': -0.012857634523901745, 'brightly colored logo': 0.2826773815547698, 'lively': 0.12550827795437736, 'variety': 0.17920547046707774, 'well decorated': 0.11966768704986638, 'expensive': -0.29991989021440446, 'quick': 0.24504742209076236, 'casual': 0.23089662426660587}


data = sorted(data, key=lambda k: k['subject_id'])

animals = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "zebra", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "giraffe", "bull", "whale", "rabbit", "lion", "hippo", "baboon", "bird", "monkey", "snake", "tiger", "panther", "kangaroo", "owl", "elephant", "otter", "rhino", "cheetah", "gazelle", "alligator", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "grizzly bear", "lizard", "fish"]

#get correlation between desriptor generation score and whatever dict is passed in
def getGenCorr(descriptorData):
    x, y = [], []
    for d in descriptors:
        x.append(descriptorData[d])
        y.append(genCorr[d])
    return np.corrcoef(x, y)[0][1]

##### all subjects ######

#get average number of responses given in timed trial for each descriptor
def getNumResPerDescriptor():
    resDict = {}
    for trial in data:
        d = trial["descriptor"]
        #for each descriptor, list with num total responses, num times descriptor given
        resDict[d] = resDict.get(d, [0, 0])
        if trial["responses"] == '': num = 0
        else: num = len(trial["responses"].split(","))
        resDict[d][0] = resDict[d][0] + num
        resDict[d][1] = resDict[d][1] + 1
    #calc average
    for d in resDict.keys():
        resDict[d] = resDict[d][0]/resDict[d][1]
    return resDict
#numResPerDescriptor = getNumResPerDescriptor()
#for i in numResPerDescriptor.keys():
#    print(i + ": " + str(numResPerDescriptor[i])+", " + str(genCorr[i]))
#correlation between generation and ave num responses for each descriptor
#getGenCorr(numResPerDescriptor))

#returns time it took to give first n responses for each descriptor
#only includes trials where at least n responses were given?
def getFirstNResponseTime(n):
    resDict = {}
    firsts = {}
    for trial in data:
        d = trial["descriptor"]
        #for each descriptor, list with reaction time for first n, num times descriptor given
        resDict[d] = resDict.get(d, [0, 0])
        if(trial["responses"] == '' or len(trial["responses"].split(",")) < n): continue
        times = list(map(float, trial["rt"].split(",")))
        resDict[d][0] = resDict[d][0] + sum(times[:n])
        resDict[d][1] = resDict[d][1] + 1
    #calc average
    for d in resDict.keys():
        resDict[d] = resDict[d][0]/resDict[d][1]
    return resDict
firstNResponseTime = getFirstNResponseTime(2)
#correlation between generation and rave esponse time for first n responses for each descriptor
#print(getGenCorr(firstNResponseTime))



#first/time+second/time...
def getCombinedResponseMetric():
    times = {}
    scores = {}
    firsts = {}
    for trial in data:
        score = 0
        d = trial["descriptor"]
        if trial["responses"] != "":
            rtList = list(map(float, trial["rt"].split(",")))
            score = sum([(1000/rt) for rt in rtList])
        scores[d] = scores.get(d, [0,0])
        scores[d][0] = scores[d][0] + score
        scores[d][1] = scores[d][1] + 1
        if(trial["q_order"]==1):
            firsts[d] = firsts.get(d, [])
            firsts[d].append(score)
    combined = {}
    for d in descriptors:
        combined[d] = scores[d][0]/scores[d][1]
    return combined, firsts

comb, firsts = getCombinedResponseMetric()
for d in descriptors:
    print(d + ":")
    print(str(comb[d]) + ", " + str(sum(firsts.get(d,[]))/max(1, len(firsts.get(d,[])))) + ", " + str(firsts.get(d,[])))

print(getGenCorr(comb))


def getCorr(d1,d2):
    x, y = [], []
    for d in descriptors:
        x.append(d1[d])
        y.append(d2[d])
    return np.corrcoef(x, y)[0][1]
#print(getCorr(firstNResponseTime,numResPerDescriptor))
c = []
x = []
ds = []
times = []
num = []
for d in descriptors:
    c.append(comb[d])
    x.append(genCorr[d])
    ds.append(d)
    times.append(firstNResponseTime[d])
    #num.append(numResPerDescriptor[d])

print(c)
print(x)
#print(ds)
#print(times)
#print(num)

#descriptors = ["large", "cool", "striking", "dangerous", "lifespan", "has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little", "dishes", "popular", "available", "crunchy", "think", "warm", "heavy", "calories", "fragrant", "sweet", "interesting side dishes", "soft food", "cold food", "desserts", "healthy", "popular", "many locations", "casual", "quick", "brightly colored logo"]
genCorrs = [0.3458998251843229, 0.2777483689929533, 0.3521983036172046, 0.3271850392200191, 0.317285976201681, 0.07622946411113914, -0.20459332100398267, 0.07487908633416952, 0.10441947183906619, -0.04724035442610212, 0.5705715245609457, 0.5414066993921484, 0.7111093760951049, 0.4246094506168629, 0.47655677204291835, -0.05142553559714049, 0.03928128161072006, -0.09369407427843358, -0.11504084613286147, 0.16918140757029312, 0.05797794277449986, 0.11357816033282128, -0.0679028961223725, 0.052718285665607136, -0.012857634523901745, 0.4220453392935601, 0.5335387989116023, 0.23089662426660587, 0.24504742209076236, 0.2826773815547698]
#combinedScores = [0.7189398702112204, 0.5909158132579565, 0.587057954098114, 1.0211121278923745, 0.3810966808515722, 0.1944878747764516, 0.31419667511194976, 0.38907005725220234, 0.2212369645787548, 0.16663319587310355, 0.5436974142643161, 0.7867610008156921, 0.6244867949209689, 0.42563974330414467, 0.6108285607858428, 0.26577769247077554, 0.25793559056728604, 0.19636094504383597, 0.22191666586474829, 0.22531908620900626, 0.2599724688012331, 0.2343423436083872, 0.32435216997275274, 0.25366827692634614, 0.2510137135438032, 0.5325641390749037, 0.6081199150509464, 0.6089924428787277, 0.5406169736933395, 0.3321984821509997]
combinedScores = [1.9867284996822925, 2.0729161108743117, 1.9092906289027687, 2.9366090364809323, 1.213744129581771, 0.7194530691208522, 1.0581686705305398, 1.35268608171713, 0.6537736038755312, 0.5741224719656765, 1.6838110999322993, 2.2625079823661824, 1.8826960638739754, 1.1035458215019527, 1.7685460700009088, 0.8437819942275065, 0.7493571504025612, 0.535350553229499, 0.7025648511651744, 0.5839945901151662, 1.2226002605889164, 0.7134663532212875, 1.244913019848883, 0.7841424838909161, 0.8561252768548857, 1.6949834391066232, 2.306599381186884, 2.342543193968948, 1.924250778138444, 0.9922838646385286]
print("hi")
print(np.corrcoef(genCorrs, combinedScores)[0][1])


######### within subject ###########

#get average distance from subject average of number of responses given in timed trial for each descriptor
#want dictionary with each descriptor, for each subejct add distance from average for that descriptor to dict
def getNumResPerDescriptorWithin():
    resDict = {}
    id = ""
    for trial in data:
        if trial["subject_id"] != id:
            #finish up last one
            if trial != data[0]:
                ave = sum(numRes.values())/len(numRes.values())
                #add deviation from average to list for each descriptor
                for d in numRes.keys():
                    deviation = numRes[d] - ave
                    resDict[d] = resDict.get(d, [])
                    resDict[d].append(deviation)
            id = trial["subject_id"]
            numRes = {}
        #how many responses for this descriptor
        d = trial["descriptor"]
        if trial["responses"] == '': num = 0
        else: num = len(trial["responses"].split(","))   
        numRes[d] = num
    #calc average
    for d in resDict.keys():
        resDict[d] = sum(resDict[d])/len(resDict[d])
    return resDict
numResPerDescriptorWithin = getNumResPerDescriptorWithin()
#correlation between generation and ave num responses for each descriptor
#print(getGenCorr(numResPerDescriptorWithin))

#returns average distance from subject average time it takes to give first n responses for each descriptor
#only includes subjects where at least n responses were given for each descriptor
def getFirstNResponseTimeWithin(n):
    resDict = {}
    id = ""
    for trial in data:
        if trial["subject_id"] != id:
            #finish up last one
            if trial != data[0] and not skipSubject:
                ave = sum(times.values())/len(times.values())
                #add deviation from average to list for each descriptor
                for d in times.keys():
                    deviation = times[d] - ave
                    resDict[d] = resDict.get(d, [])
                    resDict[d].append(deviation)
            skipSubject = False
            id = trial["subject_id"]
            times = {}
        if skipSubject: continue
        #how many responses for this descriptor
        d = trial["descriptor"]
        if trial["responses"] == '' or len(trial["responses"].split(",")) < n:
            skipSubject = True
            continue
        times[d] = sum(list(map(float, trial["rt"].split(",")))[:n])
    #calc average
    for d in resDict.keys():
        resDict[d] = sum(resDict[d])/len(resDict[d])
    return resDict
getFirstNResponseTimeWithin = getFirstNResponseTimeWithin(1)
#print(getFirstNResponseTimeWithin)
#correlation between generation and ave num responses for each descriptor
#print(getGenCorr(getFirstNResponseTimeWithin))
a1 = []
a2 = []
a3 = []
des = []
#for d in descriptors:
#    a1.append(genCorr[d])
#    a2.append(numResPerDescriptor[d])
#    a3.append(firstNResponseTime[d])
#    des.append(d)
#print(a1)
#print(a2)
#print(a3)
#print(des)

