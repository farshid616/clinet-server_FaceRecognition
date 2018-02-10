import communication
import recognition
import threading
# import logging

haar_file_path = 'haarcascade_frontalface_default.xml'
SOURCE_IP = '127.0.0.1'
SOURCE_PORT = 5006
DESTINATION_IP = '127.0.0.1'
DESTINATION_PORT = 5005
connection = communication.Communication(SOURCE_IP, DESTINATION_IP, SOURCE_PORT, DESTINATION_PORT)
connection.bind_socket()
face_recognition = recognition.Recognition(haar_file_path)
# log = logging.getLogger(__name__)
# LOG_FILENAME = 'local.log'
# logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s %(message)s')


def receive():
    while True:
        data, address = connection.receive_packet()
        print(data, address)


command = ""
t = threading.Thread(target=receive)
t.daemon = True
t.start()

while command != 'q':
    command = input("Please enter l for Learning, r for Recognizing and q for Quiting ")
    if command == 'l':
        person = input("please enter person name")
        db = input("please enter database name")
        info = input("please enter person info")
        (images, labels) = ([], [])
        images, labels = face_recognition.take_pictures(2)
        msg = face_recognition.create_learn_msg(db, person, info, images)
        connection.send_packet(msg)
    elif command == 'r':
        db = input("please enter db name")
        (images, labels) = ([], [])
        images, labels = face_recognition.take_pictures(1)
        msg = face_recognition.create_recognize_msg(db, images)
        connection.send_packet(msg)
        # log.debug("send recognize packet ")
        # logging.warning("send recognize packet ")
    elif command == 'q':
        break
