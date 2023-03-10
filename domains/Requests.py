from .my_additional import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Requests:
    ''' Статичный класс для работы с запросами '''

    @staticmethod
    def generate_url(request):
        ''' Генерация URL из данных '''
        url = ''
        url += request.pop("main_url")
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
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Api отработал со статусом {resp.status}: {await resp.text()}")
        except asyncio.TimeoutError:
            logger.error(f"Вызвано исключение из-за ожидания АПИ {name}")
        except:
            logger.error(f"Ошибка при отправке API запроса {url}: {await resp.text()}")

    @staticmethod
    def init_driver_chrome():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # silently run Chrome
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        driver = webdriver.Chrome(chrome_options=options)
        return driver
    @staticmethod
    async def run_selenium(driver, url, domain_name):
        try:
            # driver.implicitly_wait(10)
            driver.get(url)
            await asyncio.sleep(2)

            driver.set_window_size(800, 600)
            FOLDER_DOMAIN = os.path.join(PATH_RESULTS_DIR, domain_name)
            if not os.path.exists(FOLDER_DOMAIN):
                os.mkdir(FOLDER_DOMAIN)
            driver.get_screenshot_as_file(FOLDER_DOMAIN + "/screenshot.png")

            if driver.execute_script("return document.readyState") == "complete":
                state = "Доступен"
            else:
                state = "Не доступен"
            return {"state": state}
        except WebDriverException:
            logger.error("Вызвано исключение в Selenium из-за незащищенного соединения к сайту")
            return {"state": "Не доступен"}
        except Exception as err:
            logger.error(f"Вызвано исключение в Selenium АПИ {domain_name} : {str(err)}")
            return {"state": "Не доступен"}


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

