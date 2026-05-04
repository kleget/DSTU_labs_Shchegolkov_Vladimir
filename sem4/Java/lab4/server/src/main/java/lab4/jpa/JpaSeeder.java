package lab4.jpa;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import lab4.auth.PasswordUtil;
import lab4.model.AppUser;
import lab4.model.Book;
import lab4.model.Category;
import lab4.model.Manufacturer;
import lab4.model.Product;
import lab4.model.Warehouse;

import java.math.BigDecimal;

public final class JpaSeeder {
    private JpaSeeder() {
    }

    public static void seed(EntityManagerFactory emf) {
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            if (count(em, AppUser.class) == 0) {
                em.persist(new AppUser("admin", PasswordUtil.sha256("admin"), "ADMIN"));
                em.persist(new AppUser("user", PasswordUtil.sha256("user"), "USER"));
            }
            if (count(em, Book.class) == 0) {
                em.persist(book("Java для начинающих", "Иванов", "программирование", 2022));
                em.persist(book("Алгоритмы на Java", "Петров", "программирование", 2021));
                em.persist(book("История вычислительной техники", "Сидоров", "история", 2019));
            }
            if (count(em, Product.class) == 0) {
                Category parts = new Category("Комплектующие ПК");
                Category network = new Category("Сетевое оборудование");
                Manufacturer logitech = new Manufacturer("Logitech");
                Manufacturer tplink = new Manufacturer("TP-Link");
                Warehouse warehouse = new Warehouse("Основной склад", "Ростов-на-Дону, Гагарина 1");
                em.persist(parts);
                em.persist(network);
                em.persist(logitech);
                em.persist(tplink);
                em.persist(warehouse);
                em.persist(product("Мышь M185", parts, logitech, warehouse, "1290.00", 18));
                em.persist(product("Wi-Fi роутер Archer C6", network, tplink, warehouse, "3890.00", 7));
            }
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            if (em.getTransaction().isActive()) {
                em.getTransaction().rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }

    private static long count(EntityManager em, Class<?> entityClass) {
        String name = entityClass.getSimpleName();
        return em.createQuery("SELECT COUNT(e) FROM " + name + " e", Long.class).getSingleResult();
    }

    private static Product product(String name, Category category, Manufacturer manufacturer, Warehouse warehouse,
                                   String price, int quantity) {
        Product product = new Product();
        product.setName(name);
        product.setCategory(category);
        product.setManufacturer(manufacturer);
        product.setWarehouse(warehouse);
        product.setPrice(new BigDecimal(price));
        product.setQuantity(quantity);
        return product;
    }

    private static Book book(String title, String author, String genre, int year) {
        Book book = new Book();
        book.setTitle(title);
        book.setAuthor(author);
        book.setGenre(genre);
        book.setYear(year);
        return book;
    }
}
