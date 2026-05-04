package lab4.config;

public class DbConfig {
    private String driver = "org.h2.Driver";
    private String url = "jdbc:h2:./lab4db;DB_CLOSE_DELAY=-1";
    private String user = "sa";
    private String password = "";

    public String getDriver() {
        return driver;
    }

    public void setDriver(String driver) {
        this.driver = value(driver);
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = value(url);
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = value(user);
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password == null ? "" : password;
    }

    private static String value(String text) {
        return text == null ? "" : text.trim();
    }
}
