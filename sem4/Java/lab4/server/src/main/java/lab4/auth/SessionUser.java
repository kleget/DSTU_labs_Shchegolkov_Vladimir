package lab4.auth;

import java.io.Serializable;

public class SessionUser implements Serializable {
    private final String login;
    private final String role;

    public SessionUser(String login, String role) {
        this.login = login;
        this.role = role;
    }

    public String getLogin() {
        return login;
    }

    public String getRole() {
        return role;
    }

    public boolean isAdmin() {
        return "ADMIN".equals(role);
    }
}
