import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from typing import List
import os
import time
import matplotlib.pyplot as plt

if __name__ == '__main__':
    stopwords_file_path = os.path.join('.', 'data', 'hinglish_stopwords.txt')
else:
    stopwords_file_path = os.path.join('.', 'NLP', 'data', 'hinglish_stopwords.txt')


class WordCloudGenerate:
    text: str
    stopwords: List[str] = []
    # max_words: int max_words
    mask: np.ndarray = None

    def __init__(self, text, mask_image_path=None):
        self.text = text
        self.mask_image_path = mask_image_path
        self.add_stopwords()
        self.wordcloud_obj = self.get_wordcloud()
        if mask_image_path:
            self.set_colors()

    def add_stopwords(self, lang='hinglish'):
        if lang == 'hinglish':
            with open(stopwords_file_path, 'r') as f:
                words = f.read().strip().split('\n')
            self.stopwords += words
        self.stopwords += STOPWORDS

    def get_mask_image(self):
        if self.mask_image_path:
            mask = np.array(Image.open(self.mask_image_path))
            return mask
        return None

    def get_wordcloud(self):
        wc = WordCloud(background_color='white', width=1980, height=1080, mask=self.get_mask_image(), stopwords=set(self.stopwords))
        wc.generate(self.text)
        return wc

    def set_colors(self):
        if not self.mask_image_path:
            raise ValueError(f'file path is not valid {self.mask_image_path}')
        if not os.path.exists(self.mask_image_path):
            raise FileNotFoundError(f'{self.mask_image_path} file path does not exist.')
        mask = self.get_mask_image()
        image_colors = ImageColorGenerator(mask)
        self.wordcloud_obj.recolor(color_func=image_colors)

    def save_wordcloud(self, directory=None, file_name=None):
        file_name = 'wc_'+(str(int(time.time())) + '.png') if not file_name else file_name
        directory = os.getcwd() if not directory else directory
        save_path = os.path.join(directory, file_name)
        self.wordcloud_obj.to_file(save_path)
        print(f'File saved in {save_path}')

    def show_wordcloud(self):
        plt.figure(figsize=[7, 7])
        plt.imshow(self.wordcloud_obj,  interpolation="bilinear")
        plt.axis('off')
        plt.show()
