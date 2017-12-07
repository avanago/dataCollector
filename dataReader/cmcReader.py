###################################
###################################
###################################
# Data Reader
import pandas as pd
currency = 'bitcoin'
source = 'coinmarketcap'


basePath= '/collectData'


start_time = datetime.datetime(2017,11,29,15,0,0)
end_time = datetime.datetime(2017,11,29,18,30,0)

n_iter = (end_time-start_time).days + 1


# Load input data
df1 = pd.DataFrame()

for i in range(n_iter)
    candidate_time = start_time + datetime.timedelta(days=i)
    extPath= '{:s}/{:s}/{:04d}/{:02d}/{:02d}/{:s}.json'.format(basePath,
                                                             source,
                                                             candidate_time.year,
                                                             candidate_time.month,
                                                             candidate_time.day,
                                                             currency)
    df_new = pd.DataFrame.read_json(extPath)
    df1 = df1.append(df_new)
    
# Extract data
df_extract = df1.iloc[(df1.index>start_time) & (df1.index<end_time)]

df_extract
