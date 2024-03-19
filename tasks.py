from transformers import AutoModelForCausalLM, AutoTokenizer
from celery import Celery

app = Celery('tasks')
app.config_from_object('celeryconfig')

models = {}

def load_model(model_name):
    if model_name not in models:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        models[model_name] = (model, tokenizer)
    return models[model_name]

@app.task
def generate_text(prompt, model_name):
    model, tokenizer = load_model(model_name)
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    max_length = len(input_ids[0]) + 50  # Adjust as needed
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    text_output = tokenizer.decode(output[0], skip_special_tokens=True)
    return text_output