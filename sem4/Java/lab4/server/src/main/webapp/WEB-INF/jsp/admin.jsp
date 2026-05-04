<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List,lab4.model.AppUser,lab4.config.DbConfig,lab4.auth.SessionUser" %>
<%!
    private String esc(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;");
    }
    private String selected(String actual, String expected) {
        return expected.equals(actual) ? "selected" : "";
    }
%>
<%
    List<AppUser> users = (List<AppUser>) request.getAttribute("users");
    DbConfig dbConfig = (DbConfig) request.getAttribute("config");
    SessionUser user = (SessionUser) request.getAttribute("user");
    String message = (String) request.getAttribute("message");
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Администрирование</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 24px; max-width: 1100px; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0; }
        th, td { border: 1px solid #bbb; padding: 6px; }
        th { background: #f3eadb; }
        input, select { box-sizing: border-box; max-width: 100%; padding: 4px; }
        .message { font-weight: bold; }
        .panel { border: 1px solid #ccc; padding: 12px; margin: 16px 0; }
    </style>
</head>
<body>
<h1>Администрирование</h1>
<p>
    <a href="<%= request.getContextPath() %>/">На главную</a> |
    <a href="<%= request.getContextPath() %>/jpa/books">Книги JPA</a> |
    <a href="<%= request.getContextPath() %>/jpa/products">Товары JPA</a> |
    <a href="<%= request.getContextPath() %>/logout">Выйти</a>
</p>
<p>Текущий пользователь: <b><%= user == null ? "" : esc(user.getLogin()) %></b></p>
<% if (message != null && !message.isBlank()) { %>
    <p class="message"><%= esc(message) %></p>
<% } %>

<div class="panel">
    <h2>Пользователи</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Логин</th>
            <th>Новый пароль</th>
            <th>Роль</th>
            <th>Действия</th>
        </tr>
        <% if (users != null) {
            for (AppUser appUser : users) { %>
            <tr>
                <form method="post" action="<%= request.getContextPath() %>/admin">
                    <td>
                        <%= appUser.getId() %>
                        <input type="hidden" name="id" value="<%= appUser.getId() %>">
                    </td>
                    <td><input name="login" required value="<%= esc(appUser.getLogin()) %>"></td>
                    <td><input name="password" type="password" placeholder="не менять"></td>
                    <td>
                        <select name="role">
                            <option value="USER" <%= selected(appUser.getRole(), "USER") %>>USER</option>
                            <option value="ADMIN" <%= selected(appUser.getRole(), "ADMIN") %>>ADMIN</option>
                        </select>
                    </td>
                    <td>
                        <button name="action" value="saveUser" type="submit">Сохранить</button>
                        <button name="action" value="deleteUser" type="submit">Удалить</button>
                    </td>
                </form>
            </tr>
        <%  }
        } %>
    </table>

    <h3>Добавить пользователя</h3>
    <form method="post" action="<%= request.getContextPath() %>/admin">
        <input type="hidden" name="action" value="saveUser">
        <p><label>Логин: <input name="login" required placeholder="student"></label></p>
        <p><label>Пароль: <input name="password" type="password" required></label></p>
        <p><label>Роль:
            <select name="role">
                <option value="USER">USER</option>
                <option value="ADMIN">ADMIN</option>
            </select>
        </label></p>
        <button type="submit">Добавить</button>
    </form>
</div>

<div class="panel">
    <h2>Настройки соединения с БД</h2>
    <form method="post" action="<%= request.getContextPath() %>/admin">
        <input type="hidden" name="action" value="saveConfig">
        <p><label>JDBC driver:
            <input name="driver" required value="<%= dbConfig == null ? "" : esc(dbConfig.getDriver()) %>">
        </label></p>
        <p><label>URL:
            <input name="url" required style="width: 520px" value="<%= dbConfig == null ? "" : esc(dbConfig.getUrl()) %>">
        </label></p>
        <p><label>User:
            <input name="dbUser" value="<%= dbConfig == null ? "" : esc(dbConfig.getUser()) %>">
        </label></p>
        <p><label>Password:
            <input name="dbPassword" type="password" value="<%= dbConfig == null ? "" : esc(dbConfig.getPassword()) %>">
        </label></p>
        <button type="submit">Сохранить настройки</button>
    </form>
</div>
</body>
</html>
