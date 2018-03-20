#!/usr/local/bin/python3
# basic osc client example with osc4py3
# 3/1/18
# updated 3/20/18

from socket import gaierror
from .utility import load_config
from osc4py3.as_allthreads import *
from osc4py3 import oscbuildparse as oscbp


class OSCClient:
    '''specify host, port, client name, and osc message address in osc_config.yaml'''

    def __init__(self):
        self.config = load_config('client')
        self.host = self.config['host']
        self.port = self.config['port']
        self.name = self.config['name']
        self.address = self.config['address']
        self._initialize_osc()

    def _initialize_osc(self):
        osc_startup()

        try:
            osc_udp_client(self.host, self.port, self.name)
        except gaierror:
            print("can't find host {self.host}, unable to create client {self.name}".format(self.host, self.name))
            print('reraising exception')
            raise

    def _construct_msg(self, data):
        '''
        None as second argument to OSCMessage means datatypes are autodetected.
        replace None with explicit datatype formatted as ',sif' for string, integer, float.
        data should be a list or tuple of args to pass in message like ['string', 42, 4.2]
        '''

        return oscbp.OSCMessage(self.address, None, data)

    def send(self, data):
        msg = self._construct_msg(data)
        osc_send(msg, self.name)

    def shutdown(self):
        '''call this when terminating a script that uses OSCClient'''
        osc_terminate()
