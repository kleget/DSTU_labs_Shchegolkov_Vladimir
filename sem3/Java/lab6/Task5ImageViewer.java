package lab6;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;

/**
 * Простое окно: показывает картинку и переворачивает её по клику.
 */
public class Task5ImageViewer extends JFrame {
    public Task5ImageViewer() {
        super("Task 5");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new ImagePanel(loadImage()));
        setSize(500, 400);
        setLocationRelativeTo(null);
    }

    private BufferedImage loadImage() {
        try {
            URL url = Task5ImageViewer.class.getResource("sample.jpg");
            if (url == null) {
                throw new IllegalStateException("Нет sample.jpg");
            }
            return ImageIO.read(url);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task5ImageViewer().setVisible(true));
    }

    private static class ImagePanel extends JPanel {
        private final BufferedImage image;
        private boolean rotated;

        private ImagePanel(BufferedImage image) {
            this.image = image;
            setBackground(Color.BLACK);
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    rotated = !rotated;
                    repaint();
                }
            });
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            if (image == null) {
                return;
            }
            BufferedImage src = rotated ? rotate180(image) : image;
            Dimension fit = fit(src.getWidth(), src.getHeight(), getWidth(), getHeight());
            int x = (getWidth() - fit.width) / 2;
            int y = (getHeight() - fit.height) / 2;
            g.drawImage(src.getScaledInstance(fit.width, fit.height, Image.SCALE_SMOOTH), x, y, null);
        }

        private BufferedImage rotate180(BufferedImage src) {
            BufferedImage copy = new BufferedImage(src.getWidth(), src.getHeight(), BufferedImage.TYPE_INT_ARGB);
            Graphics2D g2 = copy.createGraphics();
            g2.rotate(Math.PI, src.getWidth() / 2.0, src.getHeight() / 2.0);
            g2.drawImage(src, 0, 0, null);
            g2.dispose();
            return copy;
        }

        private Dimension fit(int w, int h, int areaW, int areaH) {
            double ratio = Math.min(areaW / (double) w, areaH / (double) h);
            return new Dimension((int) (w * ratio), (int) (h * ratio));
        }
    }
}
