class Serializer:

    def __init__(self, response):
        self.response = response
        self.results = {}

    def parse_key(self, keys):
        return list(map(lambda x: x.strip(), keys.split(">")))

    def get(self, keys, default=""):
        keys = self.parse_key(keys)
        value = self.validate(self.response, keys, default)
        if not value:
            return default
        return value

    def validate(self, massive, keys, default=""):
        ''' Валидация поступающих данных с АПИ '''
        if keys[0].isdigit():
            keys[0] = int(keys[0])
        try:
            if len(keys) == 1:
                return massive[keys[0]]
            else:
                if massive[keys[0]]:
                    return self.validate(massive[keys[0]], keys[1:])
        except:
            return default

    def __str__(self):
        return str(self.results)

    def __setitem__(self, key, value):
        self.results[key] = value
        return value

    def __getitem__(self, item):
        return self.results[item]


