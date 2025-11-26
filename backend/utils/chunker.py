import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

def chunk_text(text, max_tokens=900):
    sentences = sent_tokenize(text)
    chunks = []
    current = ""
    length = 0

    for s in sentences:
        tokens = len(s.split())
        if length + tokens <= max_tokens:
            current += s + " "
            length += tokens
        else:
            chunks.append(current)
            current = s + " "
            length = tokens

    if current:
        chunks.append(current)

    return chunks
