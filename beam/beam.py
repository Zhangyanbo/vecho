"""
Author: Yanbo Zhang
Date: Dec 27, 2023 EST

Description:
    Beam is a simple vector database that supports vector insertion, deletion, update and query.
    It stores (vector, id) pairs and supports query.
"""
import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Union


def _check_id_type(id: Union[str, List[str]]):
    # make sure id is str or list of str
    if isinstance(id, str):
        pass
    elif isinstance(id, list):
        for i in id:
            if not isinstance(i, str):
                raise ValueError("ID must be str or list of str")
    else:
        raise ValueError("ID must be str or list of str")


class Beam:
    def __init__(self, dim, method='cosine'):
        self.dim = dim
        self.vector = None
        self.ids = []

        assert method in ['cosine']
        self.method = method

    def _check_dim(self, vector):
        if vector.shape[-1] != self.dim:
            raise ValueError("Vector dimension mismatch")

    def _similarity(self, vec):
        if self.method == 'cosine':
            return np.dot(self.vector, vec) / (np.linalg.norm(self.vector, axis=1) * np.linalg.norm(vec))

    def _delete(self, id: str):
        _check_id_type(id)
        if not id in self.ids:
            raise ValueError("ID not found")

        idx = self.ids.index(id)
        self.vector = np.delete(self.vector, idx, axis=0)
        self.ids.remove(id)

    def insert(self, id: str, vector: Union[np.ndarray, List[float]]):
        _check_id_type(id)
        self._check_dim(vector)
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)

        if not id in self.ids:
            self.ids.append(id)
        else:
            raise ValueError("ID already exists")

        if self.vector is None:
            self.vector = vector.reshape(1, -1)
        else:
            self.vector = np.append(self.vector, vector.reshape(1, -1), axis=0)

    def delete(self, id: Union[str, List[str]]):
        _check_id_type(id)
        if isinstance(id, str):
            self._delete(id)
        elif isinstance(id, list):
            for i in id:
                self._delete(i)
        else:
            raise ValueError("ID must be str or list of str")

    def update(self, id: str, vector: Union[np.ndarray, List[float]]):
        _check_id_type(id)
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)
        self._check_dim(vector)

        if not id in self.ids:
            raise ValueError("ID not found")

        idx = self.ids.index(id)
        self.vector[idx] = vector

    def query(self, vector: Union[np.ndarray, List[float]], k: int=1):
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)

        self._check_dim(vector)

        if self.vector is None:
            return None

        sim = self._similarity(vector)
        idx = np.argsort(sim)[::-1][:k]
        return [self.ids[i] for i in idx], sim[idx]
