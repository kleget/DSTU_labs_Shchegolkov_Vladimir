# Lab2

## Быстрый запуск одной командой

Из корня репозитория:

```bash
mvn -f sem4/java/lab2/server/pom.xml jetty:run
```

Или из папки лабораторной:

```powershell
cd sem4/java/lab2
.\run.ps1
```

Для другого порта через скрипт:

```powershell
.\run.ps1 8081
```

После запуска открыть:

```text
http://localhost:8080/lab2/
```

Остановить сервер можно сочетанием `Ctrl+C` в терминале.

Важно: команда запуска не возвращает prompt, пока сервер работает. Это нормально. Нужно оставить терминал открытым и перейти в браузере по адресу выше.

Если в консоли Jetty пишет предупреждения вида `The XML schema ... could not be found`, это не ошибка запуска. Сервер все равно работает, если ниже есть строки `Started ... /lab2` или страница открывается в браузере.

Если порт `8080` занят, можно выбрать другой порт:

```bash
mvn -f sem4/java/lab2/server/pom.xml -Djetty.http.port=8081 jetty:run
```

Если сервер запущен не на `8080`, в JavaFX-клиентах нужно заменить порт в поле URL.

## Быстрый запуск JavaFX-клиентов

Сначала запусти сервер lab2. Затем в новом терминале:

```powershell
cd sem4/java/lab2/client_task3
.\run.ps1
```

Это задание 3, клиент авторизации.

Для задания 5:

```powershell
cd sem4/java/lab2/client_task5
.\run.ps1
```

Скрипты запускают JavaFX с флагом `-Dprism.order=sw`. Он включает программный рендеринг и помогает, если окно JavaFX отображается как битая картинка, плитки, артефакты или случайные текстуры.

Если JavaFX SDK установлен в другом месте:

```powershell
.\run.ps1 "D:\path\to\javafx-sdk\lib"
```

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
