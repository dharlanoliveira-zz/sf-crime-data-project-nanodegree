from zipfile import ZipFile
from kafka import KafkaProducer
import json
import time
import os


class ProducerServer(KafkaProducer):

    def __init__(self, input_file,zip_file, topic, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.zip_file = zip_file
        self.topic = topic

    def extract_zip_file(self):
        with ZipFile(self.zip_file, 'r') as zipObj:
            listOfFileNames = zipObj.namelist()
            for fileName in listOfFileNames:
                if fileName == self.input_file:
                    zipObj.extract(fileName, path=os.getcwd())

    def generate_data(self):
        self.extract_zip_file()
        with open(self.input_file) as f:
            all_file = json.load(f)
            for line in all_file:
                message = self.dict_to_binary(line)
                # TODO send the correct data
                self.send(self.topic, message)
                time.sleep(1)

    @staticmethod
    def dict_to_binary(json_dict):
        return json.dumps(json_dict).encode()
