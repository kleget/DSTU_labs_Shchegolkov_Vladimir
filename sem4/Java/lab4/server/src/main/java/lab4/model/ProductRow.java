package lab4.model;

import java.math.BigDecimal;

public class ProductRow {
    private final int id;
    private final String name;
    private final String categoryName;
    private final String manufacturerName;
    private final String warehouseName;
    private final String warehouseAddress;
    private final BigDecimal price;
    private final int quantity;

    public ProductRow(int id, String name, String categoryName, String manufacturerName,
                      String warehouseName, String warehouseAddress, BigDecimal price, int quantity) {
        this.id = id;
        this.name = name;
        this.categoryName = categoryName;
        this.manufacturerName = manufacturerName;
        this.warehouseName = warehouseName;
        this.warehouseAddress = warehouseAddress;
        this.price = price;
        this.quantity = quantity;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getCategoryName() {
        return categoryName;
    }

    public String getManufacturerName() {
        return manufacturerName;
    }

    public String getWarehouseName() {
        return warehouseName;
    }

    public String getWarehouseAddress() {
        return warehouseAddress;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }
}
