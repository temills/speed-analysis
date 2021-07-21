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
with open('/Users/traceymills/consideration/speed-analysis/data.csv.json') as f:
  data = json.load(f)
data = sorted(data, key=lambda k: k['subject_id'])
#correlation of descriptor with coming to mind, as calculated from rating data
#genCorr = {'large': 0.3443250488940599, 'cool': 0.2786921485840363, 'striking': 0.35164786386252667, 'dangerous': 0.3241003513545623, 'lifespan': 0.31874309221991487, 'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}
genCorr = {'type, mammal': 0.18894731849701007, 'diet, carnivore': 0.2038779167838987, 'large': 0.3458998251843229, 'cute': 0.05406309013621359, 'cool': 0.2777483689929533, 'normal': -0.18053805054990885, 'striking': 0.3521983036172046, 'dangerous': 0.3271850392200191, 'tropics': 0.04016115026339956, 'land': 0.12875489519410027, 'lifespan': 0.317285976201681, 'think': 0.10311812598072409, 'awake': 0.06481348622086591,'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}
#descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan", "cute", "normal", "land", "think", "awake", "type, mammal", "tropics", "diet, carnivore"]
descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
descriptors = descriptors1 + descriptors2

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
numResPerDescriptor = getNumResPerDescriptor()
for i in numResPerDescriptor.keys():
    print(i + ": " + str(numResPerDescriptor[i])+", " + str(genCorr[i]))
#correlation between generation and ave num responses for each descriptor


#returns time it took to give first n responses for each descriptor
#only includes trials where at least n responses were given?
def getFirstNResponseTime(n):
    resDict = {}
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

def getCorr(d1,d2):
    x, y = [], []
    for d in descriptors:
        x.append(d1[d])
        y.append(d2[d])
    return np.corrcoef(x, y)[0][1]
print(getCorr(firstNResponseTime,numResPerDescriptor))
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
for d in descriptors:
    a1.append(genCorr[d])
    a2.append(numResPerDescriptor[d])
    a3.append(firstNResponseTime[d])
    des.append(d)
#print(a1)
#print(a2)
#print(a3)
#print(des)

