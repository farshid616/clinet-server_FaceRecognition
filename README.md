# clinet-server_FaceRecognition
A python implementation of client server face recognition based on LBPH algorithm.
In this implementation we used openCV face recognition tools and you can change the main algorithm easily to eigenFace or FisherFace.
in client side we take pictures and send it to server for store in a database or using for recognition. client and server communication is a UDP connection and all of the messages are sending in JSON format.

## Details
Project consists of four file:
* client.py
* server.py
* communication.py
* recognition.py

In `communication.py` we have everything that need to send or receive a packet to `client` or `server` and in `recognition.py` we implement all of the function to store or restore a face in a database.

## Requarements:
* Python 2.x - 3.x
* OpenCV 2.x - 3.x

Python Library:
* cv2
* os
* numpy
* threading
* json
* base64
* socket

## How to run
You can run `client.py` and `server.py` localy in a single machine or in seprate machines.
```
    $ python client.py
    $ python server.py
```
## Author
Farshid Abdollahi
