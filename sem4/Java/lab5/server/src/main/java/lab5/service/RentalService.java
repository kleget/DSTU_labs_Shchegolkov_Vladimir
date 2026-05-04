package lab5.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.NoResultException;
import jakarta.persistence.Persistence;
import lab5.model.Car;
import lab5.model.Rental;
import lab5.model.Role;
import lab5.model.User;

import java.util.List;

@ApplicationScoped
public class RentalService {
    private static EntityManagerFactory emf;
    private static boolean seeded;

    private EntityManager em() {
        if (emf == null) {
            emf = Persistence.createEntityManagerFactory("lab5PU");
        }
        ensureSeedData();
        return emf.createEntityManager();
    }

    private static synchronized void ensureSeedData() {
        if (seeded || emf == null) {
            return;
        }

        EntityManager entityManager = emf.createEntityManager();
        try {
            Long userCount = entityManager.createQuery("select count(u) from User u", Long.class)
                    .getSingleResult();
            Long carCount = entityManager.createQuery("select count(c) from Car c", Long.class)
                    .getSingleResult();

            entityManager.getTransaction().begin();
            if (userCount == 0) {
                entityManager.persist(new User("manager", "manager@rental.local", "+70000000001", "manager", Role.MANAGER));
                entityManager.persist(new User("client", "client@rental.local", "+70000000002", "client", Role.CLIENT));
            }
            if (carCount == 0) {
                entityManager.persist(new Car("Toyota Camry", "Черный", "CAMRY-001", "новый", 4200));
                entityManager.persist(new Car("Kia Rio", "Белый", "RIO-014", "после ремонта", 2100));
                entityManager.persist(new Car("Hyundai Solaris", "Синий", "SOL-232", "хорошее", 2400));
            }
            entityManager.getTransaction().commit();
            seeded = true;
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }

    public User login(String name, String password) {
        EntityManager entityManager = em();
        try {
            return entityManager.createQuery(
                            "select u from User u where lower(u.name) = lower(:name) and u.password = :password",
                            User.class)
                    .setParameter("name", name == null ? "" : name.trim())
                    .setParameter("password", password == null ? "" : password)
                    .getSingleResult();
        } catch (NoResultException ex) {
            return null;
        } finally {
            entityManager.close();
        }
    }

    public User register(String name, String email, String phone, String password, Role role) {
        EntityManager entityManager = em();
        try {
            long duplicateCount = entityManager.createQuery(
                            "select count(u) from User u where lower(u.name) = lower(:name) or lower(u.email) = lower(:email)",
                            Long.class)
                    .setParameter("name", name.trim())
                    .setParameter("email", email.trim())
                    .getSingleResult();
            if (duplicateCount > 0) {
                throw new IllegalArgumentException("Пользователь с таким именем или e-mail уже существует");
            }

            User user = new User(name.trim(), email.trim(), phone.trim(), password, role);
            entityManager.getTransaction().begin();
            entityManager.persist(user);
            entityManager.getTransaction().commit();
            return user;
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }

    public List<Car> findAvailableCars() {
        EntityManager entityManager = em();
        try {
            return entityManager.createQuery("""
                            select c from Car c
                            where c.id not in (
                                select r.car.id from Rental r where r.active = true
                            )
                            order by c.id
                            """, Car.class)
                    .getResultList();
        } finally {
            entityManager.close();
        }
    }

    public List<Rental> findActiveRentals() {
        EntityManager entityManager = em();
        try {
            return entityManager.createQuery(
                            "select r from Rental r where r.active = true order by r.endDate, r.id",
                            Rental.class)
                    .getResultList();
        } finally {
            entityManager.close();
        }
    }

    public List<Rental> findClientRentals(Long clientId) {
        EntityManager entityManager = em();
        try {
            return entityManager.createQuery(
                            "select r from Rental r where r.active = true and r.client.id = :clientId order by r.endDate, r.id",
                            Rental.class)
                    .setParameter("clientId", clientId)
                    .getResultList();
        } finally {
            entityManager.close();
        }
    }

    public Car findCar(Long carId) {
        EntityManager entityManager = em();
        try {
            return entityManager.find(Car.class, carId);
        } finally {
            entityManager.close();
        }
    }

    public void saveCar(Long id, String name, String color, String serialNumber, String conditionInfo, double pricePerDay) {
        EntityManager entityManager = em();
        try {
            entityManager.getTransaction().begin();
            Car car = id == null ? new Car() : entityManager.find(Car.class, id);
            if (car == null) {
                throw new IllegalArgumentException("Автомобиль не найден");
            }
            car.setName(name.trim());
            car.setColor(color.trim());
            car.setSerialNumber(serialNumber.trim());
            car.setConditionInfo(conditionInfo.trim());
            car.setPricePerDay(pricePerDay);
            if (id == null) {
                entityManager.persist(car);
            }
            entityManager.getTransaction().commit();
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }

    public void deleteCar(Long carId) {
        EntityManager entityManager = em();
        try {
            long activeRentals = entityManager.createQuery(
                            "select count(r) from Rental r where r.active = true and r.car.id = :carId",
                            Long.class)
                    .setParameter("carId", carId)
                    .getSingleResult();
            if (activeRentals > 0) {
                throw new IllegalArgumentException("Нельзя удалить автомобиль, который сейчас арендован");
            }

            entityManager.getTransaction().begin();
            Car car = entityManager.find(Car.class, carId);
            if (car != null) {
                entityManager.remove(car);
            }
            entityManager.getTransaction().commit();
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }

    public void rentCar(Long clientId, Long carId, int days) {
        if (days < 1) {
            throw new IllegalArgumentException("Срок аренды должен быть больше нуля");
        }

        EntityManager entityManager = em();
        try {
            long activeRentals = entityManager.createQuery(
                            "select count(r) from Rental r where r.active = true and r.car.id = :carId",
                            Long.class)
                    .setParameter("carId", carId)
                    .getSingleResult();
            if (activeRentals > 0) {
                throw new IllegalArgumentException("Этот автомобиль уже арендован");
            }

            entityManager.getTransaction().begin();
            User client = entityManager.find(User.class, clientId);
            Car car = entityManager.find(Car.class, carId);
            if (client == null || car == null) {
                throw new IllegalArgumentException("Клиент или автомобиль не найден");
            }
            entityManager.persist(new Rental(client, car, days));
            entityManager.getTransaction().commit();
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }

    public void closeRental(Long clientId, Long rentalId) {
        EntityManager entityManager = em();
        try {
            entityManager.getTransaction().begin();
            Rental rental = entityManager.find(Rental.class, rentalId);
            if (rental == null || !rental.isActive() || !rental.getClient().getId().equals(clientId)) {
                throw new IllegalArgumentException("Активная аренда не найдена");
            }
            rental.setActive(false);
            entityManager.getTransaction().commit();
        } catch (RuntimeException ex) {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            throw ex;
        } finally {
            entityManager.close();
        }
    }
}
