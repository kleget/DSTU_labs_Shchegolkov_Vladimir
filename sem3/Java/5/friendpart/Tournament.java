package friendpart;

import mypart.Bag;
import mypart.GenericPairBag;
import mypart.Pair;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

/**
 * Простая жеребьевка турнира через мешки.
 */
public class Tournament {
    private final Bag teams;
    private final GenericPairBag<String, String> matches = new GenericPairBag<>();
    private final Random random = new Random();

    public Tournament(int teamCount) {
        int normalized = normalizeTeamCount(teamCount);
        teams = new Bag(normalized);
        for (int i = 1; i <= normalized; i++) {
            teams.add("Команда" + i);
        }
    }

    private int normalizeTeamCount(int count) {
        if (count < 2 || count % 2 != 0) {
            return 8;
        }
        return count;
    }

    public String run(Scanner scanner) {
        while (teams.size() > 1) {
            while (teams.size() > 1) {
                String a = (String) teams.remove();
                String b = (String) teams.remove();
                matches.add(new Pair<>(a, b));
            }
            List<String> winners = new ArrayList<>();
            while (!matches.isEmpty()) {
                Pair<String, String> match = matches.remove();
                winners.add(askWinner(match, scanner));
            }
            for (String winner : winners) {
                teams.add(winner);
            }
        }
        return (String) teams.remove();
    }

    private String askWinner(Pair<String, String> match, Scanner scanner) {
        System.out.println("Кто выиграл? 1 - " + match.first + ", 2 - " + match.second + " (по умолчанию случайно)");
        String line = scanner.hasNextLine() ? scanner.nextLine().trim() : "";
        if ("1".equals(line)) {
            return match.first;
        }
        if ("2".equals(line)) {
            return match.second;
        }
        return random.nextBoolean() ? match.first : match.second;
    }
}
