package lab3;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public class BooksApiServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain; charset=UTF-8");
        try {
            StringBuilder csv = new StringBuilder("id;title;author;genre;year\n");
            for (Book b : new BookStore(getServletContext()).list(req.getParameter("genre"))) {
                csv.append(cell(b.getId())).append(';')
                        .append(cell(b.getTitle())).append(';')
                        .append(cell(b.getAuthor())).append(';')
                        .append(cell(b.getGenre())).append(';')
                        .append(cell(b.getYear())).append('\n');
            }
            resp.getWriter().print(csv);
        } catch (Exception e) {
            resp.setStatus(500);
            resp.getWriter().print("ERROR;" + e.getMessage());
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setContentType("text/plain; charset=UTF-8");
        try {
            BookStore store = new BookStore(getServletContext());
            String action = value(req.getParameter("action"));
            if ("add".equals(action)) {
                store.add(new Book("", req.getParameter("title"), req.getParameter("author"),
                        req.getParameter("genre"), req.getParameter("year")));
                resp.getWriter().print("OK;added");
            } else if ("delete".equals(action)) {
                resp.getWriter().print(store.delete(req.getParameter("id")) ? "OK;deleted" : "ERROR;not found");
            } else {
                resp.getWriter().print("ERROR;unknown action");
            }
        } catch (Exception e) {
            resp.setStatus(500);
            resp.getWriter().print("ERROR;" + e.getMessage());
        }
    }

    private static String cell(String s) {
        return value(s).replace(';', ',').replace('\n', ' ');
    }

    private static String value(String s) {
        return s == null ? "" : s.trim();
    }
}
