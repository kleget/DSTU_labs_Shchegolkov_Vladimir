package lab4.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab4.auth.AuthGuard;
import lab4.auth.AuthService;
import lab4.auth.SessionUser;

import java.io.IOException;

public class LoginServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        SessionUser user = AuthGuard.current(req);
        if (user != null) {
            resp.sendRedirect(req.getContextPath() + (user.isAdmin() ? "/admin" : "/jpa/books"));
            return;
        }
        req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        try {
            SessionUser user = new AuthService(getServletContext()).login(
                    req.getParameter("login"),
                    req.getParameter("password")
            );
            if (user == null) {
                req.setAttribute("message", "Неверный логин или пароль.");
                req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
                return;
            }
            req.getSession(true).setAttribute(AuthGuard.SESSION_KEY, user);
            resp.sendRedirect(req.getContextPath() + (user.isAdmin() ? "/admin" : "/jpa/books"));
        } catch (Exception e) {
            req.setAttribute("message", "Ошибка: " + e.getMessage());
            req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
        }
    }
}
