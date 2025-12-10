package lab7;

import javax.swing.*;
import java.awt.*;

public class Task8SimpleGame extends JFrame {
    private final int[] board = {0,5,-3,0,0,10,-10,0,0,15,-20,0,0,0,0};
    private final boolean[] repeat = {false,false,true,false,false,false,false,false,false,false,false,false,false,true,false};
    private final boolean[] loseAll = {false,false,false,false,false,false,false,false,true,false,false,false,false,false,false};

    private final CustomComponents.SimpleDie d1 = new CustomComponents.SimpleDie();
    private final CustomComponents.SimpleDie d2 = new CustomComponents.SimpleDie();
    private final JLabel s1 = new JLabel(), s2 = new JLabel();
    private final JTextArea log = new JTextArea(8,30);
    private int p1=0,p2=0, sc1=0, sc2=0, turn=1;
    private boolean done=false;

    public Task8SimpleGame() {
        super("Lab 7 - Task 8");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel top=new JPanel(new GridLayout(2,1));
        top.add(s1); top.add(s2);
        add(top,BorderLayout.NORTH);

        log.setEditable(false);
        add(new JScrollPane(log),BorderLayout.CENTER);

        JButton roll=new JButton("Бросить");
        JButton reset=new JButton("Сброс");
        JPanel bottom=new JPanel(new GridLayout(2,2,5,5));
        bottom.add(d1); bottom.add(d2); bottom.add(roll); bottom.add(reset);
        add(bottom,BorderLayout.SOUTH);

        roll.addActionListener(e->roll());
        reset.addActionListener(e->reset());

        reset();
        setSize(420,360);
        setLocationRelativeTo(null);
    }

    private void roll(){
        if(done){ log("Игра завершена."); return; }
        CustomComponents.SimpleDie d=turn==1?d1:d2;
        d.roll();
        int v=d.getValue();
        log("Игрок "+turn+" бросил "+v);
        move(v);
    }

    private void move(int steps){
        if(turn==1){ p1=Math.min(board.length-1,p1+steps); apply(1); }
        else { p2=Math.min(board.length-1,p2+steps); apply(2); }
        updateLabels();
        if(done) return;
        boolean extra = turn==1 ? repeat[p1] : repeat[p2];
        if(extra) log("Игрок "+turn+" ходит еще раз");
        else turn = 3 - turn;
    }

    private void apply(int player){
        int pos = player==1 ? p1 : p2;
        int delta = board[pos];
        if(loseAll[pos]){
            if(player==1) sc1=0; else sc2=0;
            log("Игрок "+player+" потерял все очки");
        } else if(delta!=0){
            if(player==1) sc1+=delta; else sc2+=delta;
            log("Изменение очков игрока "+player+": "+delta);
        }
        if(pos==board.length-1){
            if(player==1) sc1+=50; else sc2+=50;
            done=true;
            log("Финиш! Игрок "+player+" получает +50.");
            announce();
        }
    }

    private void announce(){
        if(sc1>sc2) log("Победил игрок 1 ("+sc1+")");
        else if(sc2>sc1) log("Победил игрок 2 ("+sc2+")");
        else log("Ничья ("+sc1+")");
    }

    private void reset(){
        p1=p2=0; sc1=sc2=0; turn=1; done=false;
        log.setText("");
        log("Новая игра. Начинает игрок 1.");
        updateLabels();
    }

    private void updateLabels(){
        s1.setText("Игрок 1: позиция "+p1+" / очки "+sc1);
        s2.setText("Игрок 2: позиция "+p2+" / очки "+sc2);
    }

    private void log(String msg){ log.append(msg+System.lineSeparator()); }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task8SimpleGame().setVisible(true));
    }
}
