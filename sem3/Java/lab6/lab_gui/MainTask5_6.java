package lab6.lab_gui;

import lab6.lab_gui.image.ImagePanel;
import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.IOException;

public class MainTask5_6 {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                BufferedImage img = ImageIO.read(
                        MainTask5_6.class.getResource("/images/test.jpg")
                );

                JFrame frame = new JFrame("Task 5–6: Image & filters");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setSize(600, 400);
                frame.setLocationRelativeTo(null);
                frame.add(new ImagePanel(img));
                frame.setVisible(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}
