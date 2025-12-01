package mypart;

/**
 * Обобщенный мешок только для пар одного типа.
 * Использует уже готовый класс Bag внутри.
 */
public class GPairBag<T1, T2> {
    private final Bag bag;

    public GPairBag(int capacity) {
        this.bag = new Bag(capacity);
    }

    public void add(Pair<T1, T2> pair) {
        if (pair == null) {
            throw new IllegalArgumentException("Пара не может быть null");
        }
        bag.add(pair);
    }

    @SuppressWarnings("unchecked")
    public Pair<T1, T2> remove() {
        return (Pair<T1, T2>) bag.remove();
    }

    @SuppressWarnings("unchecked")
    public Pair<T1, T2> peek() {
        return (Pair<T1, T2>) bag.peek();
    }

    public int size() {
        return bag.size();
    }
}
