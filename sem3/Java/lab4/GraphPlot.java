package lab4;

import java.util.ArrayList;
import java.util.List;

public class GraphPlot {
    private final String title;
    private final Axis xAxis;
    private final Axis yAxis;
    private final Grid grid;
    private final List<Curve> curves = new ArrayList<>();
    private final List<String> notes = new ArrayList<>();

    public GraphPlot(String title, Axis xAxis, Axis yAxis, Grid grid) {
        this.title = title;
        this.xAxis = xAxis;
        this.yAxis = yAxis;
        this.grid = grid;
    }

    public void addCurve(Curve curve) {
        curves.add(curve);
    }

    public void addNote(String note) {
        notes.add(note);
    }

    public void renderText() {
        System.out.println("=== Plot ===");
        System.out.println("Title: " + title);
        System.out.println("X: " + xAxis.describe());
        System.out.println("Y: " + yAxis.describe());
        System.out.println("Grid: " + grid.describe());
        System.out.println("Curves:");
        if (curves.isEmpty()) {
            System.out.println(" (none)");
        } else {
            for (Curve curve : curves) {
                System.out.println(" - " + curve.describe());
            }
        }
        if (!notes.isEmpty()) {
            System.out.println("Notes:");
            for (String note : notes) {
                System.out.println(" * " + note);
            }
        }
        System.out.println("============");
    }
}
