package lab_1;

import javafx.application.Application;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.converter.IntegerStringConverter;

public class Five extends Application {
    private final ObservableList<LanguageItem> data = FXCollections.observableArrayList();

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        TableView<LanguageItem> table = new TableView<>();
        table.setEditable(true);

        TableColumn<LanguageItem, String> languageCol = new TableColumn<>("Язык");
        languageCol.setCellValueFactory(cell -> cell.getValue().languageProperty());
        languageCol.setCellFactory(TextFieldTableCell.forTableColumn());
        languageCol.setOnEditCommit(e -> e.getRowValue().setLanguage(e.getNewValue()));

        TableColumn<LanguageItem, String> authorCol = new TableColumn<>("Автор");
        authorCol.setCellValueFactory(cell -> cell.getValue().authorProperty());
        authorCol.setCellFactory(TextFieldTableCell.forTableColumn());
        authorCol.setOnEditCommit(e -> e.getRowValue().setAuthor(e.getNewValue()));

        TableColumn<LanguageItem, Integer> yearCol = new TableColumn<>("Год");
        yearCol.setCellValueFactory(cell -> cell.getValue().yearProperty().asObject());
        yearCol.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()));
        yearCol.setOnEditCommit(e -> e.getRowValue().setYear(e.getNewValue()));

        table.getColumns().addAll(languageCol, authorCol, yearCol); 
        fillStartData();
        table.setItems(data);

        TextField languageField = new TextField();
        languageField.setPromptText("Язык");

        TextField authorField = new TextField();
        authorField.setPromptText("Автор");

        TextField yearField = new TextField();
        yearField.setPromptText("Год");

        Button addButton = new Button("Добавить строку");
        addButton.setOnAction(e -> {
            String language = languageField.getText().trim();
            String author = authorField.getText().trim();
            int year = parseYear(yearField.getText().trim(), 0);

            if (language.isEmpty() || author.isEmpty()) {
                return;
            }

            data.add(new LanguageItem(language, author, year));
            languageField.clear();
            authorField.clear();
            yearField.clear();
        });

        HBox addBox = new HBox(8,
                new Label("Новая запись:"),
                languageField,
                authorField,
                yearField,
                addButton
        );

        CheckBox showLanguage = new CheckBox("Показать язык");
        CheckBox showAuthor = new CheckBox("Показать автора");
        CheckBox showYear = new CheckBox("Показать год");
        showLanguage.setSelected(true);
        showAuthor.setSelected(true);
        showYear.setSelected(true);

        languageCol.visibleProperty().bind(showLanguage.selectedProperty());
        authorCol.visibleProperty().bind(showAuthor.selectedProperty());
        yearCol.visibleProperty().bind(showYear.selectedProperty());

        HBox visibleBox = new HBox(12,
                new Label("Столбцы:"),
                showLanguage,
                showAuthor,
                showYear
        );

        VBox bottom = new VBox(10, addBox, visibleBox);
        bottom.setPadding(new Insets(10));

        BorderPane root = new BorderPane();
        root.setPadding(new Insets(10));
        root.setCenter(table);
        root.setBottom(bottom);   

        Scene scene = new Scene(root, 820, 500);
        stage.setTitle("Лаба 1 — Задание 5");
        stage.setScene(scene);
        stage.show();
    }

    private void fillStartData() {
        data.addAll(
                new LanguageItem("C", "Dennis Ritchie", 1972),
                new LanguageItem("C++", "Bjarne Stroustrup", 1983),
                new LanguageItem("Python", "Guido van Rossum", 1991),
                new LanguageItem("Java", "James Gosling", 1995),
                new LanguageItem("JavaScript", "Brendan Eich", 1995),
                new LanguageItem("C#", "Anders Hejlsberg", 2001),
                new LanguageItem("Scala", "Martin Odersky", 2003)
        );
    }

    private int parseYear(String value, int defaultValue) {
        try {
            return Integer.parseInt(value);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static class LanguageItem {
        private final SimpleStringProperty language;
        private final SimpleStringProperty author;
        private final SimpleIntegerProperty year;

        public LanguageItem(String language, String author, int year) {
            this.language = new SimpleStringProperty(language);
            this.author = new SimpleStringProperty(author);
            this.year = new SimpleIntegerProperty(year);
        }

        public SimpleStringProperty languageProperty() {
            return language;
        }

        public String getLanguage() {
            return language.get();
        }

        public void setLanguage(String value) {
            language.set(value);
        }

        public SimpleStringProperty authorProperty() {
            return author;
        }

        public String getAuthor() {
            return author.get();
        }

        public void setAuthor(String value) {
            author.set(value);
        }

        public SimpleIntegerProperty yearProperty() {
            return year;
        }

        public int getYear() {
            return year.get();
        }

        public void setYear(int value) {
            year.set(value);
        }
    }
}

