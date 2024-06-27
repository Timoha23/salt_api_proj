### Установка salt-api

1. Проверить установлен ли salt-api: ```salt-api --version```
2. Если не установлен, то установить согласно выбранному методу начальной установки (pip, apt, ...)
3. Основная библиотека Python при использовании salt-api в данном проекте: CherryPy


### Настройка конфигурации для salt-api

1. Через HTTP:
  - Добавляем [внешнюю аутентификацию](https://docs.saltproject.io/en/latest/topics/eauth/index.html#external-authentication-system-configuration) в конфиг-файл:
  
  ```
  # /etc/salt/master

  external_auth:
    file:
      ^filename: /etc/salt/creds.txt
      <username>:
        - .*
        - '@runners'
        - '@wheels'
  ```

  ```
  # /etc/salt/creds.txt
  
  <username>:<password>
  ```

  Здесь мы используем аутентификацию через [файл](https://docs.saltproject.io/en/latest/ref/auth/all/salt.auth.file.html), так как для использования "pam" процесс мастера должен быть запущен от root юзера. К тому же способ прост в реализации.

  - Добавляем конфигурацию для [CherryPy](https://docs.saltproject.io/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#a-rest-api-for-salt) в конфиг-файл:

  ```
  # /etc/salt/master

  rest_cherrypy:
    port: <port>
    host: <ip>
    disable_ssl: True
  ```

  - Добавляем список [клиентов](https://docs.saltproject.io/en/latest/ref/configuration/master.html#netapi-enable-clients) salt, к которым будет доступ через api в конфиг-файл:

  ```
  # /etc/salt/master

  netapi_enable_clients:
    - .*  # all
    # - local
    # - local_async
    # - local_batch
    # - local_subset
    # - runner
    # - runner_async
    # - ssh
    # - wheel
    # - wheel_async
  ```


2. Через HTTPS:

    Проделываем то же самое, что и через HTTP, но:

  - Генерируем ssl сертификат средствами salt:

  ```
  salt-call --local tls.create_self_signed_cert cacert_path=<path_to_certs>
  ```

  - Добавляем конфигурацию для CherryPy в конфиг-файл:

  ```
  # /etc/salt/master

  rest_cherrypy:
    port: <port>
    ssl_crt: <path_to_certs>/localhost.crt
    ssl_key: <path_to_certs>/localhost.key
  ```
	

### Запуск salt-api сервиса

```
systemctl start salt-api
```



### Проверка работоспособности REST API (salt-api):

- Через curl:

  - Получаем токен:
  
  ```
  curl -sSk http://<ip>:<port>/login \
    -H 'Accept: application/json' \
    -d username=<username> \
    -d password=<password> \
    -d eauth=file
  ```

  - Отправляем запрос на исполнение модуля

  ```
  curl -sSk http://<ip>:<port> \
    -H 'Accept: application/json' \
    -H 'X-Auth-Token: <token>'
    -d client=local
    -d tgt='*'
    -d fun=test.ping
  ```

- Через [Python](requests_examples.py)



### Полезные источники

1. [PYTHON CLIENT API](https://docs.saltproject.io/en/latest/ref/clients/index.html)
2. [EXTERNAL AUTHENTICATION SYSTEM](https://docs.saltproject.io/en/latest/topics/eauth/index.html)
3. [REST CHERRYPY](https://docs.saltproject.io/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)
4. [NETAPI SALT CLIENTS](https://docs.saltproject.io/en/latest/ref/configuration/master.html#netapi-enable-clients)
5. [SALT AUTH TYPES](https://docs.saltproject.io/en/latest/ref/auth/all/index.html)
