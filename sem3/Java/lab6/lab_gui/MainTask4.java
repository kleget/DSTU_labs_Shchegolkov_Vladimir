package lab6.lab_gui;

import lab6.lab_gui.mouse.MouseCoordsPanel;
import javax.swing.*;


public class MainTask4 {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Task 4: Mouse coords");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(400, 400);
            frame.setLocationRelativeTo(null);

            frame.add(new MouseCoordsPanel());
            frame.setVisible(true);
        });
    }
}
