package lab2;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class CurrencyServlet extends HttpServlet {
    private static final DateTimeFormatter UI = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    private final CbrService service = new CbrService();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.setCharacterEncoding("UTF-8");
        String type = val(req.getParameter("type"), "currency");
        String code = val(req.getParameter("code"), "USD");

        LocalDate from = parseDate(req.getParameter("from"), LocalDate.now());
        LocalDate to = parseDate(req.getParameter("to"), LocalDate.now());
        if (to.isBefore(from)) {
            LocalDate t = from;
            from = to;
            to = t;
        }

        try {
            List<CbrService.Quote> list = "metal".equalsIgnoreCase(type)
                    ? service.metal(code, from, to)
                    : service.currency(code, from, to);

            if ("csv".equalsIgnoreCase(req.getParameter("format"))) {
                resp.setContentType("text/plain; charset=UTF-8");
                StringBuilder sb = new StringBuilder("date;value\n");
                for (CbrService.Quote q : list) {
                    sb.append(UI.format(q.date())).append(';').append(q.value()).append('\n');
                }
                resp.getWriter().print(sb);
                return;
            }

            resp.setContentType("text/html; charset=UTF-8");
            StringBuilder html = new StringBuilder();
            html.append("<html><body><h2>Результат запроса ЦБ РФ</h2>");
            html.append("<p>Тип: ").append(type).append(", код: ").append(code.toUpperCase())
                    .append(", период: ").append(UI.format(from)).append(" - ").append(UI.format(to)).append("</p>");
            html.append("<table border='1' cellpadding='6'><tr><th>Дата</th><th>Значение</th></tr>");
            for (CbrService.Quote q : list) {
                html.append("<tr><td>").append(UI.format(q.date())).append("</td><td>")
                        .append(String.format(java.util.Locale.US, "%.4f", q.value())).append("</td></tr>");
            }
            html.append("</table><p><a href='currency.html'>Назад</a></p></body></html>");
            resp.getWriter().print(html);
        } catch (Exception e) {
            resp.setContentType("text/html; charset=UTF-8");
            resp.getWriter().print("<html><body><h3>Ошибка: " + escape(e.getMessage()) + "</h3><p><a href='currency.html'>Назад</a></p></body></html>");
        }
    }

    private static String val(String s, String def) {
        return s == null || s.isBlank() ? def : s.trim();
    }

    private static LocalDate parseDate(String s, LocalDate def) {
        if (s == null || s.isBlank()) {
            return def;
        }
        try {
            return LocalDate.parse(s.trim(), UI);
        } catch (Exception e) {
            return def;
        }
    }

    private static String escape(String s) {
        return s == null ? "" : s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
}
