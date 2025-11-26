from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

PEGASUS_DIR = "V:/projects/WhisPeg/models/pegasus_saved"

tokenizer = AutoTokenizer.from_pretrained(PEGASUS_DIR, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(PEGASUS_DIR)

def summarize_text(chunks):
    summaries = []

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    return "\n".join(summaries)
