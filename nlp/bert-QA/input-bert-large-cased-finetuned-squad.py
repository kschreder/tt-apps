# from https://huggingface.co/transformers/v2.8.0/usage.html#extractive-question-answering
import os

import torch
import numpy as np
from torch.utils.data import DataLoader, RandomSampler
from transformers import AutoTokenizer
from testify.tests import get_full_path_to_test_file

dataset_iter = None

text = r"""
🤗 Transformers (formerly known as pytorch-transformers and pytorch-pretrained-bert) provides general-purpose
architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet…) for Natural Language Understanding (NLU) and Natural
Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between
TensorFlow 2.0 and PyTorch.
"""

questions = [
    "How many pretrained models are available in Transformers?",
    "What does Transformers provide?",
    "Transformers provides interoperability between which frameworks?",
    "What architectures?"
]


def cleanup():
    # Release the memory
    global dataset_iter
    dataset_iter = None


def get_input_activations(
    input_shapes=[[1, 128]],
    filename="/home/software/mount/data/software/graph_compiler/activation_data/squad/squad_bert.pt",
    return_token_type_ids=True,
    return_attention_mask=False,
):
    global dataset_iter
    assert (
        len(input_shapes) == 1
    ), f"Expecting only one input shape request for bert squad, got: {input_shapes}"
    assert (
        len(input_shapes[0]) == 2
    ), "Expecting 2D shape request for bert squad, of shape (batch_size, sequence_len)"
    batch_size = input_shapes[0][0]
    model_name = "bert-large-cased-whole-word-masking-finetuned-squad"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    question = questions[3]
    print('TEXT:\n', text)
    print('QUESTION:\n', question)
    inputs = tokenizer.encode_plus(question, text,  # randomly chosen
                                   add_special_tokens=True,
                                   pad_to_max_length=True,
                                   return_tensors="pt")
    input_data = inputs['input_ids']
    token_type_ids = inputs['token_type_ids']

    # print('input data\n', input_data)
    # print('token_type_ids\n', token_type_ids)

    ret = [input_data.detach().numpy().astype(np.int64)]
    if return_token_type_ids:
        ret.append(token_type_ids.detach().numpy().astype(np.int64))
    if return_attention_mask:
        ret.append(attention_mask.detach().numpy().astype(np.int64))
    return ret
