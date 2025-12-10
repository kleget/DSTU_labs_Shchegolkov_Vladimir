package lab7;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class Task1LookAndFeel extends JFrame {
    private final JComboBox<UIManager.LookAndFeelInfo> laf = new JComboBox<>(UIManager.getInstalledLookAndFeels());

    public Task1LookAndFeel() {
        super("Lab 7 - Task 1");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        JPanel top = new JPanel();
        top.add(new JLabel("LAF"));
        top.add(laf);
        top.add(new JButton("Кнопка"));
        top.add(new JCheckBox("Чек"));
        top.add(new JRadioButton("Опция"));
        add(top, BorderLayout.NORTH);

        JTable table = new JTable(new DefaultTableModel(new Object[][]{
                {"C", "Деннис Ритчи", 1972},
                {"C++", "Бьерн Страуструп", 1983},
                {"Python", "Гвидо ван Россум", 1991},
                {"Java", "Джеймс Гослинг", 1995},
                {"JavaScript", "Брендон Айк", 1995},
                {"C#", "Андерс Хейлсберг", 2001},
                {"Scala", "Мартин Одерски", 2003}
        }, new Object[]{"Язык", "Автор", "Год"}));
        add(new JScrollPane(table), BorderLayout.CENTER);

        laf.addActionListener(e -> {
            UIManager.LookAndFeelInfo info = (UIManager.LookAndFeelInfo) laf.getSelectedItem();
            try { UIManager.setLookAndFeel(info.getClassName()); SwingUtilities.updateComponentTreeUI(this); }
            catch (Exception ignored) { }
        });

        setSize(440, 220);
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task1LookAndFeel().setVisible(true));
    }
}
