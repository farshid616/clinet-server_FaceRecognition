import socket


class Communication:
    """
    This is communication class to create a udp connection between client and server and send or receive some packets
    """

    def __init__(self, source_ip, destination_ip, source_port, destination_port):
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packet(self, message):
        self.socket_obj.sendto(message, (self.destination_ip, self.destination_port))

    def send_packet_to(self, message, ip, port):
        self.socket_obj.sendto(message, (ip, port))

    def receive_packet(self, buffer=1024):
        data, address = self.socket_obj.recvfrom(buffer)
        return data, address

    def bind_socket(self):
        self.socket_obj.bind((self.source_ip, self.source_port))

