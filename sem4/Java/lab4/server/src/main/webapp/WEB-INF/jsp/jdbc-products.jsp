<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List,lab4.model.ProductRow" %>
<%!
    private String esc(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;");
    }
%>
<%
    List<ProductRow> products = (List<ProductRow>) request.getAttribute("products");
    String filter = (String) request.getAttribute("filter");
    String message = (String) request.getAttribute("message");
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>JDBC товары</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 24px; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0; }
        th, td { border: 1px solid #bbb; padding: 6px; vertical-align: top; }
        th { background: #e8eef7; }
        input, select { box-sizing: border-box; max-width: 100%; }
        .row-form input { width: 130px; }
        .message { font-weight: bold; }
        .panel { border: 1px solid #ccc; padding: 12px; margin: 16px 0; }
    </style>
</head>
<body>
<h1>Товары: JDBC</h1>
<p>
    <a href="<%= request.getContextPath() %>/">На главную</a> |
    <a href="<%= request.getContextPath() %>/login">JPA-версия с входом</a>
</p>

<% if (message != null && !message.isBlank()) { %>
    <p class="message"><%= esc(message) %></p>
<% } %>

<form method="get" action="<%= request.getContextPath() %>/jdbc/products">
    <label>Фильтр:
        <input name="filter" value="<%= esc(filter) %>" placeholder="товар, категория, склад">
    </label>
    <button type="submit">Показать</button>
    <a href="<%= request.getContextPath() %>/jdbc/products">Сбросить</a>
</form>

<h2>Список товаров</h2>
<table>
    <tr>
        <th>ID</th>
        <th>Название</th>
        <th>Категория</th>
        <th>Производитель</th>
        <th>Склад</th>
        <th>Адрес</th>
        <th>Цена</th>
        <th>Кол-во</th>
        <th>Действия</th>
    </tr>
    <% if (products != null) {
        for (ProductRow product : products) { %>
        <tr>
            <form class="row-form" method="post" action="<%= request.getContextPath() %>/jdbc/products">
                <td>
                    <%= product.getId() %>
                    <input type="hidden" name="id" value="<%= product.getId() %>">
                </td>
                <td><input name="name" required value="<%= esc(product.getName()) %>"></td>
                <td><input name="category" required value="<%= esc(product.getCategoryName()) %>"></td>
                <td><input name="manufacturer" required value="<%= esc(product.getManufacturerName()) %>"></td>
                <td><input name="warehouse" required value="<%= esc(product.getWarehouseName()) %>"></td>
                <td><input name="warehouseAddress" value="<%= esc(product.getWarehouseAddress()) %>"></td>
                <td><input name="price" type="number" min="0" step="0.01" required value="<%= product.getPrice() %>"></td>
                <td><input name="quantity" type="number" min="0" step="1" required value="<%= product.getQuantity() %>"></td>
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
    <h2>Добавить товар</h2>
    <form method="post" action="<%= request.getContextPath() %>/jdbc/products">
        <input type="hidden" name="action" value="add">
        <p><label>Название: <input name="name" required placeholder="Клавиатура K120"></label></p>
        <p><label>Категория: <input name="category" required placeholder="Компьютерная периферия"></label></p>
        <p><label>Производитель: <input name="manufacturer" required placeholder="Logitech"></label></p>
        <p><label>Склад: <input name="warehouse" required placeholder="Основной склад"></label></p>
        <p><label>Адрес склада: <input name="warehouseAddress" placeholder="Ростов-на-Дону"></label></p>
        <p><label>Цена: <input name="price" type="number" min="0" step="0.01" required value="1000.00"></label></p>
        <p><label>Количество: <input name="quantity" type="number" min="0" step="1" required value="1"></label></p>
        <button type="submit">Добавить</button>
    </form>
</div>
</body>
</html>
