package mypart;

/**
 * Мешок, который принимает только пары.
 * Необобщенная версия - пары могут быть с любыми типами внутри.
 */
public class PairBag extends Bag {

    public PairBag(int capacity) {
        super(capacity);
    }

    public void addPair(Pair<?, ?> pair) {
        if (pair == null) {
            throw new IllegalArgumentException("Пара не может быть null");
        }
        super.add(pair);
    }

    public Pair<?, ?> removePair() {
        return (Pair<?, ?>) super.remove();
    }

    public Pair<?, ?> peekPair() {
        return (Pair<?, ?>) super.peek();
    }
}
