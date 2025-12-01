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
                    addVariants(combos[sum], combos[sum - coin], coin);
                } else if (candidate == best[sum]) {
                    addVariants(combos[sum], combos[sum - coin], coin);
                }
            }
        }

        DList<Integer, Integer> table = new DList<>();
        for (int sum = 1; sum <= amount; sum++) {
            // сортируем варианты для стабильного вывода
            for (List<Integer> variant : combos[sum]) {
                Collections.sort(variant);
            }
            // убираем дубликаты вариантов
            combos[sum] = removeDuplicates(combos[sum]);
            table.add(sum, combos[sum]);
        }
        return table;
    }

    private static void addVariants(List<List<Integer>> target, List<List<Integer>> from, int coin) {
        for (List<Integer> prev : from) {
            List<Integer> next = new ArrayList<>(prev);
            next.add(coin);
            target.add(next);
        }
    }

    private static List<List<Integer>> removeDuplicates(List<List<Integer>> variants) {
        List<List<Integer>> result = new ArrayList<>();
        List<String> seen = new ArrayList<>();
        for (List<Integer> variant : variants) {
            String key = variant.toString();
            if (!seen.contains(key)) {
                seen.add(key);
                result.add(variant);
            }
        }
        return result;
    }
}
