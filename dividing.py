import pandas as pd


df = pd.read_csv('gramdoctor_triage_balanced.csv')
print("Total patients:", len(df))
df['triage-no']=df['triage'].map({
    'green':0,
    'orange':1,
    'red':2
})
df.drop(['triage','jaw swelling'],inplace=True,axis=1)
# print(df)
split_idx=int(0.8*len(df))
train=df.iloc[:split_idx]
test=df.iloc[split_idx:]
train.to_csv('Training_dataset.csv',index=False)
test.to_csv('Testing_dataset.csv',index=False)
print(len(train),len(test))

