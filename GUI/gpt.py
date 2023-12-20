import torch
import torch.nn as nn
from transformers import GPT2TokenizerFast, GPT2LMHeadModel
from transformers import Trainer, TrainingArguments
from tqdm.auto import tqdm
import pandas as pd
import numpy as np
from transformers import pipeline
pl = pipeline(task='text-generation',model='gpt')
 
 
def create_prompt(ingredients):
    ingredients = ingredients.split(',')
    ingredients = ','.join([x.strip().lower() for x in ingredients])
    ingredients = ingredients.strip().replace(',','\n')
    s = f"Ingredients:\n{ingredients}\n"
    for ing in ingredients:
        prompt = s
        a = pl(prompt, max_new_tokens=512, penalty_alpha=0.6, top_k=4, pad_token_id=50259)[0]['generated_text']
    return a