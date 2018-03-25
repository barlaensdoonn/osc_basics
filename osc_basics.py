#!/usr/local/bin/python3
# basic osc client example with osc4py3
# 3/1/18
# updated 3/24/18

import os
import yaml
from socket import gaierror
from osc4py3.as_allthreads import *
from osc4py3 import oscmethod as osm
from osc4py3 import oscbuildparse as oscbp


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


class OSCClient:
    '''specify host, port, client name, and OSC message address in osc_config.yaml'''

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
            print("can't find host {}, unable to create client {}".format(self.host, self.name))
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


class OSCServer:
    '''
    config file defaults to all open interfaces (0.0.0.0) on port 5555
    and listens to clients sending messages addressed to any subset of '/rfider'

    use handler='flex' for variable data in the message [default]
    use handler='static' if data is fixed, or you want to add type or length checking
    '''

    def __init__(self, handler='flex'):
        self.handlers = {
            'flex': {
                'handler': self._flex_handler,
                'arg_scheme': osm.OSCARG_DATA
            },
            'static': {
                'handler': self._static_handler,
                'arg_scheme': osm.OSCARG_DATAUNPACK
            }
        }

        self.config = load_config('server')
        self.host = self.config['host']
        self.port = self.config['port']
        self.address = self.config['address']
        self.handler = self.handlers[handler]['handler']
        self.arg_scheme = self.handlers[handler]['arg_scheme']
        self._initialize_osc()

    def _flex_handler(self, address, *args):
        '''
        use this for variable # of arguments in osc message's data.
        need to speciy argscheme OSCARG_DATA in osc_method() call
        '''

        print('received message addressed to: {}'.format(address))
        print('message: {}'.format(*args))

    def _static_handler(self, address, x, y, z):
        '''
        use this for static # of arguments in osc message's data.
        corresponds to argscheme OSCARG_DATAUNPACK, which is the default
        '''

        print('received message addressed to: {}'.format(address))
        print('message: {}, {}, {}'.format(x, y, z))

    def _initialize_osc(self):
        '''
        osc_method() binds handler function to an address, which is specified in osc_config.yaml
        adding OSCARG_ADDRESS to argscheme sends address in message so server can see it
        '''

        osc_startup()
        osc_udp_server(self.host, self.port, 'server')
        osc_method(self.address, self.handler, argscheme=osm.OSCARG_ADDRESS + self.arg_scheme)

    def serve(self):
        '''
        a method like this that calls osc_process() is only needed when using osc4py3.as_eventloop
        '''
        running = True

        try:
            while running:
                osc_process()
        except KeyboardInterrupt:
            print('shutting down server')
            osc_terminate()
            running = False
            raise

    def shutdown(self):
        '''call this when terminating a script that uses OSCServer with osc4py3.as_allthreads'''
        osc_terminate()
