<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="lab3.GameBean" %>
<%!
    private String show(String s) {
        return s == null || s.isEmpty() ? "&nbsp;" : s;
    }
%>
<%
    GameBean game = (GameBean) request.getAttribute("game");
    String[] cells = game.getCells();
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Крестики-нолики</title>
</head>
<body>
<h1>Крестики-нолики 3x3</h1>
<p><a href="<%= request.getContextPath() %>/">На главную</a></p>
<p><b><%= game.getMessage() %></b></p>

<table border="1" cellpadding="18">
    <% for (int r = 0; r < 3; r++) { %>
    <tr>
        <% for (int c = 0; c < 3; c++) { %>
        <td align="center"><b><%= show(cells[r * 3 + c]) %></b></td>
        <% } %>
    </tr>
    <% } %>
</table>

<h2>Ваш ход</h2>
<form action="<%= request.getContextPath() %>/game" method="post">
    <p><label>Строка (1-3): <input name="row" type="number" min="1" max="3" required></label></p>
    <p><label>Столбец (1-3): <input name="col" type="number" min="1" max="3" required></label></p>
    <button type="submit" <%= game.isOver() ? "disabled" : "" %>>Сделать ход</button>
</form>

<form action="<%= request.getContextPath() %>/game" method="post">
    <input type="hidden" name="action" value="reset">
    <button type="submit">Новая игра</button>
</form>
</body>
</html>
