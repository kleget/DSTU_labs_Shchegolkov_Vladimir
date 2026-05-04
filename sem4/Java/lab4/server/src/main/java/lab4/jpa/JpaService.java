package lab4.jpa;

import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import jakarta.servlet.ServletContext;
import lab4.config.DbConfig;
import lab4.config.DbConfigStore;
import lab4.jdbc.DatabaseBootstrap;

import java.util.HashMap;
import java.util.Map;

public final class JpaService {
    private static EntityManagerFactory entityManagerFactory;

    private JpaService() {
    }

    public static synchronized EntityManagerFactory emf(ServletContext context) throws Exception {
        if (entityManagerFactory == null || !entityManagerFactory.isOpen()) {
            DbConfig config = new DbConfigStore(context).load();
            DatabaseBootstrap.ensure(config);
            Class.forName(config.getDriver());

            Map<String, Object> properties = new HashMap<>();
            properties.put("jakarta.persistence.jdbc.driver", config.getDriver());
            properties.put("jakarta.persistence.jdbc.url", config.getUrl());
            properties.put("jakarta.persistence.jdbc.user", config.getUser());
            properties.put("jakarta.persistence.jdbc.password", config.getPassword());
            properties.put("hibernate.hbm2ddl.auto", "update");
            properties.put("hibernate.show_sql", "false");

            entityManagerFactory = Persistence.createEntityManagerFactory("lab4PU", properties);
            JpaSeeder.seed(entityManagerFactory);
        }
        return entityManagerFactory;
    }

    public static synchronized void reset() {
        if (entityManagerFactory != null && entityManagerFactory.isOpen()) {
            entityManagerFactory.close();
        }
        entityManagerFactory = null;
    }
}
