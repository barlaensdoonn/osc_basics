#!/usr/local/bin/python3
# basic osc server example with osc4py3
# 3/1/18
# updated 3/20/18

from utility import load_config
from osc4py3.as_allthreads import *
from osc4py3 import oscmethod as oscm


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
                'arg_scheme': oscm.OSCARG_DATA
            },
            'static': {
                'handler': self._static_handler,
                'arg_scheme': oscm.OSCARG_DATAUNPACK
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
        osc_method(self.address, self.handler, argscheme=oscm.OSCARG_ADDRESS + self.arg_scheme)

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


if __name__ == '__main__':
    try:
        print('initiating server...')

        # if we use osc4py3.as_allthreads, server runs in the background after
        # it's constructed. no need to call server.serve() in an event loop
        server = OSCServer()
    except KeyboardInterrupt:
        print('...user interrupt received, exiting...')
        server.shutdown()
