import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import pickle
from sklearn.metrics import confusion_matrix
import plotly.express as px
import numpy as np

df = pd.read_csv('anomaly_detection_data.csv')
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df = df.drop_duplicates()

df['sex'] = df['gender'].map({'F': 1, 'M': 0})

drop_cols = [
    "patient_id",
    'gender',
    'nurse_alert',
    'deterioration_next_12h'
]

y = df['deterioration_next_12h']
X = df.drop(columns=drop_cols)

split = int(0.8 * len(df))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = XGBClassifier(
    random_state=42,
    scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1])
)

model.fit(X_train, y_train)

proba = model.predict_proba(X_test)[:,1]

# ===== DIAGNOSTICS =====
print("Min:", proba.min(), "Max:", proba.max(), "Mean:", proba.mean())
print("90th percentile:", np.percentile(proba, 90))
print("95th percentile:", np.percentile(proba, 95))
print("99th percentile:", np.percentile(proba, 99))

# pick threshold based on percentile above
THRESHOLD = np.percentile(proba, 90)
y_pred = (proba >= THRESHOLD).astype(int)

print("Chosen threshold:", THRESHOLD)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred, labels=[0,1]))

with open('anomaly_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('anomaly_threshold.pkl', 'wb') as f:
    pickle.dump(THRESHOLD, f)

feature_cols = list(X_train.columns)
with open('deterioration_feature_cols.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)

cm = confusion_matrix(y_test, y_pred, labels=[0,1])
fig = px.imshow(cm, text_auto=True,
                 x=['No Deterioration','Deterioration'],
                 y=['No Deterioration','Deterioration'],
                 color_continuous_scale='RdYlGn',
                 labels=dict(x="Predicted", y="Actual"),
                 title='Deterioration Prediction — Confusion Matrix')
fig.write_image("assets/deterioration_confusion_matrix.png")

importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False).head(12)

fig = px.bar(importance_df, x='importance', y='feature', orientation='h',
              title='Top Predictors of Patient Deterioration')
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.write_image("assets/deterioration_feature_importance.png")