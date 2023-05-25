from tensorflow import keras
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import numpy as np
from keras.preprocessing import image

def cnn_run():
    model = keras.models.load_model('parkingline_class_epoch500_cnn.h5')

    test_dir = "C:/Users/wsup9/OneDrive/Desktop/capston_file/parking_pic"
    filenames = os.listdir(test_dir)

    fig = plt.figure(figsize=(10,6))
    
    fn = filenames[0]

    path = test_dir+'/'+fn
    test_img = tf.keras.utils.load_img(path, color_mode = 'grayscale', target_size = (150,150), interpolation = 'bilinear')
    x = tf.keras.utils.img_to_array(test_img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes = model.predict(images, batch_size = 15)

    if int(classes)==1:
        print("주차 성공")
    else:
        print("주차 실패")

    fig.add_subplot(1, 1, 1)

    if classes[0]==0:
        plt.title("BAD")
        plt.axis('off')
        plt.imshow(test_img, cmap = 'gray')
    else:
        plt.title("GOOD")
        plt.axis('off')
        plt.imshow(test_img, cmap='gray')

    plt.show()

    return int(classes)
