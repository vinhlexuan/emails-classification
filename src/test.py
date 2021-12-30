from data import DataHandler
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

data_handler = DataHandler()

data = data_handler.get_data()

data_dictionary = {'topic': [], 'content': [], 'label': []}

data_handler.process_email(data['spam'], 1, data_dictionary)
data_handler.process_email(data['ham'], 0, data_dictionary)
df = pd.DataFrame(data_dictionary)
df.dropna(inplace=True)
df = df.sample(frac=1)

topic_and_contents = []
for (topic, content) in zip(df["topic"], df["content"]):
    topic_and_contents.append(data_handler.preprocess_text(topic + " " + content))
df["topic_content"] = topic_and_contents

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(df["topic_content"])
x = x.toarray()
X = []
for i in x:
    X.append(i.flatten())
Y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Number of emails in traning: ",len(y_train))
print("Number of emails in testing: ",len(y_test))

clf_NB = GaussianNB()
clf_NB.fit(X_train, y_train)

y_pred = clf_NB.predict(X_test)
print (f"Accuracy in testing dataset:",(100*accuracy_score(y_test, y_pred)))