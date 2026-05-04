package lab4.servlet;

import jakarta.servlet.http.HttpServletRequest;
import lab4.model.BookForm;

final class BookRequest {
    private BookRequest() {
    }

    static BookForm form(HttpServletRequest request) {
        BookForm form = new BookForm();
        String id = request.getParameter("id");
        if (id != null && !id.isBlank()) {
            form.setId(Integer.parseInt(id));
        }
        form.setTitle(request.getParameter("title"));
        form.setAuthor(request.getParameter("author"));
        form.setGenre(request.getParameter("genre"));
        form.setYear(Integer.parseInt(value(request.getParameter("year"))));
        return form;
    }

    static int intParameter(HttpServletRequest request, String name) {
        return Integer.parseInt(value(request.getParameter(name)));
    }

    static String value(String text) {
        return text == null ? "" : text.trim();
    }
}
