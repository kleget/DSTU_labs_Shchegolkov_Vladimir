package lab4.model;

public class BookForm {
    private Integer id;
    private String title;
    private String author;
    private String genre;
    private int year;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = value(title);
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = value(author);
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = value(genre);
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    private static String value(String text) {
        return text == null ? "" : text.trim();
    }
}
