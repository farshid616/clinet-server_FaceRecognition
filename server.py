import communication
import recognition
import json
import numpy
import cv2
import base64

SOURCE_IP = '127.0.0.1'
SOURCE_PORT = 5005
DESTINATION_IP = ''
DESTINATION_PORT = 5006
connection = communication.Communication(SOURCE_IP, DESTINATION_IP, SOURCE_PORT, DESTINATION_PORT)
connection.bind_socket()
haar_file_path = 'haarcascade_frontalface_default.xml'
face_recognition = recognition.Recognition(haar_file_path)


def deserialize_learn_packet(packet):
    images = []
    num = int(packet.get('data').get('number_of_images'))
    i = 0
    while i < num:
        im = packet.get('data').get('image'+str(i))
        image_str = base64.b64decode(im)
        image_array = numpy.fromstring(image_str, dtype=numpy.uint8)
        org_image = cv2.imdecode(image_array, 0)
        images.append(org_image)
        i += 1
    person = packet.get('data').get('person_name')
    database = packet.get('data').get('db_name')
    info = packet.get('data').get('info')
    face_recognition.learn_person(database, person, info, images)


def deserialize_recognition_packet(packet, destination_address):
    images = []
    im = packet.get('data').get('image0')
    image_str = base64.b64decode(im)
    image_array = numpy.fromstring(image_str, dtype=numpy.uint8)
    org_image = cv2.imdecode(image_array, 0)
    images.append(org_image)
    database = packet.get('data').get('db_name')
    recognize, info = face_recognition.recognize_person(database, images)
    connection.send_packet_to(recognize+" "+info, destination_address[0], DESTINATION_PORT)

while True:
    data, address = connection.receive_packet(35000)
    converted = json.loads(data)
    if converted.get('data').get('type') == "learn":
        deserialize_learn_packet(converted)
    elif converted.get('data').get('type') == "recognize":
        deserialize_recognition_packet(converted, address)




