from xgboost import XGBClassifier
import pandas as pd
from sklearn.metrics import classification_report
import pickle
from sklearn.metrics import confusion_matrix

train=pd.DataFrame(pd.read_csv("Training_dataset.csv"))
test=pd.DataFrame(pd.read_csv("Testing_dataset.csv"))
drop_cols=['sex','pregnancy_status','triage','home_advice','triage-no']
X_train=train.drop(columns=drop_cols)
y_train=train['triage-no']
x_test=test.drop(columns=drop_cols)
y_test=test['triage-no']
model = XGBClassifier(random_state=42)
model.fit(X_train,y_train)
y_pred=model.predict(x_test)
print(classification_report(y_test, y_pred, target_names=['green', 'orange', 'red']))
print(confusion_matrix(y_test,y_pred,labels=[0,1,2]))
with open('comparison_model.pkl', 'wb') as f:
    pickle.dump(model, f)