package lab7;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Task3BallController extends JFrame {
    public Task3BallController() {
        super("Lab 7 - Task 3");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        BallPanel panel = new BallPanel();
        add(panel, BorderLayout.CENTER);

        JSpinner max = new JSpinner(new SpinnerNumberModel(5, 1, 20, 1));
        JLabel info = new JLabel("0 / 5");
        JButton add = new JButton("Добавить");
        JButton toggle = new JButton("Пауза");

        JPanel controls = new JPanel();
        controls.add(new JLabel("Макс:"));
        controls.add(max);
        controls.add(add);
        controls.add(toggle);
        controls.add(info);
        add(controls, BorderLayout.SOUTH);

        max.addChangeListener(e -> { panel.setMax((int) max.getValue()); info.setText(panel.count()+" / "+panel.getMax()); });
        add.addActionListener(e -> { panel.addBall(); info.setText(panel.count()+" / "+panel.getMax()); });
        toggle.addActionListener(e -> { panel.toggle(); toggle.setText(panel.running()?"Пауза":"Старт"); });

        setSize(420,300);
        setLocationRelativeTo(null);
    }

    private static class BallPanel extends JPanel {
        private final List<Ball> balls = new ArrayList<>();
        private final Timer timer;
        private final Random rnd = new Random();
        private int max = 5;
        private boolean run = true;

        BallPanel() {
            setPreferredSize(new Dimension(380,220));
            setBackground(Color.WHITE);
            timer = new Timer(16, e -> { if(run) move(); repaint(); });
            timer.start();
        }

        void setMax(int m){ max=m; while(balls.size()>max) balls.remove(balls.size()-1); }
        int getMax(){ return max; }
        int count(){ return balls.size(); }
        boolean running(){ return run; }
        void toggle(){ run=!run; }

        void addBall() {
            if (balls.size()>=max) return;
            int s=20;
            balls.add(new Ball(rnd.nextInt(Math.max(1,getWidth()-s)), rnd.nextInt(Math.max(1,getHeight()-s)),
                    rnd.nextDouble()*4-2, rnd.nextDouble()*4-2, s));
        }

        private void move() {
            int w=getWidth(), h=getHeight();
            for (Ball b: balls) {
                b.x+=b.dx; b.y+=b.dy;
                if(b.x<0||b.x+b.size>w) b.dx=-b.dx;
                if(b.y<0||b.y+b.size>h) b.dy=-b.dy;
            }
        }

        @Override protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.setColor(Color.ORANGE);
            for (Ball b: balls) g.fillOval((int)b.x,(int)b.y,b.size,b.size);
        }
    }

    private static class Ball {
        double x, y, dx, dy;
        int size;
        Ball(double x, double y, double dx, double dy, int size){ this.x=x; this.y=y; this.dx=dx; this.dy=dy; this.size=size; }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task3BallController().setVisible(true));
    }
}
