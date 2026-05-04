<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List,lab4.model.Book,lab4.auth.SessionUser" %>
<%!
    private String esc(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;");
    }
%>
<%
    List<Book> books = (List<Book>) request.getAttribute("books");
    String genre = (String) request.getAttribute("genre");
    String message = (String) request.getAttribute("message");
    SessionUser user = (SessionUser) request.getAttribute("user");
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>JPA библиотека</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 24px; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0; }
        th, td { border: 1px solid #bbb; padding: 6px; vertical-align: top; }
        th { background: #e8f4ea; }
        input { box-sizing: border-box; max-width: 100%; }
        .row-form input { width: 170px; }
        .message { font-weight: bold; }
        .panel { border: 1px solid #ccc; padding: 12px; margin: 16px 0; }
    </style>
</head>
<body>
<h1>Библиотека книг: JPA + роли</h1>
<p>
    <a href="<%= request.getContextPath() %>/">На главную</a> |
    <a href="<%= request.getContextPath() %>/jdbc/products">Товары JDBC</a> |
    <a href="<%= request.getContextPath() %>/jpa/products">Товары JPA</a> |
    <% if (user != null && user.isAdmin()) { %><a href="<%= request.getContextPath() %>/admin">Админка</a> |<% } %>
    <a href="<%= request.getContextPath() %>/logout">Выйти</a>
</p>
<p>Текущий пользователь: <b><%= user == null ? "" : esc(user.getLogin()) %></b>,
    роль: <b><%= user == null ? "" : esc(user.getRole()) %></b></p>

<% if (message != null && !message.isBlank()) { %>
    <p class="message"><%= esc(message) %></p>
<% } %>

<form method="get" action="<%= request.getContextPath() %>/jpa/books">
    <label>Жанр:
        <input name="genre" value="<%= esc(genre) %>" placeholder="программирование">
    </label>
    <button type="submit">Показать</button>
    <a href="<%= request.getContextPath() %>/jpa/books">Сбросить</a>
</form>

<h2>Список книг</h2>
<table>
    <tr>
        <th>ID</th>
        <th>Название</th>
        <th>Автор</th>
        <th>Жанр</th>
        <th>Год</th>
        <th>Действия</th>
    </tr>
    <% if (books != null) {
        for (Book book : books) { %>
        <tr>
            <form class="row-form" method="post" action="<%= request.getContextPath() %>/jpa/books">
                <td>
                    <%= book.getId() %>
                    <input type="hidden" name="id" value="<%= book.getId() %>">
                </td>
                <td><input name="title" required value="<%= esc(book.getTitle()) %>"></td>
                <td><input name="author" required value="<%= esc(book.getAuthor()) %>"></td>
                <td><input name="genre" required value="<%= esc(book.getGenre()) %>"></td>
                <td><input name="year" type="number" min="1500" max="2099" required value="<%= book.getYear() %>"></td>
                <td>
                    <button name="action" value="update" type="submit">Изменить</button>
                    <button name="action" value="delete" type="submit">Удалить</button>
                </td>
            </form>
        </tr>
    <%  }
    } %>
</table>

<div class="panel">
    <h2>Добавить книгу</h2>
    <form method="post" action="<%= request.getContextPath() %>/jpa/books">
        <input type="hidden" name="action" value="add">
        <p><label>Название: <input name="title" required placeholder="Java и базы данных"></label></p>
        <p><label>Автор: <input name="author" required placeholder="Иванов"></label></p>
        <p><label>Жанр: <input name="genre" required placeholder="программирование"></label></p>
        <p><label>Год: <input name="year" type="number" min="1500" max="2099" required value="2024"></label></p>
        <button type="submit">Добавить</button>
    </form>
</div>
</body>
</html>
