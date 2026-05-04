package lab4.model;

import java.math.BigDecimal;

public final class ProductValidator {
    private static final String TEXT_RE = "^[\\p{L}\\p{N} .,'\"()\\-]{2,120}$";

    private ProductValidator() {
    }

    public static void validate(ProductForm form) {
        requireText(form.getName(), "Название товара");
        requireText(form.getCategoryName(), "Категория");
        requireText(form.getManufacturerName(), "Производитель");
        requireText(form.getWarehouseName(), "Склад");
        if (form.getPrice() == null || form.getPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Цена должна быть неотрицательным числом.");
        }
        if (form.getQuantity() < 0) {
            throw new IllegalArgumentException("Количество должно быть неотрицательным числом.");
        }
    }

    private static void requireText(String value, String field) {
        if (value == null || !value.matches(TEXT_RE)) {
            throw new IllegalArgumentException(field + ": от 2 до 120 символов, буквы, цифры, пробелы и простые знаки.");
        }
    }
}
