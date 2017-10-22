import pandas as pd

tr_data = pd.read_csv('path_to_data.csv')

tr_data.rename(columns={'Unnamed: 0':'id','class':'target'},inplace=True)
train_features = [f for f in tr_data.columns if ('Time' not in f)and('target' not in f)]
temp = tr_data.loc[:,train_features]
temp.fillna(-999,inplace=True)
long_tr_data = temp.melt(id_vars='id',value_vars=train_features[1:])
del temp
