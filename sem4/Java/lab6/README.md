# Лабораторная 6: Jakarta REST

Работа сделана по файлу `sem4/java/all_labs/lab6.pdf`.

Тема: REST, HTTP-команды, представления ресурсов, Jakarta REST (JAX-RS), JSON и Client API.

## Быстрый запуск

Из корня репозитория одной командой:

```powershell
.\sem4\java\lab6\run.ps1
```

Открыть в браузере:

```text
http://localhost:8086/lab6/
```

Если порт `8086` занят:

```powershell
.\sem4\java\lab6\run.ps1 8090
```

Остановить сервер: `Ctrl+C` в терминале.

## Что реализовано

### Задания 1-2

Создан RESTful-сервис добавления пользователя:

```text
POST /lab6/api/users
Content-Type: application/x-www-form-urlencoded
```

Пользователь хранит:

- имя;
- фамилию;
- e-mail;
- пароль.

Проверка через web-форму:

```text
http://localhost:8086/lab6/users-post.html
```

Форма использует ровно обычный HTML:

```html
<form method="POST" enctype="application/x-www-form-urlencoded">
```

### Задания 3-4

Созданы RESTful-сервисы получения пользователей:

```text
GET /lab6/api/users
GET /lab6/api/users/search?email=ivan@example.com
GET /lab6/api/users/{email}
```

Проверка через GET-форму:

```text
http://localhost:8086/lab6/users-get.html
```

### Задания 5-6

Созданы RESTful-сервисы изменения и удаления пользователя по e-mail:

```text
PUT    /lab6/api/users/{email}
DELETE /lab6/api/users/{email}
```

Проверка выполняется через `curl.exe`, примеры ниже.

### Задания 7-8

Создан JSON REST API для соревнований:

```text
GET    /lab6/api/competitions
GET    /lab6/api/competitions/{id}
POST   /lab6/api/competitions
PUT    /lab6/api/competitions/{id}
DELETE /lab6/api/competitions/{id}
```

Дополнительно есть операции над вложенной информацией:

```text
POST   /lab6/api/competitions/{id}/stages
PUT    /lab6/api/competitions/{id}/stages/{stageId}
DELETE /lab6/api/competitions/{id}/stages/{stageId}

POST   /lab6/api/competitions/{id}/participants
PUT    /lab6/api/competitions/{id}/participants/{participantId}
DELETE /lab6/api/competitions/{id}/participants/{participantId}
```

В соревновании хранятся:

- название;
- дата и время проведения;
- организаторы;
- дополнительная информация;
- этапы с временем проведения;
- участники и их результаты.

Все данные в запросах и ответах этого API передаются как JSON.

### Задание 9

Создано простое web-приложение для соревнований:

```text
http://localhost:8086/lab6/app?role=admin
http://localhost:8086/lab6/app?role=participant
http://localhost:8086/lab6/app?role=spectator
```

Роли:

- администратор задает тему соревнования, расписание и результаты;
- участник регистрируется и отправляет результат этапа;
- зритель без регистрации смотрит расписание и результаты.

Важно: web-часть не ходит в хранилище напрямую. Сервлеты `AdminServlet`, `ParticipantServlet` и `AppServlet` обращаются к REST API через `CompetitionApiClient`, который использует `jakarta.ws.rs.client.ClientBuilder`, `WebTarget` и `Entity`.

## Структура проекта

```text
sem4/java/lab6/
+-- README.md
+-- run.ps1
+-- server/
    +-- pom.xml
    +-- src/main/java/lab6/
    |   +-- client/CompetitionApiClient.java
    |   +-- model/
    |   +-- rest/
    |   +-- store/
    |   +-- web/
    +-- src/main/webapp/
        +-- index.html
        +-- users-post.html
        +-- users-get.html
        +-- resources/css/styles.css
        +-- WEB-INF/web.xml
```

## Как работает

`RestApplication` задает REST-приложение и регистрирует ресурсы:

```java
@ApplicationPath("/api")
public class RestApplication extends ResourceConfig
```

`UserResource` обрабатывает запросы к `/api/users`. Для POST из HTML-формы используется `@FormParam`, потому что браузер отправляет данные как `application/x-www-form-urlencoded`.

`CompetitionResource` обрабатывает запросы к `/api/competitions`. Для JSON указаны:

```java
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
```

Хранилище учебное, в памяти процесса сервера:

- `UserStore` хранит пользователей по e-mail;
- `CompetitionStore` хранит соревнования, этапы и участников.

После перезапуска сервера данные возвращаются к тестовым значениям. Это нормально для этой лабораторной, потому что в задании не требуется база данных.

## Проверка через curl

В PowerShell для JSON-команд ниже используется `--%`. Это останавливает разбор кавычек PowerShell и позволяет `curl.exe` отправить JSON без поломки.

Список пользователей:

```powershell
curl.exe "http://localhost:8086/lab6/api/users"
```

Добавить пользователя JSON-запросом:

```powershell
curl.exe --% -X POST http://localhost:8086/lab6/api/users -H "Content-Type: application/json" -d "{\"firstName\":\"Петр\",\"lastName\":\"Сидоров\",\"email\":\"petr@example.com\",\"password\":\"12345\"}"
```

Найти пользователя:

```powershell
curl.exe "http://localhost:8086/lab6/api/users/search?email=petr@example.com"
```

Изменить пользователя:

```powershell
curl.exe --% -X PUT http://localhost:8086/lab6/api/users/petr@example.com -H "Content-Type: application/json" -d "{\"firstName\":\"Петр\",\"lastName\":\"Иванов\",\"password\":\"newpass\"}"
```

Удалить пользователя:

```powershell
curl.exe -X DELETE "http://localhost:8086/lab6/api/users/petr@example.com"
```

Список соревнований:

```powershell
curl.exe "http://localhost:8086/lab6/api/competitions"
```

Добавить соревнование:

```powershell
curl.exe --% -X POST http://localhost:8086/lab6/api/competitions -H "Content-Type: application/json" -d "{\"title\":\"Осенний турнир\",\"eventDateTime\":\"2026-10-10T12:00\",\"organizers\":\"ДГТУ\",\"extraInfo\":\"Спонсоры уточняются\",\"stages\":[{\"name\":\"Открытие\",\"startsAt\":\"2026-10-10T12:00\"},{\"name\":\"Финал\",\"startsAt\":\"2026-10-10T16:00\"}],\"participants\":[]}"
```

Добавить этап к соревнованию `1`:

```powershell
curl.exe --% -X POST http://localhost:8086/lab6/api/competitions/1/stages -H "Content-Type: application/json" -d "{\"name\":\"Награждение\",\"startsAt\":\"2026-05-20T17:00\"}"
```

Добавить участника и результат:

```powershell
curl.exe --% -X POST http://localhost:8086/lab6/api/competitions/1/participants -H "Content-Type: application/json" -d "{\"name\":\"Мария Орлова\",\"email\":\"maria@example.com\",\"stageName\":\"Финал\",\"result\":\"92 балла\"}"
```

Изменить соревнование `1`:

```powershell
curl.exe --% -X PUT http://localhost:8086/lab6/api/competitions/1 -H "Content-Type: application/json" -d "{\"title\":\"Весенняя олимпиада\",\"eventDateTime\":\"2026-05-20T10:30\",\"organizers\":\"Кафедра ПОВТиАС\",\"extraInfo\":\"Финальная версия расписания\",\"stages\":[{\"id\":1,\"name\":\"Открытие\",\"startsAt\":\"2026-05-20T10:30\"}],\"participants\":[]}"
```

Удалить соревнование:

```powershell
curl.exe -X DELETE "http://localhost:8086/lab6/api/competitions/1"
```

## Необходимая теория

REST - архитектурный стиль, где сервер предоставляет ресурсы по URI, а клиент работает с ними через HTTP-команды.

CRUD через HTTP:

- `GET` получает ресурс;
- `POST` создает ресурс;
- `PUT` изменяет ресурс;
- `DELETE` удаляет ресурс.

URI - адрес ресурса. Например, `/api/users/ivan@example.com` указывает на конкретного пользователя.

Представление ресурса - формат тела запроса или ответа: `text/plain`, `text/html`, `application/json`, `text/xml` и т.д.

`Content-Type` задает тип данных, которые клиент отправляет серверу.

`Accept` задает тип данных, которые клиент хочет получить от сервера.

Jakarta REST (JAX-RS) - API Jakarta EE для создания RESTful web-сервисов на обычных Java-классах.

Основные аннотации:

- `@ApplicationPath` задает общий путь REST-приложения;
- `@Path` задает путь ресурса или метода;
- `@GET`, `@POST`, `@PUT`, `@DELETE` связывают метод Java с HTTP-командой;
- `@Produces` задает формат ответа;
- `@Consumes` задает формат входного тела запроса;
- `@PathParam` получает параметр из пути, например `{id}`;
- `@QueryParam` получает параметр из строки запроса, например `?email=...`;
- `@FormParam` получает поле HTML-формы `application/x-www-form-urlencoded`.

Client API - часть Jakarta REST для выполнения HTTP-запросов из Java-кода. Основные классы:

- `ClientBuilder` создает клиент;
- `Client` выполняет запросы;
- `WebTarget` хранит URI ресурса;
- `Entity` заворачивает тело POST/PUT-запроса.

## Как защитить

1. Запустить `.\sem4\java\lab6\run.ps1` и открыть `http://localhost:8086/lab6/`.
2. Открыть `users-post.html`, добавить пользователя и показать, что POST-форма отправляет `application/x-www-form-urlencoded` на `/api/users`.
3. Открыть `users-get.html`, найти пользователя по e-mail и открыть список всех пользователей.
4. Показать `UserResource.java`: `@POST`, `@GET`, `@PUT`, `@DELETE`, `@FormParam`, `@QueryParam`, `@PathParam`.
5. Выполнить пару команд `curl.exe`: список пользователей, добавление, изменение, удаление.
6. Открыть `/api/competitions` и показать JSON с соревнованием, этапами и участниками.
7. Через `curl.exe` добавить этап или участника к `/api/competitions/1`.
8. Открыть `app?role=admin`, изменить название/расписание и внести результат.
9. Открыть `app?role=participant`, зарегистрировать участника и отправить результат.
10. Открыть `app?role=spectator` и показать, что зритель видит расписание и результаты без регистрации.
11. Показать `CompetitionApiClient.java` и объяснить, что web-часть обращается к REST-сервисам через Client API, а не напрямую к хранилищу.

Короткие ответы на контрольные вопросы:

- Jakarta REST (JAX-RS) - технология для RESTful сервисов в Java.
- Путь задается через `@ApplicationPath` и `@Path`.
- `@Path` можно ставить на класс ресурса и на метод.
- Получение - `GET`, добавление - `POST`, изменение - `PUT`, удаление - `DELETE`.
- `@Produces` описывает формат ответа.
- `@Consumes` описывает формат входных данных.
- `Content-Type` задает тип тела запроса.
- `Accept` задает желаемый тип ответа.
- Параметр запроса - значение после `?`, например `?email=...`.
- Значение query-параметра получает `@QueryParam`.
- Значение из пути получает `@PathParam`.
- Параметризованный путь задается как `@Path("/{id}")`.
- Подресурс задается дополнительным `@Path` на методе, например `/{id}/stages`.
- Client API нужен, чтобы Java-программа сама отправляла HTTP-запросы к REST-сервису.
