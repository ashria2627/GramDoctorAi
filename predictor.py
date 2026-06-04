import pickle
import pandas as pd
from modules.triage_rules import check_red_flags

model = pickle.load(open('used_model.pkl', 'rb'))
feature_cols = pickle.load(open('feature_cols.pkl', 'rb'))

symptoms = {}
symptoms['age'] = int(input("Age: "))
symptoms['sex-no'] = int(input("Sex (0=male, 1=female): "))
symptoms['ispregnant'] = int(input("Pregnant? (0=no, 1=yes, 2=not applicable): "))
symptoms['fever'] = int(input("Fever? (1=yes, 0=no): "))
symptoms['sharp chest pain'] = int(input("Chest pain? (1=yes, 0=no): "))
symptoms['weakness'] = int(input("Weakness? (1=yes, 0=no): "))
symptoms['headache'] = int(input("Headache? (1=yes, 0=no): "))
symptoms['sweating'] = int(input("Sweating? (1=yes, 0=no): "))
symptoms['shortness of breath'] = int(input("Shortness of breath? (1=yes, 0=no): "))
symptoms['vomiting'] = int(input("Vomiting? (1=yes, 0=no): "))

# Rules run first
result = check_red_flags(symptoms)

if result == 'red':
    print("RESULT: RED - Go to emergency immediately!")
else:
    input_row = {col: symptoms.get(col, 0) for col in feature_cols}
    input_df = pd.DataFrame([input_row])
    prediction = model.predict(input_df)[0]
    labels = {0: 'GREEN - Rest at home', 1: 'ORANGE - Visit hospital within 48 hours', 2: 'RED - Go to emergency now'}
    print(f"RESULT: {labels[prediction]}")