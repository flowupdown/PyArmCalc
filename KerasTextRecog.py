# simple handwritten text recognition with keras
# only numbers allowed

import numpy as np
import cv2
from imutils import contours
import keras
import os
from make_dir import make_dir
import uuid
from SharedNames import model

class ProcessText():
    def __init__(self, image, words_dir="."):
        self.image = image
        self.words_dir = words_dir
                
    def image_to_words(self):
        image = cv2.imread(self.image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
        
        kernel = np.ones((8, 45), np.uint8)
        img_dilation = cv2.dilate(thresh, kernel, iterations=2)
        ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
        words_dim_dict = {"height": 0,
                          "weigth": 0}
        for ctr in ctrs:
            x, y, w, h = cv2.boundingRect(ctr)
            if w > words_dim_dict["weigth"]: words_dim_dict["weigth"] = w
            if h > words_dim_dict["height"]: words_dim_dict["height"] = h
            
        make_dir(self.words_dir)
        words_list = []
        for i, ctr in enumerate(ctrs):
            x, y, w, h = cv2.boundingRect(ctr)
            if h > words_dim_dict["height"] * 0.5:
                roi = image[y: y + h, x: x + w]
                word = "{}.png".format(i)
                words_list.append(word)
                cv2.imwrite(self.words_dir + word, roi)
        words_list = words_list[::-1]       
        lines_list = []
        for i in range(0, len(words_list), 3):
            lines_list.append(words_list[i : i+3][::-1])
            
        return lines_list, self.words_dir       
    
class ProcessWord():
    def __init__(self, image, words_dir):
        self.image = image
        self.words_dir = words_dir
        
    def image_to_digits(self):
        image = cv2.imread(self.words_dir + self.image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
        
        
        kernel = np.ones((2, 2), np.uint8)
        img_dilation = cv2.dilate(thresh, kernel, iterations=2)
        ctrs, hier = cv2.findContours(img_dilation.copy(),
                                      cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
        symbols_dim_dict = {"height": 0,
                            "weigth": 0}
        for ctr in ctrs:
            x, y, w, h = cv2.boundingRect(ctr)
            if w > symbols_dim_dict["weigth"]: symbols_dim_dict["weigth"] = w
            if h > symbols_dim_dict["height"]: symbols_dim_dict["height"] = h
            
        word_dir = self.words_dir + self.image.split(".")[0] + "\\"
        make_dir(word_dir)
        sorted_ctrs = contours.sort_contours(ctrs,
                                             method="left-to_right")[0]
        digits_list = []
        for i, ctr in enumerate(sorted_ctrs):
            x, y, w, h = cv2.boundingRect(ctr)
            if h > symbols_dim_dict["height"] * 0.5:
                roi = thresh[y: y + h, x: x + w]
                img = "{}.png".format(i)
                digits_list.append(img)
                cv2.imwrite(word_dir + img, roi)
                
        return digits_list, word_dir
    
class ProcessDigitsList():
    def __init__(self, word_dir):
        model_dir = os.getcwd() + "\\" + model
        self.model = keras.models.load_model(model_dir)
        self.digits_dir = word_dir
        
    def list_to_digits(self):
        dataset = keras.utils.image_dataset_from_directory(
            directory=self.digits_dir,
            label_mode=None,
            color_mode="grayscale",
            image_size=(20, 20),
            shuffle=False,
            pad_to_aspect_ratio=True,
            )
        dataset = dataset.map(lambda x: keras.ops.image.pad_images(x,
                                                                   top_padding=4,
                                                                   left_padding=4,
                                                                   bottom_padding=4,
                                                                   right_padding=4) / 255)
        
        predictions = self.model.predict(dataset)
        predictions = [str(prediction.argmax()) for prediction in predictions]
        predictions = "".join(predictions)
        return predictions

if __name__ == "__main__":
    test_image = os.getcwd() + "\\" + "armtest_2.jpg"
    lines_list, words_dir = ProcessText(test_image).image_to_words()
    predictions_list = []
    for line in lines_list:
        for item in line:
            digits_list, word_dir = ProcessWord(item, words_dir).image_to_digits()
            predictions = ProcessDigitsList(word_dir).list_to_digits()
            predictions_list.append(predictions)
            
    lines_list = []
    for i in range(0, len(predictions_list), 3):
        lines_list.append(predictions_list[i : i+3])
    print(lines_list)



