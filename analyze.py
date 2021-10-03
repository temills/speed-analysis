#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import random
import pandas as pd

with open('/Users/traceymills/consideration/speed-analysis/data.csv.json') as f:
 data = json.load(f)
descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan", "cute", "normal", "land", "think", "awake", "type, mammal", "tropics", "diet, carnivore"]
descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
descriptors = descriptors1 + descriptors2
genCorr = {'type, mammal': 0.18894731849701007, 'diet, carnivore': 0.2038779167838987, 'large': 0.3458998251843229, 'cute': 0.05406309013621359, 'cool': 0.2777483689929533, 'normal': -0.18053805054990885, 'striking': 0.3521983036172046, 'dangerous': 0.3271850392200191, 'tropics': 0.04016115026339956, 'land': 0.12875489519410027, 'lifespan': 0.317285976201681, 'think': 0.10311812598072409, 'awake': 0.06481348622086591,'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}


# with open('/Users/traceymills/consideration/speed-analysis/vegetables.json') as f:
#  data = json.load(f)
# descriptors = ["dishes", "popular", "available", "crunchy", "think", "warm", "heavy", "calories", "fragrant", "sweet"]
# genCorr = {'think': 0.47655677204291835, 'dishes': 0.5705715245609457, 'popular': 0.5414066993921484, 'available': 0.7111093760951049, 'fragrant': -0.11504084613286147, 'warm': -0.05142553559714049, 'sweet': 0.16918140757029312, 'crunchy': 0.4246094506168629, 'heavy': 0.03928128161072006, 'calories': -0.09369407427843358}

# with open('/Users/traceymills/consideration/speed-analysis/restaurants.json') as f:#
#  data = json.load(f)
# descriptors = ["interesting side dishes", "soft food", "cold food", "desserts", "healthy", "popular", "many locations", "casual", "quick", "brightly colored logo"]
# genCorr = {'interesting side dishes': 0.05797794277449986, 'soft food': 0.11357816033282128, 'cold food': -0.0679028961223725, 'desserts': 0.052718285665607136, 'popular': 0.4220453392935601, 'many locations': 0.5335387989116023, 'is unique': -0.2925555800029079, 'healthy': -0.012857634523901745, 'brightly colored logo': 0.2826773815547698, 'lively': 0.12550827795437736, 'variety': 0.17920547046707774, 'well decorated': 0.11966768704986638, 'expensive': -0.29991989021440446, 'quick': 0.24504742209076236, 'casual': 0.23089662426660587}

# with open('/Users/traceymills/consideration/speed-analysis/sports.json') as f:#
#  data = json.load(f)
# descriptors = ['think', 'popular', 'spectators', 'competitive', 'strenuous', 'dangerous', 'expensive', 'been around', 'flexibility', 'learn']
# genCorr = {'think': 0.5411744845692085, 'likes': 0.2710478139502008, 'popular': 0.5814709969892956, 'high energy': 0.23551330747669924, 'dangerous': 0.0889992003601851, 'strenuous': 0.30486850156710427, 'spectators': 0.6487580074053295, 'competitive': 0.45308748027122253, 'agility': 0.23949694172010771, 'expensive': -0.024276796370763777, 'space': 0.2200882507709032, 'been around': 0.17906979519434446, 'learn': 0.2568288124641362, 'flexibility': 0.012709898648517461}

# with open('/Users/traceymills/consideration/speed-analysis/holidays.json') as f:#
#   data = json.load(f)
# descriptors = ['reflective', 'early', 'partying', 'political', 'meaningful', 'time off', 'think', 'likes', 'romantic', 'widely celebrated']
# genCorr = {'religious': 0.13342600520188547, 'political': -0.17428491077383237, 'around': 0.25735584877955553, 'family oriented': 0.28097925711053734, 'partying': 0.09511255394503539, 'time off': 0.5359626511977721, 'romantic': 0.4159679097116104, 'traditions': 0.2509433980927829, 'likes': 0.5506060109052386, 'think': 0.5845506051005428, 'widely celebrated': 0.4987269939170238, 'reflective': -0.016752173733000794, 'joyous': 0.2623663725405865, 'meaningful': 0.18083577002258705, 'early': -0.03950684312667569}

# with open('/Users/traceymills/consideration/speed-analysis/kitchen.json') as f:#
#  data = json.load(f)
# descriptors = ['common', 'essential', 'plain sight', 'often', 'think', 'dangerous', 'loud', 'metallic', 'expensive', 'easy', 'heavy']
# genCorr = {'expensive': 0.17403243707330637, 'large': 0.3156406209802045, 'requires electricity': 0.278298673234939, 'gets hot': 0.30456517983814224, 'specialized': -0.2945935281445191, 'common': 0.5323111426150905, 'dangerous': 0.10255125976511446, 'essential': 0.45066043215834845, 'loud': -0.14225560857539987, 'heavy': 0.23928122712203087, 'plain sight': 0.5310725900811576, 'often': 0.48771763519993, 'easy': 0.2665930694697609, 'likes': 0.44938429739354896, 'think': 0.5094253391194362, 'metallic': 0.013828408304296968}

with open('/Users/traceymills/consideration/speed-analysis/jobs.json') as f:#
    data = json.load(f)
descriptors = ['people oriented', 'common', 'think', 'important', 'creativity', 'dangerous', 'physical', 'been around', 'glamorous', 'male dominated', 'difficult']
genCorr = {'people oriented': 0.17076524068052476, 'pays well': 0.1387987737619098, 'desirable': 0.10129620798819618, 'common': 0.2546180555663148, 'think': 0.07498222261861116, 'likes': 0.1521180329930711, 'important': 0.2368511770294124, 'creativity': -0.005579682718462679, 'skills': 0.16581927741987965, 'physical': 0.0038028483717259943, 'dangerous': 0.0190282279225156, 'detail oriented': 0.16115413823914826, 'been around': 0.2588587970296977, 'glamorous': 0.00049943902030669, 'male dominated': 0.009671553455618126, 'difficult': 0.1549744021970941}

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
#for d in descriptors:
#    print(d + ":")
#    print(str(comb[d]) + ", " + str(sum(firsts.get(d,[]))/max(1, len(firsts.get(d,[])))) + ", " + str(firsts.get(d,[])))
print("correlation for this category:")
print(getGenCorr(comb))


def getCorr(d1,d2):
    x, y = [], []
    for d in descriptors:
        x.append(d1[d])
        y.append(d2[d])
    return np.corrcoef(x, y)[0][1]
#print(getCorr(firstNResponseTime,numResPerDescriptor))

"""
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
print(ds)
#print(times)
#print(num)

#descriptors = ["large", "cool", "striking", "dangerous", "lifespan", "has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little", "dishes", "popular", "available", "crunchy", "think", "warm", "heavy", "calories", "fragrant", "sweet", "interesting side dishes", "soft food", "cold food", "desserts", "healthy", "popular", "many locations", "casual", "quick", "brightly colored logo"]
genCorrs = [0.3458998251843229, 0.2777483689929533, 0.3521983036172046, 0.3271850392200191, 0.317285976201681, 0.07622946411113914, -0.20459332100398267, 0.07487908633416952, 0.10441947183906619, -0.04724035442610212, 0.5705715245609457, 0.5414066993921484, 0.7111093760951049, 0.4246094506168629, 0.47655677204291835, -0.05142553559714049, 0.03928128161072006, -0.09369407427843358, -0.11504084613286147, 0.16918140757029312, 0.05797794277449986, 0.11357816033282128, -0.0679028961223725, 0.052718285665607136, -0.012857634523901745, 0.4220453392935601, 0.5335387989116023, 0.23089662426660587, 0.24504742209076236, 0.2826773815547698, 0.5411744845692085, 0.5814709969892956, 0.6487580074053295, 0.45308748027122253, 0.30486850156710427, 0.0889992003601851, -0.024276796370763777, 0.17906979519434446, 0.012709898648517461, 0.2568288124641362, -0.016752173733000794, -0.03950684312667569, 0.09511255394503539, -0.17428491077383237, 0.18083577002258705, 0.5359626511977721, 0.5845506051005428, 0.5506060109052386, 0.4159679097116104, 0.4987269939170238, 0.5323111426150905, 0.45066043215834845, 0.5310725900811576, 0.48771763519993, 0.5094253391194362, 0.10255125976511446, -0.14225560857539987, 0.013828408304296968, 0.17403243707330637, 0.2665930694697609, 0.23928122712203087, 0.17076524068052476, 0.2546180555663148, 0.07498222261861116, 0.2368511770294124, -0.005579682718462679, 0.0190282279225156, 0.0038028483717259943, 0.2588587970296977, 0.00049943902030669, 0.009671553455618126, 0.154974402197094]
combinedScores = [1.9867284996822925, 2.0729161108743117, 1.9092906289027687, 2.9366090364809323, 1.213744129581771, 0.7194530691208522, 1.0581686705305398, 1.35268608171713, 0.6537736038755312, 0.5741224719656765, 1.6838110999322993, 2.2625079823661824, 1.8826960638739754, 1.1035458215019527, 1.7685460700009088, 0.8437819942275065, 0.7493571504025612, 0.535350553229499, 0.7025648511651744, 0.5839945901151662, 1.2226002605889164, 0.7134663532212875, 1.244913019848883, 0.7841424838909161, 0.8561252768548857, 1.6949834391066232, 2.306599381186884, 2.342543193968948, 1.924250778138444, 0.9922838646385286, 1.3422595319016208, 2.4740060823847245, 2.3106646812348566, 2.715881148693045, 1.886396087543236, 1.1455198115314706, 1.2712206236136547, 1.968625039902069, 1.2778090594208569, 1.2186310236281495, 1.0148157841852952, 0.6815335632538537, 0.8813111155593616, 0.5143986164416299, 1.2079916046585866, 1.334540064277405, 1.142627128919521, 1.1502194194748625, 0.6816802157601393, 1.2200114841288323, 2.1336138143507486, 1.5806180081304801, 1.5245264425652085, 1.7177768916119387, 1.3948471200836197, 1.1420218319492679, 0.8029263040483713, 1.1528151633015107, 2.15341392351095, 2.037698047498753, 0.7579103860316669, 1.3300959695953154, 1.5609363641132934, 1.3565194766663784, 1.9680084508058024, 1.5614469228261232, 1.4199985313454895, 1.0828618897787057, 1.6142907296259088, 1.7567347362868382, 1.3406539098362444, 2.2274018190949914]
print("combined correlation:")
print(np.corrcoef(genCorrs, combinedScores)[0][1])
"""



"""
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
print(getFirstNResponseTimeWithin)
correlation between generation and ave num responses for each descriptor
print(getGenCorr(getFirstNResponseTimeWithin))
a1 = []
a2 = []
a3 = []
des = []
for d in descriptors:
    a1.append(genCorr[d])
    a2.append(numResPerDescriptor[d])
    a3.append(firstNResponseTime[d])
    des.append(d)
print(a1)
print(a2)
print(a3)
print(des)
"""
