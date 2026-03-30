package lab_1;

import javafx.application.Application;
import javafx.embed.swing.SwingFXUtils;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Toggle;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.image.WritableImage;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class One extends Application {
    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        BorderPane root = new BorderPane();

        Pane drawingPane = new Pane();
        drawingPane.setPrefSize(800, 600);
        drawingPane.setStyle("-fx-background-color: white;");

        VBox paletteVBox = new VBox(8);

        Button saveButton = new Button("Сохранить");

        ToggleGroup group = new ToggleGroup();

        ToggleButton catBtn = createIconToggle("images/cat.png", group, 64);
        ToggleButton carBtn = createIconToggle("images/car.png", group, 64);
        ToggleButton treeBtn = createIconToggle("images/tree.png", group, 64);

        paletteVBox.getChildren().addAll(catBtn, carBtn, treeBtn);

        drawingPane.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.SECONDARY) {
                Toggle selected = group.getSelectedToggle();
                System.out.println(selected);
                Image img = (Image) selected.getUserData();
                ImageView placed = new ImageView(img);
                placed.setFitWidth(128);
                placed.setFitHeight(128);
                placed.setPreserveRatio(true);
                placed.setLayoutX(e.getX() - 32);
                placed.setLayoutY(e.getY() - 32);
                drawingPane.getChildren().add(placed);
            }
        });

        saveButton.setOnAction(e -> {
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Сохранить");
            fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("PNG", "*.png"));
            fileChooser.setInitialFileName("картинка.png");

            File file = fileChooser.showSaveDialog(primaryStage);
            if (file == null) {
                return;
            }

            WritableImage image = drawingPane.snapshot(null, null);
            BufferedImage bimg = SwingFXUtils.fromFXImage(image, null);
            try {
                ImageIO.write(bimg, "png", file);
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        });

        root.setLeft(paletteVBox);
        root.setCenter(drawingPane);
        root.setBottom(saveButton);

        primaryStage.setScene(new Scene(root));
        primaryStage.setTitle("Лаба 1 — Задание 1");
        primaryStage.show();
    }

    private ToggleButton createIconToggle(String resourceName, ToggleGroup group, double size) {
        Image image = new Image(getClass().getResourceAsStream(resourceName));
        ImageView imageView = new ImageView(image);
        imageView.setFitWidth(size);
        imageView.setFitHeight(size);
        imageView.setPreserveRatio(true);
        ToggleButton button = new ToggleButton();
        button.setGraphic(imageView);
        button.setToggleGroup(group);
        button.setUserData(image);
        return button;
    }
}

