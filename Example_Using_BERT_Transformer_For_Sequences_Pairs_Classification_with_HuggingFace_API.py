## CLASSER DES SEQUENCES, AVEC LE TANSFORMER BERT DE LA LIBRAIRIE TANSFORMERS
## DE HUGGINGFACE, SUR LE BACKEND TENSORFLOW ET SON IMPLEMENTATION SPECIFIQUE
## DE L'API KERAS.
## NOUS ALLONS CLASSER CHAQUE PAIRE DE PHRASES EN DEUX CLASSES /
##       LE SENS DE CHAQUE PHRASE DE LA PAIRE EST EQUIVALENT
##               VS. 
##       LE SENS DE CHAQUE PHRASE DE LA PAIRE N'EST PAS EQUIVALENT
## Notre but est de trouver des équivalences sémantiques. Nous utilisons 
## pour ce faire une tâche de classification, attribuant une classe aux paires de sens similaire,
## et une autre classe aux paires de sens différents.
## Nous aurions pu aussi utiliser des embeddings niveau phrase, en prenant par exemple
## l'embedding contextuel des séparateurs [CLS] et [SEP] de BERT, qui pourraient servir
## à "représenter" les phrases de la paire (cf. https://towardsdatascience.com/bleu-bert-y-comparing-sentence-scores-307e0975994d),
## pour ensuite comparer ces représentations avec la corrélation de Spearman
## (sans doute préférable à la similarité cosinus dans ce cas là). 

#Credits to : https://colab.research.google.com/drive/1l39vWjZ5jRUimSQDoUcuWGIoNjLjA2zu
#OS : Windows 10
#Python version 3.7.4
#CUDA version 10.0.130
#Installed Tensorflow CPU 2.0 : pip install tensorflow
#Installed Keras 2.3.1 : pip install Keras - 
#Installed HuggingFace Transformers 2.2.0 : pip install transformers
#Installed Tensorflow example datasets : pip install tensorflow_datasets

#Documentation : https://huggingface.co/transformers/index.html

#Importer Tensorflow
import tensorflow as tf

#Si vous avez Tensorflow CPU ET GPU installés, vous pouvez forcer l'utilisation
#de Tensorflow CPU avec la manipulation suivante :
#   Tester que l'environnement a bien accès au(x) GPU(s) - ou pas accès...
print('La GPU est elle disponible : ', tf.test.is_gpu_available(), '\n')
from tensorflow.python.client import device_lib
print('Liste des CPU/GPU disponibles : ', device_lib.list_local_devices(), '\n')
#   Forcer l'utilisation de Tensorflow CPU
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"    # Voir https://github.com/tensorflow/tensorflow/issues/152
os.environ["CUDA_VISIBLE_DEVICES"]= ""          # Permet de rendre la/les GPU(s) invisibles. Parfois plutôt 
                                                # que de laisser vide "", les valeurs "0" ou "-1" sont recommandées
#   Tester à nouveau que l'environnement a bien accès au(x) GPU(s) - ou pas accès...
print('La GPU est elle disponible : ', tf.test.is_gpu_available(), '\n')
print('Liste des CPU/GPU disponibles : ', device_lib.list_local_devices(), '\n')

#Datasets d'exemple, pour la démo d'utilisation des Transformers de HuggingFace
import tensorflow_datasets

# Charger un modèle pré-entraîné avec son tokenizer, ici BERT dans sa version TensorFlow (notez que le nom du modèle est préfixé "TF")
from transformers import (TFBertForSequenceClassification, BertTokenizer)
bert_model = TFBertForSequenceClassification.from_pretrained("bert-base-cased") # Charge la conf automatiquement
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

#   Illustration de la tokenisation
sequence = "Systolic arrays are cool. This 🐳 is cool too."
print("\r\n", "Sequence brute, pour illustrer la tokenisation : ", sequence)
bert_tokenized_sequence = bert_tokenizer.tokenize(sequence)
print("\r\n", "Sequence tokenisée pour BERT : ", bert_tokenized_sequence, "\r\n")

#Fine tuner un modèle
from transformers import glue_convert_examples_to_features  #GLUE c'est pour General Language Understanding Evaluation (https://gluebenchmark.com/),
                                                            #Ça consiste en un ensemble de ressources, comme des tâches classiques de NLP avec leurs
                                                            #jeux de données, des données permettant d'évaluer ces tâches etc...
                                                            #glue_convert_examples_to_features va nous permettre de convertir le jeu de données
                                                            #d'exemple de TensorFlow en features, utilisables par la méthode "fit" de Keras
                                                            #appliquée au modèle de Transformer préfabriqué par HuggingFace

#   Charger des données texte et les pré-processer (pipeline d'entrée)
#      Importer les données
data = tensorflow_datasets.load("glue/mrpc")

#      Répartir les données en train et test/validation
train_dataset = data["train"]
validation_dataset = data["validation"]

#      Pour illustrer le contenu du jeu de données d'entraînement, observons son premier élément
example = list(train_dataset.__iter__())[0]
print("Exemple : ", example, "\r\n")
print('',
    'idx:      ', example['idx'],       '\n',
    'label:    ', example['label'],     '\n',
    'sentence1:', example['sentence1'], '\n',
    'sentence2:', example['sentence2'], '\n',)
seq0 = example['sentence1'].numpy().decode('utf-8')  #Converti en chaîne de caractères les bytes récupérés du tenseur
seq1 = example['sentence2'].numpy().decode('utf-8')  #Converti en chaîne de caractères les bytes récupérés du tenseur
print("Première séquence:", seq0, '\n',)
print("Seconde séquence:", seq1, '\n',)

#   Encoder les séquences au bon format pour notre modèle.
#   Deux possibilités : encode()et encode_plus() (qui retourne des informations en plus que nous ne détaillerons pas ici)
#      Illustration de encode()
encoded_bert_sequence = bert_tokenizer.encode(seq0, seq1, add_special_tokens=True, max_length=128)
print("Séquence encodée pour BERT : séparateur du tokeniseur, cls_token_id:   ",                #Notez qu'ici, 101 est l'ID du Token qui stipule qu'il s'agira
      encoded_bert_sequence, bert_tokenizer.sep_token_id, bert_tokenizer.cls_token_id, '\n')    #d'une tâche de classification [CLS], il arrive au début de la séquence de tokens.
                                                                                                #102 est quand à lui l'ID du tiken de séparation des phrases, [SEP].
                                                                                                #Le formalisme de BERT pour les paires de phrases est : [CLS] A [SEP] B [SEP]

#      Encodage de nos jeux d'entrainement et de test :
#       Dans notre cas d'exemple, pas besoin de encode() ou encode_plus() car il existe la librairie "glue_convert_examples_to_features"
#       (qui utilise sous cape la méthode encode_plus()) qui converti directement les jeux de données d'exemple de TensorFlow en features
#       exploitables par le modèle. De plus cette librairie de dépend ni du type de tâche (GLUE) ni du tokenizer.
bert_train_dataset = glue_convert_examples_to_features(train_dataset, bert_tokenizer, 128, 'mrpc')          #La tâche 'mrpc' se base sur le "Microsoft Research Paraphrase Corpus"
bert_validation_dataset = glue_convert_examples_to_features(validation_dataset, bert_tokenizer, 128, 'mrpc')#(https://www.microsoft.com/en-us/download/details.aspx?id=52398), et 
                                                                                                            #sert à déterminer l'équivalence sémantique de paires de phrases.

#       On mélange les données (shuffle) et découpe en lots (mini-batchs)
bert_train_dataset = bert_train_dataset.shuffle(100).batch(32).repeat(2)
bert_validation_dataset = bert_validation_dataset.batch(64)

#   On définit les hyper-paramètres
optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

bert_model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

#   Entraîner le modèle avec la méthode "fit" de Keras
#   BERT a déjà été préalablement pré-entrainé. Il nous est servi déjà pré-entraîné par l'API de HuggingFace.
#   Ici l'entraînement ne fait que fine-tuner, spécialiser (en incrémental) le modèle (BERT dans notre cas).
print('\n', "Fine-tuning BERT avec MRPC (Microsoft Research Paraphrase Corpus)", '\n')
bert_history = bert_model.fit(bert_train_dataset, epochs=3, validation_data=bert_validation_dataset)

#   Evaluer le modèle avec Keras
print('\n', "Evaluating the BERT model", '\n')
bert_model.evaluate(bert_validation_dataset)
