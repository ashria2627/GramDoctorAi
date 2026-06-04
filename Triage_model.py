from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pickle
import pandas as pd
import plotly.express as px

model=RandomForestClassifier(class_weight='balanced',random_state=42)
train=pd.DataFrame(pd.read_csv("Training_dataset.csv"))
test=pd.DataFrame(pd.read_csv("Testing_dataset.csv"))
drop_cols=['sex','pregnancy_status','triage','home_advice','triage-no']
X_train=train.drop(columns=drop_cols)
y_train=train['triage-no']
x_test=test.drop(columns=drop_cols)
y_test=test['triage-no']
model.fit(X_train,y_train)

y_pred = model.predict(x_test)
# print(classification_report(y_test, y_pred, target_names=['green', 'orange', 'red']))

with open('used_model.pkl', 'wb') as f:
    pickle.dump(model, f)
feature_cols = list(X_train.columns)
pickle.dump(feature_cols, open('feature_cols.pkl', 'wb'))
# print("Model saved!")
# print(confusion_matrix(y_test,y_pred,labels=[0,1,2]))

important=model.feature_importances_
cols=X_train.columns
important_df=pd.DataFrame({
    'symptoms':cols,
    'importance':important
})
important_df.sort_values("importance",ascending=False,inplace=True)
common_symptoms=important_df.head(20)
# print(common_symptoms)
fig=px.pie(common_symptoms, values='importance', names='symptoms', title='Most Common Symptoms',color_discrete_sequence=px.colors.sequential.RdBu)

fig.show()