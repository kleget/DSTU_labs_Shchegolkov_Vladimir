package lab4.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab4.auth.AuthGuard;
import lab4.auth.AuthService;
import lab4.config.DbConfig;
import lab4.config.DbConfigStore;
import lab4.jdbc.DatabaseBootstrap;
import lab4.jpa.JpaService;

import java.io.IOException;
import java.util.List;

public class AdminServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        if (!AuthGuard.requireAdmin(req, resp)) {
            return;
        }
        show(req, resp, "");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        if (!AuthGuard.requireAdmin(req, resp)) {
            return;
        }
        req.setCharacterEncoding("UTF-8");
        String action = ProductRequest.value(req.getParameter("action"));
        try {
            if ("saveConfig".equals(action)) {
                saveConfig(req);
                show(req, resp, "Настройки БД сохранены, JPA EntityManagerFactory пересоздан.");
            } else if ("saveUser".equals(action)) {
                new AuthService(getServletContext()).saveUser(
                        req.getParameter("id"),
                        req.getParameter("login"),
                        req.getParameter("password"),
                        req.getParameter("role")
                );
                show(req, resp, "Пользователь сохранен.");
            } else if ("deleteUser".equals(action)) {
                new AuthService(getServletContext()).deleteUser(
                        ProductRequest.intParameter(req, "id"),
                        AuthGuard.current(req).getLogin()
                );
                show(req, resp, "Пользователь удален.");
            } else {
                show(req, resp, "");
            }
        } catch (Exception e) {
            show(req, resp, "Ошибка: " + e.getMessage());
        }
    }

    private void saveConfig(HttpServletRequest req) throws Exception {
        DbConfig config = new DbConfig();
        config.setDriver(req.getParameter("driver"));
        config.setUrl(req.getParameter("url"));
        config.setUser(req.getParameter("dbUser"));
        config.setPassword(req.getParameter("dbPassword"));
        DatabaseBootstrap.ensure(config);
        new DbConfigStore(getServletContext()).save(config);
        JpaService.reset();
        JpaService.emf(getServletContext());
    }

    private void show(HttpServletRequest req, HttpServletResponse resp, String message)
            throws ServletException, IOException {
        try {
            req.setAttribute("users", new AuthService(getServletContext()).users());
            req.setAttribute("config", new DbConfigStore(getServletContext()).load());
        } catch (Exception e) {
            req.setAttribute("users", List.of());
            if (message == null || message.isBlank()) {
                message = "Ошибка: " + e.getMessage();
            }
        }
        req.setAttribute("user", AuthGuard.current(req));
        req.setAttribute("message", message);
        req.getRequestDispatcher("/WEB-INF/jsp/admin.jsp").forward(req, resp);
    }
}
