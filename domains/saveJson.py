from .my_additional import *


class saveJson:
    def __init__(self, domain):
        self.domain = domain

    def run(self, response):
        try:
            result = {}
            for name in response:
                for block in response[name]:
                    if block in result and type(result[block]) == dict:
                        result[block].update(response[name][block])
                    elif block in result and type(result[block]) == list:
                        result[block].append(response[name][block][0])
                    else:
                        result[block] = response[name][block]

            for name in result:
                self.save(result[name], name)

            # logger.info("Данные в формате JSON успешно записаны")
        except Exception as err:
            logger.error(f"Ошибка при запуске обработчика Json: {str(err)}")

    def save(self, result, filename):
        FOLDER_DOMAIN = os.path.join(PATH_RESULTS_DIR, self.domain)
        try:
            if not os.path.exists(FOLDER_DOMAIN):
                os.mkdir(FOLDER_DOMAIN)
            with open(os.path.join(FOLDER_DOMAIN, filename + '.json'), "a", encoding='utf-8') as file:
                json.dump(result, file, indent=3, ensure_ascii=False)
        except Exception as err:
            logger.error(f"Ошибка при записи в JSON файл: {str(err)}")
