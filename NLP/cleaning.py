import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from typing import List
import os
import uuid


class WordCloudGenerate:
    text: str
    stopwords: List[str] = []
    # max_words: int max_words
    mask: np.ndarray = None

    def __init__(self, text):
        self.text = text
        self.add_stopwords()

    def add_text(self, text):
        self.text += text

    def add_stopwords(self, lang='hinglish'):
        if lang == 'hinglish':
            path = os.path.join('.', 'NLP', 'data', 'hinglish_stopwords.txt')
            with open(path, 'r') as f:
                words = f.read().strip().split('\n')
            self.stopwords += words
        self.stopwords += STOPWORDS

    def set_mask_image(self, img_path):
        self.image_path = img_path
        if self.image_path:
            self.mask = np.array(Image.open(self.image_path))

    def save_wordcloud(self, filepath, stream=False):
        wc = WordCloud(background_color='white', width=1980, height=1080, mask=self.mask, stopwords=self.stopwords)
        wc.generate(self.text)
        wc.to_file(filepath if filepath else (str(uuid.uuid4()) + '.png'))
