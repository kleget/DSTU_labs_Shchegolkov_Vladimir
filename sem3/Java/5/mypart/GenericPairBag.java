package mypart;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;



public class GenericPairBag<T1, T2> {
    private final List<Pair<T1, T2>> list = new ArrayList<>();
    private final Random random = new Random();

    public void add(Pair<T1, T2> pair) {
        if (pair == null) {
            throw new IllegalArgumentException("Пара не может быть null");
        }
        list.add(pair);
    }

    public Pair<T1, T2> remove() {
        if (list.isEmpty()) {
            throw new IllegalStateException("Мешок пуст");
        }
        int index = random.nextInt(list.size());
        return list.remove(index);
    }

    public Pair<T1, T2> peek() {
        if (list.isEmpty()) {
            throw new IllegalStateException("Мешок пуст");
        }
        return list.get(random.nextInt(list.size()));
    }

    public int size() {
        return list.size();
    }

    public boolean isEmpty() {
        return list.isEmpty();
    }
}
