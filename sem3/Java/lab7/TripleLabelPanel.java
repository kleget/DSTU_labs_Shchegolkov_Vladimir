package lab7;

import javax.swing.*;
import java.awt.*;

public class TripleLabelPanel extends JPanel {
    private final JLabel upperLabel = new JLabel("Верхняя");
    private final JLabel centerLabel = new JLabel("Центр");
    private final JLabel downLabel = new JLabel("Нижняя");

    public TripleLabelPanel() {
        setLayout(new BorderLayout());
        upperLabel.setHorizontalAlignment(SwingConstants.LEFT);
        downLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        centerLabel.setHorizontalAlignment(SwingConstants.CENTER);

        Font small = new Font("dialog", Font.BOLD | Font.ITALIC, 10);
        Font big = new Font("dialog", Font.BOLD, 18);
        upperLabel.setFont(small);
        downLabel.setFont(small);
        centerLabel.setFont(big);

        add(upperLabel, BorderLayout.NORTH);
        add(centerLabel, BorderLayout.CENTER);
        add(downLabel, BorderLayout.SOUTH);
    }

    public void setPanelBackground(Color color) {
        setBackground(color);
    }

    public void setUpperText(String text) {
        upperLabel.setText(text);
    }

    public void setCenterText(String text) {
        centerLabel.setText(text);
    }

    public void setDownText(String text) {
        downLabel.setText(text);
    }

    public void setUpperColor(Color color) {
        upperLabel.setForeground(color);
    }

    public void setCenterColor(Color color) {
        centerLabel.setForeground(color);
    }

    public void setDownColor(Color color) {
        downLabel.setForeground(color);
    }
}
