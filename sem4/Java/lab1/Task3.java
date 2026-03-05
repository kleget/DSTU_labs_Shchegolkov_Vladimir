import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.WritableImage;
import javafx.scene.input.KeyCode;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import javafx.embed.swing.SwingFXUtils;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Task3 extends Application {

    private Pane drawingPane;
    private ToggleGroup paletteGroup;
    private ColorPicker strokePicker;
    private ColorPicker fillPicker;
    private ChoiceBox<String> lineStyleChoice;
    private Spinner<Double> lineWidthSpinner;
    private TextField imageWidthField;
    private TextField imageHeightField;

    private final List<DrawableItem> items = new ArrayList<>();
    private DrawableItem currentItem;

    @Override
    public void start(Stage stage) {
        BorderPane root = new BorderPane();

        // Menu.
        MenuItem saveItem = new MenuItem("Save...");
        saveItem.setOnAction(e -> saveDrawing(stage));
        MenuItem exitItem = new MenuItem("Exit");
        exitItem.setOnAction(e -> stage.close());
        Menu fileMenu = new Menu("File", null, saveItem, exitItem);

        MenuItem helpItem = new MenuItem("Instruction");
        helpItem.setOnAction(e -> showHelp());
        Menu helpMenu = new Menu("Help", null, helpItem);

        MenuBar menuBar = new MenuBar(fileMenu, helpMenu);
        root.setTop(menuBar);

        // Left palette.
        paletteGroup = new ToggleGroup();
        ToggleButton lineBtn = new ToggleButton("Line");
        lineBtn.setUserData("LINE");
        lineBtn.setToggleGroup(paletteGroup);
        ToggleButton rectBtn = new ToggleButton("Rectangle");
        rectBtn.setUserData("RECT");
        rectBtn.setToggleGroup(paletteGroup);
        ToggleButton ellipseBtn = new ToggleButton("Ellipse");
        ellipseBtn.setUserData("ELLIPSE");
        ellipseBtn.setToggleGroup(paletteGroup);
        rectBtn.setSelected(true);

        VBox palette = new VBox(10, new Label("Palette"), lineBtn, rectBtn, ellipseBtn);
        palette.setPadding(new Insets(10));
        root.setLeft(palette);

        // Right control panel.
        strokePicker = new ColorPicker(Color.BLACK);
        fillPicker = new ColorPicker(Color.LIGHTGRAY);
        lineStyleChoice = new ChoiceBox<>();
        lineStyleChoice.getItems().addAll("Solid", "Dashed", "Dotted");
        lineStyleChoice.setValue("Solid");

        lineWidthSpinner = new Spinner<>(1.0, 10.0, 2.0, 0.5);
        lineWidthSpinner.setEditable(true);

        imageWidthField = new TextField("800");
        imageHeightField = new TextField("600");

        VBox controls = new VBox(10,
                new Label("Stroke color"), strokePicker,
                new Label("Fill color"), fillPicker,
                new Label("Line style"), lineStyleChoice,
                new Label("Line width"), lineWidthSpinner,
                new Label("Image width (px)"), imageWidthField,
                new Label("Image height (px)"), imageHeightField
        );
        controls.setPadding(new Insets(10));
        root.setRight(controls);

        // Drawing area.
        drawingPane = new Pane();
        drawingPane.setPrefSize(800, 600);
        drawingPane.setStyle("-fx-background-color: white; -fx-border-color: #999;");
        root.setCenter(drawingPane);

        // Right-click adds a new primitive.
        drawingPane.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.SECONDARY) {
                addPrimitive(e.getX(), e.getY());
            }
        });

        Scene scene = new Scene(root);
        scene.setOnKeyPressed(e -> handleKey(e.getCode()));
        stage.setTitle("Task 3 - Simple Graphic Editor");
        stage.setScene(scene);
        stage.show();
    }

    private void addPrimitive(double x, double y) {
        Toggle selected = paletteGroup.getSelectedToggle();
        if (selected == null) {
            return;
        }

        String type = (String) selected.getUserData();
        double w = 120;
        double h = 80;
        double left = x - w / 2.0;
        double top = y - h / 2.0;

        DrawableItem item = new DrawableItem(type, left, top, w, h);
        item.applyStyle(strokePicker.getValue(), fillPicker.getValue(),
                lineWidthSpinner.getValue(), lineStyleChoice.getValue());

        items.add(item);
        drawingPane.getChildren().addAll(item.frame, item.shape);

        // Select the new item on left click.
        item.shape.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.PRIMARY) {
                setCurrentItem(item);
            }
        });
        item.frame.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.PRIMARY) {
                setCurrentItem(item);
            }
        });

        setCurrentItem(item);
    }

    private void setCurrentItem(DrawableItem item) {
        currentItem = item;
        for (DrawableItem it : items) {
            it.frame.setVisible(it == currentItem);
        }
        if (currentItem != null) {
            currentItem.frame.toFront();
            currentItem.shape.toFront();
        }
    }

    private void handleKey(KeyCode code) {
        if (currentItem == null) {
            return;
        }
        double moveStep = 10;
        double sizeStep = 10;

        switch (code) {
            case UP:
                currentItem.y -= moveStep;
                break;
            case DOWN:
                currentItem.y += moveStep;
                break;
            case LEFT:
                currentItem.x -= moveStep;
                break;
            case RIGHT:
                currentItem.x += moveStep;
                break;
            case PLUS:
            case EQUALS:
            case ADD:
                currentItem.h += sizeStep;
                break;
            case MINUS:
            case SUBTRACT:
                currentItem.h = Math.max(20, currentItem.h - sizeStep);
                break;
            case LESS:
            case COMMA:
                currentItem.w = Math.max(20, currentItem.w - sizeStep);
                break;
            case GREATER:
            case PERIOD:
                currentItem.w += sizeStep;
                break;
            default:
                return;
        }
        currentItem.updateGeometry();
    }

    private void saveDrawing(Stage stage) {
        double targetW = parseDouble(imageWidthField.getText(), drawingPane.getWidth());
        double targetH = parseDouble(imageHeightField.getText(), drawingPane.getHeight());

        FileChooser chooser = new FileChooser();
        chooser.setTitle("Save Image");
        chooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("PNG Image", "*.png"),
                new FileChooser.ExtensionFilter("JPG Image", "*.jpg", "*.jpeg")
        );
        File file = chooser.showSaveDialog(stage);
        if (file == null) {
            return;
        }

        // Resize the drawing pane to the requested image size for snapshot.
        double oldW = drawingPane.getWidth();
        double oldH = drawingPane.getHeight();
        drawingPane.setPrefSize(targetW, targetH);
        drawingPane.applyCss();
        drawingPane.layout();

        WritableImage image = new WritableImage((int) targetW, (int) targetH);
        drawingPane.snapshot(null, image);

        // Restore the old size.
        drawingPane.setPrefSize(oldW, oldH);
        drawingPane.applyCss();
        drawingPane.layout();

        String ext = getExtension(file);
        if (ext == null) {
            file = new File(file.getAbsolutePath() + ".png");
            ext = "png";
        }
        try {
            ImageIO.write(SwingFXUtils.fromFXImage(image, null), ext, file);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private double parseDouble(String text, double fallback) {
        try {
            return Double.parseDouble(text.trim());
        } catch (Exception ex) {
            return fallback;
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

    private void showHelp() {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Instruction");
        alert.setHeaderText("How to use");
        alert.setContentText(
                "1) Choose a primitive in the palette.\n" +
                "2) Right-click on the canvas to add it.\n" +
                "3) Click a shape to select it.\n" +
                "4) Use arrows and +/-/< > to move and resize."
        );
        alert.showAndWait();
    }

    private static class DrawableItem {
        final String type;
        final Shape shape;
        final Rectangle frame;

        double x;
        double y;
        double w;
        double h;

        DrawableItem(String type, double x, double y, double w, double h) {
            this.type = type;
            this.x = x;
            this.y = y;
            this.w = w;
            this.h = h;

            switch (type) {
                case "LINE":
                    shape = new Line();
                    break;
                case "ELLIPSE":
                    shape = new Ellipse();
                    break;
                case "RECT":
                default:
                    shape = new Rectangle();
                    break;
            }

            frame = new Rectangle();
            frame.setFill(Color.color(0.2, 0.6, 1.0, 0.15));
            frame.setStroke(Color.DODGERBLUE);
            frame.getStrokeDashArray().setAll(10.0, 5.0);

            updateGeometry();
        }

        void applyStyle(Color stroke, Color fill, double width, String lineStyle) {
            shape.setStroke(stroke);
            shape.setStrokeWidth(width);
            shape.getStrokeDashArray().clear();

            if ("Dashed".equals(lineStyle)) {
                shape.getStrokeDashArray().addAll(10.0, 5.0);
            } else if ("Dotted".equals(lineStyle)) {
                shape.getStrokeDashArray().addAll(2.0, 8.0);
            }

            if (shape instanceof Line) {
                shape.setFill(Color.TRANSPARENT);
            } else {
                shape.setFill(fill);
            }
        }

        void updateGeometry() {
            frame.setX(x);
            frame.setY(y);
            frame.setWidth(w);
            frame.setHeight(h);

            if (shape instanceof Line) {
                Line line = (Line) shape;
                line.setStartX(x);
                line.setStartY(y);
                line.setEndX(x + w);
                line.setEndY(y + h);
            } else if (shape instanceof Ellipse) {
                Ellipse ell = (Ellipse) shape;
                ell.setCenterX(x + w / 2.0);
                ell.setCenterY(y + h / 2.0);
                ell.setRadiusX(w / 2.0);
                ell.setRadiusY(h / 2.0);
            } else if (shape instanceof Rectangle) {
                Rectangle rect = (Rectangle) shape;
                rect.setX(x);
                rect.setY(y);
                rect.setWidth(w);
                rect.setHeight(h);
            }
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
