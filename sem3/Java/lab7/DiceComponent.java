package lab7;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

public class DiceComponent extends JComponent {
    private static final int SIZE = 80;
    private static final Random RANDOM = new Random();
    private Color dotColor = Color.BLACK;
    private Color faceColor = new Color(240, 240, 240);
    private int value = 1;
    private boolean active = true;

    public DiceComponent() {
        setPreferredSize(new Dimension(SIZE, SIZE));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                roll();
            }
        });
    }

    public int roll() {
        if (active) {
            value = RANDOM.nextInt(6) + 1;
            repaint();
        }
        return value;
    }

    public int getValue() {
        return value;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public void setDotColor(Color dotColor) {
        this.dotColor = dotColor;
        repaint();
    }

    public void setFaceColor(Color faceColor) {
        this.faceColor = faceColor;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(faceColor);
        g2.fillRoundRect(2, 2, SIZE - 4, SIZE - 4, 15, 15);
        g2.setColor(Color.GRAY);
        g2.drawRoundRect(2, 2, SIZE - 4, SIZE - 4, 15, 15);

        g2.setColor(dotColor);
        int[][] positions = {
            {40, 40},
            {20, 20}, {60, 60},
            {20, 20}, {40, 40}, {60, 60},
            {20, 20}, {60, 20}, {20, 60}, {60, 60},
            {20, 20}, {60, 20}, {20, 60}, {60, 60}, {40, 40},
            {20, 20}, {60, 20}, {20, 60}, {60, 60}, {20, 40}, {60, 40}
        };
        int start = switch (value) {
            case 1 -> 0;
            case 2 -> 1;
            case 3 -> 3;
            case 4 -> 6;
            case 5 -> 10;
            default -> 15;
        };
        int count = switch (value) {
            case 1 -> 1;
            case 2 -> 2;
            case 3 -> 3;
            case 4 -> 4;
            case 5 -> 5;
            default -> 6;
        };
        for (int i = 0; i < count; i++) {
            int[] p = positions[start + i];
            g2.fillOval(p[0] - 6, p[1] - 6, 12, 12);
        }
    }
}
