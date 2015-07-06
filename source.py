__author__ = 'Zakaria'
import node
import asyncio
import pickle


#source or first node of the network
class Source(node.Node):

    def send(self, message, receiver_host, receiver_port):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.tcp_echo_client(message, receiver_host, receiver_port, loop))
        # loop.close()

    @asyncio.coroutine
    def tcp_echo_client(self, message, receiver_host, receiver_port, loop):
        reader, writer = yield from asyncio.open_connection(receiver_host, receiver_port, loop=loop)

        writer.write(pickle.dumps(message))
        yield from writer.drain()

        print('----------------')
        writer.close()

###########################################################




#Test run
if __name__ == '__main__':
    src = Source('127.0.0.1', '12344')
    hst = '127.0.0.1'

    with open('infile.py') as f:
        msg = f.readlines()

    src.send(msg, '127.0.0.1', 12345)


