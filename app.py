# ============================
# Importing necessary libraries
# ============================

#read files & directory
import os
# hold data in DataFrame
import pandas as pd
import numpy as np
# for randomness during training
import random
# randomize and split dataframe for training and testing
from sklearn.model_selection import train_test_split
# to compute metric during training
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
# automatically converts text to tokens
from transformers import AutoTokenizer
# PreTrained model from theHuggingFace for classifier ---> classifying [ vul | non_vul ]
from transformers import AutoModelForSequenceClassification
# handles training loop [forward_pass, loss_calc, back_prop, optimizer, update, evaluation]
from transformers import Trainer
# training arguments for the Trainer
from transformers import TrainingArguments
# deep-learning framework to work with tokens -> tensors, hadling computations
import torch
# HuggingFace pipeline for easy inference
from transformers import pipeline
# Early Stopping Callback to stop training if upper bound is reached
from transformers import EarlyStoppingCallback





# ============================
# Trainer needs data in special format
# len --> number of items in dataset
# getitem --> to get i'th item
# ============================
class ContractDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item





# ============================
# Compute Metrics passed as an argument to trainer
# to calulate different measures during training
# ============================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }




# ============================
# Load from Google Drive (Colab)
# ============================
from google.colab import drive
drive.mount('/content/drive')

base_path = "/content/drive/MyDrive/SmartContractsDataset"


# ============================
# Load from Local Machine (Uncomment to use locally)
# ============================
# base_path = "data"

# ============================
# Contract Paths (same for both cases)
# ============================
vul_dir = os.path.join(base_path, "vulnerable_smart_contracts")
non_vul_dir = os.path.join(base_path, "non_vulnerable_smart_contracts")

# ============================
# Load files  [:9000] training data limit ----> 9000
# ============================
vul_files = [
    open(os.path.join(vul_dir, f), "r", encoding="utf-8", errors="ignore").read()
    for f in os.listdir(vul_dir)[:9000]
]
non_vul_files = [
    open(os.path.join(non_vul_dir, f), "r", encoding="utf-8", errors="ignore").read()
    for f in os.listdir(non_vul_dir)[:9000]
]

# ============================
# Create DataFrame
# ============================
df = pd.DataFrame({
    "code": vul_files + non_vul_files,
    "label": [1] * len(vul_files) + [0] * len(non_vul_files)   # 1 = vulnerable, 0 = safe
})

# Cleaning the Code => removing New Lines and extra spaces
df["code"] = df["code"].str.replace("\n", " ", regex=False).str.strip()

# Random splitting the data for training and testing the model
contracts_train, contracts_test, labels_train, labels_test = train_test_split(
    df["code"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)







# ============================
# Tokenization
# ============================

# load tokenizer from pretrained codebert-base
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
# tokenize the training smartContracts
train_encodings = tokenizer(list(contracts_train), truncation=True, padding=True, max_length=256)
# tokenize the testing smartContracts
test_encodings = tokenizer(list(contracts_test), truncation=True, padding=True, max_length=256)





# ============================
# Create Dataset for Training and Testing
# to be used by Torch and Trainer
# ============================

train_dataset = ContractDataset(train_encodings, list(labels_train))
test_dataset = ContractDataset(test_encodings, list(labels_test))



# ============================
# Model Initialization
# import pretrained model - codebert-base
# 
# codebert-base - model to handle codes, plag detection, tokenization, etc
# num_labels === no. of output labels, 0 and 1, vuln and non_vuln
# ============================

model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/codebert-base", 
    num_labels=2
)



# ============================
# Initialising training args
# ============================

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    evaluation_strategy="steps",
    eval_steps=200,
    save_strategy="steps",
    save_steps=200,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
    logging_dir="./logs",
    logging_steps=50,
    fp16=True,
)


# ============================
# Setting Seeds for Reproducibility && Randomness
# ============================
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)


# ============================
# Trainer Initialization &&
# training model on dataset
# ============================

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
)

trainer.train()


# ============================
# Runs the trained model on test Dataset
# print result [loss, runtime, samples/s, eval-step/s]
# ============================

eval_result = trainer.evaluate()
print(eval_result)


# ============================
# Saving Trained Model and Tokenized keywords
# ============================

model.save_pretrained("/content/smart_contract_model")
tokenizer.save_pretrained("/content/smart_contract_model")


# ============================
# Initializing Classifier Pipeline,
# for testing input code using trained
# model.
# ============================

classifier = pipeline(
    "text-classification",
    model="/content/smart_contract_model",
    tokenizer="/content/smart_contract_model",
    return_all_scores=False
)

# assigning label with human_friendly_names
id2label = {0: "Safe", 1: "Vulnerable"}
label2id = {"Safe": 0, "Vulnerable": 1}

classifier.model.config.id2label = id2label
classifier.model.config.label2id = label2id

# testing code on trained model and printing the results
test_code = "function withdraw(uint amount) public { msg.sender.call.value(amount)(); }"  #harmful
print(classifier(test_code))


test_code1 = "function deposit() public payable {}"  # harmless

print(classifier(test_code1))

