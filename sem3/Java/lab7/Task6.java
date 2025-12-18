package lab7;

import javax.swing.*;

public class Task6 {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Task6 Dice");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            DiceComponent dice = new DiceComponent();
            frame.add(dice);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}
