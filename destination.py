__author__ = 'Zakaria'

import node
import asyncio
import pickle
import os


#destination or sink or last node of the network
class Destination(node.Node):

    def run_server(self):
        loop = asyncio.get_event_loop()
        job = asyncio.start_server(self.handle_echo, self.host, self.port, loop=loop)
        server = loop.run_until_complete(job)

        print('MSG: Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    @asyncio.coroutine
    def handle_echo(self, reader, writer):
        data = yield from reader.read()
        packet = pickle.loads(data)
        sender = writer.get_extra_info('peername')
        if packet:
            self.save_and_execute(packet, sender)
        writer.close()

    def save_and_execute(self, packet, sender):
        print(packet)
        with open('outfile.py', 'w+') as f:
            f.writelines(packet)
        os.system("python outfile.py")




#Test run
if __name__ == '__main__':
    dest = Destination('127.0.0.1', 12345)
    dest.run_server()
