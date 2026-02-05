# Sample TensorFlow Lite Model Placeholder

This directory should contain your trained TensorFlow Lite model file.

## Model Requirements

- **File name**: `cattle_disease_model.tflite`
- **Input**: 224x224x3 RGB image (normalized to [0, 1])
- **Output**: Probability distribution over disease classes

## Disease Classes

The model should be trained to classify the following diseases:
1. Healthy
2. Foot and Mouth Disease
3. Lumpy Skin Disease
4. Mastitis
5. Pink Eye

## Training Your Model

To train a custom model:

1. Collect and label cattle images for each disease class
2. Use TensorFlow/Keras to build and train a CNN model
3. Convert the trained model to TFLite format:
   ```python
   converter = tf.lite.TFLiteConverter.from_keras_model(model)
   tflite_model = converter.convert()
   with open('cattle_disease_model.tflite', 'wb') as f:
       f.write(tflite_model)
   ```
4. Place the `.tflite` file in this directory

## Current Implementation

The current implementation uses a sample ML service that simulates predictions without a real model. This is for demonstration purposes and should be replaced with an actual trained model in production.
