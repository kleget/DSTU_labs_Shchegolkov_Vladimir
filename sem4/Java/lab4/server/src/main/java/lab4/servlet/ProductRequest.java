package lab4.servlet;

import jakarta.servlet.http.HttpServletRequest;
import lab4.model.ProductForm;

import java.math.BigDecimal;

final class ProductRequest {
    private ProductRequest() {
    }

    static ProductForm form(HttpServletRequest request) {
        ProductForm form = new ProductForm();
        String id = request.getParameter("id");
        if (id != null && !id.isBlank()) {
            form.setId(Integer.parseInt(id));
        }
        form.setName(request.getParameter("name"));
        form.setCategoryName(request.getParameter("category"));
        form.setManufacturerName(request.getParameter("manufacturer"));
        form.setWarehouseName(request.getParameter("warehouse"));
        form.setWarehouseAddress(request.getParameter("warehouseAddress"));
        form.setPrice(new BigDecimal(value(request.getParameter("price")).replace(',', '.')));
        form.setQuantity(Integer.parseInt(value(request.getParameter("quantity"))));
        return form;
    }

    static int intParameter(HttpServletRequest request, String name) {
        return Integer.parseInt(value(request.getParameter(name)));
    }

    static String value(String text) {
        return text == null ? "" : text.trim();
    }
}
