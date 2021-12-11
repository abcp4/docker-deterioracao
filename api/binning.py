import pandas as pd
import numpy as np

column_names=[  'Idade','Setor','Temperatura','Frequência respiratória',
                'Pressão Sistólica','Pressão Diastólica',
                'Pressão Média','Saturação O2',
                'Bin_Temperatura','Bin_Respiração',
                'Bin_Sistólica','Bin_Média','Bin_o2']
                
def binning(df):
    df={column_names[k]:[df[k]] for k in range(len(df))}
    df=pd.DataFrame.from_dict(df)
    
    features = np.zeros((len(df), 5))

    #temperatura
    for i in range(len(df)):
        temperatura = df.iloc[i, 2]
        if temperatura <= 35:
            temperatura_bin = 3
        elif temperatura >= 39.1:
            temperatura_bin = 2
        elif (35.1 <= temperatura <= 36.0) | (38.1 <= temperatura <= 39.0):
            temperatura_bin = 1
        else:
            temperatura_bin = 0
        features[i, 0] = temperatura_bin

        #frequencia respiratoria
        respiracao = df.iloc[i, 3]
        if (respiracao < 8)|(respiracao > 25):
            respiracao_bin = 3
        elif 21 <= respiracao <= 24:
            respiracao_bin = 2
        elif 9 <= respiracao <= 11:
            respiracao_bin = 1
        else:
            respiracao_bin = 0
        features[i,1] = respiracao_bin

        #pressao sistolica
        sistolica = df.iloc[i, 4]  
        if (sistolica <= 100):
            sistolica_bin = 1
        elif (sistolica <= 90) & (sistolica >= 220):
            sistolica_bin = 3
        elif (sistolica >= 91) & (sistolica <= 100):
            sistolica_bin = 2
        elif (sistolica >= 101) & (sistolica <= 110):
            sistolica_bin = 1
        else:
            sistolica_bin = 0
        features[i, 2] = sistolica_bin

        #media
        media = df.iloc[i, 6]
        if media >= 70:
            media_bin = 0
        else:
            media_bin = 1
        features[i, 3] = media_bin

        #o2
        o2 = df.iloc[i, 6]
        if o2 <= 91:
            o2_bin = 3
        elif o2 >= 96:
            o2_bin = 0
        elif o2 >= 92 and o2 <= 93:
            o2_bin = 2
        elif o2 > 93 and o2 <= 95:
            o2_bin = 1

        features[i, 4] = o2_bin

    features=np.reshape(features,(5,len(df)))

    return features