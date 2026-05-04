package lab4.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab4.jdbc.JdbcProductRepository;

import java.io.IOException;
import java.util.List;

public class JdbcProductServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        show(req, resp, "");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        String action = ProductRequest.value(req.getParameter("action"));
        try {
            JdbcProductRepository repository = new JdbcProductRepository(getServletContext());
            if ("add".equals(action)) {
                repository.add(ProductRequest.form(req));
                show(req, resp, "Товар добавлен через JDBC.");
            } else if ("update".equals(action)) {
                repository.update(ProductRequest.form(req));
                show(req, resp, "Товар изменен через JDBC.");
            } else if ("delete".equals(action)) {
                repository.delete(ProductRequest.intParameter(req, "id"));
                show(req, resp, "Товар удален через JDBC.");
            } else {
                show(req, resp, "");
            }
        } catch (Exception e) {
            show(req, resp, "Ошибка: " + e.getMessage());
        }
    }

    private void show(HttpServletRequest req, HttpServletResponse resp, String message)
            throws ServletException, IOException {
        try {
            String filter = req.getParameter("filter");
            req.setAttribute("products", new JdbcProductRepository(getServletContext()).list(filter));
            req.setAttribute("filter", ProductRequest.value(filter));
        } catch (Exception e) {
            req.setAttribute("products", List.of());
            req.setAttribute("filter", "");
            if (message == null || message.isBlank()) {
                message = "Ошибка: " + e.getMessage();
            }
        }
        req.setAttribute("message", message);
        req.getRequestDispatcher("/WEB-INF/jsp/jdbc-products.jsp").forward(req, resp);
    }
}
