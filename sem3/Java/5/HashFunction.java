/**
 * Абстрактная хэш-функция. Потомок знает, как превратить ключ в число.
 */
public abstract class HashFunction<K> {
    private final int tableSize;

    protected HashFunction(int tableSize) {
        if (tableSize <= 0) {
            throw new IllegalArgumentException("Размер таблицы должен быть положительным");
        }
        this.tableSize = tableSize;
    }

    /**
     * Отдает корректный индекс в пределах таблицы.
     */
    public final int index(K key) {
        int raw = Math.abs(hash(key));
        return raw % tableSize;
    }

    public final int tableSize() {
        return tableSize;
    }

    /**
     * Сырое значение до нормализации по размеру таблицы.
     */
    protected abstract int hash(K key);
}
