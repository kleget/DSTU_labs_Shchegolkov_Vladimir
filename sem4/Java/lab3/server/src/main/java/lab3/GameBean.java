package lab3;

import java.io.Serializable;

public class GameBean implements Serializable {
    private String[] cells = new String[9];
    private boolean over;
    private String message;

    public GameBean() {
        reset();
    }

    public void reset() {
        cells = new String[]{"", "", "", "", "", "", "", "", ""};
        over = false;
        message = "Ваш ход. Вы играете крестиками.";
    }

    public void playerMove(int row, int col) {
        if (over) {
            return;
        }
        int index = (row - 1) * 3 + (col - 1);
        if (index < 0 || index >= 9 || !cells[index].isEmpty()) {
            message = "Некорректный ход.";
            return;
        }
        cells[index] = "X";
        if (finishAfterMove("X")) {
            return;
        }
        serverMove();
        finishAfterMove("O");
    }

    private void serverMove() {
        for (int i = 0; i < cells.length; i++) {
            if (cells[i].isEmpty()) {
                cells[i] = "O";
                message = "Сервер сделал ход. Ваш ход.";
                return;
            }
        }
    }

    private boolean finishAfterMove(String mark) {
        if (wins(mark)) {
            over = true;
            message = "X".equals(mark) ? "Вы победили." : "Победил сервер.";
            return true;
        }
        if (draw()) {
            over = true;
            message = "Ничья.";
            return true;
        }
        return false;
    }

    private boolean wins(String mark) {
        int[][] lines = {
                {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
                {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
                {0, 4, 8}, {2, 4, 6}
        };
        for (int[] line : lines) {
            if (mark.equals(cells[line[0]]) && mark.equals(cells[line[1]]) && mark.equals(cells[line[2]])) {
                return true;
            }
        }
        return false;
    }

    private boolean draw() {
        for (String cell : cells) {
            if (cell.isEmpty()) {
                return false;
            }
        }
        return true;
    }

    public String[] getCells() {
        return cells;
    }

    public void setCells(String[] cells) {
        this.cells = cells;
    }

    public boolean isOver() {
        return over;
    }

    public void setOver(boolean over) {
        this.over = over;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
