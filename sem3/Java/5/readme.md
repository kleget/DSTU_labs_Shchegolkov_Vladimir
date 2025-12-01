# Запуск проекта (если вы уже в `sem3/Java/5`)

1) Установите JDK (например, `C:\Program Files\Java\jdk-25`) и убедитесь, что можете вызвать `javac`/`java`.
2) Скомпилируйте оба пакета в текущую папку:
   ```pwsh
   javac -d . mypart\*.java friendpart\*.java
   ```
   Если `javac` не в PATH, используйте полный путь, например:
   ```pwsh
   "C:\Program Files\Java\jdk-25\bin\javac.exe" -d . mypart\*.java friendpart\*.java
   ```
3) Для корректной кириллицы в выводе (опционально):
   ```pwsh
   chcp 65001 > $null
   ```
4) Запустите демонстрацию:
   ```pwsh
   java -cp . friendpart.Lab5Main
   ```
   Или с полным путём к `java.exe`, если не в PATH:
   ```pwsh
   "C:\Program Files\Java\jdk-25\bin\java.exe" -cp . friendpart.Lab5Main
   ```

Все команды выполняются из каталога `sem3/Java/5`. При необходимости поменяйте путь к JDK на свой.***
