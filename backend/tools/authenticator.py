from dotenv import load_dotenv
import os
import hashlib



class Authenticator:
    __HASH_KEY = None

    def __init__(self):
        load_dotenv()
        self.__HASH_KEY = os.getenv("HASH_KEY")
    
    def hash_it(self, data):
        return hashlib.sha256(self.__HASH_KEY.encode("utf-8") + data.encode("utf-8")).hexdigest()
    
    