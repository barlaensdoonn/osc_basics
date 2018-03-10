#!/usr/local/bin/python3
# basic osc server example with osc4py3
# 3/1/18
# updated 3/9/18

from osc4py3.as_allthreads import *
from osc4py3 import oscmethod as oscm


class OSCServer:
    '''
    defaults to all open interfaces (0.0.0.0) on port 5555

    use handler='flex' for variable data in the message.
    use handler='static' if data is fixed, or you want to add type or length checking
    '''

    def __init__(self, handler='flex', host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
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

        self.handler = self.handlers[handler]['handler']
        self.arg_scheme = self.handlers[handler]['arg_scheme']
        self._initialize()

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

    def _initialize(self):
        '''
        osc_method() binds handler function to an address, here all subaddresses of /test/
        adding OSCARG_ADDRESS to argscheme sends address in message so server can see it
        '''

        osc_startup()
        osc_udp_server(self.host, self.port, 'server')
        osc_method('/test/*', self.handler, argscheme=oscm.OSCARG_ADDRESS + self.arg_scheme)

    def serve(self):
        '''
        a method like this that calls osc_process()
        is only needed when using osc4py3.as_eventloop
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


if __name__ == '__main__':
    try:
        # if use osc4py3.as_allthreads, server runs in the background
        # no need to call server.serve() in an event loop
        server = OSCServer()
    except KeyboardInterrupt:
        print('...user interrupt received, exiting...')
