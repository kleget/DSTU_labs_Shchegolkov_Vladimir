# Lab2

Минимальная реализация 5 заданий.

## Структура

- `server/` — веб-приложение с сервлетами и html-формами.
- `client_task3/AuthClientFx.java` — JavaFX клиент для задания 3 (GET/POST к `/auth`).
- `client_task5/CurrencyClientFx.java` — JavaFX клиент для задания 5 (таблица + график по `/currency`).

## Что где

- Задание 1: `/auth` + `index.html`
- Задание 2: `/session-info` + `session.html`
- Задание 3: `AuthServlet` поддерживает GET и POST + `client_task3`
- Задание 4: `/currency` + `currency.html`
- Задание 5: `client_task5` (использует `/currency?format=csv`; в формулировке задания 5, вероятно, опечатка про ссылку на задание 3)

## Сборка сервера

```bash
cd sem4/java/lab2/server
mvn clean package
```

Далее `target/lab2-server-1.0.0.war` развернуть в Tomcat (контекст `/lab2`).

## Jakarta (Servlet API)

В проекте уже прописана зависимость `jakarta.servlet-api` в `server/pom.xml` (`scope=provided`).

- Если Maven установлен, зависимость подтянется автоматически при сборке.
- Если Maven не установлен, для подсветки/компиляции в IDE можно добавить в classpath `jakarta.servlet-api*.jar` из `TOMCAT_HOME/lib`.

## Запуск JavaFX клиентов

Компиляция/запуск как обычных JavaFX классов с `--module-path` и модулями:

- `javafx.controls`
- `javafx.graphics`

Если используешь JDK 21 + JavaFX SDK:

```bash
javac --module-path "C:\soft\javafx-sdk-21.0.10\lib" --add-modules javafx.controls,javafx.graphics AuthClientFx.java
java  --module-path "C:\soft\javafx-sdk-21.0.10\lib" --add-modules javafx.controls,javafx.graphics AuthClientFx
```

Аналогично для `CurrencyClientFx.java`.
