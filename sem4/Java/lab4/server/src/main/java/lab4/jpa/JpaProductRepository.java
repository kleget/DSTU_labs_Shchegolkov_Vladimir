package lab4.jpa;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.servlet.ServletContext;
import lab4.model.Category;
import lab4.model.Manufacturer;
import lab4.model.Product;
import lab4.model.ProductForm;
import lab4.model.ProductRow;
import lab4.model.ProductValidator;
import lab4.model.Warehouse;

import java.util.List;

public class JpaProductRepository {
    private final EntityManagerFactory emf;

    public JpaProductRepository(ServletContext context) throws Exception {
        this.emf = JpaService.emf(context);
    }

    public List<ProductRow> list(String filter) {
        EntityManager em = emf.createEntityManager();
        try {
            String cleanFilter = filter == null ? "" : filter.trim().toLowerCase();
            String pattern = "%" + cleanFilter + "%";
            return em.createQuery("""
                            SELECT p FROM Product p
                            JOIN FETCH p.category c
                            JOIN FETCH p.manufacturer m
                            JOIN FETCH p.warehouse w
                            WHERE :filter = ''
                               OR LOWER(p.name) LIKE :pattern
                               OR LOWER(c.name) LIKE :pattern
                               OR LOWER(m.name) LIKE :pattern
                               OR LOWER(w.name) LIKE :pattern
                            ORDER BY p.id
                            """, Product.class)
                    .setParameter("filter", cleanFilter)
                    .setParameter("pattern", pattern)
                    .getResultList()
                    .stream()
                    .map(this::row)
                    .toList();
        } finally {
            em.close();
        }
    }

    public void add(ProductForm form) {
        ProductValidator.validate(form);
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            Product product = new Product();
            apply(em, product, form);
            em.persist(product);
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            rollback(em);
            throw e;
        } finally {
            em.close();
        }
    }

    public void update(ProductForm form) {
        ProductValidator.validate(form);
        if (form.getId() == null) {
            throw new IllegalArgumentException("Для изменения нужен ID товара.");
        }
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            Product product = em.find(Product.class, form.getId());
            if (product == null) {
                throw new IllegalArgumentException("Товар не найден.");
            }
            apply(em, product, form);
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
            Product product = em.find(Product.class, id);
            if (product != null) {
                em.remove(product);
            }
            em.getTransaction().commit();
        } catch (RuntimeException e) {
            rollback(em);
            throw e;
        } finally {
            em.close();
        }
    }

    private void apply(EntityManager em, Product product, ProductForm form) {
        product.setName(form.getName());
        product.setCategory(findOrCreateCategory(em, form.getCategoryName()));
        product.setManufacturer(findOrCreateManufacturer(em, form.getManufacturerName()));
        product.setWarehouse(findOrCreateWarehouse(em, form.getWarehouseName(), form.getWarehouseAddress()));
        product.setPrice(form.getPrice());
        product.setQuantity(form.getQuantity());
    }

    private Category findOrCreateCategory(EntityManager em, String name) {
        List<Category> found = em.createQuery("SELECT c FROM Category c WHERE LOWER(c.name) = :name", Category.class)
                .setParameter("name", name.toLowerCase())
                .getResultList();
        if (!found.isEmpty()) {
            return found.get(0);
        }
        Category category = new Category(name);
        em.persist(category);
        return category;
    }

    private Manufacturer findOrCreateManufacturer(EntityManager em, String name) {
        List<Manufacturer> found = em.createQuery("SELECT m FROM Manufacturer m WHERE LOWER(m.name) = :name", Manufacturer.class)
                .setParameter("name", name.toLowerCase())
                .getResultList();
        if (!found.isEmpty()) {
            return found.get(0);
        }
        Manufacturer manufacturer = new Manufacturer(name);
        em.persist(manufacturer);
        return manufacturer;
    }

    private Warehouse findOrCreateWarehouse(EntityManager em, String name, String address) {
        List<Warehouse> found = em.createQuery("SELECT w FROM Warehouse w WHERE LOWER(w.name) = :name", Warehouse.class)
                .setParameter("name", name.toLowerCase())
                .getResultList();
        if (!found.isEmpty()) {
            Warehouse warehouse = found.get(0);
            if (address != null && !address.isBlank()) {
                warehouse.setAddress(address);
            }
            return warehouse;
        }
        Warehouse warehouse = new Warehouse(name, address);
        em.persist(warehouse);
        return warehouse;
    }

    private ProductRow row(Product product) {
        return new ProductRow(
                product.getId(),
                product.getName(),
                product.getCategory().getName(),
                product.getManufacturer().getName(),
                product.getWarehouse().getName(),
                product.getWarehouse().getAddress(),
                product.getPrice(),
                product.getQuantity()
        );
    }

    private static void rollback(EntityManager em) {
        if (em.getTransaction().isActive()) {
            em.getTransaction().rollback();
        }
    }
}
