#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Wei Zheng, Feb'2021
# ref: https://www.tensorflow.org/tutorials/keras/text_classification

import matplotlib.pyplot as plt
import os
import re
# import shu
import string
import pickle
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

params = {'BATCH_SIZE': 64,
          'SEED': 2021,
          'LR': 1e-3,
          'MAX_FEATURES': 5000, # google suggests <= 20000
          'SEQ_LENGTH': 250,
          'EMBEDDING_DIM': 16,
          'DROP_RATE': 0.2}
text_pth = 'data/aclImdb/'
callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                              patience=2,
                                              save_best_only=True)]

# load training data from training
raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join(text_pth, 'train/'),
    batch_size=params['BATCH_SIZE'],
    validation_split=0.2,
    subset='training',
    seed=params['SEED'])

# print sample data from raw_train_ds
for text_batch, label_batch in raw_train_ds.take(1):
    for i in range(2):
        print("Review", text_batch.numpy()[i])
        print("Label", label_batch.numpy()[i])

# load validation data from training
raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join(text_pth, 'train/'),
    batch_size=params['BATCH_SIZE'],
    validation_split=0.2,
    subset='validation',
    seed=params['SEED'])

# load test data
raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join(text_pth, 'test/'),
    batch_size=params['BATCH_SIZE'])


def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    return tf.strings.regex_replace(stripped_html, '[%s]' % re.escape(string.punctuation),'')


# define vectorization layer
vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens=params['MAX_FEATURES'],
    output_mode='int', # int, count, tf-idf
    output_sequence_length=params['SEQ_LENGTH']
)

# Make a text-only dataset (without labels), then call adapt
train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

# @tf.keras.utils.register_keras_serializable()
def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label


# retrieve a batch (of 32 reviews and labels) from the dataset
text_batch, label_batch = next(iter(raw_train_ds))
first_review, first_label = text_batch[0], label_batch[0]
print(' ')
print("Review", first_review)
print("Label", raw_train_ds.class_names[first_label])
print("Vectorized review", vectorize_text(first_review, first_label))

# from tokenized back to text data
print("7 ---> ",vectorize_layer.get_vocabulary()[7])
print(" 313 ---> ",vectorize_layer.get_vocabulary()[313])
print('Vocabulary size: {}'.format(len(vectorize_layer.get_vocabulary())))

# build data for model
train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)


# settings for model performance
auto_tune = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=auto_tune)
val_ds = val_ds.cache().prefetch(buffer_size=auto_tune)
test_ds = test_ds.cache().prefetch(buffer_size=auto_tune)

# create model structure
model = tf.keras.Sequential([
    layers.Embedding(params['MAX_FEATURES'] + 1, params['EMBEDDING_DIM']),
    layers.Dropout(params['DROP_RATE']),
    layers.GlobalAveragePooling1D(),
    layers.Dropout(params['DROP_RATE']),
    layers.Dense(1)
])
model.summary()


# compile the model
model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
             optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
             metrics=tf.keras.metrics.BinaryAccuracy(threshold=0.4))

# fit the model
epochs = 50
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=callbacks,
    verbose=2)

# evaluate the model with test data
loss, accuracy = model.evaluate(test_ds)
print("Loss: ", loss)
print("Accuracy: ", accuracy)

# plot history training results
history_dict = history.history
# history_dict.keys()
acc = history_dict['binary_accuracy']
val_acc = history_dict['val_binary_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = range(1, len(acc) + 1)

# plot on loss
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# plot on accuracy
plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()


def export_vectorized_model(vetor_layer, model, eval_ds, export=False):
    # Pickle the config and weights
    pickle.dump({'config': vetor_layer.get_config(),
                 'weights': vetor_layer.get_weights()}
                , open("model/vectorized_model.pkl", "wb"))

    # Test it with transformed `raw_test_ds`, which yields raw strings
    loss, accuracy = model.evaluate(eval_ds)
    print(accuracy)
    if export == True:
        model.save('model/vectorized_model')

# export_vectorized_model(vectorize_layer, model, test_ds, export=False)


def load_vectorized_model(vt_pkl, model_pth):
    with open(vt_pkl, 'rb') as r:
        config_file = pickle.load(r)
        vt_layer = TextVectorization.from_config(config_file['config'])
        # You have to call `adapt` with some dummy data (BUG in Keras)
        vt_layer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
        vt_layer.set_weights(config_file['weights'])

    new_model = tf.keras.models.load_model(model_pth)

    # can be used on raw_oot_data
    export_model = tf.keras.Sequential([
        vt_layer,
        new_model,
        layers.Activation('sigmoid')])
    export_model.compile(loss=losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy'])
    print(export_model.summary())
    return export_model
