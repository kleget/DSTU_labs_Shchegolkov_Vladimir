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

public class Task2 extends Application {

    private enum PrimitiveType {
        LINE, CIRCLE, ELLIPSE, RECTANGLE
    }

    private PrimitiveType type;
    private Rectangle frame;
    private Shape shape;

    // Bounding box of the primitive.
    private double boxX = 120;
    private double boxY = 80;
    private double boxW = 240;
    private double boxH = 160;

    @Override
    public void start(Stage stage) {
        type = pickRandomType();

        Pane root = new Pane();
        root.setPrefSize(640, 480);
        root.setStyle("-fx-background-color: white;");

        frame = new Rectangle();
        frame.setFill(Color.color(0.2, 0.6, 1.0, 0.15));
        frame.setStroke(Color.DODGERBLUE);
        frame.getStrokeDashArray().setAll(10.0, 5.0);

        shape = createShapeForType(type);
        shape.setStroke(Color.BLACK);
        shape.setFill(Color.TRANSPARENT);

        root.getChildren().addAll(frame, shape);

        updateGeometry();

        Scene scene = new Scene(root);
        scene.setOnKeyPressed(e -> handleKey(e.getCode()));

        stage.setTitle("Task 2 - Random Primitive");
        stage.setScene(scene);
        stage.show();

        // Give focus to the scene so key events work.
        root.requestFocus();
    }

    private PrimitiveType pickRandomType() {
        PrimitiveType[] values = PrimitiveType.values();
        return values[new Random().nextInt(values.length)];
    }

    private Shape createShapeForType(PrimitiveType type) {
        switch (type) {
            case LINE:
                return new Line();
            case CIRCLE:
                return new Circle();
            case ELLIPSE:
                return new Ellipse();
            case RECTANGLE:
            default:
                return new Rectangle();
        }
    }

    private void handleKey(KeyCode code) {
        double moveStep = 10;
        double sizeStep = 10;

        switch (code) {
            case UP:
                boxY -= moveStep;
                break;
            case DOWN:
                boxY += moveStep;
                break;
            case LEFT:
                boxX -= moveStep;
                break;
            case RIGHT:
                boxX += moveStep;
                break;
            case PLUS:
            case EQUALS:
            case ADD:
                boxH += sizeStep;
                break;
            case MINUS:
            case SUBTRACT:
                boxH = Math.max(20, boxH - sizeStep);
                break;
            case LESS:
            case COMMA:
                boxW = Math.max(20, boxW - sizeStep);
                break;
            case GREATER:
            case PERIOD:
                boxW += sizeStep;
                break;
            default:
                return;
        }

        updateGeometry();
    }

    private void updateGeometry() {
        frame.setX(boxX);
        frame.setY(boxY);
        frame.setWidth(boxW);
        frame.setHeight(boxH);

        switch (type) {
            case LINE: {
                Line line = (Line) shape;
                line.setStartX(boxX);
                line.setStartY(boxY);
                line.setEndX(boxX + boxW);
                line.setEndY(boxY + boxH);
                break;
            }
            case CIRCLE: {
                Circle circle = (Circle) shape;
                double r = Math.min(boxW, boxH) / 2.0;
                circle.setCenterX(boxX + boxW / 2.0);
                circle.setCenterY(boxY + boxH / 2.0);
                circle.setRadius(r);
                break;
            }
            case ELLIPSE: {
                Ellipse ellipse = (Ellipse) shape;
                ellipse.setCenterX(boxX + boxW / 2.0);
                ellipse.setCenterY(boxY + boxH / 2.0);
                ellipse.setRadiusX(boxW / 2.0);
                ellipse.setRadiusY(boxH / 2.0);
                break;
            }
            case RECTANGLE:
            default: {
                Rectangle rect = (Rectangle) shape;
                rect.setX(boxX);
                rect.setY(boxY);
                rect.setWidth(boxW);
                rect.setHeight(boxH);
                break;
            }
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
