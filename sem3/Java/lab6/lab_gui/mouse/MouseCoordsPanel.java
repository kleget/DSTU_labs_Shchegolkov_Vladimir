package lab6.lab_gui.mouse;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class MouseCoordsPanel extends JPanel
        implements MouseListener, KeyListener {

    private int x = -1, y = -1;
    private Color color = Color.BLACK;

    public MouseCoordsPanel() {
        addMouseListener(this);
        addKeyListener(this);
        setFocusable(true);
        requestFocusInWindow();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (x >= 0 && y >= 0) {
            g.setColor(color);
            g.drawString("(" + x + ", " + y + ")", x, y);
        }
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        x = e.getX();
        y = e.getY();
        repaint();
    }

    // остальные методы mouseListener можно оставить пустыми

    @Override
    public void keyTyped(KeyEvent e) {
        switch (e.getKeyChar()) {
            case 'b' -> color = Color.BLACK;
            case 'w' -> color = Color.WHITE;
            case 'r' -> color = Color.RED;
            case 'g' -> color = Color.GREEN;
            case 'o' -> color = Color.ORANGE;
        }
        repaint();
    }
}
