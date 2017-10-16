"""
The MIT License (MIT)

Copyright (c) 2017 Marvin Teichmann
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import numpy as np
import scipy as scp

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)


from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral
from pydensecrf.utils import create_pairwise_gaussian

import pydensecrf.pairwise as pair


def exp_and_normalize(features):
    """
    Aka "softmax" in deep learning literature
    """
    exp_features = np.exp(features - np.max(features, axis=0))
    normalize_features = exp_features / np.sum(exp_features, axis=0)

    return normalize_features


def potts_comp_update(weight, features):
    return -weight * features


class DenseCRF():
    """This is a reimplementation of DenseCRF (almost) entirely in python.
    """
    def __init__(self, npixels, nclasses):
        super(DenseCRF, self).__init__()
        self.npixels = npixels
        self.nclasses = nclasses
        self.kernel_list = []
        self.compact_list = []
        self.potential_list = []

    def set_unary_energy(self, unary):
        self.unary = unary
        return

    def add_pairwise_energy(self, feats, compat=3,
                            kernel_type=None, normalization=None):

        kernel = pair.DenseKernel(feats)
        self.kernel_list.append(kernel)
        self.compact_list.append(pair.PottsComp(compat))
        self.potential_list.append(pair.PairwisePotentials(feats, compat))

    def inference(self, num_iter=5):
        prediction = exp_and_normalize(-self.unary)
        for i in range(num_iter):
            tmp1 = -self.unary
            for kernel, comp in zip(self.kernel_list, self.compact_list):
                tmp2 = kernel.apply(prediction)

                tmp2 = comp.apply(tmp2)
                tmp1 = tmp1 - tmp2
            prediction = exp_and_normalize(tmp1)

        # assert(False)
        # todo: write wrapper for matrixXF
        # no copy required.
        return prediction

    def start_inference():
        pass

    def step_inference():
        pass