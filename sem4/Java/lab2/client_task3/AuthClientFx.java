import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

public class AuthClientFx extends Application {
    private final TextField url = new TextField("http://localhost:8080/lab2/auth");
    private final ComboBox<String> method = new ComboBox<>();
    private final ComboBox<String> action = new ComboBox<>();
    private final TextField login = new TextField();
    private final PasswordField password = new PasswordField();
    private final TextArea output = new TextArea();

    @Override
    public void start(Stage stage) {
        method.getItems().addAll("GET", "POST");
        method.getSelectionModel().select("GET");
        action.getItems().addAll("login", "register");
        action.getSelectionModel().select("login");

        GridPane form = new GridPane();
        form.setHgap(8);
        form.setVgap(8);
        form.addRow(0, new Label("Адрес"), url);
        form.addRow(1, new Label("Метод"), method);
        form.addRow(2, new Label("Действие"), action);
        form.addRow(3, new Label("Логин"), login);
        form.addRow(4, new Label("Пароль"), password);

        Button send = new Button("Отправить");
        send.setOnAction(e -> sendRequest());

        output.setEditable(false);
        output.setPrefRowCount(12);

        VBox root = new VBox(10, form, send, new Label("Ответ сервлета"), output);
        root.setPadding(new Insets(10));

        stage.setTitle("Лаба 2 - Задание 3");
        stage.setScene(new Scene(root, 760, 480));
        stage.show();
    }

    private void sendRequest() {
        try {
            String body = "action=" + enc(action.getValue())
                    + "&login=" + enc(login.getText())
                    + "&password=" + enc(password.getText());

            HttpRequest req;
            if ("POST".equals(method.getValue())) {
                req = HttpRequest.newBuilder(URI.create(url.getText()))
                        .header("Content-Type", "application/x-www-form-urlencoded")
                        .POST(HttpRequest.BodyPublishers.ofString(body))
                        .build();
            } else {
                req = HttpRequest.newBuilder(URI.create(url.getText() + "?" + body))
                        .GET()
                        .build();
            }

            String res = HttpClient.newHttpClient()
                    .send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8))
                    .body();
            output.setText(res);
        } catch (Exception ex) {
            output.setText("Ошибка: " + ex.getMessage());
        }
    }

    private static String enc(String s) {
        return URLEncoder.encode(s == null ? "" : s, StandardCharsets.UTF_8);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
