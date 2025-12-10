package lab7;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

/**
 * Минимальные компоненты: панель с тремя метками и простая "кость".
 */
public class CustomComponents {
    public static class ThreeLabelPanel extends JPanel {
        private final JLabel top = new JLabel("Top");
        private final JLabel center = new JLabel("Center", SwingConstants.CENTER);
        private final JLabel bottom = new JLabel("Bottom", SwingConstants.RIGHT);

        public ThreeLabelPanel() {
            setLayout(new BorderLayout());
            top.setFont(new Font("dialog", Font.BOLD | Font.ITALIC, 10));
            bottom.setFont(new Font("dialog", Font.BOLD | Font.ITALIC, 10));
            center.setFont(new Font("dialog", Font.BOLD, 18));
            add(top, BorderLayout.NORTH);
            add(center, BorderLayout.CENTER);
            add(bottom, BorderLayout.SOUTH);
        }

        public void setPanelBackground(Color c) {
            setBackground(c);
            top.setOpaque(true);
            center.setOpaque(true);
            bottom.setOpaque(true);
            top.setBackground(c);
            center.setBackground(c);
            bottom.setBackground(c);
        }

        public void setUpperText(String text) { top.setText(text); }
        public void setCenterText(String text) { center.setText(text); }
        public void setDownText(String text) { bottom.setText(text); }
    }

    public static class SimpleDie extends JComponent {
        private final Random rnd = new Random();
        private int value = 1;
        private boolean active = true;
        private Color pip = Color.BLACK, face = Color.WHITE;

        public SimpleDie() {
            setPreferredSize(new Dimension(80, 80));
            addMouseListener(new MouseAdapter() {
                @Override public void mouseClicked(MouseEvent e) { if (active) roll(); }
            });
        }

        public void roll() { setValue(rnd.nextInt(6) + 1); }
        public void setValue(int v) { if (v>=1&&v<=6){ value=v; repaint(); } }
        public int getValue() { return value; }
        public void setPipColor(Color c){ pip=c; repaint(); }
        public void setFaceColor(Color c){ face=c; repaint(); }
        public void setActive(boolean a){ active=a; }
        public boolean isActive(){ return active; }

        @Override protected void paintComponent(Graphics g) {
            int s = Math.min(getWidth(), getHeight()) - 10;
            int x = (getWidth()-s)/2, y=(getHeight()-s)/2, r=Math.max(4,s/12);
            g.setColor(face); g.fillRoundRect(x,y,s,s,10,10);
            g.setColor(Color.BLACK); g.drawRoundRect(x,y,s,s,10,10);
            g.setColor(pip);
            boolean[][] m={
                    {false,false,false,false,true,false,false,false,false},
                    {true,false,false,false,false,false,false,false,true},
                    {true,false,false,false,true,false,false,false,true},
                    {true,false,true,false,false,false,true,false,true},
                    {true,false,true,false,true,false,true,false,true},
                    {true,true,true,true,false,true,true,true,true}};
            int step=s/4;
            for(int i=0;i<3;i++) for(int j=0;j<3;j++)
                if(m[value-1][i*3+j]) g.fillOval(x+step*(j+1)-r, y+step*(i+1)-r, 2*r,2*r);
        }
    }

    public static class CustomComponentsDemo extends JFrame {
        public CustomComponentsDemo() {
            super("Components demo");
            setDefaultCloseOperation(EXIT_ON_CLOSE);
            setLayout(new BorderLayout());

            ThreeLabelPanel labels = new ThreeLabelPanel();
            labels.setPanelBackground(new Color(230,230,255));
            labels.setUpperText("Upper");
            labels.setCenterText("Center");
            labels.setDownText("Lower");

            SimpleDie die = new SimpleDie();
            JButton toggle = new JButton("Отключить");
            toggle.addActionListener(e -> {
                die.setActive(!die.isActive());
                toggle.setText(die.isActive() ? "Отключить" : "Включить");
            });

            add(labels, BorderLayout.NORTH);
            add(die, BorderLayout.CENTER);
            add(toggle, BorderLayout.SOUTH);
            setSize(260,220);
            setLocationRelativeTo(null);
        }

        public static void main(String[] args) {
            SwingUtilities.invokeLater(() -> new CustomComponentsDemo().setVisible(true));
        }
    }
}
