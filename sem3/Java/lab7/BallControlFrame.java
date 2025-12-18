package lab7;

import javax.swing.*;
import java.awt.*;
import java.util.Random;

public class BallControlFrame extends JFrame {
    private final JTextField maxField = new JTextField("5", 4);
    private final JLabel infoLabel = new JLabel("Шариков: 0 / 5");
    private final Timer timer;
    private int current = 0;

    public BallControlFrame() {
        super("Управление шарами (простая версия)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 200);
        setLocationRelativeTo(null);

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton start = new JButton("Старт");
        JButton stop = new JButton("Стоп");
        controls.add(new JLabel("Макс:"));
        controls.add(maxField);
        controls.add(start);
        controls.add(stop);
        controls.add(infoLabel);

        JPanel dummyAnimation = new JPanel();
        dummyAnimation.setBackground(new Color(230, 240, 255));
        dummyAnimation.setBorder(BorderFactory.createTitledBorder("Здесь могла быть анимация"));

        add(controls, BorderLayout.NORTH);
        add(dummyAnimation, BorderLayout.CENTER);

        timer = new Timer(500, e -> {
            int max = getMax();
            if (current < max) {
                current++;
            } else if (current > 0) {
                current--;
            }
            infoLabel.setText("Шариков: " + current + " / " + max);
        });

        start.addActionListener(e -> timer.start());
        stop.addActionListener(e -> timer.stop());
    }

    private int getMax() {
        try {
            return Math.max(1, Integer.parseInt(maxField.getText().trim()));
        } catch (NumberFormatException ex) {
            return 1;
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new BallControlFrame().setVisible(true));
    }
}
