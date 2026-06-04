def check_red_flags(symptoms):
    from collections import defaultdict
    symptoms = defaultdict(int, symptoms)
    if symptoms['sharp chest pain'] == 1 and symptoms['sweating'] == 1 and symptoms['shortness of breath'] == 1:
        return 'red'
    if (symptoms['slurring words']==1 or symptoms['blindness']==1 or symptoms['diminished vision']==1) and symptoms['headache']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['ispregnant']==1 and( symptoms['spotting or bleeding during pregnancy']==1 or symptoms['headache']==1 or symptoms['abnormal involuntary movements']==1):
        return 'red'
    if symptoms['fever']==1 and symptoms['vomiting']==1 and symptoms['sharp abdominal pain']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['age']<13 and (symptoms['seizures']==1 or symptoms['abnormal involuntary movements']==1 ):
        return 'red'
    if (symptoms['blood in stool']==1 or symptoms['vomiting blood']==1 or symptoms['rectal bleeding']==1 ) and symptoms['weakness']==1:
        return 'red'
    if symptoms['irregular heartbeat']==1 and symptoms['weakness']==1 and symptoms['fainting']==1:
        return "red"
    if symptoms['sex-no']==1 and symptoms['nausea']==1 and symptoms['sweating']==1 and symptoms['arm pain']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['sex-no']==1 and symptoms['sharp abdominal pain']==1 and symptoms['dizziness']==1 and symptoms['fainting']==1:
        return 'red'
    if symptoms['sharp abdominal pain']==1 and symptoms['fever']==1 and symptoms['vomiting']==1 and symptoms['decreased appetite']==1:
        return "red"
    if symptoms['shortness of breath']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1 )and symptoms['leg swelling']==1 :
        return 'red'
    if symptoms['pain in testicles']==1 and symptoms['vomiting']==1 and symptoms['sweating']==1:
        return 'red'
    if symptoms['back pain']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1)and symptoms['sweating']==1:
        return 'red'
    if symptoms['headache']==1 and symptoms['dizziness']==1 and symptoms['nausea']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['difficulty in swallowing']==1  and symptoms['hoarse voice']==1 :
        return "red"
    if symptoms['back pain']==1 and symptoms['involuntary urination']==1 and symptoms['loss of sensation']==1:
        return "red"
    if symptoms['age']<13 and symptoms['depressive or psychotic symptoms']==1 and symptoms['blood in stool']==1 and symptoms['vomiting']==1:
        return 'red'
    if symptoms['blindness']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1)and symptoms['weakness']==1:
        return 'red'
    if symptoms['diminished vision'] == 1 and symptoms['headache'] == 1:
        return 'red'
    return None