package lab5.model;

public enum Role {
    MANAGER("Менеджер"),
    CLIENT("Клиент");

    private final String title;

    Role(String title) {
        this.title = title;
    }

    public String getTitle() {
        return title;
    }
}
