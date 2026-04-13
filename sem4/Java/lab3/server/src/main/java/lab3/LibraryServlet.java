package lab3;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public class LibraryServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        show(req, resp, "");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        String action = value(req.getParameter("action"));
        try {
            BookStore store = new BookStore(getServletContext());
            if ("add".equals(action)) {
                store.add(new Book("", req.getParameter("title"), req.getParameter("author"),
                        req.getParameter("genre"), req.getParameter("year")));
                show(req, resp, "Книга добавлена.");
            } else if ("delete".equals(action)) {
                boolean deleted = store.delete(req.getParameter("id"));
                show(req, resp, deleted ? "Книга удалена." : "Книга не найдена.");
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
            req.setAttribute("books", new BookStore(getServletContext()).list(genre));
            req.setAttribute("genre", value(genre));
            req.setAttribute("message", message);
        } catch (Exception e) {
            req.setAttribute("message", "Ошибка: " + e.getMessage());
        }
        req.getRequestDispatcher("/WEB-INF/jsp/library.jsp").forward(req, resp);
    }

    private static String value(String s) {
        return s == null ? "" : s.trim();
    }
}
