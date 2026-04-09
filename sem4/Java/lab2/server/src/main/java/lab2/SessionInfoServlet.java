package lab2;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class SessionInfoServlet extends HttpServlet {
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/html; charset=UTF-8");
        HttpSession s = req.getSession(true);

        Integer count = (Integer) s.getAttribute("session.count");
        int current = (count == null ? 0 : count) + 1;
        s.setAttribute("session.count", current);

        boolean showId = req.getParameter("showId") != null;
        boolean showCreated = req.getParameter("showCreated") != null;
        boolean showNow = req.getParameter("showNow") != null;
        boolean showCount = req.getParameter("showCount") != null;

        StringBuilder html = new StringBuilder("<html><body><h2>Информация о сессии</h2><ul>");
        if (showId) {
            html.append("<li>ID сессии: ").append(s.getId()).append("</li>");
        }
        if (showCreated) {
            var created = LocalDateTime.ofInstant(Instant.ofEpochMilli(s.getCreationTime()), ZoneId.systemDefault());
            html.append("<li>Создана: ").append(FMT.format(created)).append("</li>");
        }
        if (showNow) {
            html.append("<li>Сейчас на сервере: ").append(FMT.format(LocalDateTime.now())).append("</li>");
        }
        if (showCount) {
            html.append("<li>Запросов в сессии: ").append(current).append("</li>");
        }
        html.append("</ul><p><a href='session.html'>Назад</a></p></body></html>");

        resp.getWriter().print(html);
    }
}
