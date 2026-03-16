package lab_1;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.geometry.Insets;
import javafx.geometry.Point3D;
import javafx.scene.AmbientLight;
import javafx.scene.Group;
import javafx.scene.PerspectiveCamera;
import javafx.scene.PointLight;
import javafx.scene.Scene;
import javafx.scene.SceneAntialiasing;
import javafx.scene.SubScene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ColorPicker;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.control.Tooltip;
import javafx.scene.image.WritableImage;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.paint.PhongMaterial;
import javafx.scene.shape.Cylinder;
import javafx.scene.shape.Sphere;
import javafx.scene.transform.Rotate;
import javafx.scene.transform.Translate;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.embed.swing.SwingFXUtils;

import javax.imageio.ImageIO;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

public class Six extends Application {
    private final List<Atom> atoms = new ArrayList<>();
    private final Map<String, Color> elementColors = new HashMap<>();

    private final Group moleculeGroup = new Group();
    private final Rotate rotateX = new Rotate(-15, Rotate.X_AXIS);
    private final Rotate rotateY = new Rotate(-20, Rotate.Y_AXIS);
    private final Rotate rotateZ = new Rotate(0, Rotate.Z_AXIS);

    private final Label infoLabel = new Label("Load an .xyz file");
    private final ComboBox<String> elementBox = new ComboBox<>();
    private final ColorPicker colorPicker = new ColorPicker(Color.SADDLEBROWN);

    private String moleculeDescription = "";

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        moleculeGroup.getTransforms().addAll(rotateX, rotateY, rotateZ);

        Group world = new Group();
        world.getChildren().add(moleculeGroup);

        AmbientLight ambient = new AmbientLight(Color.color(0.7, 0.7, 0.7));
        PointLight light = new PointLight(Color.WHITE);
        light.setTranslateX(-200);
        light.setTranslateY(-150);
        light.setTranslateZ(-400);
        world.getChildren().addAll(ambient, light);

        PerspectiveCamera camera = new PerspectiveCamera(true);
        camera.setNearClip(0.1);
        camera.setFarClip(10000);
        camera.setTranslateZ(-700);

        SubScene subScene = new SubScene(world, 900, 600, true, SceneAntialiasing.BALANCED);
        subScene.setFill(Color.rgb(235, 235, 235));
        subScene.setCamera(camera);

        StackPane centerPane = new StackPane(subScene);
        subScene.widthProperty().bind(centerPane.widthProperty());
        subScene.heightProperty().bind(centerPane.heightProperty());

        Button loadButton = new Button("Open XYZ");
        loadButton.setOnAction(e -> loadMolecule(stage));

        Button saveButton = new Button("Save Image");
        saveButton.setOnAction(e -> saveSnapshot(subScene, stage));

        Button applyColorButton = new Button("Apply Color");
        applyColorButton.setOnAction(e -> {
            String element = elementBox.getValue();
            if (element == null) {
                return;
            }
            elementColors.put(element.toUpperCase(Locale.ROOT), colorPicker.getValue());
            rebuildMolecule();
        });

        Slider scaleSlider = new Slider(30, 250, 100);
        scaleSlider.setShowTickLabels(true);
        scaleSlider.setShowTickMarks(true);
        scaleSlider.setTooltip(new Tooltip("Molecule size"));
        scaleSlider.valueProperty().addListener((obs, oldV, newV) -> {
            double s = newV.doubleValue() / 100.0;
            moleculeGroup.setScaleX(s);
            moleculeGroup.setScaleY(s);
            moleculeGroup.setScaleZ(s);
        });

        Slider xSlider = createRotationSlider(rotateX.getAngle(), angle -> rotateX.setAngle(angle));
        Slider ySlider = createRotationSlider(rotateY.getAngle(), angle -> rotateY.setAngle(angle));
        Slider zSlider = createRotationSlider(rotateZ.getAngle(), angle -> rotateZ.setAngle(angle));

        HBox row1 = new HBox(10,
                loadButton,
                saveButton,
                new Label("Element"), elementBox,
                colorPicker,
                applyColorButton
        );

        VBox row2 = new VBox(6,
                new HBox(8, new Label("Scale"), scaleSlider),
                new HBox(8, new Label("Rotate X"), xSlider),
                new HBox(8, new Label("Rotate Y"), ySlider),
                new HBox(8, new Label("Rotate Z"), zSlider)
        );

        VBox controls = new VBox(8, row1, row2, infoLabel);
        controls.setPadding(new Insets(10));

        BorderPane root = new BorderPane();
        root.setTop(controls);
        root.setCenter(centerPane);

        Scene scene = new Scene(root, 1000, 750, true);
        stage.setTitle("Lab 1 - Task 6");
        stage.setScene(scene);
        stage.show();
    }

    private Slider createRotationSlider(double initial, java.util.function.DoubleConsumer consumer) {
        Slider slider = new Slider(-180, 180, initial);
        slider.setShowTickLabels(true);
        slider.setShowTickMarks(true);
        slider.valueProperty().addListener((obs, oldV, newV) -> consumer.accept(newV.doubleValue()));
        return slider;
    }

    private void loadMolecule(Stage stage) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Open .xyz file");
        chooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("XYZ files", "*.xyz"));

        File file = chooser.showOpenDialog(stage);
        if (file == null) {
            return;
        }

        try {
            readXyz(file);
            updateElementSelector();
            rebuildMolecule();
            infoLabel.setText("Loaded: " + file.getName() + " | " + moleculeDescription + " | atoms: " + atoms.size());
        } catch (Exception ex) {
            showError("Cannot read xyz file", ex.getMessage());
        }
    }

    private void readXyz(File file) throws IOException {
        List<String> lines = Files.readAllLines(file.toPath());
        if (lines.isEmpty()) {
            throw new IllegalArgumentException("File is empty");
        }

        int atomCount;
        try {
            atomCount = Integer.parseInt(stripBom(lines.get(0)).trim());
        } catch (Exception e) {
            throw new IllegalArgumentException("First line must contain atom count");
        }

        if (lines.size() < atomCount + 2) {
            throw new IllegalArgumentException("Not enough lines for declared atom count");
        }

        moleculeDescription = lines.get(1).trim();
        atoms.clear();

        for (int i = 0; i < atomCount; i++) {
            String line = stripBom(lines.get(i + 2)).trim();
            if (line.isEmpty()) {
                continue;
            }

            String[] p = line.split("\\s+");
            if (p.length < 4) {
                throw new IllegalArgumentException("Bad atom line: " + line);
            }

            String element = p[0];
            double x = Double.parseDouble(p[1].replace(',', '.'));
            double y = Double.parseDouble(p[2].replace(',', '.'));
            double z = Double.parseDouble(p[3].replace(',', '.'));
            atoms.add(new Atom(element, x, y, z));

            String key = element.toUpperCase(Locale.ROOT);
            if (!elementColors.containsKey(key)) {
                elementColors.put(key, getDefaultColor(key));
            }
        }
    }

    private String stripBom(String text) {
        if (text == null || text.isEmpty()) {
            return "";
        }
        if (text.charAt(0) == '\uFEFF') {
            return text.substring(1);
        }
        return text;
    }

    private void updateElementSelector() {
        Set<String> unique = new HashSet<>();
        for (Atom a : atoms) {
            unique.add(a.element.toUpperCase(Locale.ROOT));
        }

        List<String> elements = new ArrayList<>(unique);
        elements.sort(Comparator.naturalOrder());

        elementBox.setItems(FXCollections.observableArrayList(elements));
        if (!elements.isEmpty()) {
            elementBox.getSelectionModel().select(0);
            Color selected = elementColors.get(elements.get(0));
            if (selected != null) {
                colorPicker.setValue(selected);
            }
        }

        elementBox.setOnAction(e -> {
            String selected = elementBox.getValue();
            if (selected != null && elementColors.containsKey(selected)) {
                colorPicker.setValue(elementColors.get(selected));
            }
        });
    }

    private void rebuildMolecule() {
        moleculeGroup.getChildren().clear();
        if (atoms.isEmpty()) {
            return;
        }

        double cx = 0;
        double cy = 0;
        double cz = 0;
        for (Atom atom : atoms) {
            cx += atom.x;
            cy += atom.y;
            cz += atom.z;
        }
        cx /= atoms.size();
        cy /= atoms.size();
        cz /= atoms.size();

        double coordScale = 80.0;
        List<Point3D> points = new ArrayList<>();
        List<Sphere> spheres = new ArrayList<>();

        for (Atom atom : atoms) {
            double x = (atom.x - cx) * coordScale;
            double y = (atom.y - cy) * coordScale;
            double z = (atom.z - cz) * coordScale;
            points.add(new Point3D(x, y, z));

            Sphere sphere = new Sphere(getRadius(atom.element));
            sphere.setTranslateX(x);
            sphere.setTranslateY(y);
            sphere.setTranslateZ(z);

            String key = atom.element.toUpperCase(Locale.ROOT);
            Color color = elementColors.getOrDefault(key, Color.LIGHTGRAY);
            sphere.setMaterial(new PhongMaterial(color));
            spheres.add(sphere);
        }

        addAllBonds(points);
        moleculeGroup.getChildren().addAll(spheres);
    }

    private void addAllBonds(List<Point3D> points) {
        PhongMaterial bondMaterial = new PhongMaterial(Color.DIMGRAY);

        for (int i = 0; i < points.size(); i++) {
            for (int j = i + 1; j < points.size(); j++) {
                Cylinder bond = createConnection(points.get(i), points.get(j), 4, bondMaterial);
                moleculeGroup.getChildren().add(bond);
            }
        }
    }

    private Cylinder createConnection(Point3D origin, Point3D target, double radius, PhongMaterial material) {
        Point3D yAxis = new Point3D(0, 1, 0);
        Point3D diff = target.subtract(origin);
        double height = diff.magnitude();

        Point3D mid = target.midpoint(origin);
        Translate moveToMidpoint = new Translate(mid.getX(), mid.getY(), mid.getZ());

        Cylinder line = new Cylinder(radius, height);
        line.setMaterial(material);

        Point3D axisOfRotation = diff.crossProduct(yAxis);
        if (axisOfRotation.magnitude() < 1e-6) {
            if (diff.getY() < 0) {
                line.getTransforms().addAll(moveToMidpoint, new Rotate(180, Rotate.X_AXIS));
            } else {
                line.getTransforms().add(moveToMidpoint);
            }
            return line;
        }

        double angle = Math.acos(diff.normalize().dotProduct(yAxis));
        Rotate rotateAroundCenter = new Rotate(-Math.toDegrees(angle), axisOfRotation);
        line.getTransforms().addAll(moveToMidpoint, rotateAroundCenter);
        return line;
    }

    private void saveSnapshot(SubScene subScene, Stage stage) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Save image");
        chooser.setInitialFileName("molecule.png");
        chooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("PNG", "*.png"),
                new FileChooser.ExtensionFilter("JPG", "*.jpg", "*.jpeg"),
                new FileChooser.ExtensionFilter("GIF", "*.gif")
        );

        File file = chooser.showSaveDialog(stage);
        if (file == null) {
            return;
        }

        String format = getFormat(file.getName());
        if (format.isEmpty()) {
            format = "png";
            file = new File(file.getAbsolutePath() + ".png");
        }

        WritableImage image = subScene.snapshot(null, null);
        BufferedImage buffered = SwingFXUtils.fromFXImage(image, null);

        try {
            if ("jpg".equals(format) || "jpeg".equals(format)) {
                BufferedImage rgb = new BufferedImage(buffered.getWidth(), buffered.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g = rgb.createGraphics();
                g.drawImage(buffered, 0, 0, java.awt.Color.WHITE, null);
                g.dispose();
                ImageIO.write(rgb, "jpg", file);
            } else {
                ImageIO.write(buffered, format, file);
            }
            infoLabel.setText("Saved: " + file.getName());
        } catch (IOException e) {
            showError("Cannot save image", e.getMessage());
        }
    }

    private String getFormat(String fileName) {
        int dot = fileName.lastIndexOf('.');
        if (dot < 0 || dot == fileName.length() - 1) {
            return "";
        }
        return fileName.substring(dot + 1).toLowerCase(Locale.ROOT);
    }

    private Color getDefaultColor(String element) {
        switch (element) {
            case "H":
                return Color.WHITE;
            case "C":
                return Color.SADDLEBROWN;
            case "N":
                return Color.DODGERBLUE;
            case "O":
                return Color.CRIMSON;
            case "S":
                return Color.GOLD;
            case "CL":
                return Color.GREEN;
            default:
                return Color.LIGHTGRAY;
        }
    }

    private double getRadius(String element) {
        String key = element.toUpperCase(Locale.ROOT);
        switch (key) {
            case "H":
                return 9;
            case "C":
                return 14;
            case "N":
                return 13;
            case "O":
                return 13;
            case "S":
                return 16;
            default:
                return 12;
        }
    }

    private void showError(String header, String text) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Error");
        alert.setHeaderText(header);
        alert.setContentText(text);
        alert.showAndWait();
    }

    private static class Atom {
        final String element;
        final double x;
        final double y;
        final double z;

        Atom(String element, double x, double y, double z) {
            this.element = element;
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
}

