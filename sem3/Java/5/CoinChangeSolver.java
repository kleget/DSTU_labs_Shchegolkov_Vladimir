import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Решение задачи выдачи суммы монетами динамическим программированием.
 * Таблица хранится в DList: первая колонка - сумма, вторая - список вариантов.
 */
public class CoinChangeSolver {

    public static DList<Integer, Integer> buildTable(int amount, int[] coins) {
        int[] best = new int[amount + 1];
        @SuppressWarnings("unchecked")
        List<List<Integer>>[] combos = new ArrayList[amount + 1];
        for (int i = 0; i <= amount; i++) {
            best[i] = Integer.MAX_VALUE / 4;
            combos[i] = new ArrayList<>();
        }
        best[0] = 0;
        combos[0].add(new ArrayList<>());

        for (int sum = 1; sum <= amount; sum++) {
            for (int coin : coins) {
                if (sum - coin < 0 || best[sum - coin] == Integer.MAX_VALUE / 4) {
                    continue;
                }
                int candidate = best[sum - coin] + 1;
                if (candidate < best[sum]) {
                    best[sum] = candidate;
                    combos[sum].clear();
                    for (List<Integer> prev : combos[sum - coin]) {
                        List<Integer> next = new ArrayList<>(prev);
                        next.add(coin);
                        combos[sum].add(next);
                    }
                } else if (candidate == best[sum]) {
                    for (List<Integer> prev : combos[sum - coin]) {
                        List<Integer> next = new ArrayList<>(prev);
                        next.add(coin);
                        combos[sum].add(next);
                    }
                }
            }
        }

        DList<Integer, Integer> table = new DList<>();
        for (int sum = 1; sum <= amount; sum++) {
            // сортируем варианты для стабильного вывода
            for (List<Integer> variant : combos[sum]) {
                Collections.sort(variant);
            }
            table.add(sum, combos[sum]);
        }
        return table;
    }
}
