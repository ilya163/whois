Инструкция по установке

1. Заходим в командную строку и переходим в дирректорию где установим проект.
2. Вводим команду:                https://github.com/ilya163/whois.git
3. Создаём виртульное окружение:  cd whois && python venv env
4. Активируем ВО:                 env\Scripts\activate
5. Устанавливаем зависимости      pip install -r whois\requirements.txt
6. Запускаем скрипт     
          


Инструкция по скрипту:

1. Для запуска требуется добавить АПИ ключ в файл конфигурации. Путь domain/settings.py
2. Загрузить в файл resource.csv список доменов.
3. запустить скрипт main.py