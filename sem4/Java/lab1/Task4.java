import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.Spinner;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Task4 extends Application {

    private LineChart<Number, Number> chart;
    private CheckBox sinBox;
    private CheckBox cosBox;
    private CheckBox quadBox;
    private TextField minField;
    private TextField maxField;
    private TextField stepField;
    private Spinner<Double> widthSpinner;

    @Override
    public void start(Stage stage) {
        NumberAxis xAxis = new NumberAxis();
        NumberAxis yAxis = new NumberAxis();
        chart = new LineChart<>(xAxis, yAxis);
        chart.setCreateSymbols(false);
        chart.setAnimated(false);
        chart.setTitle("Function Graphs");

        sinBox = new CheckBox("sin(x)");
        cosBox = new CheckBox("cos(x)");
        quadBox = new CheckBox("x^2");
        sinBox.setSelected(true);

        minField = new TextField("-10");
        maxField = new TextField("10");
        stepField = new TextField("0.5");

        widthSpinner = new Spinner<>(1.0, 6.0, 2.0, 0.5);
        widthSpinner.setEditable(true);

        Button plotBtn = new Button("Plot");
        plotBtn.setOnAction(e -> plot());

        VBox controls = new VBox(10,
                new Label("Functions"),
                sinBox, cosBox, quadBox,
                new Label("Min X"), minField,
                new Label("Max X"), maxField,
                new Label("Step"), stepField,
                new Label("Line width"), widthSpinner,
                plotBtn
        );
        controls.setPadding(new Insets(10));

        BorderPane root = new BorderPane();
        root.setLeft(controls);
        root.setCenter(chart);

        Scene scene = new Scene(root, 900, 600);
        stage.setTitle("Task 4 - Graphs");
        stage.setScene(scene);
        stage.show();

        plot();
    }

    private void plot() {
        double minX = parseDouble(minField.getText(), -10);
        double maxX = parseDouble(maxField.getText(), 10);
        double step = parseDouble(stepField.getText(), 0.5);
        if (step <= 0) {
            step = 0.5;
        }
        if (maxX <= minX) {
            double tmp = minX;
            minX = maxX;
            maxX = tmp;
        }

        chart.getData().clear();

        if (sinBox.isSelected()) {
            chart.getData().add(buildSeries("sin(x)", minX, maxX, step, Math::sin));
        }
        if (cosBox.isSelected()) {
            chart.getData().add(buildSeries("cos(x)", minX, maxX, step, Math::cos));
        }
        if (quadBox.isSelected()) {
            chart.getData().add(buildSeries("x^2", minX, maxX, step, x -> x * x));
        }

        double width = widthSpinner.getValue();
        Platform.runLater(() -> {
            for (XYChart.Series<Number, Number> s : chart.getData()) {
                if (s.getNode() != null) {
                    s.getNode().setStyle("-fx-stroke-width: " + width + ";");
                }
            }
        });
    }

    private XYChart.Series<Number, Number> buildSeries(String name, double minX, double maxX,
                                                       double step, Function f) {
        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName(name);
        for (double x = minX; x <= maxX; x += step) {
            series.getData().add(new XYChart.Data<>(x, f.eval(x)));
        }
        return series;
    }

    private double parseDouble(String text, double fallback) {
        try {
            return Double.parseDouble(text.trim());
        } catch (Exception ex) {
            return fallback;
        }
    }

    // Simple functional interface to avoid extra imports.
    private interface Function {
        double eval(double x);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
