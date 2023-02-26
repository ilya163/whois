from .Domains import *

class CollectorRequests:
    ''' Управляющий класс доменов '''

    def __init__(self, file=None, **params):
        self.params = params
        self.save = None
        if not file:
            raise "Задайте файл для запуска"
        else:
            self.file = Domains.get_file_domains(file)


    def run_async_worker(self, async_worker):
        ''' Запускаем ассинхронный воркер для каждого домена '''
        for domain in self.file:
            try:
                logger.info(f"Запуск {domain}")
                instance = Domains(domain, **self.params)  # Create new instanse domain
                async_run = async_worker(instance)         # formed async function
                result = asyncio.run(async_run)            # run async task { 1,2,3 .. N }
                if self.save:
                    instance.save(self.save, result)
                logger.info(f"Успешное завершение для {domain}")
            except Exception as err:
                logger.error(f"Воркер {domain} отработал некорректно {str(err)}")



    def __repr__(self):
        return self

    def __str__(self):
        return str(self.__class__)
