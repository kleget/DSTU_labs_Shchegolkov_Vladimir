package lab4.jdbc;

import jakarta.servlet.ServletContext;
import lab4.config.DbConfig;
import lab4.config.DbConfigStore;
import lab4.model.ProductForm;
import lab4.model.ProductRow;
import lab4.model.ProductValidator;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class JdbcProductRepository {
    private final DbConfig config;

    public JdbcProductRepository(ServletContext context) throws Exception {
        this.config = new DbConfigStore(context).load();
        DatabaseBootstrap.ensure(config);
    }

    public List<ProductRow> list(String filter) throws SQLException {
        String value = "%" + safe(filter).toLowerCase() + "%";
        String sql = """
                SELECT p.id, p.name, c.name AS category_name, m.name AS manufacturer_name,
                       w.name AS warehouse_name, w.address AS warehouse_address, p.price, p.quantity
                FROM product p
                JOIN category c ON c.id = p.category_id
                JOIN manufacturer m ON m.id = p.manufacturer_id
                JOIN warehouse w ON w.id = p.warehouse_id
                WHERE ? = '%%'
                   OR LOWER(p.name) LIKE ?
                   OR LOWER(c.name) LIKE ?
                   OR LOWER(m.name) LIKE ?
                   OR LOWER(w.name) LIKE ?
                ORDER BY p.id
                """;
        try (Connection connection = connection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, value);
            statement.setString(2, value);
            statement.setString(3, value);
            statement.setString(4, value);
            statement.setString(5, value);
            try (ResultSet resultSet = statement.executeQuery()) {
                List<ProductRow> products = new ArrayList<>();
                while (resultSet.next()) {
                    products.add(row(resultSet));
                }
                return products;
            }
        }
    }

    public void add(ProductForm form) throws SQLException {
        ProductValidator.validate(form);
        String sql = """
                INSERT INTO product(name, category_id, manufacturer_id, warehouse_id, price, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
                """;
        try (Connection connection = connection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            fillStatement(connection, statement, form);
            statement.executeUpdate();
        }
    }

    public void update(ProductForm form) throws SQLException {
        ProductValidator.validate(form);
        if (form.getId() == null) {
            throw new IllegalArgumentException("Для изменения нужен ID товара.");
        }
        String sql = """
                UPDATE product
                SET name = ?, category_id = ?, manufacturer_id = ?, warehouse_id = ?, price = ?, quantity = ?
                WHERE id = ?
                """;
        try (Connection connection = connection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            fillStatement(connection, statement, form);
            statement.setInt(7, form.getId());
            statement.executeUpdate();
        }
    }

    public void delete(int id) throws SQLException {
        try (Connection connection = connection();
             PreparedStatement statement = connection.prepareStatement("DELETE FROM product WHERE id = ?")) {
            statement.setInt(1, id);
            statement.executeUpdate();
        }
    }

    private void fillStatement(Connection connection, PreparedStatement statement, ProductForm form) throws SQLException {
        int categoryId = DatabaseBootstrap.findOrCreateName(connection, "category", form.getCategoryName());
        int manufacturerId = DatabaseBootstrap.findOrCreateName(connection, "manufacturer", form.getManufacturerName());
        int warehouseId = DatabaseBootstrap.findOrCreateWarehouse(connection, form.getWarehouseName(), form.getWarehouseAddress());
        statement.setString(1, form.getName());
        statement.setInt(2, categoryId);
        statement.setInt(3, manufacturerId);
        statement.setInt(4, warehouseId);
        statement.setBigDecimal(5, form.getPrice());
        statement.setInt(6, form.getQuantity());
    }

    private Connection connection() throws SQLException {
        return DriverManager.getConnection(config.getUrl(), config.getUser(), config.getPassword());
    }

    private static ProductRow row(ResultSet resultSet) throws SQLException {
        return new ProductRow(
                resultSet.getInt("id"),
                resultSet.getString("name"),
                resultSet.getString("category_name"),
                resultSet.getString("manufacturer_name"),
                resultSet.getString("warehouse_name"),
                resultSet.getString("warehouse_address"),
                resultSet.getBigDecimal("price"),
                resultSet.getInt("quantity")
        );
    }

    private static String safe(String text) {
        return text == null ? "" : text.trim();
    }
}
