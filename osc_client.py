#!/usr/local/bin/python3
# basic osc client example with osc4py3
# 3/1/18
# updated 3/15/18

from socket import gaierror
from osc4py3.as_allthreads import *
from osc4py3 import oscbuildparse as oscbp


class OSCClient:

    def __init__(self, host='raspberrypi.local', port=5555, name='test_client', address='/test'):
        self.name = name
        self.address = address
        self.host = host
        self.port = port
        self._initialize()

    def _initialize(self):
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
