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
    if symptoms['fever'] == 1 and symptoms['weakness'] == 1 and symptoms['stomach bloating'] == 1 and symptoms['age'] > 5:
        return 'red'
    if symptoms['delusions or hallucinations'] == 1 and symptoms['sweating'] == 0 and symptoms['headache'] == 1 and symptoms['weakness'] == 1:
        return 'red'
    if symptoms['sweating'] == 1 and symptoms['vomiting'] == 1 and symptoms['seizures'] == 1:
        return 'red'
    if symptoms['age'] < 1 and symptoms['seizures'] == 1 and symptoms['difficulty in swallowing'] == 1:
        return 'red'
    if symptoms['sleepiness'] == 1 and symptoms['difficulty in swallowing'] == 1 and symptoms['weakness'] == 1:
        return 'red'
    if symptoms['ispregnant'] == 1 and symptoms['headache'] == 1 and symptoms['leg swelling'] == 1 and symptoms['spots or clouds in vision'] == 1:
       return 'red'
    if symptoms['diarrhea'] == 1 and symptoms['vomiting'] == 1 and symptoms['weakness'] == 1 and symptoms['dizziness'] == 1:
       return 'red'
    if symptoms['fever'] == 0 and symptoms['weakness'] == 1 and symptoms['sweating'] == 1 and symptoms['dizziness'] == 1:
       return 'red'
    if symptoms['age'] > 50 and symptoms['foot or toe pain'] == 0 and symptoms['skin swelling'] == 1 and symptoms['loss of sensation'] == 1:
       return 'red'
    if symptoms['age'] > 60 and symptoms['leg pain'] == 1 and symptoms['problems with movement'] == 1 and symptoms['weakness'] == 1:
       return 'red'
    if symptoms['age'] > 60 and symptoms['fever'] == 0 and symptoms['shortness of breath'] == 1 and symptoms['weakness'] == 1 and symptoms['decreased appetite'] == 1:
       return 'red'
    if symptoms['sex-no'] == 0 and symptoms['age'] > 50 and symptoms['retention of urine'] == 1 and symptoms['lower abdominal pain'] == 1:
       return 'red'
    if symptoms['sex-no'] == 0 and symptoms['swelling of scrotum'] == 1 and symptoms['back pain'] == 1 and symptoms['pain in testicles'] == 0:
      return 'red'
    if symptoms['sex-no'] == 0 and symptoms['sharp abdominal pain'] == 1 and symptoms['vomiting'] == 1 and symptoms['constipation'] == 1:
      return 'red'
    if symptoms['sweating'] == 0 and symptoms['delusions or hallucinations'] == 1 and symptoms['headache'] == 1 and symptoms['weakness'] == 1:
      return 'red'
    if symptoms['fever'] == 1 and symptoms['leg pain'] == 1 and symptoms['jaundice'] == 1:
      return 'red'
    if symptoms['pain in eye'] == 1 and symptoms['eye redness'] == 1 and symptoms['diminished vision'] == 1:
      return 'red'

    return None