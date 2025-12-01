package friendpart;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Простейшая хэш-таблица на массиве списков.
 */
public class HashTable<T extends Keyed<K>, K> {
    private final List<List<T>> buckets;
    private final HashFunction<K> hashFunction;

    public HashTable(int size, HashFunction<K> hashFunction) {
        if (hashFunction.tableSize() != size) {
            throw new IllegalArgumentException("Размер таблицы и функции должны совпадать");
        }
        this.hashFunction = hashFunction;
        this.buckets = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            buckets.add(new ArrayList<>());
        }
    }

    public void add(T value) {
        int index = hashFunction.index(value.key());
        buckets.get(index).add(value);
    }

    public boolean contains(K key) {
        return findFirst(key).isPresent();
    }

    public Optional<T> findFirst(K key) {
        int index = hashFunction.index(key);
        for (T value : buckets.get(index)) {
            if (value.matches(key)) {
                return Optional.of(value);
            }
        }
        return Optional.empty();
    }

    public List<T> bucket(K key) {
        return buckets.get(hashFunction.index(key));
    }
}
