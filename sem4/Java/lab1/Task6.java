import javafx.application.Application;
import javafx.embed.swing.SwingFXUtils;
import javafx.geometry.Insets;
import javafx.geometry.Point3D;
import javafx.scene.*;
import javafx.scene.control.*;
import javafx.scene.image.WritableImage;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.paint.PhongMaterial;
import javafx.scene.shape.Cylinder;
import javafx.scene.shape.Sphere;
import javafx.scene.transform.Rotate;
import javafx.scene.transform.Translate;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class Task6 extends Application {

    private final Group moleculeGroup = new Group();
    private final Group atomsGroup = new Group();
    private final Group bondsGroup = new Group();

    private final Rotate rotateX = new Rotate(20, Rotate.X_AXIS);
    private final Rotate rotateY = new Rotate(-30, Rotate.Y_AXIS);
    private double anchorX;
    private double anchorY;
    private double anchorAngleX;
    private double anchorAngleY;

    private SubScene subScene;
    private Slider scaleSlider;
    private ComboBox<String> elementBox;
    private ColorPicker elementColorPicker;

    private final List<Atom> atoms = new ArrayList<>();
    private final Map<String, Color> elementColors = new HashMap<>();

    @Override
    public void start(Stage stage) {
        BorderPane root = new BorderPane();

        // Top buttons.
        Button openBtn = new Button("Open XYZ");
        Button saveBtn = new Button("Save Image");
        ToolBar toolBar = new ToolBar(openBtn, saveBtn);
        root.setTop(toolBar);

        // Right controls.
        scaleSlider = new Slider(0.3, 3.0, 1.0);
        scaleSlider.valueProperty().addListener((obs, oldV, newV) -> updateScale());

        elementBox = new ComboBox<>();
        elementColorPicker = new ColorPicker(Color.LIGHTGRAY);
        Button applyColorBtn = new Button("Apply Color");
        applyColorBtn.setOnAction(e -> applyElementColor());

        VBox right = new VBox(10,
                new Label("Scale"), scaleSlider,
                new Label("Element type"), elementBox,
                new Label("Element color"), elementColorPicker,
                applyColorBtn
        );
        right.setPadding(new Insets(10));
        root.setRight(right);

        // 3D scene.
        moleculeGroup.getChildren().addAll(bondsGroup, atomsGroup);
        moleculeGroup.getTransforms().addAll(rotateX, rotateY);

        subScene = new SubScene(new Group(moleculeGroup), 800, 600, true, SceneAntialiasing.BALANCED);
        subScene.setFill(Color.WHITE);
        subScene.setCamera(createCamera());

        enableMouseRotation(subScene);
        root.setCenter(subScene);

        openBtn.setOnAction(e -> openFile(stage));
        saveBtn.setOnAction(e -> saveImage(stage));

        Scene scene = new Scene(root, 1000, 700);
        stage.setTitle("Task 6 - Molecule 3D");
        stage.setScene(scene);
        stage.show();
    }

    private PerspectiveCamera createCamera() {
        PerspectiveCamera camera = new PerspectiveCamera(true);
        camera.setTranslateZ(-800);
        camera.setNearClip(0.1);
        camera.setFarClip(5000);
        return camera;
    }

    private void enableMouseRotation(SubScene scene) {
        scene.setOnMousePressed(e -> {
            anchorX = e.getSceneX();
            anchorY = e.getSceneY();
            anchorAngleX = rotateX.getAngle();
            anchorAngleY = rotateY.getAngle();
        });
        scene.setOnMouseDragged(e -> {
            rotateY.setAngle(anchorAngleY + (e.getSceneX() - anchorX));
            rotateX.setAngle(anchorAngleX - (e.getSceneY() - anchorY));
        });
    }

    private void openFile(Stage stage) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Open XYZ File");
        chooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("XYZ Files", "*.xyz"));
        File file = chooser.showOpenDialog(stage);
        if (file == null) {
            return;
        }

        try {
            loadMolecule(file);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void loadMolecule(File file) throws IOException {
        Scanner sc = new Scanner(file);
        int count = sc.nextInt();
        if (sc.hasNextLine()) {
            sc.nextLine(); // rest of first line
        }
        if (sc.hasNextLine()) {
            sc.nextLine(); // comment line
        }

        atoms.clear();
        atomsGroup.getChildren().clear();
        bondsGroup.getChildren().clear();

        double minX = Double.MAX_VALUE, minY = Double.MAX_VALUE, minZ = Double.MAX_VALUE;
        double maxX = -Double.MAX_VALUE, maxY = -Double.MAX_VALUE, maxZ = -Double.MAX_VALUE;

        List<RawAtom> raw = new ArrayList<>();
        for (int i = 0; i < count && sc.hasNext(); i++) {
            String element = sc.next();
            double x = sc.nextDouble();
            double y = sc.nextDouble();
            double z = sc.nextDouble();
            raw.add(new RawAtom(element, x, y, z));

            minX = Math.min(minX, x);
            minY = Math.min(minY, y);
            minZ = Math.min(minZ, z);
            maxX = Math.max(maxX, x);
            maxY = Math.max(maxY, y);
            maxZ = Math.max(maxZ, z);
        }
        sc.close();

        double centerX = (minX + maxX) / 2.0;
        double centerY = (minY + maxY) / 2.0;
        double centerZ = (minZ + maxZ) / 2.0;
        double baseScale = 80; // converts model units to pixels

        for (RawAtom ra : raw) {
            double sx = (ra.x - centerX) * baseScale;
            double sy = (ra.y - centerY) * baseScale;
            double sz = (ra.z - centerZ) * baseScale;

            Sphere sphere = new Sphere(radiusFor(ra.element));
            Color color = elementColors.computeIfAbsent(ra.element, this::defaultColorFor);
            sphere.setMaterial(new PhongMaterial(color));
            sphere.setTranslateX(sx);
            sphere.setTranslateY(sy);
            sphere.setTranslateZ(sz);

            Atom atom = new Atom(ra.element, sx, sy, sz, sphere);
            atoms.add(atom);
            atomsGroup.getChildren().add(sphere);
        }

        buildBonds();
        updateScale();
        populateElementBox();
    }

    private void buildBonds() {
        bondsGroup.getChildren().clear();
        Set<String> used = new HashSet<>();

        for (int i = 0; i < atoms.size(); i++) {
            Atom a = atoms.get(i);
            double bestDist = Double.MAX_VALUE;
            int bestIdx = -1;

            for (int j = 0; j < atoms.size(); j++) {
                if (i == j) {
                    continue;
                }
                Atom b = atoms.get(j);
                double dist = a.distanceTo(b);
                if (dist < bestDist) {
                    bestDist = dist;
                    bestIdx = j;
                }
            }

            if (bestIdx >= 0) {
                int i1 = Math.min(i, bestIdx);
                int i2 = Math.max(i, bestIdx);
                String key = i1 + "-" + i2;
                if (used.add(key)) {
                    Atom b = atoms.get(bestIdx);
                    Cylinder bond = createConnection(a.point(), b.point());
                    bond.setMaterial(new PhongMaterial(Color.GRAY));
                    bondsGroup.getChildren().add(bond);
                }
            }
        }
    }

    private void populateElementBox() {
        Set<String> elements = new TreeSet<>();
        for (Atom a : atoms) {
            elements.add(a.element);
        }
        elementBox.getItems().setAll(elements);
        if (!elements.isEmpty()) {
            elementBox.setValue(elements.iterator().next());
        }
    }

    private void applyElementColor() {
        String element = elementBox.getValue();
        if (element == null) {
            return;
        }
        Color color = elementColorPicker.getValue();
        elementColors.put(element, color);
        for (Atom a : atoms) {
            if (a.element.equals(element)) {
                a.sphere.setMaterial(new PhongMaterial(color));
            }
        }
    }

    private void updateScale() {
        double scale = scaleSlider.getValue();
        moleculeGroup.setScaleX(scale);
        moleculeGroup.setScaleY(scale);
        moleculeGroup.setScaleZ(scale);
    }

    private void saveImage(Stage stage) {
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
        String ext = getExtension(file);
        if (ext == null) {
            file = new File(file.getAbsolutePath() + ".png");
            ext = "png";
        }

        WritableImage image = subScene.snapshot(null, null);
        try {
            ImageIO.write(SwingFXUtils.fromFXImage(image, null), ext, file);
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

    private Cylinder createConnection(Point3D origin, Point3D target) {
        Point3D yAxis = new Point3D(0, 1, 0);
        Point3D diff = target.subtract(origin);
        double height = diff.magnitude();
        Point3D mid = target.midpoint(origin);

        Translate moveToMidpoint = new Translate(mid.getX(), mid.getY(), mid.getZ());
        Point3D axisOfRotation = diff.crossProduct(yAxis);
        double angle = Math.acos(diff.normalize().dotProduct(yAxis));

        if (axisOfRotation.magnitude() == 0) {
            axisOfRotation = new Point3D(1, 0, 0);
        }

        Rotate rotateAroundCenter = new Rotate(-Math.toDegrees(angle), axisOfRotation);
        Cylinder line = new Cylinder(2, height);
        line.getTransforms().addAll(moveToMidpoint, rotateAroundCenter);
        return line;
    }

    private double radiusFor(String element) {
        switch (element) {
            case "H":
                return 8;
            case "C":
                return 12;
            case "O":
                return 14;
            case "N":
                return 13;
            default:
                return 10;
        }
    }

    private Color defaultColorFor(String element) {
        switch (element) {
            case "H":
                return Color.WHITE;
            case "C":
                return Color.DARKGRAY;
            case "O":
                return Color.RED;
            case "N":
                return Color.DODGERBLUE;
            default:
                return Color.LIGHTGRAY;
        }
    }

    private static class RawAtom {
        final String element;
        final double x;
        final double y;
        final double z;

        RawAtom(String element, double x, double y, double z) {
            this.element = element;
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }

    private static class Atom {
        final String element;
        final double x;
        final double y;
        final double z;
        final Sphere sphere;

        Atom(String element, double x, double y, double z, Sphere sphere) {
            this.element = element;
            this.x = x;
            this.y = y;
            this.z = z;
            this.sphere = sphere;
        }

        double distanceTo(Atom other) {
            double dx = x - other.x;
            double dy = y - other.y;
            double dz = z - other.z;
            return Math.sqrt(dx * dx + dy * dy + dz * dz);
        }

        Point3D point() {
            return new Point3D(x, y, z);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
