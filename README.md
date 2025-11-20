# Трекер привычек


### Локальный деплой
Шаги:
1. Запустить Docker приложение
2. Логин в Docker Hub (если необходим)
    * в cmd-консоле `docker login -u <docker hub username>`, потом ввести токен от Docker Hub
3. `docker compose -f docker-compose.local.yml up --build` - запустить контейнер с билдом из `docker-compose.local.yml` для локального деплоя
4. В браузере перейти на  `localhost`


### Деплой на сервер
В ДАННЫЙ МОМЕНТ деплой происходит при любом push и проект берется из ветки feature/6_deploy.
Адрес сервера: `158.160.206.209`

Шаги:
1. Сделать свои `.env` из `.env.samles`
2. Создать и настроить свой сервер (например на Яндекс Cloud)
   * в консоле сервера:
     * `sudo apt update`
     * `sudo apt upgrade`
     * скачать Docker по официальному туториалу https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
3. Настройка GitHub Secrets:
   * `SSH_USER` - юзер сервера
   * `SSH_KEY` - приватный SSH
   * `SERVER_IP` - публичный IP сервера
   * `ENV_FILE` - твой .env файл с данными
   * `DOCKER_HUB_USERNAME` и `DOCKER_HUB_ACCESS_TOKEN` - юзернейм и токен от Docker Hub
   * `DEPLOY_DIR` - директория для деплоя на сервере
   * `DOC_COMP_DEPLOY` - `docker-compose.deploy.yml` из корня проекта (так проще)
   * `NGINX_CONF` - `Dockerfiles/nginx/nginx.conf`
4. Также важно добавить пользователя `SSH_USER` в группу `docker` на сервере
   * `getent group docker` - проверить, есть ли группа `docker` (если нет никакого output, то создать - `sudo groupadd docker`)
   * `sudo usermod -aG docker <username>` - добавление <username> в группу
   * перезайти на сервер
   * еще раз `getent group docker` - проверка, должно быть что-то вроде `docker:x:999:<username>`

Можно пользоваться



### Отслеживания привычек
* интегрирование информирование через Telegram о создании, изменении и удалении привычки
* интегрирование информирование через Telegram о привычке за час до ее начала
* документирование через swagger/redoc