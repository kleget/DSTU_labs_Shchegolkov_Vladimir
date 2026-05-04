package lab4.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab4.auth.AuthGuard;
import lab4.jpa.JpaBookRepository;

import java.io.IOException;
import java.util.List;

public class JpaBookServlet extends HttpServlet {
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
        String action = BookRequest.value(req.getParameter("action"));
        try {
            JpaBookRepository repository = new JpaBookRepository(getServletContext());
            if ("add".equals(action)) {
                repository.add(BookRequest.form(req));
                show(req, resp, "Книга добавлена через JPA.");
            } else if ("update".equals(action)) {
                repository.update(BookRequest.form(req));
                show(req, resp, "Книга изменена через JPA.");
            } else if ("delete".equals(action)) {
                repository.delete(BookRequest.intParameter(req, "id"));
                show(req, resp, "Книга удалена через JPA.");
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
            String genre = req.getParameter("genre");
            req.setAttribute("books", new JpaBookRepository(getServletContext()).list(genre));
            req.setAttribute("genre", BookRequest.value(genre));
        } catch (Exception e) {
            req.setAttribute("books", List.of());
            req.setAttribute("genre", "");
            if (message == null || message.isBlank()) {
                message = "Ошибка: " + e.getMessage();
            }
        }
        req.setAttribute("message", message);
        req.setAttribute("user", AuthGuard.current(req));
        req.getRequestDispatcher("/WEB-INF/jsp/jpa-books.jsp").forward(req, resp);
    }
}
