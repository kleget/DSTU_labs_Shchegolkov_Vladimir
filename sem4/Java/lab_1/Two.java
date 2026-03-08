package lab_1;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;
import javafx.stage.Stage;

import java.util.Random;

public class Two extends Application {
    // Размеры окна (холста), где рисуем примитив.
    private static final double PANE_W = 800;
    private static final double PANE_H = 600;
    // Шаги для перемещения и изменения размеров.
    private static final double MOVE_STEP = 10;
    private static final double SIZE_STEP = 10;
    // Минимальный размер рамки, чтобы она не схлопывалась.
    private static final double MIN_SIZE = 20;

    // Координаты левого верхнего угла рамки.
    private double x = 200;
    private double y = 150;
    // Ширина и высота рамки.
    private double w = 200;
    private double h = 150;

    // Рамка (описанный прямоугольник) вокруг примитива.
    private final Rectangle frame = new Rectangle();
    // Сам примитив: линия, окружность, эллипс или прямоугольник.
    private Shape primitive;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        // Холст, где размещаем рамку и примитив.
        Pane pane = new Pane();
        pane.setPrefSize(PANE_W, PANE_H);

        // Настраиваем рамку и создаем случайный примитив.
        setupFrame();
        primitive = createPrimitive();
        // Подгоняем примитив под текущие координаты и размеры.
        updateShapes();

        // Добавляем объекты на холст.
        pane.getChildren().addAll(frame, primitive);

        // Сцена и обработка клавиатуры.
        Scene scene = new Scene(pane);
        scene.setOnKeyPressed(e -> handleKey(e.getCode(), pane));

        primaryStage.setScene(scene);
        primaryStage.setTitle("Лаба 1 — Задание 2");
        primaryStage.show();
        // Фокус нужен, чтобы ловить нажатия клавиш.
        pane.requestFocus();
    }

    // Настраиваем пунктирную рамку: прозрачная заливка, полупрозрачная обводка.
    private void setupFrame() {
        frame.setFill(Color.TRANSPARENT);
        frame.setStroke(Color.rgb(0, 0, 0, 0.6));
        frame.getStrokeDashArray().setAll(8.0, 6.0);
    }

    // Случайно создаем один из 4 примитивов.
    private Shape createPrimitive() {
        // 0 - линия, 1 - окружность, 2 - эллипс, 3 - прямоугольник.
        int t = new Random().nextInt(4);
        Shape s = (t == 0) ? new Line()
                : (t == 1) ? new Circle()
                : (t == 2) ? new Ellipse()
                : new Rectangle();
        // Все примитивы рисуем только обводкой.
        s.setFill(Color.TRANSPARENT);
        s.setStroke(Color.BLACK);
        return s;
    }

    // Применяем текущие x, y, w, h к рамке и примитиву.
    private void updateShapes() {
        // Сначала обновляем рамку.
        frame.setX(x);
        frame.setY(y);
        frame.setWidth(w);
        frame.setHeight(h);

        // Затем подгоняем примитив под рамку.
        if (primitive instanceof Line) {
            Line l = (Line) primitive;
            l.setStartX(x);
            l.setStartY(y);
            l.setEndX(x + w);
            l.setEndY(y + h);
        } else if (primitive instanceof Circle) {
            Circle c = (Circle) primitive;
            double r = Math.min(w, h) / 2.0;
            c.setCenterX(x + w / 2.0);
            c.setCenterY(y + h / 2.0);
            c.setRadius(r);
        } else if (primitive instanceof Ellipse) {
            Ellipse e = (Ellipse) primitive;
            e.setCenterX(x + w / 2.0);
            e.setCenterY(y + h / 2.0);
            e.setRadiusX(w / 2.0);
            e.setRadiusY(h / 2.0);
        } else if (primitive instanceof Rectangle) {
            Rectangle r = (Rectangle) primitive;
            r.setX(x);
            r.setY(y);
            r.setWidth(w);
            r.setHeight(h);
        }
    }

    // Обработка клавиш: перемещение и изменение размеров.
    private void handleKey(KeyCode code, Pane pane) {
        // Стрелки - движение рамки.
        if (code == KeyCode.LEFT) {
            x -= MOVE_STEP;
        } else if (code == KeyCode.RIGHT) {
            x += MOVE_STEP;
        } else if (code == KeyCode.UP) {
            y -= MOVE_STEP;
        } else if (code == KeyCode.DOWN) {
            y += MOVE_STEP;
        // Плюс/минус - меняем высоту (двигаем нижнюю границу).
        } else if (code == KeyCode.PLUS || code == KeyCode.EQUALS || code == KeyCode.ADD) {
            h += SIZE_STEP;
        } else if (code == KeyCode.MINUS || code == KeyCode.SUBTRACT) {
            h -= SIZE_STEP;
        // < и > - меняем ширину (двигаем правую границу).
        } else if (code == KeyCode.COMMA || code == KeyCode.LESS) {
            w -= SIZE_STEP;
        } else if (code == KeyCode.PERIOD || code == KeyCode.GREATER) {
            w += SIZE_STEP;
        }

        proverka_sizov(pane);
        updateShapes();
    }

    private void proverka_sizov(Pane pane) {
        double maxW = pane.getPrefWidth();
        double maxH = pane.getPrefHeight();

        if (w < MIN_SIZE) {
            w = MIN_SIZE;
        }
        if (h < MIN_SIZE) {
            h = MIN_SIZE;
        }

        if (x < 0) {
            x = 0;
        }
        if (y < 0) {
            y = 0;
        }
        if (x + w > maxW) {
            x = maxW - w;
        }
        if (y + h > maxH) {
            y = maxH - h;
        }

        if (w > maxW) {
            w = maxW;
            x = 0;
        }
        if (h > maxH) {
            h = maxH;
            y = 0;
        }
    }
}