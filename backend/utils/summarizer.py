from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))   # backend/
PEGASUS_DIR = os.path.join(BASE_DIR, "..", "models", "pegasus_saved")

tokenizer = AutoTokenizer.from_pretrained(PEGASUS_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(PEGASUS_DIR)

def summarize_text(chunks):
    summaries = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True)
        output_ids = model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
        )
        text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        summaries.append(text)
    return "\n".join(summaries)
