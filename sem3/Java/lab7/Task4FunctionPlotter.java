package lab7;

import javax.swing.*;
import java.awt.*;
import java.util.function.DoubleUnaryOperator;

public class Task4FunctionPlotter extends JFrame {
    private final JTextField startField = new JTextField("-10", 5);
    private final JTextField endField = new JTextField("10", 5);
    private final JComboBox<String> fnBox = new JComboBox<>(new String[]{
            "sin(x)", "sin(x*x)+cos(x*x)", "2*sin(x)+cos(2*x)"
    });
    private Color color = Color.RED;
    private final Plot plot = new Plot();

    public Task4FunctionPlotter() {
        super("Lab 7 - Task 4");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel top = new JPanel();
        JButton choose = new JButton("Цвет");
        JButton redraw = new JButton("Обновить");
        top.add(new JLabel("От"));
        top.add(startField);
        top.add(new JLabel("До"));
        top.add(endField);
        top.add(fnBox);
        top.add(choose);
        top.add(redraw);
        add(top, BorderLayout.NORTH);
        add(plot, BorderLayout.CENTER);

        choose.addActionListener(e -> {
            Color c = JColorChooser.showDialog(this, "Цвет линии", color);
            if (c != null) color = c;
            plot.repaint();
        });
        redraw.addActionListener(e -> plot.repaint());

        setSize(560, 360);
        setLocationRelativeTo(null);
    }

    private class Plot extends JPanel {
        Plot() { setPreferredSize(new Dimension(500, 280)); setBackground(Color.WHITE); }

        @Override protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            double a = parse(startField.getText(), -10), b = parse(endField.getText(), 10);
            DoubleUnaryOperator fn = pick((String) fnBox.getSelectedItem());
            g.setColor(Color.LIGHT_GRAY); g.drawRect(10,10,getWidth()-20,getHeight()-20);
            g.setColor(color);
            int w=getWidth(), h=getHeight(), n=200;
            double px=a, py=fn.applyAsDouble(px);
            int sx=toX(px,a,b,w), sy=toY(py,h);
            for(int i=1;i<=n;i++){
                double x=a+i*(b-a)/n, y=fn.applyAsDouble(x);
                int nx=toX(x,a,b,w), ny=toY(y,h);
                g.drawLine(sx,sy,nx,ny);
                sx=nx; sy=ny;
            }
        }
        int toX(double x,double a,double b,int w){ return (int)(10+(x-a)/(b-a)*(w-20)); }
        int toY(double y,int h){ double k=Math.max(-1,Math.min(1,y)); return (int)(10+(1-(k+1)/2)*(h-20)); }
    }

    private static double parse(String s,double d){ try{ return Double.parseDouble(s);}catch(Exception e){return d;} }
    private DoubleUnaryOperator pick(String n){
        if("sin(x*x)+cos(x*x)".equals(n)) return x->Math.sin(x*x)+Math.cos(x*x);
        if("2*sin(x)+cos(2*x)".equals(n)) return x->2*Math.sin(x)+Math.cos(2*x);
        return Math::sin;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task4FunctionPlotter().setVisible(true));
    }
}
