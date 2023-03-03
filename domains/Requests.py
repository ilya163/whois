from .my_additional import *

class Requests:
    ''' Статичный класс для работы с запросами '''

    @staticmethod
    def generate_url(request):
        ''' Генерация URL из данных '''
        url = ''
        url += request.pop("url")
        temp = True
        for key, value in request.items():
            if value.count(' ') > 0:
                value = "'" + str(value) + "'"
            if temp:
                url += "?" + str(key) + "=" + str(value)
                temp = False
            else:
                url += "&" + str(key) + "=" + str(value)
        return str(url)

    @staticmethod
    async def run(url, name):
        ''' Запуска ассинхронного запроса '''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.json()
        except asyncio.TimeoutError:
            logger.error(f"Вызвано исключение из-за ожидания АПИ {name}")
        except:
            logger.error(f"Ошибка при отправке API запроса {url}: {await resp.text()}")



    # ================== Методы для тестирования =============

    @staticmethod
    async def run_test(url, name):
        ''' Запуска ассинхронного запроса '''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.json()
        except asyncio.TimeoutError:
            logger.error(f"Вызвано исключение из-за ожидания АПИ {name}")
        except:
            logger.error(f"Ошибка при отправке API запроса {url}: {await resp.text()}")

    @staticmethod
    async def read_api_test(domain, name):
        ''' Чтение данных из файлов для теста '''
        path = os.path.join(PATH_TESTING_DIR, domain, name)
        if os.path.exists(path):
            with open(path, "r") as file:
                return json.load(file)


    @staticmethod
    async def write_api_test(domain, name, answer):
        ''' Загрузка данных в файлы для теста '''
        if not os.path.exists(PATH_TESTING_DIR):
            os.mkdir(PATH_TESTING_DIR)
        path_folder = os.path.join(PATH_TESTING_DIR, domain)
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)
        path_file = os.path.join(path_folder, name)
        with open(path_file, "w") as file:
            json.dump(answer, file, indent=3, ensure_ascii=False)

