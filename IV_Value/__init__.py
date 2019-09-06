import pandas as pd
import numpy as np
import math
pd.set_option('display.max_columns', None)

def getIVValue(df,coloumnName,targetVariable):
    # print("Hello")
    try:
        if df[coloumnName].dtype != "object":
            df["{}_rank".format(coloumnName)] = pd.cut(df[coloumnName],10,labels=[0,1,2,3,4,5,6,7,8,9])
            # print(df["{}_rank".format(coloumnName)].value_counts())
            total_event = len(df[df[targetVariable] == 1])
            total_non_event = len(df[df[targetVariable] == 0])
            # print("Events Non Events",total_event,total_non_event)
            iv_cum = 0

            for i in range(10):
                event_in_decile = len(df[df[targetVariable] == 1][df["{}_rank".format(coloumnName)] == i])
                non_event_in_decile = len(df[df[targetVariable] == 0][df["{}_rank".format(coloumnName)] == i])

                percent_event = event_in_decile/total_event
                percent_non_event = non_event_in_decile/total_non_event
                # print(percent_event,percent_non_event,coloumnName)
                if percent_non_event != 0 and percent_event != 0:
                    iv = (percent_event - percent_non_event) * math.log(percent_event / percent_non_event)
                    iv_cum = iv_cum + iv
            return iv_cum,""
        return 0,"Variable is in qualitative. Hence Convert it into quantitative"
    except Exception as e:
        # print("Exception in coloumn Name",coloumnName, "Exception IS",e)
        return 0,e



def getIVValueOfAllVariables(df,targetVariable):


    allColoumns = df.columns
    list1 = []
    for each in allColoumns:
        if each != targetVariable:
            iv = getIVValue(df,each,targetVariable)
            # print("IV FOR ",each)
            dict1 = {"iv_value":iv[0], "Reason": iv[1], "column_name": each}
            list1.append(dict1)
    print(list1)
    return list1
