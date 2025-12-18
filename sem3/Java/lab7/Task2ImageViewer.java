package lab7;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
// import java.io.File;


public class Task2ImageViewer extends JFrame {
    private BufferedImage original;
    private BufferedImage current;
    private final JLabel imageLabel = new JLabel("", SwingConstants.CENTER);

    public Task2ImageViewer() {
        super("Просмотр изображений (минимал)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        JButton openBtn = new JButton("Открыть");
        JButton grayBtn = new JButton("Ч/Б");
        JButton invertBtn = new JButton("Инверсия");
        JButton resetBtn = new JButton("Сброс");

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.LEFT));
        controls.add(openBtn);
        controls.add(grayBtn);
        controls.add(invertBtn);
        controls.add(resetBtn);

        add(controls, BorderLayout.NORTH);
        add(new JScrollPane(imageLabel), BorderLayout.CENTER);

        openBtn.addActionListener(e -> openImage());
        grayBtn.addActionListener(e -> applyFilter(Filter.GRAY));
        invertBtn.addActionListener(e -> applyFilter(Filter.INVERT));
        resetBtn.addActionListener(e -> reset());
    }

    private void openImage() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                original = ImageIO.read(chooser.getSelectedFile());
                current = original;
                showImage();
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Не удалось открыть файл: " + ex.getMessage());
            }
        }
    }

    private void applyFilter(Filter filter) {
        if (original == null) return;
        int w = original.getWidth();
        int h = original.getHeight();
        BufferedImage out = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                int rgb = original.getRGB(x, y);
                int a = (rgb >> 24) & 0xff;
                int r = (rgb >> 16) & 0xff;
                int g = (rgb >> 8) & 0xff;
                int b = rgb & 0xff;
                switch (filter) {
                    case GRAY -> {
                        int v = (r + g + b) / 3;
                        r = g = b = v;
                    }
                    case INVERT -> {
                        r = 255 - r;
                        g = 255 - g;
                        b = 255 - b;
                    }
                }
                out.setRGB(x, y, (a << 24) | (r << 16) | (g << 8) | b);
            }
        }
        current = out;
        showImage();
    }

    private void reset() {
        if (original != null) {
            current = original;
            showImage();
        }
    }

    private void showImage() {
        imageLabel.setIcon(new ImageIcon(current));
    }

    private enum Filter {GRAY, INVERT}

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task2ImageViewer().setVisible(true));
    }
}
