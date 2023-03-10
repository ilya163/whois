from .Domains import *
from .Requests import *

class CollectorRequests:
    ''' Управляющий класс доменов '''

    def __init__(self, path_file_with_domains=None, setting_save_to_file=None):
        self.save_result = None
        self.list_domains = self.get_file_domains(path_file_with_domains)
        self.setting_save_to_file = setting_save_to_file
        self.driver_chrome = Requests.init_driver_chrome()  #chrome Driver

    def run_async_worker(self, async_worker):
        ''' Запускаем ассинхронный воркер для каждого домена '''
        if not self.setting_save_to_file:
            return logger.warning(f"Не задан параметр для сохранения SAVE_FILES ")
        if not APIKEY:
            return logger.warning(f"Не задан ключ подключения к АПИ")
        if not async_worker:
            return logger.warning(f"Не передана ассинхронная функция")

        for num, name_domain in enumerate(self.list_domains, start=1):
            ''' Перебираем список доменов и запускам таски '''
            try:
                logger.info(f"Запуск {num} {name_domain}")
                instance = Domains(name_domain, self.setting_save_to_file, self.driver_chrome)  # Create new instance domain
                async_run = async_worker(instance)         # create coroutine | Вывел корутину в файл main.py для удобства
                result = asyncio.run(async_run)            # run async task { 1,2,3 .. N }

                if not result:
                    logger.warning(f"Результаты по {name_domain} пустые")
                    continue
                instance.save(result)
            #     logger.info(f"Завершение сессии для {name_domain}")
            except Exception as err:
                logger.error(f"Воркер {name_domain} отработал некорректно {str(err)}")
        self.finally_process()

    @staticmethod
    def get_file_domains(path):
        ''' Инициируем файл с доменами'''
        if not os.path.exists(path):
            raise logger.error("Не найден путь к файлу с доменами")
        results = []
        try:
            with open(path, "r", encoding="utf-8") as f_domains:
                for i in f_domains:
                    if len(i) > 3:
                        results.append(i.strip())
        except Exception as err:
            logger.error("Ошибка при считывании файла: " + str(err))
        return results


    def finally_process(self):
        try:
            if "excel" in self.setting_save_to_file:
                SaveExcel.finally_xls()
            if self.driver_chrome:
                self.driver_chrome.quit()
        except Exception as err:
            logger.error(f"Ошибка на завершающей функции скрипта {str(err)}")
    def __repr__(self):
        return self

    def __str__(self):
        return str(self.__class__)
