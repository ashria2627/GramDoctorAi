import pandas as pd

df = pd.read_csv('gramdoctor_dataset_v2.csv')
print("Total patients:", len(df))
df['triage-no']=df['triage'].map({
    'green':0,
    'orange':1,
    'red':2
})
df['sex-no']=df['sex'].map({
    'female':1,
    'male':0
})
df['ispregnant']=df['pregnancy_status'].map({
    'no':0,
    'yes':1,
    'not_applicable':2
    
})
# df.drop(['sex','pregnancy_status','triage'],inplace=True,axis=1)
# print(df)
split_idx=int(0.8*len(df))
train=df.iloc[:split_idx]
test=df.iloc[split_idx:]
train.to_csv('Training_dataset.csv',index=False)
test.to_csv('Testing_dataset.csv',index=False)
print(len(train),len(test))

