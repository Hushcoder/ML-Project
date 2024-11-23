import re

def clean(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z0-9$-_@.&+!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove special Characters
    text = re.sub(r'[^a-zA-Z0-9]','', text)

    # Replace multiple spaces with a simple space
    text = re.sub(r'\s{2,}', '', text)

    # Trim leading and Trailing whitespaces 
    text = text.strip()

    # Remove extra whitespaces
    text = ' '.join(text.split())

    return text