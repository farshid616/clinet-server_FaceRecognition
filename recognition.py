import cv2
import base64
import json
import time
import os
import numpy


class Recognition:
    """
    This class contain everything required to detect, learn or recognize a face
    """
    db_path = "database/"
    name_list_path = "database/"

    def __init__(self, haar_cascade_file_path):
        self.haar_cascade_file_path = haar_cascade_file_path

    def take_pictures(self, number_of_pics):
        (images, labels) = ([], [])
        (width, height) = (130, 100)
        face_cascade = cv2.CascadeClassifier(self.haar_cascade_file_path)
        webcam = cv2.VideoCapture(0)
        count = 1
        while count < number_of_pics + 1:
            ret_val, im = webcam.read()
            time.sleep(1)
            if ret_val:
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    images.append(face_resize)
                    labels.append(count)
                count += 1
        webcam.release()
        cv2.destroyAllWindows()
        return images, labels

    @staticmethod
    def create_recognize_msg(db_name, images):
        retval, image = cv2.imencode('.png', images[0])
        json_string = {'data': {'type': "recognize", 'db_name': db_name, 'image0': base64.b64encode(image)}}
        return json.dumps(json_string)

    @staticmethod
    def create_learn_msg(db_name, person_name, info, images):
        json_string = {'data': {'type': "learn", 'db_name': db_name, 'person_name': person_name, 'info': info,
                                'number_of_images': len(images)}}
        i = 0
        for image in images:
            retval, im = cv2.imencode('.png', image)
            json_string['data']['image' + str(i)] = base64.b64encode(im)
            i += 1

        return json.dumps(json_string)

    def get_image_name(self, label, db_name):
        names_list = self.image_name_list(self.db_path)
        if db_name in names_list:
            fh = open(self.name_list_path + db_name + ".txt", "r")
            list_items = fh.readlines()
            if label >= 0:
                for item in list_items:
                    if int(item.split(":")[:-1][0]) == label:
                        return item.split(":")[1]
            else:
                return list_items[-1].split(":")[:-1][0]
        else:
            return 0

    def set_image_name(self, person_name, db_name, info):
        last_id = self.get_image_name(-1, db_name)
        fh = open(self.name_list_path + db_name + ".txt", "a")
        fh.write(str(int(last_id) + 1) + ":" + person_name + ":" + info)
        fh.write("\n")
        fh.close()
        return int(last_id) + 1

    def get_image_info(self, label, db_name):
        names_list = self.image_name_list(self.db_path)
        if db_name in names_list:
            fh = open(self.name_list_path + db_name + ".txt", "r")
            list_items = fh.readlines()
            if label >= 0:
                for item in list_items:
                    if int(item.split(":")[:-1][0]) == label:
                        return item.split(":")[2]
        else:
            return 0

    @staticmethod
    def db_list(db_path):
        names = []
        for filename in os.listdir(db_path):
            names.append(filename.split(".")[:-1][0])
        return names

    @staticmethod
    def image_name_list(path):
        names = []
        for filename in os.listdir(path):
            names.append(filename.split(".")[:-1][0])
        return names

    def learn_person(self, db_name, person_name, info, images):
        dbs = self.db_list('database/')
        label_list = [self.set_image_name(person_name, db_name, info), self.set_image_name(person_name, db_name, info)]
        (image, label) = [numpy.array(lists) for lists in [images, label_list]]
        if db_name in dbs:
            model = cv2.face.LBPHFaceRecognizer_create()  # 125 #110
            model.read(self.db_path + db_name + ".xml")
            model.update(image, label)
            model.write(self.db_path + db_name + ".xml")
        else:
            model = cv2.face.LBPHFaceRecognizer_create()  # 125 #110
            model.train(image, label)
            model.write(self.db_path + db_name + ".xml")

    def recognize_person(self, db_name, images):
        dbs = self. db_list('database/')
        if db_name in dbs:
            model = cv2.face.LBPHFaceRecognizer_create()  # 125 #110
            model.read(self.db_path + db_name + ".xml")
            for faces in images:
                prediction = model.predict(faces)
                if prediction[1] < 125:
                    rec = self.get_image_name(prediction[0], db_name)
                    info = self.get_image_info(prediction[0], db_name)
                    return rec, info
                else:
                    return "Unknown"
        else:
            return None
