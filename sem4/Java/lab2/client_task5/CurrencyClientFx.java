import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.DatePicker;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class CurrencyClientFx extends Application {
    private final TextField url = new TextField("http://localhost:8080/lab2/currency");
    private final ComboBox<String> type = new ComboBox<>();
    private final ComboBox<String> code = new ComboBox<>();
    private final DatePicker from = new DatePicker(LocalDate.now().minusDays(7));
    private final DatePicker to = new DatePicker(LocalDate.now());
    private final TableView<Row> table = new TableView<>();
    private final NumberAxis xAxis = new NumberAxis();
    private final NumberAxis yAxis = new NumberAxis();
    private final LineChart<Number, Number> chart = new LineChart<>(xAxis, yAxis);
    private final DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd.MM.yyyy");

    @Override
    public void start(Stage stage) {
        type.getItems().addAll("currency", "metal");
        type.getSelectionModel().select("currency");
        updateCodes();
        type.setOnAction(e -> updateCodes());

        TableColumn<Row, String> dateCol = new TableColumn<>("Дата");
        dateCol.setCellValueFactory(new PropertyValueFactory<>("date"));
        TableColumn<Row, String> valueCol = new TableColumn<>("Значение");
        valueCol.setCellValueFactory(new PropertyValueFactory<>("value"));
        table.getColumns().addAll(dateCol, valueCol);
        table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);

        chart.setTitle("Динамика");
        chart.setCreateSymbols(false);
        xAxis.setLabel("Номер точки");
        yAxis.setLabel("Значение");

        GridPane form = new GridPane();
        form.setHgap(8);
        form.setVgap(8);
        form.addRow(0, new Label("Адрес"), url);
        form.addRow(1, new Label("Тип"), type);
        form.addRow(2, new Label("Код"), code);
        form.addRow(3, new Label("Дата с"), from);
        form.addRow(4, new Label("Дата по"), to);

        Button load = new Button("Загрузить");
        load.setOnAction(e -> loadData());

        VBox root = new VBox(10, form, load, new Label("Таблица"), table, chart);
        root.setPadding(new Insets(10));

        stage.setTitle("Лаба 2 - Задание 5");
        stage.setScene(new Scene(root, 900, 720));
        stage.show();
    }

    private void updateCodes() {
        if ("metal".equals(type.getValue())) {
            code.getItems().setAll("AU", "AG", "PT", "PD");
        } else {
            code.getItems().setAll("USD", "EUR", "CNY", "GBP");
        }
        code.getSelectionModel().selectFirst();
    }

    private void loadData() {
        try {
            String q = "type=" + enc(type.getValue())
                    + "&code=" + enc(code.getValue())
                    + "&from=" + enc(fmt.format(from.getValue()))
                    + "&to=" + enc(fmt.format(to.getValue()))
                    + "&format=csv";

            HttpRequest req = HttpRequest.newBuilder(URI.create(url.getText() + "?" + q))
                    .GET()
                    .build();
            String body = HttpClient.newHttpClient()
                    .send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8))
                    .body();

            List<Row> rows = parseCsv(body);
            table.getItems().setAll(rows);

            XYChart.Series<Number, Number> series = new XYChart.Series<>();
            for (int i = 0; i < rows.size(); i++) {
                series.getData().add(new XYChart.Data<>(i + 1, Double.parseDouble(rows.get(i).value)));
            }
            chart.getData().setAll(series);
            chart.setVisible(rows.size() > 1);
        } catch (Exception ex) {
            table.getItems().clear();
            chart.getData().clear();
            chart.setVisible(false);
        }
    }

    private List<Row> parseCsv(String csv) {
        List<Row> rows = new ArrayList<>();
        String[] lines = csv.split("\\R");
        for (int i = 1; i < lines.length; i++) {
            String line = lines[i].trim();
            if (line.isEmpty()) {
                continue;
            }
            String[] parts = line.split(";");
            if (parts.length >= 2) {
                rows.add(new Row(parts[0], parts[1]));
            }
        }
        return rows;
    }

    private static String enc(String s) {
        return URLEncoder.encode(s == null ? "" : s, StandardCharsets.UTF_8);
    }

    public static class Row {
        private final String date;
        private final String value;

        public Row(String date, String value) {
            this.date = date;
            this.value = value;
        }

        public String getDate() {
            return date;
        }

        public String getValue() {
            return value;
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
