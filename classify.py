import pandas as pd
import numpy as np

df = pd.read_csv("data/wine-reviews/winemag-data-130k-v2.csv")
#print(df)

from io import StringIO

col = ['description', 'variety']
df = df[col]
#print(df)

df.columns = ['description', 'variety']
df['category_id'] = df['variety'].factorize()[0]
#print(df)
category_id_df = df[['variety', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'variety']].values)

#print(df)

#import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(8,6))
#df.groupby('variety').description.count().plot.bar(ylim=0)
#plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words='english')
features = tfidf.fit_transform(df.description).toarray()
labels = df.category_id
#print(type(df.category_id))
#print(features.shape)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

X_train, X_test, y_train, y_test = train_test_split(df['description'], df['variety'], test_size=.2, random_state = 0)
count_vect = CountVectorizer(stop_words='english')
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
nb = MultinomialNB()
y_train = y_train.astype(str)

nb.fit(X_train_tfidf, y_train)

X_test_counts = count_vect.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

with open('wineCharacteristics.txt', 'r') as myfile:
	data = myfile.read().replace('\n', '')

#print(data)

data_counts = count_vect.transform([data])
data_tfidf = tfidf_transformer.transform(data_counts)

classification = nb.predict(data_tfidf)[0]
print(classification)

from sklearn import metrics

#y_pred_class = nb.predict(X_test_tfidf)
#print(metrics.accuracy_score(y_test, y_pred_class))
