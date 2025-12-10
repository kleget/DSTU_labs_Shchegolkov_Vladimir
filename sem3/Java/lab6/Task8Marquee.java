package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

/**
 * Бегущая строка: строки меняются по клику и бегут слева направо.
 */
public class Task8Marquee extends JFrame {
    public Task8Marquee() {
        super("Task 8");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new MarqueePanel());
        setSize(600, 150);
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task8Marquee().setVisible(true));
    }

    private static class MarqueePanel extends JPanel {
        private final String[] messages = {
                "Практика с Swing",
                "Лабораторная №6",
                "Щёлкните, чтобы сменить текст",
                "Простой пример бегущей строки"
        };
        private final Random random = new Random();
        private int index = 0;
        private int x = 0;

        private MarqueePanel() {
            setBackground(Color.BLACK);
            setForeground(Color.GREEN);
            setFont(new Font("Monospaced", Font.BOLD, 24));
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    index = random.nextInt(messages.length);
                    x = -getFontMetrics(getFont()).stringWidth(messages[index]);
                }
            });
            new Timer(20, e -> move()).start();
        }

        private void move() {
            x += 2;
            int width = getWidth();
            FontMetrics fm = getFontMetrics(getFont());
            int textWidth = fm.stringWidth(messages[index]);
            if (x > width) {
                x = -textWidth;
            }
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.setColor(getForeground());
            FontMetrics fm = g.getFontMetrics();
            int y = getHeight() / 2 + fm.getAscent() / 2;
            g.drawString(messages[index], x, y);
        }
    }
}
