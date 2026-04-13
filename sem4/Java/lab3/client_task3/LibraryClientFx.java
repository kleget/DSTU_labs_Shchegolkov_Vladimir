import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
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
import java.util.ArrayList;
import java.util.List;

public class LibraryClientFx extends Application {
    private final TextField url = new TextField("http://localhost:8080/lab3/api/books");
    private final TextField filterGenre = new TextField();
    private final TextField title = new TextField();
    private final TextField author = new TextField();
    private final TextField genre = new TextField();
    private final TextField year = new TextField();
    private final Label status = new Label();
    private final TableView<Row> table = new TableView<>();
    private final HttpClient http = HttpClient.newHttpClient();

    @Override
    public void start(Stage stage) {
        table.getColumns().add(column("ID", "id"));
        table.getColumns().add(column("Название", "title"));
        table.getColumns().add(column("Автор", "author"));
        table.getColumns().add(column("Жанр", "genre"));
        table.getColumns().add(column("Год", "year"));
        table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);

        GridPane form = new GridPane();
        form.setHgap(8);
        form.setVgap(8);
        form.addRow(0, new Label("API"), url);
        form.addRow(1, new Label("Фильтр жанра"), filterGenre);
        form.addRow(2, new Label("Название"), title);
        form.addRow(3, new Label("Автор"), author);
        form.addRow(4, new Label("Жанр"), genre);
        form.addRow(5, new Label("Год"), year);

        Button load = new Button("Загрузить");
        load.setOnAction(e -> loadData());
        Button add = new Button("Добавить");
        add.setOnAction(e -> sendAction("add", ""));
        Button delete = new Button("Удалить выбранную");
        delete.setOnAction(e -> {
            Row row = table.getSelectionModel().getSelectedItem();
            if (row != null) {
                sendAction("delete", row.id);
            }
        });

        VBox root = new VBox(10, form, load, add, delete, status, table);
        root.setPadding(new Insets(10));

        stage.setTitle("Лабораторная 3 - задание 3");
        stage.setScene(new Scene(root, 900, 620));
        stage.show();
        loadData();
    }

    private TableColumn<Row, String> column(String title, String property) {
        TableColumn<Row, String> col = new TableColumn<>(title);
        col.setCellValueFactory(new PropertyValueFactory<>(property));
        return col;
    }

    private void loadData() {
        try {
            String requestUrl = url.getText() + "?genre=" + enc(filterGenre.getText());
            HttpRequest req = HttpRequest.newBuilder(URI.create(requestUrl)).GET().build();
            String body = http.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)).body();
            table.getItems().setAll(parseCsv(body));
            status.setText("Данные загружены.");
        } catch (Exception e) {
            status.setText("Ошибка загрузки: " + e.getMessage());
        }
    }

    private void sendAction(String action, String id) {
        try {
            String body = "action=" + enc(action)
                    + "&id=" + enc(id)
                    + "&title=" + enc(title.getText())
                    + "&author=" + enc(author.getText())
                    + "&genre=" + enc(genre.getText())
                    + "&year=" + enc(year.getText());
            HttpRequest req = HttpRequest.newBuilder(URI.create(url.getText()))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build();
            String answer = http.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)).body();
            status.setText(answer);
            loadData();
        } catch (Exception e) {
            status.setText("Ошибка запроса: " + e.getMessage());
        }
    }

    private List<Row> parseCsv(String csv) {
        List<Row> rows = new ArrayList<>();
        String[] lines = csv.split("\\R");
        for (int i = 1; i < lines.length; i++) {
            String[] p = lines[i].split(";", -1);
            if (p.length >= 5) {
                rows.add(new Row(p[0], p[1], p[2], p[3], p[4]));
            }
        }
        return rows;
    }

    private static String enc(String s) {
        return URLEncoder.encode(s == null ? "" : s, StandardCharsets.UTF_8);
    }

    public static class Row {
        private final String id;
        private final String title;
        private final String author;
        private final String genre;
        private final String year;

        public Row(String id, String title, String author, String genre, String year) {
            this.id = id;
            this.title = title;
            this.author = author;
            this.genre = genre;
            this.year = year;
        }

        public String getId() {
            return id;
        }

        public String getTitle() {
            return title;
        }

        public String getAuthor() {
            return author;
        }

        public String getGenre() {
            return genre;
        }

        public String getYear() {
            return year;
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
