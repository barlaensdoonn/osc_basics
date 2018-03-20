#!/usr/local/bin/python3
# utilities for osc_basics repo
# 3/20/18
# updated 3/20/18

import os
import yaml


osc_config = 'osc_config.yaml'


def _get_basepath():
    return os.path.dirname(os.path.realpath(__file__))


def load_config(which):
    '''
    which should be either 'server' or 'client'
    '''
    conf_path = os.path.join(_get_basepath(), osc_config)

    with open(conf_path, 'r') as conf_file:
        osc_conf = yaml.safe_load(conf_file)

    return osc_conf[which]
