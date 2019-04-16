"""
Echo Chat Server
"""

import socket
import sys
import traceback
import select
import queue


def server(log_buffer=sys.stderr):
    """
    Creates a chat server socket.
    """

    # set an address for our server
    address = ('127.0.0.1', 10000)

    # Instantiate a TCP socket with IPv4 Addressing
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Make socket nonblocking
    server.setblocking(False)

    # Set socket option to prevent "port is already used" error
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind sock to the address
    server.bind(address)

    # Listen for 5 incoming connections
    server.listen(5)

    # Sockets for reading
    inputs = [server]

    # Sockets for writing
    outputs = []

    # Outgoing message queue
    messages = queue.Queue()

    while inputs:
        try:
            # Wait for at least one socket to be ready for processing
            # print("Waiting for the next event", file=log_buffer)

            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            for sock in readable:
                if sock is server:

                    # Can accept a connection
                    connection, client_address = sock.accept()
                    print("connection from {0}:{1}".format(*client_address), file=log_buffer)

                    # Make connection nonblocking
                    connection.setblocking(False)

                    # Add connection to inputs and outputs
                    inputs.append(connection)
                    outputs.append(connection)

                else:
                    data = sock.recv(1024)

                    if data:
                        try:
                            print('Received "{0}" from {1}'.format(data.decode("utf8"), sock.getpeername()), file=log_buffer)
                            messages.put(data)

                        # except socket.timeout:??
                        # pass

                        except Exception as e:
                            traceback.print_exc()
                            sys.exit(1)

            for sock in writable:
                try:
                    # Look for a message in the queue
                    msg = messages.get(False)

                    for sock in outputs:
                        sock.sendall(msg)
                        print('sent "{}" to {}'.format(msg.decode("utf8"), sock.getpeername()))

                except queue.Empty:
                    pass

                except Exception:
                    traceback.print_exc()
                    sys.exit(1)

            for sock in exceptional:
                print("exception condition on {}".format(sock.getpeername(), file=log_buffer))

                inputs.remove(sock)
                outputs.remove(sock)
                sock.close()

        except KeyboardInterrupt:
            # Use Control + C as a signal to close the server socket
            for sock in outputs:
                sock.close()

            server.close()

            print("Quitting Echo Chat Server", file=log_buffer)


if __name__ == "__main__":
    server()
    sys.exit(0)
