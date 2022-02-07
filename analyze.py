#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt



#get correlation between desriptor generation score and whatever dict is passed in
def getGenCorr(descriptorData):
    descriptors = descriptorData.keys()
    x, y = [], []
    for d in descriptors:
        if d=='null':
            continue
        x.append(descriptorData[d])
        y.append(genCorr[d])
    return np.corrcoef(x, y)[0][1]

##### all subjects ######

#measures ease of response to each descriptor
#first/time+second/time...
def getCombinedResponseMetric(data):
    times = {}
    scores = {}
    firsts = {}
    for trial in data:
        score = 0
        d = trial["descriptor"]
        if(d=="awake"):
            d = "awake, day"
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
    for d in scores.keys():
        combined[d] = scores[d][0]/scores[d][1]
    return combined


#comb, firsts = getCombinedResponseMetric()
#with open('descriptor-speed-data/'+cat+'s.json', 'w') as f:
#  json.dump(comb, f)

#corrs = getGenCorr(comb)
#correlation between descriptor's correlation with coming to mind, and ease of response to descriptor
#with open('descriptor-speed-correlations/'+cat+'s.json', 'w') as f:
#  json.dump(corrs, f)


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
#firstNResponseTime = getFirstNResponseTime(2)
#correlation between generation and rave esponse time for first n responses for each descriptor
#print(getGenCorr(firstNResponseTime))
 
#correlation bt dicts 1 and 2 where descriptors are keys
def getCorr(d1,d2):
    x, y = [], []
    for d in descriptors:
        x.append(d1[d])
        y.append(d2[d])
    return np.corrcoef(x, y)[0][1]
#print(getCorr(firstNResponseTime,numResPerDescriptor))

def getResPerDescriptor(data):
    resDict = {}
    for trial in data:
        d = trial["descriptor"]
        #for each descriptor, list with num total responses, num times descriptor given
        resDict[d] = resDict.get(d, {})
        for res in trial["responses"].split(","):
            res = res.lower()
            if res=='bear':
                res='grizzly bear'
            resDict[d][res] = resDict[d].get(res, 0) + 1
    return resDict


#category
cat = 'animal'
#subject responses
with open('response_data/'+cat+'s.json') as f:
    data = json.load(f)
data = sorted(data, key=lambda k: k['subject_id'])

#correlations between descriptors and items coming to mind
with open('../item-ratings/descriptor-generation-correlations/'+cat+'s.json') as f:
    genCorr = json.load(f)

#comb, firsts = getCombinedResponseMetric(data)
#correlation between descriptor's correlation with coming to mind, and ease of response to descriptor
#corrs = getGenCorr(comb)
#print(corrs)

responses = getResPerDescriptor(data)
#print(sorted(responses['striking'].items(), key=lambda x: x[1], reverse=True))

with open('../item-generations/generation_data_clean/animal_counts.json') as f:
    genCounts = json.load(f)

for an, count in genCounts.items():
    if count < 3.5:
        genCounts[an] = 0

#print(sorted(genCounts.items(), key=lambda x: x[1], reverse=True))
#print(responses.keys())
#generations
g = sorted(genCounts.items(), key=lambda x: x[1], reverse=True)[:20]
g_labels = [pair[1] for pair in g]
g_data = [pair[0] for pair in g]
fig = plt.figure(figsize = (10, 5))
plt.bar(g_data, g_labels, rotation='vertical')

#timed responses
#t = sorted(responses['striking'].items(), key=lambda x: x[1], reverse=True)[:20]
#plt.bar()
#plt.show()
#for (k , l) in responses.items():
#    print(k + ': ' + str(len(l)))
t = sorted(responses['striking'].items(), key=lambda x: x[1], reverse=True)[:20]
t_labels = [pair[1] for pair in t]
t_data = [pair[0] for pair in t]
fig = plt.figure(figsize = (10, 5))
plt.bar(t_data,t_labels)
plt.show()
#striking has high correlation with coming to mind









# Some old code just in case

#with open('/Users/traceymills/consideration/speed-analysis/data.csv.json') as f:
# data = json.load(f)
##descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan", "cute", "normal", "land", "think", "awake", "type, mammal", "tropics", "diet, carnivore"]
#descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
#descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
#descriptors = descriptors1 + descriptors2
#genCorr = {'type, mammal': 0.18894731849701007, 'diet, carnivore': 0.2038779167838987, 'large': 0.3458998251843229, 'cute': 0.05406309013621359, 'cool': 0.2777483689929533, 'normal': -0.18053805054990885, 'striking': 0.3521983036172046, 'dangerous': 0.3271850392200191, 'tropics': 0.04016115026339956, 'land': 0.12875489519410027, 'lifespan': 0.317285976201681, 'think': 0.10311812598072409, 'awake': 0.06481348622086591,'has large feet relative to its body size': 0.07622946411113914, 'quiet': -0.20459332100398267, 'has good hearing': 0.07487908633416952, 'has long hair': 0.10441947183906619, 'sleeps very little': -0.04724035442610212}


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

#with open('/Users/traceymills/consideration/speed-analysis/jobs.json') as f:#
#   data = json.load(f)
#descriptors = ['people oriented', 'common', 'think', 'important', 'creativity', 'dangerous', 'physical', 'been around', 'glamorous', 'male dominated', 'difficult']
#genCorr = {'people oriented': 0.17076524068052476, 'pays well': 0.1387987737619098, 'desirable': 0.10129620798819618, 'common': 0.2546180555663148, 'think': 0.07498222261861116, 'likes': 0.1521180329930711, 'important': 0.2368511770294124, 'creativity': -0.005579682718462679, 'skills': 0.16581927741987965, 'physical': 0.0038028483717259943, 'dangerous': 0.0190282279225156, 'detail oriented': 0.16115413823914826, 'been around': 0.2588587970296977, 'glamorous': 0.00049943902030669, 'male dominated': 0.009671553455618126, 'difficult': 0.1549744021970941}
#


{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 34950.65500005148,
		"category" : "holidays",
		"trial_order" : 1,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "thanksgiving",
		"response2" : "halloween",
		"response3" : "christmas",
		"response4" : "hannukah",
		"response5" : "easter",
		"response6" : "kwanzaa",
		"response7" : "earth day",
		"response8" : "purim",
		"response9" : "passover",
		"response10" : "veterans day"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 39474.05999992043,
		"category" : "vegetables",
		"trial_order" : 2,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "broccoli",
		"response2" : "eggplant",
		"response3" : "tomato",
		"response4" : "carrot",
		"response5" : "kale",
		"response6" : "spinach",
		"response7" : "artichoke",
		"response8" : "zucchini",
		"response9" : "corn",
		"response10" : "radish"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 28586.965000024065,
		"category" : "jobs",
		"trial_order" : 3,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "engineer",
		"response2" : "lawyer",
		"response3" : "doctor",
		"response4" : "actor",
		"response5" : "director",
		"response6" : "dentist",
		"response7" : "artist",
		"response8" : "detective",
		"response9" : "police officer",
		"response10" : "soldier"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 35775.84500005469,
		"category" : "breakfast foods",
		"trial_order" : 4,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "eggos",
		"response2" : "eggs",
		"response3" : "cereal",
		"response4" : "pancakes",
		"response5" : "leftover pizza",
		"response6" : "toast",
		"response7" : "hash browns",
		"response8" : "sausage",
		"response9" : "home fries",
		"response10" : "omelette"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 50971.870000008494,
		"category" : "kitchen appliances",
		"trial_order" : 5,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "stove",
		"response2" : "microwave",
		"response3" : "sink",
		"response4" : "dishwasher",
		"response5" : "refrigerator",
		"response6" : "freezer",
		"response7" : "food processer",
		"response8" : "blender",
		"response9" : "espresso machine",
		"response10" : "coffee maker"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 24705.799999879673,
		"category" : "clothing items",
		"trial_order" : 6,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "hat",
		"response2" : "pants",
		"response3" : "shirt",
		"response4" : "sweater",
		"response5" : "scarf",
		"response6" : "mittens",
		"response7" : "gloves",
		"response8" : "jeans",
		"response9" : "jackets",
		"response10" : "socks"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 34565.78500010073,
		"category" : "zoo animals",
		"trial_order" : 7,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "zebra",
		"response2" : "lion",
		"response3" : "elephant",
		"response4" : "seal",
		"response5" : "red panda",
		"response6" : "meerkats",
		"response7" : "hippo",
		"response8" : "penguin",
		"response9" : "giraffe",
		"response10" : "rhino"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 58229.664999991655,
		"category" : "chain restaurants",
		"trial_order" : 8,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "pf changs",
		"response2" : "mcdonalds",
		"response3" : "dennys",
		"response4" : "applebees",
		"response5" : "subway",
		"response6" : "red lobster",
		"response7" : "out back steak house",
		"response8" : "five guys",
		"response9" : "wok to walk",
		"response10" : "tgi fridays"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 36432.1850000415,
		"category" : "sports",
		"trial_order" : 9,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "frisbee",
		"response2" : "soccer",
		"response3" : "football",
		"response4" : "baseball",
		"response5" : "hockey",
		"response6" : "curling",
		"response7" : "polo",
		"response8" : "water polo",
		"response9" : "volleyball",
		"response10" : "tennis"
	},
	{
		"subject_id" : "eli",
		"exp_type" : "generation",
		"rt" : 40893.38000002317,
		"category" : "types of furniture",
		"trial_order" : 10,
		"country" : "USA",
		"nationality" : "American",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "ft4ajayzo4hz",
		"response1" : "chair",
		"response2" : "bed",
		"response3" : "sofa",
		"response4" : "ottoman",
		"response5" : "desk",
		"response6" : "shelves",
		"response7" : "dresser",
		"response8" : "couch",
		"response9" : "table",
		"response10" : "lamp"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 76015.84499998717,
		"category" : "kitchen appliances",
		"trial_order" : 1,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "stove",
		"response2" : "fridge",
		"response3" : "toaster",
		"response4" : "oven",
		"response5" : "blender",
		"response6" : "hand mixer",
		"response7" : "food processer",
		"response8" : "microwave",
		"response9" : "pasta maker",
		"response10" : "stand mixer"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 52719.52500002226,
		"category" : "types of furniture",
		"trial_order" : 2,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "sofa",
		"response2" : "chair",
		"response3" : "stool",
		"response4" : "cabinet",
		"response5" : "bookshelf",
		"response6" : "amour",
		"response7" : "table",
		"response8" : "lamp",
		"response9" : "nightstand",
		"response10" : "ottaman "
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 41935.42999995407,
		"category" : "breakfast foods",
		"trial_order" : 3,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "eggs",
		"response2" : "toast",
		"response3" : "bacon",
		"response4" : "coffee",
		"response5" : "orange juice",
		"response6" : "milk",
		"response7" : "cereal",
		"response8" : "oatmeal",
		"response9" : "hashbrowns",
		"response10" : "smoothie"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 56399.77000001818,
		"category" : "chain restaurants",
		"trial_order" : 4,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "mcdonalds",
		"response2" : "chipotle",
		"response3" : "noodles",
		"response4" : "caribou",
		"response5" : "starbucks",
		"response6" : "olive garden",
		"response7" : "chillis",
		"response8" : "applebees",
		"response9" : "panera",
		"response10" : "dunkin"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 56987.460000033025,
		"category" : "zoo animals",
		"trial_order" : 5,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "zerbra",
		"response2" : "lion",
		"response3" : "tiger",
		"response4" : "polar bear",
		"response5" : "penguin",
		"response6" : "monkey ",
		"response7" : "dolphin",
		"response8" : "prairie dog",
		"response9" : "snake",
		"response10" : "lizard"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 53365.54999998771,
		"category" : "jobs",
		"trial_order" : 6,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "teacher",
		"response2" : "accountant",
		"response3" : "product managment",
		"response4" : "human resources",
		"response5" : "trader",
		"response6" : "uber driver",
		"response7" : "food service",
		"response8" : "retail",
		"response9" : "gate agent",
		"response10" : "self-employed"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 43294.1549999523,
		"category" : "vegetables",
		"trial_order" : 7,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "carrot",
		"response2" : "zuccini",
		"response3" : "celery",
		"response4" : "potatoes",
		"response5" : "peas",
		"response6" : "green beans",
		"response7" : "corn",
		"response8" : "eggplant",
		"response9" : "cucumber",
		"response10" : "broccoli"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 52760.85500000045,
		"category" : "holidays",
		"trial_order" : 8,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "thanksgiving",
		"response2" : "chirstmas",
		"response3" : "halloween",
		"response4" : "valentines day",
		"response5" : "fourth of july",
		"response6" : "indigenous peoples day",
		"response7" : "memorial day",
		"response8" : "MLK day",
		"response9" : "new years ever",
		"response10" : "birthdays"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 33718.24499999639,
		"category" : "sports",
		"trial_order" : 9,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "soccer",
		"response2" : "hockey",
		"response3" : "tennis",
		"response4" : "swim",
		"response5" : "diving",
		"response6" : "golf",
		"response7" : "badmitten",
		"response8" : "skating",
		"response9" : "climbing",
		"response10" : "lacrosse"
	},
	{
		"subject_id" : "test",
		"exp_type" : "generation",
		"rt" : 22298.97499998333,
		"category" : "clothing items",
		"trial_order" : 10,
		"country" : "USA",
		"nationality" : "american",
		"age" : 19,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "n9jprml6ogm7",
		"response1" : "shirt",
		"response2" : "pants",
		"response3" : "shorts",
		"response4" : "socks",
		"response5" : "shoes",
		"response6" : "slippers",
		"response7" : "bra",
		"response8" : "underwear",
		"response9" : "sweater",
		"response10" : "sweatshirt"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 38670.43499997817,
		"category" : "kitchen appliances",
		"trial_order" : 1,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "stove",
		"response2" : "microwave",
		"response3" : "sink",
		"response4" : "fridge",
		"response5" : "cuttingboard",
		"response6" : "soap",
		"response7" : "oven",
		"response8" : "standmixer ",
		"response9" : "food processor",
		"response10" : "coffee grinder"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 130415.42999999365,
		"category" : "jobs",
		"trial_order" : 2,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "teacher",
		"response2" : "officer",
		"response3" : "president",
		"response4" : "vice president",
		"response5" : "chief of staff",
		"response6" : "trashman",
		"response7" : "mailman",
		"response8" : "CEO",
		"response9" : "grad student",
		"response10" : "administrative assistant "
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 54205.415000003995,
		"category" : "vegetables",
		"trial_order" : 3,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "corn",
		"response2" : "potatoes",
		"response3" : "green been",
		"response4" : "kale",
		"response5" : "tomatoes",
		"response6" : "brusell sprouts",
		"response7" : "peppers",
		"response8" : "jalepenos",
		"response9" : "cabbage",
		"response10" : "onions"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 22775.419999990845,
		"category" : "clothing items",
		"trial_order" : 4,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "shirt",
		"response2" : "dress",
		"response3" : "scarf",
		"response4" : "boxers",
		"response5" : "thongs",
		"response6" : "bra",
		"response7" : "shorts",
		"response8" : "pants",
		"response9" : "slacks",
		"response10" : "blazer"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 41791.68500000378,
		"category" : "holidays",
		"trial_order" : 5,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "christmas",
		"response2" : "thanksgiving",
		"response3" : "fourth of july",
		"response4" : "birthday",
		"response5" : "columbus day",
		"response6" : "presidents day",
		"response7" : "leif erikson day",
		"response8" : "martin luther king day",
		"response9" : "new years",
		"response10" : "veterans days"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 33979.85500001232,
		"category" : "types of furniture",
		"trial_order" : 6,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "couch",
		"response2" : "bed",
		"response3" : "chair",
		"response4" : "recliner",
		"response5" : "desk",
		"response6" : "bookshelf",
		"response7" : "rug",
		"response8" : "piano",
		"response9" : "dresser",
		"response10" : "shelf"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 62682.42500000633,
		"category" : "chain restaurants",
		"trial_order" : 7,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "cracker barrel",
		"response2" : "sonic",
		"response3" : "arbys",
		"response4" : "mcdonalds",
		"response5" : "tgi fridays",
		"response6" : "wendys",
		"response7" : "dennys",
		"response8" : "chipotle",
		"response9" : "panda express",
		"response10" : "taco bell"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 40842.559999990044,
		"category" : "zoo animals",
		"trial_order" : 8,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "panda",
		"response2" : "giraffe",
		"response3" : "zebra",
		"response4" : "walybe",
		"response5" : "anaconda",
		"response6" : "giant tortoise",
		"response7" : "red panda",
		"response8" : "snow leopard",
		"response9" : "lion",
		"response10" : "mali uryomasix "
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 72438.16499999957,
		"category" : "sports",
		"trial_order" : 9,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "soccer",
		"response2" : "f1",
		"response3" : "figure skating",
		"response4" : "climbing",
		"response5" : "deep water soloing",
		"response6" : "snow boarding",
		"response7" : "free style skiing",
		"response8" : "half pipe",
		"response9" : "speed skating",
		"response10" : "cross-country skiing"
	},
	{
		"subject_id" : "kasjdksmakd",
		"exp_type" : "generation",
		"rt" : 31602.530000003753,
		"category" : "breakfast foods",
		"trial_order" : 10,
		"country" : "us",
		"nationality" : "us",
		"age" : 26,
		"student" : "Yes",
		"education" : "Graduate degree, Masters",
		"gender" : "Female",
		"language" : "english ",
		"turk_code" : "70p15la1f03j",
		"response1" : "oatmeal",
		"response2" : "bagel",
		"response3" : "eggs",
		"response4" : "hashbrown",
		"response5" : "cereal",
		"response6" : "toast",
		"response7" : "marmalade",
		"response8" : "apples",
		"response9" : "grapefruit",
		"response10" : "cinnamon roll"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 24474.634999991395,
		"category" : "clothing items",
		"trial_order" : 1,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "scarf",
		"response2" : "tie",
		"response3" : "belt",
		"response4" : "shoes",
		"response5" : "shirt",
		"response6" : "dress",
		"response7" : "skirt",
		"response8" : "pants",
		"response9" : "shorts",
		"response10" : "hat"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 34907.89999999106,
		"category" : "breakfast foods",
		"trial_order" : 2,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "eggs",
		"response2" : "bacon",
		"response3" : "toast",
		"response4" : "pancakes",
		"response5" : "waffles",
		"response6" : "yogurt",
		"response7" : "granola",
		"response8" : "oatmeal",
		"response9" : "cereal",
		"response10" : "banana"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 51389.12499998696,
		"category" : "chain restaurants",
		"trial_order" : 3,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "zaxbys",
		"response2" : "chik fil a",
		"response3" : "mcdonalds",
		"response4" : "wendys",
		"response5" : "burger king",
		"response6" : "whataburger",
		"response7" : "Kfc",
		"response8" : "taco bell",
		"response9" : "moes",
		"response10" : "chipotle"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 43538.39000000153,
		"category" : "zoo animals",
		"trial_order" : 4,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "giraffe",
		"response2" : "lion",
		"response3" : "rhino",
		"response4" : "alligator",
		"response5" : "gazelle",
		"response6" : "birds",
		"response7" : "snakes",
		"response8" : "hippo",
		"response9" : "flamingo",
		"response10" : "monkeys"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 58462.06500008702,
		"category" : "kitchen appliances",
		"trial_order" : 5,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "oven",
		"response2" : "toaster",
		"response3" : "microwave",
		"response4" : "fridge",
		"response5" : "freezer",
		"response6" : "stove",
		"response7" : "airfryer",
		"response8" : "coffee pot",
		"response9" : "sink",
		"response10" : "dishwasher"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 51485.13000004459,
		"category" : "holidays",
		"trial_order" : 6,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "christmas",
		"response2" : "new years ",
		"response3" : "thanksgiving",
		"response4" : "halloween",
		"response5" : "july 4th",
		"response6" : "st patricks day",
		"response7" : "valentines day",
		"response8" : "presidents day ",
		"response9" : "veterans day",
		"response10" : "easter"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 94258.49000003655,
		"category" : "jobs",
		"trial_order" : 7,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "construction",
		"response2" : "wall street ",
		"response3" : "valet driver",
		"response4" : "fisherman",
		"response5" : "lawyer",
		"response6" : "doctor",
		"response7" : "banker",
		"response8" : "realtor",
		"response9" : "policeman",
		"response10" : "frycook"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 33422.479999950156,
		"category" : "sports",
		"trial_order" : 8,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "baseball",
		"response2" : "football",
		"response3" : "soccer",
		"response4" : "basketball",
		"response5" : "lacrosse",
		"response6" : "swimming",
		"response7" : "hockey",
		"response8" : "golf",
		"response9" : "field hockey",
		"response10" : "track"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 49242.92499991134,
		"category" : "vegetables",
		"trial_order" : 9,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "brussel sprouts",
		"response2" : "okra",
		"response3" : "green beans",
		"response4" : "broccoli",
		"response5" : "onions",
		"response6" : "peppers",
		"response7" : "asparagus",
		"response8" : "mushrooms",
		"response9" : "snap peas",
		"response10" : "collard greens"
	},
	{
		"subject_id" : "Nathan Skinner",
		"exp_type" : "generation",
		"rt" : 76132.05000001471,
		"category" : "types of furniture",
		"trial_order" : 10,
		"country" : "USA",
		"nationality" : "White",
		"age" : 21,
		"student" : "Yes",
		"education" : "College or university degree",
		"gender" : "Male",
		"language" : "english",
		"turk_code" : "66fegu1kddsm",
		"response1" : "couch",
		"response2" : "chair",
		"response3" : "bed",
		"response4" : "bedside table",
		"response5" : "table",
		"response6" : "lamp",
		"response7" : "tv stand",
		"response8" : "barstool",
		"response9" : "hat rack",
		"response10" : "bookcase"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 81079.19499999844,
		"category" : "vegetables",
		"trial_order" : 1,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "carrots",
		"response2" : "broccoli",
		"response3" : "yams",
		"response4" : "potatos",
		"response5" : "asparagus",
		"response6" : "brussel sprouts",
		"response7" : "parsnips",
		"response8" : "radish",
		"response9" : "lettuce",
		"response10" : "spinach"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 49390.91999997618,
		"category" : "types of furniture",
		"trial_order" : 2,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "chair",
		"response2" : "table",
		"response3" : "lamp",
		"response4" : "countertop",
		"response5" : "couch",
		"response6" : "recliner",
		"response7" : "bed",
		"response8" : "cabinet",
		"response9" : "dresser",
		"response10" : "desk"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 56244.730000034906,
		"category" : "kitchen appliances",
		"trial_order" : 3,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "blender",
		"response2" : "oven",
		"response3" : "food processor",
		"response4" : "sink",
		"response5" : "microwave",
		"response6" : "toaster",
		"response7" : "toaster oven",
		"response8" : "pasta maker",
		"response9" : "stovetop",
		"response10" : "coffee maker"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 45142.25999999326,
		"category" : "jobs",
		"trial_order" : 4,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "brick layer",
		"response2" : "teacher",
		"response3" : "plumber",
		"response4" : "architect",
		"response5" : "governor",
		"response6" : "president",
		"response7" : "mailman",
		"response8" : "prison guard",
		"response9" : "artist",
		"response10" : "software engineer"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 38946.140000014566,
		"category" : "holidays",
		"trial_order" : 5,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "christmas",
		"response2" : "new years",
		"response3" : "easter",
		"response4" : "thanksgiving",
		"response5" : "fourth of july",
		"response6" : "valentines day",
		"response7" : "veterans day",
		"response8" : "memorial day",
		"response9" : "indigenous peoples day",
		"response10" : "mothers day"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 31390.429999970365,
		"category" : "zoo animals",
		"trial_order" : 6,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "zebra",
		"response2" : "giraffe",
		"response3" : "lion",
		"response4" : "cougar",
		"response5" : "rhino",
		"response6" : "hippo",
		"response7" : "elephant",
		"response8" : "tiger",
		"response9" : "gorilla",
		"response10" : "orangutan"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 25173.47500001779,
		"category" : "sports",
		"trial_order" : 7,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "soccer",
		"response2" : "football",
		"response3" : "baseball",
		"response4" : "lax",
		"response5" : "cricket",
		"response6" : "rowing",
		"response7" : "track",
		"response8" : "swimming",
		"response9" : "squash",
		"response10" : "basketball"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 23669.13500003284,
		"category" : "clothing items",
		"trial_order" : 8,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "shirt",
		"response2" : "pants",
		"response3" : "tie",
		"response4" : "belt",
		"response5" : "shoes",
		"response6" : "skirt",
		"response7" : "dress",
		"response8" : "bracelet",
		"response9" : "necklace",
		"response10" : "watch"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 33032.00000000652,
		"category" : "chain restaurants",
		"trial_order" : 9,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "wendys",
		"response2" : "applebees",
		"response3" : "chilis",
		"response4" : "mcdonalds",
		"response5" : "taco bell",
		"response6" : "panera",
		"response7" : "del taco",
		"response8" : "shake shack",
		"response9" : "five guys",
		"response10" : "burger king"
	},
	{
		"subject_id" : "xxx",
		"exp_type" : "generation",
		"rt" : 30385.25499997195,
		"category" : "breakfast foods",
		"trial_order" : 10,
		"country" : "usa",
		"nationality" : "american",
		"age" : 21,
		"student" : "Yes",
		"education" : "Some college or university",
		"gender" : "Female",
		"language" : "english",
		"turk_code" : "nlz36va8zt0t",
		"response1" : "pancakes",
		"response2" : "cereal",
		"response3" : "bacon",
		"response4" : "eggs",
		"response5" : "sausage",
		"response6" : "hash browns",
		"response7" : "bagel",
		"response8" : "lox",
		"response9" : "muffin",
		"response10" : "french toast"
	},
