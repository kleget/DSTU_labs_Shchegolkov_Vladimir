package lab6.lab_gui;


import lab6.lab_gui.graph.*;
import javax.swing.*;
import java.awt.*;
import static java.lang.Math.*;

public class MainTask2 {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            Curve curve = new Curve();
            curve.setData(Math::sin, 0, 2 * PI, 500);

            Axis axisX = new Axis(0, 2 * PI);
            Axis axisY = new Axis(-1, 1);
            Rectangle world = new Rectangle(0, -1, (int)(2 * PI), 2);

            GraphPanel panel = new GraphPanel(curve, axisX, axisY, world);

            JFrame frame = new JFrame("Task 2: Curve class sin(x)");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(300, 300);
            frame.setLocationRelativeTo(null);
            frame.add(panel);
            frame.setVisible(true);
        });
    }
}
