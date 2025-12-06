package lab6.lab_gui.image;


import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;

public class ImagePanel extends JPanel
        implements MouseListener, KeyListener {

    private BufferedImage original;
    private BufferedImage current;

    public ImagePanel(BufferedImage image) {
        this.original = image;
        this.current = image;
        addMouseListener(this);
        addKeyListener(this);
        setFocusable(true);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (current == null) return;

        int panelW = getWidth();
        int panelH = getHeight();
        int imgW = current.getWidth();
        int imgH = current.getHeight();

        double scale = Math.min((double) panelW / imgW, (double) panelH / imgH);
        int drawW = (int) (imgW * scale);
        int drawH = (int) (imgH * scale);
        int x = (panelW - drawW) / 2;
        int y = (panelH - drawH) / 2;

        g.drawImage(current, x, y, drawW, drawH, null);
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        current = Filters.rotate180(current);
        repaint();
    }

    @Override
    public void keyTyped(KeyEvent e) {
        switch (e.getKeyChar()) {
            case 'r', 'R' -> current = Filters.rotate180(current);
            case 'g', 'G' -> current = Filters.toGrayscale(current);
            case 'b', 'B' -> current = Filters.blur3x3(current);
        }
        repaint();
    }
}
