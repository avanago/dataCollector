#######################################
#######################################
#######################################
# ARCHIVER

import os
import datetime

source = 'coinmarketcap'

Ipath = '/collectdata/'
Iname = '20171129_liveMarketCap.json'

IfileComplete = Ipath + Iname



ObaseFolder = 'outFolder'

    
# creation of output folder tree structure    
Tstamp = datetime.datetime.strptime(Iname,'%Y%m%d_liveMarketCap.json')


Opath = '{}/{}/{:04d}/{:02d}/{:02d}'.format(ObaseFolder,source,Tstamp.year,Tstamp.month,Tstamp.day)

if not os.path.exists(Opath):
    os.makedirs(Opath)


# File reading

with open(IfileComplete, "r") as ins:
    data29 = []
    for line in ins:
        data29.append(json.loads(line))

# List Creator
big_list = []

for e in data29:
    
    if type(e)==list:
        for elist in e:
            big_list.append(elist)
    elif type(e)==dict:
        big_list.append(e)
    else:
        print 'error!!!'

# List Cleaner
output = []
for x in big_list:
    if x not in output:
        output.append(x)    

# DF creation

outVal = dict()

for e in output:
    
    eid = e['id']
    t = datetime.datetime.fromtimestamp(int(e['last_updated']))
    
#    e.pop('id')
#    e.pop('last_updated')
    df = pd.DataFrame(e,index=[t])
    
    if eid in outVal:
        #if t in outVal[eid].index:
        #    outVal[eid].loc[t] = df
        #else:
        outVal[eid] = outVal[eid].append(df)
    else:
        outVal[eid] = df

# Save DF in single file

for name in outVal:
    complete_out = Opath+'/'+name+'.json'
    df_element =outVal[name]
    df_element = df_element.groupby(a.index).first()
    df_element.to_json(complete_out)

        
