<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List,lab3.Book" %>
<%!
    private String esc(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
%>
<%
    List<Book> books = (List<Book>) request.getAttribute("books");
    String genre = (String) request.getAttribute("genre");
    String message = (String) request.getAttribute("message");
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Библиотека книг</title>
</head>
<body>
<h1>Библиотека книг</h1>
<p><a href="<%= request.getContextPath() %>/">На главную</a></p>

<% if (message != null && !message.isBlank()) { %>
    <p><b><%= esc(message) %></b></p>
<% } %>

<h2>Фильтр по жанру</h2>
<form action="<%= request.getContextPath() %>/library" method="get">
    <label>Жанр:
        <input name="genre" value="<%= esc(genre) %>" placeholder="программирование"
               pattern="[A-Za-zА-Яа-яЁё \-]{2,30}" title="2-30 символов: только буквы, пробел или дефис">
    </label>
    <button type="submit">Показать</button>
    <a href="<%= request.getContextPath() %>/library">Сбросить</a>
</form>

<h2>Список книг</h2>
<table border="1" cellpadding="6">
    <tr>
        <th>ID</th>
        <th>Название</th>
        <th>Автор</th>
        <th>Жанр</th>
        <th>Год</th>
    </tr>
    <% if (books != null) {
        for (Book book : books) { %>
        <tr>
            <td><%= esc(book.getId()) %></td>
            <td><%= esc(book.getTitle()) %></td>
            <td><%= esc(book.getAuthor()) %></td>
            <td><%= esc(book.getGenre()) %></td>
            <td><%= esc(book.getYear()) %></td>
        </tr>
    <%  }
    } %>
</table>

<h2>Добавить книгу</h2>
<form action="<%= request.getContextPath() %>/library" method="post">
    <input type="hidden" name="action" value="add">
    <p><label>Название: <input name="title" required maxlength="80"
                               pattern="[A-Za-zА-Яа-яЁё0-9 .,'&quot;«»:()!?\-]{1,80}"
                               title="1-80 символов: буквы, цифры, пробелы и простые знаки"></label></p>
    <p><label>Автор: <input name="author" required maxlength="60"
                            pattern="[A-Za-zА-Яа-яЁё .'\-]{2,60}"
                            title="2-60 символов: буквы, пробел, точка, апостроф или дефис"></label></p>
    <p><label>Жанр: <input name="genre" required placeholder="программирование" maxlength="30"
                           pattern="[A-Za-zА-Яа-яЁё \-]{2,30}"
                           title="2-30 символов: только буквы, пробел или дефис"></label></p>
    <p><label>Год: <input name="year" required pattern="(1[5-9][0-9]{2}|20[0-9]{2})"
                          title="Год числом от 1500 до 2099"></label></p>
    <button type="submit">Добавить</button>
</form>

<h2>Удалить книгу</h2>
<form action="<%= request.getContextPath() %>/library" method="post">
    <input type="hidden" name="action" value="delete">
    <p><label>ID книги: <input name="id" required></label></p>
    <button type="submit">Удалить</button>
</form>
</body>
</html>

