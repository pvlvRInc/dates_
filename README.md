# dates_
https://thawing-stream-00101.herokuapp.com/
1. Создание пользователя: https://thawing-stream-00101.herokuapp.com/api/clients/create
2. Получить токен можно здесь (POST запрос, в body должны быть username и password): https://thawing-stream-00101.herokuapp.com/api/obtain_token
3. Водяной знак добавляется в функции date/models/add_watermark
4. Оценка пользователей доступна только авторизированным пользователям:https://thawing-stream-00101.herokuapp.com/api/clients/create/api/clients/{id}/match
      Аутентификация посредством токена. Headers: {Authorization: Token <токен_пользователя>}
      В body добавляется поле check со значениями 'L'(Like) или 'D'(Dislike). Моделb обновляются только при check = 'L' 
      Исключаются как суперпользователи, так и авторизованный
5. Фильтрация сделана с использованием следующих полей:
    first_name, (startwith)
    last_name, (startwith)
    gender, (значения 'M' и 'F')
    distance_min,
    distance_max,
    На фильтрацию надо 4 sql запроса (аутентификация, получение авторизованного пользователя, всех ползователей, исключение по фильтрации)
    Весь процесс реализован в классе date/filters/UserFilter

6. Суперпользователь:
    username: admin password: 1
