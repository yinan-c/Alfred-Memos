#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
The file_reader converts raw corpus to input.
"""

import os
import __future__
import io
import paddle
import paddle.fluid as fluid

def load_kv_dict(dict_path,
                 reverse=False,
                 delimiter="\t",
                 key_func=None,
                 value_func=None):
    """
    Load key-value dict from file
    """
    result_dict = {}
    for line in io.open(dict_path, "r", encoding='utf8'):
        terms = line.strip("\n").split(delimiter)
        if len(terms) != 2:
            continue
        if reverse:
            value, key = terms
        else:
            key, value = terms
        if key in result_dict:
            raise KeyError("key duplicated with [%s]" % (key))
        if key_func:
            key = key_func(key)
        if value_func:
            value = value_func(value)
        result_dict[key] = value
    return result_dict

class Dataset(object):
    """data reader"""
    def __init__(self):
        # read dict
        basepath = os.path.abspath(__file__)
        folder = os.path.dirname(basepath)
        word_dict_path = os.path.join(folder, "word.dic")
        label_dict_path = os.path.join(folder, "tag.dic")
        self.word2id_dict = load_kv_dict(
            word_dict_path, reverse=True, value_func=int)
        self.id2word_dict = load_kv_dict(word_dict_path)
        self.label2id_dict = load_kv_dict(
            label_dict_path, reverse=True, value_func=int)
        self.id2label_dict = load_kv_dict(label_dict_path)
    
    @property
    def vocab_size(self):
        """vocabulary size"""
        return max(self.word2id_dict.values()) + 1
    
    @property
    def num_labels(self):
        """num_labels"""
        return max(self.label2id_dict.values()) + 1

    def word_to_ids(self, words):
        """convert word to word index"""
        word_ids = []
        for word in words:
            if word not in self.word2id_dict:
                word = "OOV"
            word_id = self.word2id_dict[word]
            word_ids.append(word_id)
        return word_ids
   
    def label_to_ids(self, labels):
        """convert label to label index"""
        label_ids = []
        for label in labels:
            if label not in self.label2id_dict:
                label = "O"
            label_id = self.label2id_dict[label]
            label_ids.append(label_id)
        return label_ids

    def get_vars(self,str1):
        words = str1.strip()
        word_ids = self.word_to_ids(words)
        return word_ids
    
   
