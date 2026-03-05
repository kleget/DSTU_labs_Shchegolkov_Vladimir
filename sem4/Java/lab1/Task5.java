import javafx.application.Application;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.converter.IntegerStringConverter;

public class Task5 extends Application {

    private final ObservableList<LangRow> data = FXCollections.observableArrayList(
            new LangRow("C", "Dennis Ritchie", 1972),
            new LangRow("C++", "Bjarne Stroustrup", 1983),
            new LangRow("Python", "Guido van Rossum", 1991),
            new LangRow("Java", "James Gosling", 1995),
            new LangRow("JavaScript", "Brendan Eich", 1995),
            new LangRow("C#", "Anders Hejlsberg", 2001),
            new LangRow("Scala", "Martin Odersky", 2003)
    );

    @Override
    public void start(Stage stage) {
        TableView<LangRow> table = new TableView<>(data);
        table.setEditable(true);

        TableColumn<LangRow, String> colLang = new TableColumn<>("Language");
        colLang.setCellValueFactory(c -> c.getValue().name);
        colLang.setCellFactory(TextFieldTableCell.forTableColumn());
        colLang.setOnEditCommit(e -> e.getRowValue().name.set(e.getNewValue()));

        TableColumn<LangRow, String> colAuthor = new TableColumn<>("Author");
        colAuthor.setCellValueFactory(c -> c.getValue().author);
        colAuthor.setCellFactory(TextFieldTableCell.forTableColumn());
        colAuthor.setOnEditCommit(e -> e.getRowValue().author.set(e.getNewValue()));

        TableColumn<LangRow, Integer> colYear = new TableColumn<>("Year");
        colYear.setCellValueFactory(c -> c.getValue().year.asObject());
        colYear.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()));
        colYear.setOnEditCommit(e -> e.getRowValue().year.set(e.getNewValue()));

        table.getColumns().addAll(colLang, colAuthor, colYear);

        // Add new row controls.
        TextField nameField = new TextField();
        nameField.setPromptText("Language");
        TextField authorField = new TextField();
        authorField.setPromptText("Author");
        TextField yearField = new TextField();
        yearField.setPromptText("Year");
        Button addBtn = new Button("Add");
        addBtn.setOnAction(e -> {
            String n = nameField.getText().trim();
            String a = authorField.getText().trim();
            int y;
            try {
                y = Integer.parseInt(yearField.getText().trim());
            } catch (Exception ex) {
                y = 0;
            }
            if (!n.isEmpty() && !a.isEmpty()) {
                data.add(new LangRow(n, a, y));
                nameField.clear();
                authorField.clear();
                yearField.clear();
            }
        });

        HBox addBox = new HBox(8, nameField, authorField, yearField, addBtn);
        addBox.setPadding(new Insets(10));

        // Column visibility toggles.
        CheckBox showLang = new CheckBox("Show Language");
        showLang.setSelected(true);
        showLang.selectedProperty().addListener((obs, oldV, newV) -> colLang.setVisible(newV));

        CheckBox showAuthor = new CheckBox("Show Author");
        showAuthor.setSelected(true);
        showAuthor.selectedProperty().addListener((obs, oldV, newV) -> colAuthor.setVisible(newV));

        CheckBox showYear = new CheckBox("Show Year");
        showYear.setSelected(true);
        showYear.selectedProperty().addListener((obs, oldV, newV) -> colYear.setVisible(newV));

        VBox rightBox = new VBox(10, showLang, showAuthor, showYear);
        rightBox.setPadding(new Insets(10));

        BorderPane root = new BorderPane();
        root.setCenter(table);
        root.setBottom(addBox);
        root.setRight(rightBox);

        Scene scene = new Scene(root, 900, 500);
        stage.setTitle("Task 5 - TableView");
        stage.setScene(scene);
        stage.show();
    }

    // Simple data holder for one row.
    public static class LangRow {
        SimpleStringProperty name;
        SimpleStringProperty author;
        SimpleIntegerProperty year;

        LangRow(String name, String author, int year) {
            this.name = new SimpleStringProperty(name);
            this.author = new SimpleStringProperty(author);
            this.year = new SimpleIntegerProperty(year);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
