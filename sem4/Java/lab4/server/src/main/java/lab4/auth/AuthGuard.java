package lab4.auth;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public final class AuthGuard {
    public static final String SESSION_KEY = "lab4User";

    private AuthGuard() {
    }

    public static SessionUser current(HttpServletRequest request) {
        Object value = request.getSession(false) == null ? null : request.getSession(false).getAttribute(SESSION_KEY);
        return value instanceof SessionUser user ? user : null;
    }

    public static boolean requireLogin(HttpServletRequest request, HttpServletResponse response) throws IOException {
        if (current(request) == null) {
            response.sendRedirect(request.getContextPath() + "/login");
            return false;
        }
        return true;
    }

    public static boolean requireAdmin(HttpServletRequest request, HttpServletResponse response) throws IOException {
        SessionUser user = current(request);
        if (user == null) {
            response.sendRedirect(request.getContextPath() + "/login");
            return false;
        }
        if (!user.isAdmin()) {
            response.sendError(HttpServletResponse.SC_FORBIDDEN, "Требуется роль ADMIN.");
            return false;
        }
        return true;
    }
}
