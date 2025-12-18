package lab7;

import javax.swing.*;
import java.awt.*;

public class GameFrame extends JFrame {
    private static final int REPEAT = -998;
    private static final int LOSE_ALL = -999;
    private static final int FINISH_CELL = -1000;

    private final DiceComponent dice1 = new DiceComponent();
    private final DiceComponent dice2 = new DiceComponent();
    private final JLabel status = new JLabel("Ход игрока 1");
    private final JLabel scoresLabel = new JLabel("Очки: 0 / 0");
    private final JLabel p1ScoreLabel = new JLabel("0", SwingConstants.CENTER);
    private final JLabel p2ScoreLabel = new JLabel("0", SwingConstants.CENTER);
    private final JButton rollBtn = new JButton("Бросить");
    private final int[] positions = {0, 0};
    private final int[] scores = {0, 0};
    private int current = 0;

    private final JLabel p1PosLabel = new JLabel("Клетка: 0");
    private final JLabel p2PosLabel = new JLabel("Клетка: 0");
    private final JLabel[] cellPlayerLabels = new JLabel[9];

    private final int[] board = {
        20,          // 0: +20
        REPEAT,      // 1: Try Again
        -50,         // 2: -50
        FINISH_CELL, // 3: Finish
        0,           // 4: центр (ничего)
        LOSE_ALL,    // 5: Lost All
        -10,         // 6: -10
        10,          // 7: +10
        30           // 8: +30
    };

    public GameFrame() {
        super("Dice game");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(900, 800);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JPanel grid = new JPanel(new GridLayout(3, 3));
        grid.add(cell(0, "+20", new Color(180, 255, 180)));
        grid.add(cell(1, "Try Again...", new Color(255, 255, 200)));
        grid.add(cell(2, "-50", new Color(255, 170, 170)));
        grid.add(cell(3, "Finish!", new Color(140, 240, 140)));
        grid.add(centerPanel());
        grid.add(cell(5, "Lost All", new Color(255, 120, 120)));
        grid.add(cell(6, "-10", new Color(255, 200, 200)));
        grid.add(cell(7, "+10", new Color(200, 255, 200)));
        grid.add(cell(8, "+30", new Color(120, 240, 120)));

        add(grid, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new FlowLayout(FlowLayout.LEFT));
        bottom.add(status);
        bottom.add(scoresLabel);
        bottom.add(rollBtn);
        bottom.add(new JLabel("| P1"));
        bottom.add(p1PosLabel);
        bottom.add(new JLabel("| P2"));
        bottom.add(p2PosLabel);
        add(bottom, BorderLayout.SOUTH);

        rollBtn.addActionListener(e -> roll());
        updatePositions();
    }

    private JPanel cell(int index, String text, Color bg) {
        JPanel p = new JPanel(new BorderLayout());
        p.setBackground(bg);
        JLabel l = new JLabel(text, SwingConstants.CENTER);
        l.setFont(l.getFont().deriveFont(Font.BOLD, 16f));
        JLabel playerLabel = new JLabel("", SwingConstants.CENTER);
        playerLabel.setFont(playerLabel.getFont().deriveFont(Font.PLAIN, 12f));
        cellPlayerLabels[index] = playerLabel;
        p.add(l, BorderLayout.CENTER);
        p.add(playerLabel, BorderLayout.SOUTH);
        return p;
    }

    private JPanel centerPanel() {
        JPanel scorePanel = new JPanel(new GridLayout(2, 2, 5, 5));
        scorePanel.setBackground(new Color(230, 230, 230));
        JLabel p1 = new JLabel("Player 1", SwingConstants.CENTER);
        JLabel p2 = new JLabel("Player 2", SwingConstants.CENTER);
        p1ScoreLabel.setBorder(BorderFactory.createTitledBorder("Score"));
        p2ScoreLabel.setBorder(BorderFactory.createTitledBorder("Score"));
        scorePanel.add(p1);
        scorePanel.add(p2);
        scorePanel.add(p1ScoreLabel);
        scorePanel.add(p2ScoreLabel);

        JPanel wrap = new JPanel(new BorderLayout());
        wrap.setBackground(new Color(230, 230, 230));
        wrap.add(dice1, BorderLayout.WEST);
        wrap.add(scorePanel, BorderLayout.CENTER);
        wrap.add(dice2, BorderLayout.EAST);
        return wrap;
    }

    private void roll() {
        int move = dice1.roll() + dice2.roll();
        positions[current] = Math.min(board.length - 1, positions[current] + move);

        int action = board[positions[current]];
        if (action == LOSE_ALL) {
            scores[current] = 0;
        } else if (action == FINISH_CELL) {
            scores[current] += 50;
            finishGame("Финиш достигнут!");
            return;
        } else if (action != REPEAT) {
            scores[current] += action;
        }

        if (positions[current] == board.length - 1) {
            scores[current] += 50;
            finishGame("Финиш достигнут!");
            return;
        }

        p1ScoreLabel.setText(String.valueOf(scores[0]));
        p2ScoreLabel.setText(String.valueOf(scores[1]));
        scoresLabel.setText("Очки: " + scores[0] + " / " + scores[1]);
        p1PosLabel.setText("Клетка: " + positions[0]);
        p2PosLabel.setText("Клетка: " + positions[1]);
        if (action != REPEAT) {
            current = 1 - current;
        }
        status.setText("Ход игрока " + (current + 1));
        updatePositions();
    }

    private void finishGame(String message) {
        rollBtn.setEnabled(false);
        String winner = scores[0] == scores[1] ? "Ничья" : (scores[0] > scores[1] ? "Победил игрок 1" : "Победил игрок 2");
        p1ScoreLabel.setText(String.valueOf(scores[0]));
        p2ScoreLabel.setText(String.valueOf(scores[1]));
        scoresLabel.setText("Очки: " + scores[0] + " / " + scores[1]);
        p1PosLabel.setText("Клетка: " + positions[0]);
        p2PosLabel.setText("Клетка: " + positions[1]);
        status.setText(winner);
        JOptionPane.showMessageDialog(this, message + "\n" + winner);
        updatePositions();
    }

    private void updatePositions() {
        for (JLabel lbl : cellPlayerLabels) {
            if (lbl != null) {
                lbl.setText("");
            }
        }
        String[] occ = new String[cellPlayerLabels.length];
        for (int i = 0; i < positions.length; i++) {
            int pos = Math.min(positions[i], board.length - 1);
            String val = "P" + (i + 1);
            if (occ[pos] == null) occ[pos] = val;
            else occ[pos] += "," + val;
        }
        for (int i = 0; i < cellPlayerLabels.length; i++) {
            if (cellPlayerLabels[i] != null) {
                cellPlayerLabels[i].setText(occ[i] == null ? "" : occ[i]);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new GameFrame().setVisible(true));
    }
}
