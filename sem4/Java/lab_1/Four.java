package lab_1;

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
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.function.DoubleUnaryOperator;

public class Four extends Application {
    private final NumberAxis xAxis = new NumberAxis();
    private final NumberAxis yAxis = new NumberAxis();
    private final LineChart<Number, Number> chart = new LineChart<>(xAxis, yAxis);

    private final FunctionRow f1 = new FunctionRow("y(x) = sin(x)", Math::sin);
    private final FunctionRow f2 = new FunctionRow("y(x) = cos(x) - 2 * sin(x)", x -> Math.cos(x) - 2 * Math.sin(x));
    private final FunctionRow f3 = new FunctionRow("y(x) = sin(x * x)", x -> Math.sin(x * x));

    private final TextField minField = new TextField("-3.14");
    private final TextField maxField = new TextField("3.14");
    private final TextField stepField = new TextField("0.1");

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        chart.setTitle("Линейные графики");
        chart.setCreateSymbols(false);
        chart.setAnimated(false);

        xAxis.setLabel("Аргумент");
        yAxis.setLabel("Функция");

        BorderPane root = new BorderPane();
        root.setPadding(new Insets(10));
        root.setCenter(chart);
        root.setBottom(createControls());

        rebuildChart();

        Scene scene = new Scene(root, 900, 600);
        stage.setTitle("Лаба 1 - Задание 4");
        stage.setScene(scene);
        stage.show();
    }

    private VBox createControls() {
        GridPane functionsGrid = new GridPane();
        functionsGrid.setHgap(8);
        functionsGrid.setVgap(6);

        addFunctionRow(functionsGrid, 0, f1);
        addFunctionRow(functionsGrid, 1, f2);
        addFunctionRow(functionsGrid, 2, f3);

        HBox rangeBox = new HBox(8,
                new Label("мин"), minField,
                new Label("макс"), maxField,
                new Label("шаг"), stepField
        );

        Button buildButton = new Button("Построить");
        buildButton.setOnAction(e -> rebuildChart());

        VBox controls = new VBox(10,
                new Label("Функции (показывать + толщина линии):"),
                functionsGrid,
                rangeBox,
                buildButton
        );
        controls.setPadding(new Insets(10, 0, 0, 0));
        return controls;
    }

    private void addFunctionRow(GridPane grid, int row, FunctionRow functionRow) {
        functionRow.showBox.setSelected(true);
        functionRow.widthField.setPrefColumnCount(4);

        grid.add(functionRow.showBox, 0, row);
        grid.add(new Label(functionRow.name), 1, row);
        grid.add(new Label("толщина"), 2, row);
        grid.add(functionRow.widthField, 3, row);
    }

    private void rebuildChart() {
        double minX = parseDouble(minField.getText(), -3.14);
        double maxX = parseDouble(maxField.getText(), 3.14);
        double step = parseDouble(stepField.getText(), 0.1);

        if (maxX <= minX) {
            maxX = minX + 1;
            maxField.setText(String.valueOf(maxX));
        }
        if (step <= 0) {
            step = 0.1;
            stepField.setText("0.1");
        }

        xAxis.setAutoRanging(false);
        xAxis.setLowerBound(minX);
        xAxis.setUpperBound(maxX);
        xAxis.setTickUnit((maxX - minX) / 10.0);

        yAxis.setAutoRanging(true);
        chart.getData().clear();

        addSeriesIfSelected(f1, minX, maxX, step);
        addSeriesIfSelected(f2, minX, maxX, step);
        addSeriesIfSelected(f3, minX, maxX, step);
    }

    private void addSeriesIfSelected(FunctionRow functionRow, double minX, double maxX, double step) {
        if (!functionRow.showBox.isSelected()) {
            return;
        }

        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName(functionRow.name);

        for (double x = minX; x <= maxX; x += step) {
            series.getData().add(new XYChart.Data<>(x, functionRow.formula.applyAsDouble(x)));
        }

        chart.getData().add(series);

        double width = parseDouble(functionRow.widthField.getText(), 2.0);
        if (width < 1) {
            width = 1;
            functionRow.widthField.setText("1");
        }

        double finalWidth = width;
        series.nodeProperty().addListener((obs, oldNode, newNode) -> {
            if (newNode != null) {
                newNode.setStyle("-fx-stroke-width: " + finalWidth + ";");
            }
        });

        Platform.runLater(() -> {
            if (series.getNode() != null) {
                series.getNode().setStyle("-fx-stroke-width: " + finalWidth + ";");
            }
        });
    }

    private static double parseDouble(String text, double defaultValue) {
        try {
            return Double.parseDouble(text.trim());
        } catch (Exception e) {
            return defaultValue;
        }
    }

    private static class FunctionRow {
        final String name;
        final DoubleUnaryOperator formula;
        final CheckBox showBox = new CheckBox("показывать");
        final TextField widthField = new TextField("2");

        FunctionRow(String name, DoubleUnaryOperator formula) {
            this.name = name;
            this.formula = formula;
        }
    }
}

