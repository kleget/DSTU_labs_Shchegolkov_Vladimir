package lab6;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;

/**
 * Задание 6: клавиши R/G/B выбирают фильтр, щелчок мышью применяет его.
 */
public class Task6ImageFilters extends JFrame {
    public Task6ImageFilters() {
        super("Task 6");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new FilterPanel(loadImage()));
        setSize(500, 420);
        setLocationRelativeTo(null);
    }

    private BufferedImage loadImage() {
        try {
            URL url = Task6ImageFilters.class.getResource("sample.jpg");
            if (url == null) {
                throw new IllegalStateException("Нет sample.jpg");
            }
            return ImageIO.read(url);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task6ImageFilters().setVisible(true));
    }

    private static class FilterPanel extends JPanel {
        private BufferedImage image;
        private char mode = 'r';
        private boolean rotated;
        private boolean grayApplied;

        private FilterPanel(BufferedImage image) {
            this.image = toArgb(image);
            setBackground(Color.BLACK);
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    applySelectedFilter();
                }
            });
            addKeyListener(new KeyAdapter() {
                @Override
                public void keyTyped(KeyEvent e) {
                    char c = Character.toLowerCase(e.getKeyChar());
                    if (c == 'r' || c == 'g' || c == 'b') {
                        mode = c;
                    }
                }
            });
            setFocusable(true);
        }

        @Override
        public void addNotify() {
            super.addNotify();
            requestFocusInWindow();
        }

        private void applySelectedFilter() {
            if (mode == 'r') {
                rotated = !rotated;
            } else if (mode == 'g' && !grayApplied) {
                image = toGray(image);
                grayApplied = true;
            } else if (mode == 'b') {
                image = blur(image);
            }
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            BufferedImage display = rotated ? rotate180(image) : image;
            Dimension fit = fitSize(display.getWidth(), display.getHeight(), getWidth(), getHeight());
            int x = (getWidth() - fit.width) / 2;
            int y = (getHeight() - fit.height) / 2;
            Image scaled = display.getScaledInstance(fit.width, fit.height, Image.SCALE_SMOOTH);
            g.drawImage(scaled, x, y, null);
        }

        private static Dimension fitSize(int w, int h, int areaW, int areaH) {
            double k = Math.min(areaW / (double) w, areaH / (double) h);
            if (k <= 0) {
                return new Dimension(1, 1);
            }
            return new Dimension((int) (w * k), (int) (h * k));
        }

        private static BufferedImage toArgb(BufferedImage src) {
            if (src.getType() == BufferedImage.TYPE_INT_ARGB) {
                return src;
            }
            BufferedImage copy = new BufferedImage(src.getWidth(), src.getHeight(), BufferedImage.TYPE_INT_ARGB);
            copy.getGraphics().drawImage(src, 0, 0, null);
            return copy;
        }

        private static BufferedImage rotate180(BufferedImage src) {
            BufferedImage dst = new BufferedImage(src.getWidth(), src.getHeight(), BufferedImage.TYPE_INT_ARGB);
            for (int y = 0; y < src.getHeight(); y++) {
                for (int x = 0; x < src.getWidth(); x++) {
                    dst.setRGB(src.getWidth() - 1 - x, src.getHeight() - 1 - y, src.getRGB(x, y));
                }
            }
            return dst;
        }

        private static BufferedImage toGray(BufferedImage src) {
            for (int y = 0; y < src.getHeight(); y++) {
                for (int x = 0; x < src.getWidth(); x++) {
                    int rgb = src.getRGB(x, y);
                    int r = (rgb >> 16) & 0xFF;
                    int g = (rgb >> 8) & 0xFF;
                    int b = rgb & 0xFF;
                    int avg = (r + g + b) / 3;
                    int gray = (0xFF << 24) | (avg << 16) | (avg << 8) | avg;
                    src.setRGB(x, y, gray);
                }
            }
            return src;
        }

        private static BufferedImage blur(BufferedImage src) {
            BufferedImage dst = new BufferedImage(src.getWidth(), src.getHeight(), BufferedImage.TYPE_INT_ARGB);
            for (int y = 0; y < src.getHeight(); y++) {
                for (int x = 0; x < src.getWidth(); x++) {
                    int sumR = 0;
                    int sumG = 0;
                    int sumB = 0;
                    int count = 0;
                    for (int dy = -1; dy <= 1; dy++) {
                        for (int dx = -1; dx <= 1; dx++) {
                            int nx = x + dx;
                            int ny = y + dy;
                            if (nx >= 0 && nx < src.getWidth() && ny >= 0 && ny < src.getHeight()) {
                                int rgb = src.getRGB(nx, ny);
                                sumR += (rgb >> 16) & 0xFF;
                                sumG += (rgb >> 8) & 0xFF;
                                sumB += rgb & 0xFF;
                                count++;
                            }
                        }
                    }
                    int r = sumR / count;
                    int g = sumG / count;
                    int b = sumB / count;
                    dst.setRGB(x, y, (0xFF << 24) | (r << 16) | (g << 8) | b);
                }
            }
            return dst;
        }
    }
}
