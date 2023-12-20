import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, Model
 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
 
 
 
def custom_image(input):
    class_names= ['apple','banana','beetroot','bell pepper','cabbage','capsicum','carrot','cauliflower','chilli pepper','corn','cucumber','eggplant','garlic','ginger','grapes','jalepeno','kiwi','lemon','lettuce','mango','onion','orange','paprika','pear','peas','pineapple','pomegranate','potato','raddish','soy beans','spinach','sweetcorn','sweetpotato','tomato','turnip','watermelon']
    
    model = load_model('fruit_vegetable_classifier.h5')
    img_path = input
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Rescale the image
 
# Make predictions
    predictions = model.predict(img)
    class_index = np.argmax(predictions)
    class_name = class_names[class_index]  # You should have a list of class names
# Load the trained model
    return class_name
 
if __name__ == "__main__":
    input = "Image_1.jpg"
    x = custom_image(input)
    print(x)