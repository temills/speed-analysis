// This file holds functions for parsing the data 

    //reformat data before saving
    function reformatData(data) {
        var numQs = 10;
        var startIndex = 5;
        //list of dictionaries, where each dictionary keeps the data for a single trial
        //Those dictionaries will become  rows in the data table
        var allData = [];
        //for (var i=startIndex; i<startIndex+(numTrials*2); i=i+2) {
        var trialIndex = startIndex;
        for (var i=0; i<numQs; i=i+1) {
            var qData = {};
            qData.q_order = i+1;
            qData.turk_code = JSON.parse(JSON.stringify(data[0]))["turk_code"];
            qData.subject_id = JSON.parse(JSON.parse(JSON.stringify(data[2]))["responses"])["subject_id"];
            qData.rt = []; //response times of each response in order
            qData.responses = []; //list of responses given (in order given)
            qData.descriptor = null;
            var trial = JSON.parse(JSON.stringify(data[trialIndex]));
            while(trial["trial_type"] == "survey-text") {
                if(!("responses" in trial)) {
                    trialIndex = trialIndex + 1;
                    trial = JSON.parse(JSON.stringify(data[trialIndex]));
                    continue; //nothing to add from this trial
                }
                var responses = JSON.parse(trial["responses"]);
                if(qData.descriptor == null) {
                    qData.descriptor = Object.keys(responses)[0];
                }
                var r = Object.values(responses)[0];
                r = r.replace(/'/gi, "");
                r = r.replace(/"/gi, "");
                r = r.replace(/;/gi, "");
                r = r.replace(/\//gi, "");
                r = r.replace(/\\/gi, "");
                qData.responses.push(r)
                qData.rt.push(trial["rt"]);
                trialIndex = trialIndex + 1;
                trial = JSON.parse(JSON.stringify(data[trialIndex]));
            }
            trialIndex = trialIndex + 2; //skip round debrief and timer start
            allData.push(qData);
        }
        trialIndex = trialIndex - 1; //don't need to skip next timer for last trial
        
        //add demo info to each trial (bruh)
        var demo1 = JSON.parse(JSON.parse(JSON.stringify(data[trialIndex]))["responses"]);
        trialIndex = trialIndex + 1;
        var demo2 = JSON.parse(JSON.parse(JSON.stringify(data[trialIndex]))["responses"]);
        for (var i=0; i<allData.length; i=i+1) {
            var qDict = allData[i];
            qDict.age = Object.values(demo1)[0];
            qDict.language = Object.values(demo1)[1];
            qDict.nationality = Object.values(demo1)[2];
            qDict.country = Object.values(demo1)[3];
            qDict.gender = Object.values(demo2)[0];
            qDict.student = Object.values(demo2)[1];
            qDict.education = Object.values(demo2)[2];
            allData[i] = qDict;
        }
        return allData;
    }
    
    export function makeQuery(data) {
        data = JSON.parse(JSON.stringify(data));
        console.log("Parsing data");
        data = reformatData(data);
        console.log("done");
        var table = 'zoo_animals';
        var keys = "";
        var keyArr = Object.keys(data[0]);
        for(var i=0; i<keyArr.length; i++) {
            keys = keys.concat(keyArr[i] + ", ");
        }
        keys = "(" + keys.substring(0, keys.length-2) + ")";
        var valuesList = [];
        var x = 0;
        for(var i=0; i<data.length; i++) {
            var dict = data[i];
            valuesList[x] = "";
            var valArray = Object.values(dict);
            for(var j=0; j<valArray.length; j++) {
                valuesList[x] = valuesList[x].concat("'" + valArray[j] + "', ");
            }
            x++;
        }
        var valuesStr = "";
        for (var i=0; i<valuesList.length; i++) {
            var values = valuesList[i];
            values = "(" + values.substring(0, values.length-2) + ")";
            valuesStr = valuesStr + values + ", ";
        }
        valuesStr = valuesStr.substring(0, valuesStr.length-2);
        //console.log("INSERT INTO " + table + keys + " " + "VALUES " + valuesStr + ";");
        return "INSERT INTO " + table + keys + " " + "VALUES " + valuesStr + ";";
    }