package lab4.jpa;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.servlet.ServletContext;
import lab4.model.Book;
import lab4.model.BookForm;
import lab4.model.BookValidator;

import java.util.List;

public class JpaBookRepository {
    private final EntityManagerFactory emf;

    public JpaBookRepository(ServletContext context) throws Exception {
        this.emf = JpaService.emf(context);
    }

    public List<Book> list(String genre) {
        EntityManager em = emf.createEntityManager();
        try {
            String cleanGenre = genre == null ? "" : genre.trim().toLowerCase();
            return em.createQuery("""
                            SELECT b FROM Book b
                            WHERE :genre = '' OR LOWER(b.genre) = :genre
                            ORDER BY b.id
                            """, Book.class)
                    .setParameter("genre", cleanGenre)
                    .getResultList();
        } finally {
            em.close();
        }
    }

    public void add(BookForm form) {
        BookValidator.validate(form);
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            Book book = new Book();
            apply(book, form);
            em.persist(book);
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            rollback(em);
            throw e;
        } finally {
            em.close();
        }
    }

    public void update(BookForm form) {
        BookValidator.validate(form);
        if (form.getId() == null) {
            throw new IllegalArgumentException("Для изменения нужен ID книги.");
        }
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            Book book = em.find(Book.class, form.getId());
            if (book == null) {
                throw new IllegalArgumentException("Книга не найдена.");
            }
            apply(book, form);
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            rollback(em);
            throw e;
        } finally {
            em.close();
        }
    }

    public void delete(int id) {
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            Book book = em.find(Book.class, id);
            if (book != null) {
                em.remove(book);
            }
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            rollback(em);
            throw e;
        } finally {
            em.close();
        }
    }

    private static void apply(Book book, BookForm form) {
        book.setTitle(form.getTitle());
        book.setAuthor(form.getAuthor());
        book.setGenre(form.getGenre());
        book.setYear(form.getYear());
    }

    private static void rollback(EntityManager em) {
        if (em.getTransaction().isActive()) {
            em.getTransaction().rollback();
        }
    }
}
