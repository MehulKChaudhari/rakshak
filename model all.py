import pandas as pd
import re
import string
import pickle
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
set(stopwords.words('english'))
data = pd.read_csv('train.csv')
data.toxic.value_counts(normalize=True)

an = lambda x: re.sub('\w*\d\w*',' ', x)
pl = lambda x: re.sub('[%s]' % re.escape(string.punctuation),' ', x.lower())
rn = lambda x: re.sub('\n',' ', x)
rna = lambda x: re.sub(r'[^\x00-\x7f]',r' ', x)
data['comment_text'] = data['comment_text'].map(an).map(pl).map(rn).map(rna)

data_1 = data.loc[:,['id','comment_text','toxic']]
data_2 = data.loc[:,['id','comment_text','severe_toxic']]
data_3 = data.loc[:,['id','comment_text','obscene']]
data_4 = data.loc[:,['id','comment_text','threat']]
data_5 = data.loc[:,['id','comment_text','insult']]
data_6 = data.loc[:,['id','comment_text','identity_hate']]
data_toxic = data_1[data_1['toxic']==1].iloc[0:5000,:]
data_nontoxic = data_1[data_1['toxic']==0].iloc[0:5000,:]
data_con1 = pd.concat([data_toxic, data_nontoxic], axis=0)

data_sevtox = data_2[data_2['severe_toxic']==1].iloc[0:5000,:]
data_nonsevtox = data_2[data_2['severe_toxic']==0].iloc[0:5000,:]
data_con2 = pd.concat([data_sevtox, data_nonsevtox], axis=0)

data_obscene = data_3[data_3['obscene']==1].iloc[0:5000,:]
data_nonobscene = data_3[data_3['obscene']==0].iloc[0:5000,:]
data_con3 = pd.concat([data_obscene, data_nonobscene], axis=0)

data_threat = data_4[data_4['threat']==1].iloc[0:478,:]
data_nonthreat = data_4[data_4['threat']==0].iloc[0:1912,:]
data_con4 = pd.concat([data_threat, data_nonthreat], axis=0)

data_insult = data_5[data_5['insult']==1].iloc[0:5000,:]
data_noninsult = data_5[data_5['insult']==0].iloc[0:5000,:]
data_con5 = pd.concat([data_insult, data_noninsult], axis=0)

data_idhate = data_6[data_6['identity_hate']==1].iloc[0:1405,:]
data_nonidhate = data_6[data_6['identity_hate']==0].iloc[0:5620,:]
data_con6 = pd.concat([data_idhate, data_nonidhate], axis=0)

x = data_con1.comment_text
y = data_con1['toxic']
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=42)
tfv = TfidfVectorizer(ngram_range=(1,1), stop_words='english')
xtrainfit = tfv.fit_transform(xtrain)
xtestfit = tfv.transform(xtest)
rf1 = RandomForestClassifier(n_estimators=100, random_state=42)
rf1.fit(xtrainfit,ytrain)
rf1.predict(xtestfit)

string = input("Enter string: ")
string = [string]
string_vect = tfv.transform(string)
print("Toxicity: ")
print(rf1.predict_proba(string_vect)[:,1])

