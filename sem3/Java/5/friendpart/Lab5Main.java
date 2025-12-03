package friendpart;

import mypart.Bag;
import mypart.CoinChangeSolver;
import mypart.DList;
import mypart.GPairBag;
import mypart.GenericPairBag;
import mypart.Pair;
import mypart.PairBag;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;


public class Lab5Main {
    public static void main(String[] args) {
        demoPairAndBag();
        demoPairBags();
        demoCoinChange();
        demoHashTable();
        demoTournament();
    }

    private static void demoPairAndBag() {
        System.out.println("== Pair и Bag ==");
        Pair<Integer, String> pair = Pair.makePair(1, "один");
        System.out.println("Пара: " + pair);

        Bag bag = new Bag(4);
        bag.add(123);
        bag.add("строка");
        bag.add(pair);
        System.out.println("Случайный элемент из мешка: " + bag.peek());
        System.out.println("Извлекли: " + bag.remove());
        System.out.println("Размер сейчас: " + bag.size());
        System.out.println();
    }

    private static void demoPairBags() {
        System.out.println("== PairBag, GPairBag, GenericPairBag ==");
        PairBag pairBag = new PairBag(3);
        pairBag.addPair(Pair.makePair("a", 10));
        pairBag.addPair(Pair.makePair(2, 3));
        System.out.println("PairBag достал: " + pairBag.removePair());

        GPairBag<String, Integer> gPairBag = new GPairBag<>(3);
        gPairBag.add(Pair.makePair("x", 5));
        gPairBag.add(Pair.makePair("y", 6));
        System.out.println("GPairBag просмотр: " + gPairBag.peek());

        GenericPairBag<String, String> genericPairBag = new GenericPairBag<>();
        genericPairBag.add(Pair.makePair("left", "right"));
        genericPairBag.add(Pair.makePair("hello", "world"));
        System.out.println("GenericPairBag достал: " + genericPairBag.remove());
        System.out.println();
    }

    private static void demoCoinChange() {
        System.out.println("== Выдача суммы монетами ==");
        int[] coins = {1, 2, 3};
        int amount = 5;
        DList<Integer, Integer> table = CoinChangeSolver.buildTable(amount, coins);
        for (int i = 0; i < table.size(); i++) {
            System.out.println("Сумма " + table.getFirst(i) + " -> " + table.getSecond(i));
        }
        System.out.println();
    }

    private static void demoHashTable() {
        System.out.println("== Хэш-таблица с Person ==");
        int size = 20;
        HashFunction<String> hf = new PersonHashFunction(size);
        HashTable<Person, String> table = new HashTable<>(size, hf);
        List<Person> persons = Arrays.asList(
                new Person("Иванов", 30, "111-11-11"),
                new Person("Лобанов", 25, "222-22-22"),
                new Person("Балонов", 28, "333-33-33")
        );
        for (Person p : persons) {
            table.add(p);
        }
        System.out.println("Поиск Иванов: " + table.findFirst("Иванов").orElse(null));
        System.out.println("Поиск Петров: " + table.findFirst("Петров").orElse(null));
        System.out.println();
    }

    private static void demoTournament() {
        System.out.println("== Турнир ==");
        Scanner scanner = new Scanner(new ByteArrayInputStream(new byte[0]), StandardCharsets.UTF_8);
        Tournament tournament = new Tournament(6);
        String winner = tournament.run(scanner);
        System.out.println("Победитель: " + winner);
    }
}
