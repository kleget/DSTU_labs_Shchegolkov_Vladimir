package lab_1;

import javafx.application.Application;
import javafx.embed.swing.SwingFXUtils;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.WritableImage;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Three extends Application {
    // Размеры окна (холста), где рисуем.
    private static final double PANE_W = 800;
    private static final double PANE_H = 600;
    // Шаги для перемещения и изменения размеров.
    private static final double MOVE_STEP = 10;
    private static final double SIZE_STEP = 10;
    // Минимальный размер рамки.
    private static final double MIN_SIZE = 20;

    private final Pane drawingPane = new Pane();
    private final Rectangle frame = new Rectangle();
    private final List<Item> items = new ArrayList<>();
    private Item current;

    // Элементы управления справа.
    private final ColorPicker strokeColorPicker = new ColorPicker(Color.BLACK);
    private final ColorPicker fillColorPicker = new ColorPicker(Color.LIGHTGRAY);
    private final TextField strokeWidthField = new TextField("2");
    private final Button strokePlusBtn = new Button("+");
    private final Button strokeMinusBtn = new Button("-");
    private final ComboBox<String> lineTypeBox = new ComboBox<>();
    private final TextField saveWidthField = new TextField("800");
    private final TextField saveHeightField = new TextField("600");

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        BorderPane root = new BorderPane();

        drawingPane.setPrefSize(PANE_W, PANE_H);
        drawingPane.setStyle("-fx-background-color: white;");

        setupFrame();
        setupLineTypeBox();

        ToggleGroup group = new ToggleGroup();
        VBox leftPalette = createPalette(group);
        VBox rightPanel = createRightPanel();

        MenuBar menuBar = createMenu(primaryStage);

        root.setTop(menuBar);
        root.setLeft(leftPalette);
        root.setCenter(drawingPane);
        root.setRight(rightPanel);

        // Фильтр, чтобы клавиши работали даже когда фокус на TextField.
        Scene scene = new Scene(root);
        scene.addEventFilter(KeyEvent.KEY_PRESSED, e -> {
            if (isControlKey(e.getCode())) {
                handleKey(e.getCode());
                e.consume();
            }
        });

        drawingPane.setOnMouseClicked(e -> {
            if (e.getButton() == MouseButton.SECONDARY) {
                Toggle t = group.getSelectedToggle();
                if (t != null) {
                    String type = (String) t.getUserData();
                    addPrimitive(type, e.getX(), e.getY());
                }
            }
        });

        primaryStage.setScene(scene);
        primaryStage.setTitle("Лаба 1 — Задание 3");
        primaryStage.show();
        drawingPane.requestFocus();
    }

    // Пунктирная рамка вокруг текущего примитива.
    private void setupFrame() {
        frame.setFill(Color.TRANSPARENT);
        frame.setStroke(Color.rgb(0, 0, 0, 0.6));
        frame.getStrokeDashArray().setAll(8.0, 6.0);
        frame.setVisible(false);
    }

    // Заполняем список типов линий.
    private void setupLineTypeBox() {
        lineTypeBox.getItems().addAll("Сплошная", "Пунктирная", "Точечная");
        lineTypeBox.getSelectionModel().select(0);
    }

    // Левая панель: выбор примитива.
    private VBox createPalette(ToggleGroup group) {
        ToggleButton lineBtn = new ToggleButton("Линия");
        lineBtn.setUserData("LINE");
        ToggleButton circleBtn = new ToggleButton("Окружность");
        circleBtn.setUserData("CIRCLE");
        ToggleButton ellipseBtn = new ToggleButton("Эллипс");
        ellipseBtn.setUserData("ELLIPSE");
        ToggleButton rectBtn = new ToggleButton("Прямоугольник");
        rectBtn.setUserData("RECT");

        lineBtn.setToggleGroup(group);
        circleBtn.setToggleGroup(group);
        ellipseBtn.setToggleGroup(group);
        rectBtn.setToggleGroup(group);

        VBox box = new VBox(8, new Label("Палитра"), lineBtn, circleBtn, ellipseBtn, rectBtn);
        box.setPrefWidth(140);
        return box;
    }

    // Правая панель: настройки.
    private VBox createRightPanel() {
        strokeWidthField.setPrefColumnCount(5);
        saveWidthField.setPrefColumnCount(5);
        saveHeightField.setPrefColumnCount(5);

        // Кнопки + / - меняют толщину линии без ввода цифр.
        strokePlusBtn.setOnAction(e -> changeStrokeWidth(1));
        strokeMinusBtn.setOnAction(e -> changeStrokeWidth(-1));

        HBox strokeBox = new HBox(6, strokeWidthField, strokeMinusBtn, strokePlusBtn);

        VBox box = new VBox(8,
                new Label("Настройки"),
                new Label("Цвет линии"), strokeColorPicker,
                new Label("Цвет заливки"), fillColorPicker,
                new Label("Толщина линии"), strokeBox,
                new Label("Тип линии"), lineTypeBox,
                new Label("Сохранить: ширина"), saveWidthField,
                new Label("Сохранить: высота"), saveHeightField
        );
        box.setPrefWidth(200);
        return box;
    }

    // Верхнее меню: сохранить, выход, справка.
    private MenuBar createMenu(Stage stage) {
        Menu fileMenu = new Menu("Файл");
        MenuItem saveItem = new MenuItem("Сохранить...");
        MenuItem exitItem = new MenuItem("Выход");
        fileMenu.getItems().addAll(saveItem, exitItem);

        Menu helpMenu = new Menu("Помощь");
        MenuItem infoItem = new MenuItem("Инструкция");
        helpMenu.getItems().add(infoItem);

        saveItem.setOnAction(e -> saveImage(stage));
        exitItem.setOnAction(e -> stage.close());
        infoItem.setOnAction(e -> showInfo());

        return new MenuBar(fileMenu, helpMenu);
    }

    // Добавление примитива в точку клика.
    private void addPrimitive(String type, double clickX, double clickY) {
        Shape shape = createShape(type);
        Item item = new Item(shape);

        item.w = 120;
        item.h = 80;
        item.x = clickX - item.w / 2.0;
        item.y = clickY - item.h / 2.0;

        applyStyle(shape, type);
        clamp(item);
        updateShape(item);

        items.add(item);
        drawingPane.getChildren().add(shape);

        setCurrent(item);
    }

    // Создаем примитив по типу.
    private Shape createShape(String type) {
        switch (type) {
            case "LINE":
                return new Line();
            case "CIRCLE":
                return new Circle();
            case "ELLIPSE":
                return new Ellipse();
            case "RECT":
            default:
                return new Rectangle();
        }
    }

    // Применяем цвета, толщину и тип линии.
    private void applyStyle(Shape shape, String type) {
        shape.setStroke(strokeColorPicker.getValue());
        shape.setStrokeWidth(parseDouble(strokeWidthField.getText(), 2));

        if (!"LINE".equals(type)) {
            shape.setFill(fillColorPicker.getValue());
        } else {
            shape.setFill(Color.TRANSPARENT);
        }

        String lineType = lineTypeBox.getSelectionModel().getSelectedItem();
        shape.getStrokeDashArray().clear();
        if ("Пунктирная".equals(lineType)) {
            shape.getStrokeDashArray().addAll(10.0, 6.0);
        } else if ("Точечная".equals(lineType)) {
            shape.getStrokeDashArray().addAll(2.0, 6.0);
        }
    }

    // Делаем выбранный примитив активным.
    private void setCurrent(Item item) {
        current = item;
        frame.setVisible(true);
        if (!drawingPane.getChildren().contains(frame)) {
            drawingPane.getChildren().add(frame);
        }
        frame.toFront();
        updateFrame(item);
    }

    // Обновляем геометрию примитива.
    private void updateShape(Item item) {
        Shape shape = item.shape;
        if (shape instanceof Line) {
            Line l = (Line) shape;
            l.setStartX(item.x);
            l.setStartY(item.y);
            l.setEndX(item.x + item.w);
            l.setEndY(item.y + item.h);
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            double r = Math.min(item.w, item.h) / 2.0;
            c.setCenterX(item.x + item.w / 2.0);
            c.setCenterY(item.y + item.h / 2.0);
            c.setRadius(r);
        } else if (shape instanceof Ellipse) {
            Ellipse e = (Ellipse) shape;
            e.setCenterX(item.x + item.w / 2.0);
            e.setCenterY(item.y + item.h / 2.0);
            e.setRadiusX(item.w / 2.0);
            e.setRadiusY(item.h / 2.0);
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            r.setX(item.x);
            r.setY(item.y);
            r.setWidth(item.w);
            r.setHeight(item.h);
        }
    }

    // Обновляем положение рамки.
    private void updateFrame(Item item) {
        frame.setX(item.x);
        frame.setY(item.y);
        frame.setWidth(item.w);
        frame.setHeight(item.h);
    }

    // Управление клавиатурой для текущего примитива.
    private void handleKey(KeyCode code) {
        if (current == null) {
            return;
        }

        if (code == KeyCode.LEFT) {
            current.x -= MOVE_STEP;
        } else if (code == KeyCode.RIGHT) {
            current.x += MOVE_STEP;
        } else if (code == KeyCode.UP) {
            current.y -= MOVE_STEP;
        } else if (code == KeyCode.DOWN) {
            current.y += MOVE_STEP;
        } else if (code == KeyCode.PLUS || code == KeyCode.EQUALS || code == KeyCode.ADD) {
            current.h += SIZE_STEP;
        } else if (code == KeyCode.MINUS || code == KeyCode.SUBTRACT) {
            current.h -= SIZE_STEP;
        } else if (code == KeyCode.COMMA || code == KeyCode.LESS) {
            current.w -= SIZE_STEP;
        } else if (code == KeyCode.PERIOD || code == KeyCode.GREATER) {
            current.w += SIZE_STEP;
        }

        clamp(current);
        updateShape(current);
        updateFrame(current);
    }

    // Проверяем, что это управляющая клавиша.
    private boolean isControlKey(KeyCode code) {
        return code == KeyCode.LEFT
                || code == KeyCode.RIGHT
                || code == KeyCode.UP
                || code == KeyCode.DOWN
                || code == KeyCode.PLUS
                || code == KeyCode.EQUALS
                || code == KeyCode.ADD
                || code == KeyCode.MINUS
                || code == KeyCode.SUBTRACT
                || code == KeyCode.COMMA
                || code == KeyCode.LESS
                || code == KeyCode.PERIOD
                || code == KeyCode.GREATER;
    }

    // Ограничения по границам и минимальным размерам.
    private void clamp(Item item) {
        double maxW = drawingPane.getPrefWidth();
        double maxH = drawingPane.getPrefHeight();

        if (item.w < MIN_SIZE) {
            item.w = MIN_SIZE;
        }
        if (item.h < MIN_SIZE) {
            item.h = MIN_SIZE;
        }

        if (item.x < 0) {
            item.x = 0;
        }
        if (item.y < 0) {
            item.y = 0;
        }
        if (item.x + item.w > maxW) {
            item.x = maxW - item.w;
        }
        if (item.y + item.h > maxH) {
            item.y = maxH - item.h;
        }

        if (item.w > maxW) {
            item.w = maxW;
            item.x = 0;
        }
        if (item.h > maxH) {
            item.h = maxH;
            item.y = 0;
        }
    }

    // Сохранение в файл PNG.
    private void saveImage(Stage stage) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Сохранить");
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("PNG", "*.png"));
        fileChooser.setInitialFileName("картинка.png");

        File file = fileChooser.showSaveDialog(stage);
        if (file == null) {
            return;
        }

        int w = parseInt(saveWidthField.getText(), (int) drawingPane.getPrefWidth());
        int h = parseInt(saveHeightField.getText(), (int) drawingPane.getPrefHeight());
        if (w <= 0) {
            w = (int) drawingPane.getPrefWidth();
        }
        if (h <= 0) {
            h = (int) drawingPane.getPrefHeight();
        }

        boolean wasVisible = frame.isVisible();
        frame.setVisible(false);
        WritableImage image = new WritableImage(w, h);
        drawingPane.snapshot(null, image);
        frame.setVisible(wasVisible);

        try {
            ImageIO.write(SwingFXUtils.fromFXImage(image, null), "png", file);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    // Простая справка.
    private void showInfo() {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Инструкция");
        alert.setHeaderText("Как пользоваться");
        alert.setContentText(
                "1) Выберите примитив слева.\n" +
                "2) ПКМ по холсту — добавить примитив.\n" +
                "3) Стрелки — перемещение.\n" +
                "4) + / - — высота, < / > — ширина.\n" +
                "5) Файл -> Сохранить... — сохранить картинку."
        );
        alert.showAndWait();
    }

    // Простой класс для хранения примитива и его размеров.
    private static class Item {
        final Shape shape;
        double x;
        double y;
        double w;
        double h;

        Item(Shape shape) {
            this.shape = shape;
        }
    }

    // Простое чтение чисел.
    private static int parseInt(String text, int def) {
        try {
            return Integer.parseInt(text.trim());
        } catch (Exception e) {
            return def;
        }
    }

    private static double parseDouble(String text, double def) {
        try {
            return Double.parseDouble(text.trim());
        } catch (Exception e) {
            return def;
        }
    }

    // Увеличиваем или уменьшаем толщину линии.
    private void changeStrokeWidth(int delta) {
        double current = parseDouble(strokeWidthField.getText(), 2);
        double next = current + delta;
        if (next < 1) {
            next = 1;
        }
        strokeWidthField.setText(String.valueOf((int) next));
    }
}