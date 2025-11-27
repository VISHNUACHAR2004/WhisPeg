from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

name = "google/pegasus-xsum"

tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForSeq2SeqLM.from_pretrained(name)

tokenizer.save_pretrained("V:/projects/WhisPeg/models/pegasus_saved")
model.save_pretrained("V:/projects/WhisPeg/models/pegasus_saved")

print("Pegasus model downloaded correctly.")
