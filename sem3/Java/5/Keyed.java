/**
 * Интерфейс для объектов, которые могут сообщить ключ для хэширования.
 */
public interface Keyed<K> {
    K key();

    default boolean matches(K value) {
        return key().equals(value);
    }
}
