import os
import email
import email.parser
import email.policy
import random
from bs4 import BeautifulSoup
import re

base_dir = 'D:/data/'
stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
"been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", 
"for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", 
"himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", 
"more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
"same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", 
"then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", 
"up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
 "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]


def load_email(is_spam, filename):
    directory = base_dir + ('spam' if is_spam else 'ham')
    with open(os.path.join(directory, filename), 'rb') as f:
        return email.parser.BytesParser(policy=email.policy.default).parse(f)

class DataHandler():

    def get_data(self):
        spam_email_dir = os.listdir(base_dir + 'spam')
        ham_email_dir = os.listdir(base_dir + 'ham')

        spam_emails = [load_email(True, filename) for filename in spam_email_dir]
        ham_emails = [load_email(False, filename) for filename in ham_email_dir]

        random.shuffle(spam_emails)
        random.shuffle(ham_emails)

        return {
            'spam': spam_emails, 
            'ham': ham_emails
            }

    def process_email(self, emails, label, data_dictionary, default_topic=None):
        for mail in emails:
            payload = mail.get_payload()
            if isinstance(payload, list):
                self.process_email(payload, label, data_dictionary, default_topic=mail["Subject"])
            else:
                if 'Content-Type' in mail.keys():
                    if 'html' in mail['Content-Type'].lower():
                        try: 
                            soup = BeautifulSoup(mail.get_content(), features="html.parser")
                            topic = mail['Subject']
                            if topic == None:
                                topic = default_topic
                            content = soup.body.text
                            data_dictionary['topic'].append(topic)
                            data_dictionary['content'].append(content)
                            data_dictionary['label'].append(label)
                        except:
                            pass
                    elif "plain" in mail['Content-Type'].lower():
                        try: 
                            topic = mail['Subject']
                            if topic == None:
                                topic = default_topic
                            content = mail.get_content()
                            data_dictionary['topic'].append(topic)
                            data_dictionary['content'].append(content)
                            data_dictionary['label'].append(label)
                        except:
                            pass
                    else:
                        pass

    def preprocess_text(self, content):
        content = content.lower()
        cleaner = re.compile('<.*?>')
        content = re.sub(cleaner, '', content)
        content = content.replace('\n',' ')
        content = re.sub(r"[^a-zA-Z0-9]+", ' ', content)
        for stopword in stopwords:
            content = content.replace(stopword + " ", "")
            content = content.replace(" " + stopword, "")
        return content