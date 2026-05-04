<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%!
    private String esc(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
%>
<%
    String message = (String) request.getAttribute("message");
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Вход</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 32px; max-width: 520px; }
        label { display: block; margin: 12px 0; }
        input { width: 100%; box-sizing: border-box; padding: 6px; }
        .message { font-weight: bold; }
    </style>
</head>
<body>
<h1>Вход в JPA-версию</h1>
<p><a href="<%= request.getContextPath() %>/">На главную</a></p>
<% if (message != null && !message.isBlank()) { %>
    <p class="message"><%= esc(message) %></p>
<% } %>
<form method="post" action="<%= request.getContextPath() %>/login">
    <label>Логин:
        <input name="login" required value="user">
    </label>
    <label>Пароль:
        <input name="password" type="password" required value="user">
    </label>
    <button type="submit">Войти</button>
</form>
<p>Администратор: <code>admin/admin</code>. Пользователь: <code>user/user</code>.</p>
</body>
</html>
