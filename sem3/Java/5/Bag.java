import java.util.Random;

/**
 * Необобщенный мешок фиксированного размера.
 * Элементы кладутся и достаются из случайных позиций.
 */
public class Bag {
    private final Object[] data;
    private int size = 0;
    private final Random random = new Random();

    public Bag(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Размер мешка должен быть положительным");
        }
        this.data = new Object[capacity];
    }

    /**
     * Добавляет элемент в случайную позицию.
     */
    public void add(Object value) {
        if (size == data.length) {
            throw new IllegalStateException("Мешок заполнен");
        }
        int insertIndex = randomIndex(size + 1);
        data[size] = value; // кладем в конец
        if (insertIndex != size) {
            // меняем местами, чтобы новый элемент оказался в случайной позиции
            Object tmp = data[insertIndex];
            data[insertIndex] = data[size];
            data[size] = tmp;
        }
        size++;
    }

    /**
     * Забирает и возвращает случайный элемент.
     */
    public Object remove() {
        if (isEmpty()) {
            throw new IllegalStateException("Мешок пуст");
        }
        int index = randomIndex(size);
        Object value = data[index];
        // Переносим последний элемент на освободившееся место
        data[index] = data[size - 1];
        data[size - 1] = null;
        size--;
        return value;
    }

    /**
     * Возвращает случайный элемент без удаления.
     */
    public Object peek() {
        if (isEmpty()) {
            throw new IllegalStateException("Мешок пуст");
        }
        return data[randomIndex(size)];
    }

    public final int size() {
        return size;
    }

    public final int capacity() {
        return data.length;
    }

    public final boolean isEmpty() {
        return size == 0;
    }

    private int randomIndex(int bound) {
        return random.nextInt(bound);
    }
}
