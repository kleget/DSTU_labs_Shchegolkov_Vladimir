package lab4.auth;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.servlet.ServletContext;
import lab4.jpa.JpaService;
import lab4.model.AppUser;

import java.util.List;

public class AuthService {
    private final EntityManagerFactory emf;

    public AuthService(ServletContext context) throws Exception {
        this.emf = JpaService.emf(context);
    }

    public SessionUser login(String login, String password) {
        EntityManager em = emf.createEntityManager();
        try {
            List<AppUser> users = em.createQuery("SELECT u FROM AppUser u WHERE u.login = :login", AppUser.class)
                    .setParameter("login", value(login))
                    .getResultList();
            if (users.isEmpty()) {
                return null;
            }
            AppUser user = users.get(0);
            if (!user.getPasswordHash().equals(PasswordUtil.sha256(password))) {
                return null;
            }
            return new SessionUser(user.getLogin(), user.getRole());
        } finally {
            em.close();
        }
    }

    public List<AppUser> users() {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery("SELECT u FROM AppUser u ORDER BY u.login", AppUser.class).getResultList();
        } finally {
            em.close();
        }
    }

    public void saveUser(String id, String login, String password, String role) {
        validateUser(login, role);
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            AppUser user = isBlank(id) ? new AppUser() : em.find(AppUser.class, Integer.parseInt(id));
            if (user == null) {
                throw new IllegalArgumentException("Пользователь не найден.");
            }
            user.setLogin(value(login));
            user.setRole(role);
            if (!isBlank(password)) {
                user.setPasswordHash(PasswordUtil.sha256(password));
            } else if (user.getPasswordHash() == null) {
                throw new IllegalArgumentException("Для нового пользователя нужен пароль.");
            }
            if (user.getId() == null) {
                em.persist(user);
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

    public void deleteUser(int id, String currentLogin) {
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            AppUser user = em.find(AppUser.class, id);
            if (user != null) {
                if (user.getLogin().equals(currentLogin)) {
                    throw new IllegalArgumentException("Нельзя удалить текущего пользователя.");
                }
                em.remove(user);
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

    private static void validateUser(String login, String role) {
        if (!value(login).matches("^[A-Za-z0-9_]{3,30}$")) {
            throw new IllegalArgumentException("Логин: 3-30 символов, латиница, цифры или подчеркивание.");
        }
        if (!"ADMIN".equals(role) && !"USER".equals(role)) {
            throw new IllegalArgumentException("Роль должна быть ADMIN или USER.");
        }
    }

    private static boolean isBlank(String text) {
        return text == null || text.isBlank();
    }

    private static String value(String text) {
        return text == null ? "" : text.trim();
    }
}
