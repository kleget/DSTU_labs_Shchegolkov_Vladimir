package lab4.model;

public final class BookValidator {
    private static final String TITLE_RE = "^[\\p{L}\\p{N} .,'\"«»:()!?\\-]{1,100}$";
    private static final String AUTHOR_RE = "^[\\p{L} .'-]{2,80}$";
    private static final String GENRE_RE = "^[\\p{L} -]{2,50}$";

    private BookValidator() {
    }

    public static void validate(BookForm form) {
        if (form.getTitle() == null || !form.getTitle().matches(TITLE_RE)) {
            throw new IllegalArgumentException("Название книги заполнено неверно.");
        }
        if (form.getAuthor() == null || !form.getAuthor().matches(AUTHOR_RE)) {
            throw new IllegalArgumentException("Автор заполнен неверно.");
        }
        if (form.getGenre() == null || !form.getGenre().matches(GENRE_RE)) {
            throw new IllegalArgumentException("Жанр заполнен неверно.");
        }
        if (form.getYear() < 1500 || form.getYear() > 2099) {
            throw new IllegalArgumentException("Год должен быть от 1500 до 2099.");
        }
    }
}
