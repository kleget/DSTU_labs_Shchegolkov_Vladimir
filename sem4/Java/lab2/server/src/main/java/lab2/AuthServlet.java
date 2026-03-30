package lab2;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class AuthServlet extends HttpServlet {
    private static final String FAIL_KEY = "auth.fail";
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        process(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        process(req, resp);
    }

    private void process(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setContentType("text/html; charset=UTF-8");

        String action = trim(req.getParameter("action"));
        String login = trim(req.getParameter("login"));
        String password = trim(req.getParameter("password"));

        HttpSession session = req.getSession(true);
        Integer fail = (Integer) session.getAttribute(FAIL_KEY);
        int failCount = fail == null ? 0 : fail;

        String message;
        try {
            if (login.isEmpty() || password.isEmpty()) {
                message = "Логин и пароль обязательны.";
            } else {
                UserStore store = new UserStore(getServletContext());
                if ("register".equalsIgnoreCase(action)) {
                    if (store.register(login, password)) {
                        message = "Регистрация успешна. Время сервера: " + FMT.format(LocalDateTime.now());
                    } else {
                        message = "Пользователь уже существует.";
                    }
                } else {
                    if (failCount >= 3) {
                        message = "Авторизация в этой сессии заблокирована после 3 неудачных попыток.";
                    } else if (store.verify(login, password)) {
                        session.setAttribute(FAIL_KEY, 0);
                        message = "Авторизация успешна. Время сервера: " + FMT.format(LocalDateTime.now());
                    } else {
                        failCount++;
                        session.setAttribute(FAIL_KEY, failCount);
                        if (failCount >= 3) {
                            message = "Неверный логин/пароль. Попытка " + failCount + ". Сессия заблокирована.";
                        } else {
                            message = "Неверный логин/пароль. Попытка " + failCount + ".";
                        }
                    }
                }
            }
        } catch (Exception e) {
            message = "Ошибка сервера: " + e.getMessage();
        }

        resp.getWriter().println("<html><body><h3>" + escape(message) + "</h3><p><a href='index.html'>Назад</a></p></body></html>");
    }

    private static String trim(String s) {
        return s == null ? "" : s.trim();
    }

    private static String escape(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
}
