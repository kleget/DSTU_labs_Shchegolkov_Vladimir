package lab7;

import javax.swing.*;
import java.awt.*;

public class Task2ControlPad extends JFrame {
    public Task2ControlPad() {
        super("Lab 7 - Task 2");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(1,2));
        add(section("Рисунок"));
        add(section("Фильтр"));
        setSize(300,140);
        setLocationRelativeTo(null);
    }

    private JPanel section(String title){
        JPanel p=new JPanel(new GridLayout(3,2));
        p.setBorder(BorderFactory.createTitledBorder(title));
        JLabel val=new JLabel("50");
        JSlider slider=new JSlider(10,100,50);
        slider.addChangeListener(e->val.setText(""+slider.getValue()));
        p.add(new JLabel("Слайдер"));
        p.add(val);
        p.add(slider);
        p.add(new JSpinner(new SpinnerNumberModel(1,1,10,1)));
        p.add(new JButton("Старт"));
        p.add(new JButton("Стоп"));
        return p;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task2ControlPad().setVisible(true));
    }
}
