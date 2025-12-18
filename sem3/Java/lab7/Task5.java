package lab7;

import javax.swing.*;

public class Task5 {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Task5 TripleLabelPanel");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            TripleLabelPanel panel = new TripleLabelPanel();
            panel.setUpperText("верх");
            panel.setCenterText("центр");
            panel.setDownText("низ");
            frame.add(panel);
            frame.setSize(300, 200);
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}
