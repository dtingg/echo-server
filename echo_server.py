"""
Echo Server
"""

import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    """
    Creates a server socket.
    """

    # set an address for our server
    address = ('127.0.0.1', 10000)

    # Instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Set socket option to prevent "port is already used" error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind sock to the address and begin to listen for incoming connections
    sock.bind(address)
    sock.listen(1)

    try:
        # Outer loop controls the creation of new connection sockets.
        # Server will handle each incoming connection one at a time.
        while True:
            print('\nwaiting for a connection', file=log_buffer)

            # Make a new socket when a client connects
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # Inner loop will receive messages sent by client in buffers.
                # When a complete message has been received, the loop will exit.

                while True:
                    # Receive 16 bytes of data from the client.
                    buffer_size = 16

                    # Set timeout in case no data is received
                    conn.settimeout(1)

                    # Store the data you receive as "data"
                    data = conn.recv(buffer_size)

                    # Check if you have received the end of the message
                    if not data:
                        break

                    print('received "{0}"'.format(data.decode('utf8')))

                    # Send the data you received back to the client
                    conn.sendall(data)

                    # Log the data using a print statement
                    print('sent "{0}"'.format(data.decode('utf8')))

            except socket.timeout:
                pass

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

            finally:
                # Close the socket you created when a client connected
                conn.close()

                print('echo complete, client connection closed', file=log_buffer)

    except KeyboardInterrupt:
        # Use the python KeyboardInterrupt (Control + C) exception as a signal
        # to close the server socket and exit from the sever function
        sock.close()

        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
