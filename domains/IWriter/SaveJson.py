from domains.my_additional import *


class SaveJson:

    @classmethod
    def save(cls, name_domain, response):
        try:
            for name in response:
                cls.save_domain(response[name], name_domain, name)
        except Exception as err:
            logger.error(f"Ошибка при запуске обработчика Json: {str(err)}")

    @staticmethod
    def save_domain(result, name_domain, filename):
        FOLDER_DOMAIN = os.path.join(PATH_RESULTS_DIR, name_domain)
        try:
            if not os.path.exists(FOLDER_DOMAIN):
                os.mkdir(FOLDER_DOMAIN)
            with open(os.path.join(FOLDER_DOMAIN, filename + '.json'), "a", encoding='utf-8') as file:
                json.dump(result, file, indent=3, ensure_ascii=False)
        except Exception as err:
            logger.error(f"Ошибка при записи в JSON файл: {str(err)}")
