package friendpart;

/**
 * Простая запись о человеке для демонстрации хэш-таблицы.
 */
public class Person implements Keyed<String> {
    private final String lastName;
    private final int age;
    private final String phone;

    public Person(String lastName, int age, String phone) {
        this.lastName = lastName;
        this.age = age;
        this.phone = phone;
    }

    @Override
    public String key() {
        return lastName;
    }

    @Override
    public boolean matches(String value) {
        return lastName.equalsIgnoreCase(value);
    }

    @Override
    public String toString() {
        return lastName + " (" + age + ", " + phone + ")";
    }
}
