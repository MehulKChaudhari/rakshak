import matplotlib.pyplot as plt
import pandas as pd
import re
import string
import seaborn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

set(stopwords.words("english"))
data = pd.read_csv("train.csv")
data.toxic.value_counts(normalize=True)
count = data.iloc[:, 2:].sum()
"""print(count)
plt.figure(figsize=(8,4))
axis = seaborn.barplot(count.index, count.values, alpha=0.8)
plt.title("Distribution of Dataset")
plt.ylabel("Count", fontsize =12)
plt.xlabel("Comment type", fontsize=12)
rectangles = axis.patches
labels = count.values
for r, l in zip(rectangles, labels):
    h = r.get_height()
    axis.text(r.get_x() + r.get_width()/2, h+5, l, ha='center', va='bottom')
plt.show()
"""
# preprocess
an = lambda x: re.sub("\w*\d\w*", " ", x)
pl = lambda x: re.sub("[%s]" % re.escape(string.punctuation), " ", x.lower())
rn = lambda x: re.sub("\n", " ", x)
rna = lambda x: re.sub(r"[^\x00-\x7f]", r" ", x)
data["comment_text"] = data["comment_text"].map(an).map(pl).map(rn).map(rna)
# split
data_1 = data.loc[:, ["id", "comment_text", "toxic"]]
data_2 = data.loc[:, ["id", "comment_text", "severe_toxic"]]
data_3 = data.loc[:, ["id", "comment_text", "obscene"]]
data_4 = data.loc[:, ["id", "comment_text", "threat"]]
data_5 = data.loc[:, ["id", "comment_text", "insult"]]
data_6 = data.loc[:, ["id", "comment_text", "identity_hate"]]
from wordcloud import WordCloud

"""
def wcloud(df, label):
    set = df[df[label]==1]
    text = set.comment_text.values
    wc = WordCloud(background_color="black", max_words=4000)
    wc.generate("".join(text))
    plt.figure(figsize=(20,20))
    plt.subplot(221)
    plt.axis("off")
    plt.title("Words in {}".format(label), fontsize=20)
    plt.imshow(wc.recolor(colormap='gist_earth', random_state=244), alpha=0.98)
    plt.show()
wcloud(data_1, 'toxic')
wcloud(data_2, 'severe_toxic')
wcloud(data_3, 'obscene')
wcloud(data_4, 'threat')
wcloud(data_5, 'insult')
wcloud(data_6, 'identity_hate')"""

data_toxic = data_1[data_1["toxic"] == 1].iloc[0:5000, :]
data_nontoxic = data_1[data_1["toxic"] == 0].iloc[0:5000, :]
data_con1 = pd.concat([data_toxic, data_nontoxic], axis=0)

data_sevtox = data_2[data_2["severe_toxic"] == 1].iloc[0:5000, :]
data_nonsevtox = data_2[data_2["severe_toxic"] == 0].iloc[0:5000, :]
data_con2 = pd.concat([data_sevtox, data_nonsevtox], axis=0)

data_obscene = data_3[data_3["obscene"] == 1].iloc[0:5000, :]
data_nonobscene = data_3[data_3["obscene"] == 0].iloc[0:5000, :]
data_con3 = pd.concat([data_obscene, data_nonobscene], axis=0)

data_threat = data_4[data_4["threat"] == 1].iloc[0:478, :]
data_nonthreat = data_4[data_4["threat"] == 0].iloc[0:1912, :]
data_con4 = pd.concat([data_threat, data_nonthreat], axis=0)

data_insult = data_5[data_5["insult"] == 1].iloc[0:5000, :]
data_noninsult = data_5[data_5["insult"] == 0].iloc[0:5000, :]
data_con5 = pd.concat([data_insult, data_noninsult], axis=0)

data_idhate = data_6[data_6["identity_hate"] == 1].iloc[0:1405, :]
data_nonidhate = data_6[data_6["identity_hate"] == 0].iloc[0:5620, :]
data_con6 = pd.concat([data_idhate, data_nonidhate], axis=0)

from sklearn import preprocessing
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    precision_recall_curve,
    fbeta_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier


def cv_tf_train_test(df_done, label, v, ngram):
    x = df_done.comment_text
    y = df_done[label]
    xtrain, xtest, ytrain, ytest = train_test_split(
        x, y, test_size=0.3, random_state=42
    )
    cv1 = v(ngram_range=(ngram), stop_words="english")
    xtrain_cv1 = cv1.fit_transform(xtrain)
    xtest_cv1 = cv1.transform(xtest)

    lr = LogisticRegression()
    lr.fit(xtrain_cv1, ytrain)
    print("LR LR")

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(xtrain_cv1, ytrain)
    print("KNN KNN")

    bnb = BernoulliNB()
    bnb.fit(xtrain_cv1, ytrain)
    print("BNB BNB")

    mnb = MultinomialNB()
    mnb.fit(xtrain_cv1, ytrain)
    print("MNB MNB")

    svm = LinearSVC()
    svm.fit(xtrain_cv1, ytrain)
    print("SVM SVM")

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(xtrain_cv1, ytrain)
    print("RDF RDF")

    f1_score_data = {
        "F1 Score": [
            f1_score(lr.predict(xtest_cv1), ytest),
            f1_score(knn.predict(xtest_cv1), ytest),
            f1_score(bnb.predict(xtest_cv1), ytest),
            f1_score(mnb.predict(xtest_cv1), ytest),
            f1_score(svm.predict(xtest_cv1), ytest),
            f1_score(rf.predict(xtest_cv1), ytest),
        ]
    }
    df_f1 = pd.DataFrame(
        f1_score_data,
        index=[
            "Log Regression",
            "KNN",
            "BernoulliNB",
            "MultinomialNB",
            "SVM",
            "Random Forest",
        ],
    )
    return df_f1


df_tox = cv_tf_train_test(data_con1, "toxic", TfidfVectorizer, (1, 1))
print(df_tox)

df_sevtox = cv_tf_train_test(data_con2, "severe_toxic", TfidfVectorizer, (1, 1))
print(df_sevtox)

df_obs = cv_tf_train_test(data_con3, "obscene", TfidfVectorizer, (1, 1))
print(df_obs)

df_threat = cv_tf_train_test(data_con4, "threat", TfidfVectorizer, (1, 1))
print(df_threat)

df_insult = cv_tf_train_test(data_con5, "insult", TfidfVectorizer, (1, 1))
print(df_insult)

df_idhate = cv_tf_train_test(data_con6, "identity_hate", TfidfVectorizer, (1, 1))
print(df_idhate)
