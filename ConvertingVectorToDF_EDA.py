import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns


############Making dataframe from vectors
df = pd.read_csv(f"pathToFileWithVectorizedWords", sep=";").fillna(" ")

pd.Series(df).sort_values(ascending=False).head(20).plot(kind='bar', title = "First 20 most frequent words in merged ISW texts", xlabel = "word", ylabel = "frequency")

dic = {}
for i in smth:
    for j in i:
        if j in dic:
            dic[j]+=i[j]
        else:
            dic[j] = i[j]

pd.Series(dic).sort_values(ascending=False).head(20).plot(kind='bar', title = "First word 20 from each vectorized text and then added", xlabel = "word", ylabel = "frequency")

dataFrameIsw_v2 = pd.DataFrame(columns=[dic.keys()])


dic2 = dic
def clearDic(dict):
    for i in dict.keys():
        dict[i] = 0
    return dict

for i in smth:
    clear_dict = clearDic(dic2)
    for j in i:
        clear_dict[j] = i[j]
    df_temp = pd.DataFrame(clear_dict, index=[0])
    dataFrameIsw_v2 = pd.concat([dataFrameIsw_v2, df_temp], ignore_index=True)

df_tfidf_v2 = dataFrameIsw_v2.drop(dataFrameIsw_v2.columns[6116:], axis=1)
df_tfidf_v2.to_csv(f"whereToSaveOutputData", sep=";", index=False)

##########Creating EDA

corr = df_tfidf_v2.corr()
ax = plt.axes()
sns.heatmap(corr)
ax.set_title("Correlation matrix of the tf-idf vectors")
plt.show()

plt.figure(figsize=(8, 12))
heatmap = sns.heatmap(corr[['city']].sort_values(by='city', ascending=False).head(20), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Top 30 correlations for "city" word', fontdict={'fontsize':18}, pad=16)



