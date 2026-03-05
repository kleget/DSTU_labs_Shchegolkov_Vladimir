import javafx.application.Application;
import javafx.embed.swing.SwingFXUtils;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.SnapshotParameters;
import javafx.scene.control.Button;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox; 
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;

public class Task1 extends Application {

    @Override
    public void start(Stage stage) {
        // Left panel with ToggleButtons and the Save button.
        ToggleGroup group = new ToggleGroup();
        VBox leftPanel = new VBox(10);
        leftPanel.setPadding(new Insets(10));

        ToggleButton b1 = createImageToggle("assets/img_circle.png", group);
        ToggleButton b2 = createImageToggle("assets/img_square.png", group);
        ToggleButton b3 = createImageToggle("assets/img_triangle.png", group);

        Button saveButton = new Button("Save");
        leftPanel.getChildren().addAll(b1, b2, b3, saveButton);

        // Drawing area.
        Pane canvas = new Pane();
        canvas.setPrefSize(640, 480);
        canvas.setStyle("-fx-background-color: white; -fx-border-color: #999;");

        // Right-click adds the selected image to the canvas.
        canvas.setOnMouseClicked(e -> {
            if (e.getButton() != MouseButton.SECONDARY) {
                return;
            }
            ToggleButton selected = (ToggleButton) group.getSelectedToggle();
            if (selected == null) {
                return;
            }
            Image img = (Image) selected.getUserData();
            ImageView view = new ImageView(img);
            // Place the image with its center at the cursor position.
            view.setLayoutX(e.getX() - img.getWidth() / 2.0);
            view.setLayoutY(e.getY() - img.getHeight() / 2.0);
            canvas.getChildren().add(view);
        });

        // Save button: snapshot the canvas and write to file.
        saveButton.setOnAction(e -> saveCanvas(stage, canvas));

        BorderPane root = new BorderPane();
        root.setLeft(leftPanel);
        root.setCenter(canvas);

        Scene scene = new Scene(root);
        stage.setTitle("Task 1 - Image Composer");
        stage.setScene(scene);
        stage.show();
    }

    private ToggleButton createImageToggle(String relativePath, ToggleGroup group) {
        // Try local path first, then a path relative to the project root.
        File file = new File(relativePath);
        if (!file.exists()) {
            file = new File("sem4/Java/lab1/" + relativePath);
        }
        Image img = new Image(file.toURI().toString());
        ImageView view = new ImageView(img);

        ToggleButton button = new ToggleButton();
        button.setGraphic(view);
        button.setToggleGroup(group);
        // Store the image so we can use it later.
        button.setUserData(img);
        return button;
    }

    private void saveCanvas(Stage stage, Pane canvas) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Save Image");
        chooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("PNG Image", "*.png"),
                new FileChooser.ExtensionFilter("JPG Image", "*.jpg", "*.jpeg"),
                new FileChooser.ExtensionFilter("GIF Image", "*.gif")
        );
        File file = chooser.showSaveDialog(stage);
        if (file == null) {
            return;
        }

        String ext = getExtension(file);
        if (ext == null) {
            file = new File(file.getAbsolutePath() + ".png");
            ext = "png";
        }

        // Snapshot the canvas.
        SnapshotParameters params = new SnapshotParameters();
        try {
            Image snapshot = canvas.snapshot(params, null);
            ImageIO.write(SwingFXUtils.fromFXImage(snapshot, null), ext, file);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private String getExtension(File file) {
        String name = file.getName();
        int dot = name.lastIndexOf('.');
        if (dot < 0 || dot == name.length() - 1) {
            return null;
        }
        return name.substring(dot + 1).toLowerCase();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
