package lab4.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab4.auth.AuthGuard;
import lab4.jpa.JpaProductRepository;

import java.io.IOException;
import java.util.List;

public class JpaProductServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        if (!AuthGuard.requireLogin(req, resp)) {
            return;
        }
        show(req, resp, "");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        if (!AuthGuard.requireLogin(req, resp)) {
            return;
        }
        req.setCharacterEncoding("UTF-8");
        String action = ProductRequest.value(req.getParameter("action"));
        try {
            JpaProductRepository repository = new JpaProductRepository(getServletContext());
            if ("add".equals(action)) {
                repository.add(ProductRequest.form(req));
                show(req, resp, "Товар добавлен через JPA.");
            } else if ("update".equals(action)) {
                repository.update(ProductRequest.form(req));
                show(req, resp, "Товар изменен через JPA.");
            } else if ("delete".equals(action)) {
                repository.delete(ProductRequest.intParameter(req, "id"));
                show(req, resp, "Товар удален через JPA.");
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
            req.setAttribute("products", new JpaProductRepository(getServletContext()).list(filter));
            req.setAttribute("filter", ProductRequest.value(filter));
        } catch (Exception e) {
            req.setAttribute("products", List.of());
            req.setAttribute("filter", "");
            if (message == null || message.isBlank()) {
                message = "Ошибка: " + e.getMessage();
            }
        }
        req.setAttribute("message", message);
        req.setAttribute("user", AuthGuard.current(req));
        req.getRequestDispatcher("/WEB-INF/jsp/jpa-products.jsp").forward(req, resp);
    }
}
