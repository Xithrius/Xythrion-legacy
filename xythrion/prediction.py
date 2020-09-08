import logging
import re
from pathlib import Path
from typing import List

import numpy as np
import tensorflow as tf
import twitter
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

log = logging.getLogger(__name__)
tf.get_logger().setLevel(3)  # Set logging to "error"

MAX_LENGTH = 60


class Model:

    def __init__(self, twitter_api: twitter.api.Api) -> None:
        self.twitter_api = twitter_api

        embeddings_index = dict()

        with open(str(Path.cwd() / 'xythrion' / 'resources' / 'TrumpLearning' / 'glove.6B.100d.txt')) as f:
            for line in f:
                values = line.split()
                embeddings_index[values[0]] = np.asarray(values[1:], dtype="float32")

        self.t = Tokenizer()
        self.t.fit_on_texts(embeddings_index.keys())

    def run_model(self, tweet: str) -> List[int]:
        status_id = re.search(r'\d{19}', tweet)
        tweet_content = self.twitter_api.GetStatus(int(status_id.group(0)))
        tweet_content = tweet_content.text

        encoded_contents = self.t.texts_to_sequences([tweet_content])
        padded_contents = pad_sequences(encoded_contents, maxlen=MAX_LENGTH, padding="post")
        model = keras.models.load_model(
            str(Path.cwd() / 'xythrion' / 'resources' / 'TrumpLearning' / 'model'))

        lst = model.predict(np.reshape(padded_contents, (1, MAX_LENGTH)))
        return [int(x) for x in lst[0]]
