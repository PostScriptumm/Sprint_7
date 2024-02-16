import random
import string


class Helper:

    # метод генерации данных
    @staticmethod
    def generate_random_string(length):
        return ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(length)))
