from domains.my_additional import *
class Writer:
    def __init__(self, name_domain, result):
        self.name_domain = name_domain
        self.result = self.prepare_data(result)

    def prepare_data(self, response):
        try:
            result = {}
            for name in response:
                for block in response[name]:
                    if block in result and type(result[block]) == dict:
                        result[block].update(response[name][block])
                    elif block in result and type(result[block]) == list and len(response[name][block]) > 0:
                        result[block].append(response[name][block][0])
                    else:
                        result[block] = response[name][block]
            return result
        except:
            logger.error("Ошибка при преподготовки данных на запись")
    def run_writer(self, obj_writer):
        obj_writer.save(self.name_domain, self.result)
