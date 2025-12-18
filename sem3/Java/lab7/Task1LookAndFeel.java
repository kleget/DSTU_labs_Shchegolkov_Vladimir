package lab7;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class Task1LookAndFeel extends JFrame {
    public Task1LookAndFeel() {
        super("Task1 Look & Feel");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(900, 400);
        setLocationRelativeTo(null);

        JComboBox<String> lafCombo = new JComboBox<>();
        for (UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
            lafCombo.addItem(info.getClassName());
        }
        JLabel label = new JLabel("Пример метки");
        JButton button = new JButton("Кнопка");
        JCheckBox checkBox = new JCheckBox("Check");
        JRadioButton radioButton = new JRadioButton("Radio");

        String[] headers = {"Язык", "Автор", "Год"};
        Object[][] data = {
            {"C", "Деннис Ритчи", 1972},
            {"C++", "Бьерн Страуструп", 1983},
            {"Python", "Гвидо ван Россум", 1991},
            {"Java", "Джеймс Гослинг", 1995},
            {"JavaScript", "Брендон Айк", 1995},
            {"C#", "Андерс Хейлсберг", 2001},
            {"Scala", "Мартин Одерски", 2003}
        };
        JTable table = new JTable(new DefaultTableModel(data, headers));
        JScrollPane scroll = new JScrollPane(table);

        lafCombo.addActionListener(e -> {
            String className = (String) lafCombo.getSelectedItem();
            try {
                UIManager.setLookAndFeel(className);
                SwingUtilities.updateComponentTreeUI(this);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Не удалось применить LAF: " + ex.getMessage());
            }
        });

        JPanel top = new JPanel(new FlowLayout(FlowLayout.LEFT));
        top.add(new JLabel("Look & Feel:"));
        top.add(lafCombo);
        top.add(label);
        top.add(button);
        top.add(checkBox);
        top.add(radioButton);

        add(top, BorderLayout.NORTH);
        add(scroll, BorderLayout.CENTER);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task1LookAndFeel().setVisible(true));
    }
}
