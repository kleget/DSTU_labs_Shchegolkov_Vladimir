package mypart;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;


public class DList<T1, T2> {
    private final List<T1> first = new ArrayList<>();
    private final List<List<List<T2>>> second = new ArrayList<>();

    public void add(T1 value, List<List<T2>> variants) {
        first.add(value);
        second.add(new ArrayList<>(variants));
    }

    public int size() {
        return first.size();
    }

    public T1 getFirst(int index) {
        return first.get(index);
    }

    public List<List<T2>> getSecond(int index) {
        return second.get(index);
    }

    public Optional<List<List<T2>>> getByFirstValue(T1 value) {
        int idx = first.indexOf(value);
        if (idx >= 0) {
            return Optional.of(second.get(idx));
        }
        return Optional.empty();
    }

    public void removeAt(int index) {
        first.remove(index);
        second.remove(index);
    }

    public boolean removeByFirstValue(T1 value) {
        int idx = first.indexOf(value);
        if (idx >= 0) {
            removeAt(idx);
            return true;
        }
        return false;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < first.size(); i++) {
            builder.append(first.get(i)).append(" -> ").append(second.get(i)).append(System.lineSeparator());
        }
        return builder.toString();
    }
}
