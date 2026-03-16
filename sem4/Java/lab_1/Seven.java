package lab_1;

import javafx.application.Application;
import javafx.beans.InvalidationListener;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.control.Slider;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.File;

public class Seven extends Application {
    private final MediaView mediaView = new MediaView();

    private MediaPlayer player;

    private final Label fileLabel = new Label("File: -");
    private final Label currentLabel = new Label("00:00");
    private final Label totalLabel = new Label("00:00");

    private final Slider progressSlider = new Slider(0, 100, 0);
    private final Slider volumeSlider = new Slider(0, 100, 50);

    private boolean userChangingProgress = false;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        MenuItem openItem = new MenuItem("Open...");
        openItem.setOnAction(e -> openMedia(stage));

        MenuItem exitItem = new MenuItem("Exit");
        exitItem.setOnAction(e -> stage.close());

        Menu fileMenu = new Menu("File");
        fileMenu.getItems().addAll(openItem, exitItem);

        MenuBar menuBar = new MenuBar(fileMenu);

        StackPane videoPane = new StackPane(mediaView);
        videoPane.setStyle("-fx-background-color: black;");
        videoPane.setPrefHeight(460);

        Button openButton = new Button("Open");
        openButton.setOnAction(e -> openMedia(stage));

        Button playButton = new Button("Play");
        playButton.setOnAction(e -> {
            if (player != null) {
                player.play();
            }
        });

        Button pauseButton = new Button("Pause");
        pauseButton.setOnAction(e -> {
            if (player != null) {
                player.pause();
            }
        });

        Button stopButton = new Button("Stop");
        stopButton.setOnAction(e -> {
            if (player != null) {
                player.stop();
            }
        });

        progressSlider.setPrefWidth(320);

        progressSlider.setOnMousePressed(e -> userChangingProgress = true);
        progressSlider.setOnMouseReleased(e -> {
            if (player != null) {
                Duration total = player.getTotalDuration();
                if (total != null && total.toMillis() > 0) {
                    double percent = progressSlider.getValue() / 100.0;
                    player.seek(total.multiply(percent));
                }
            }
            userChangingProgress = false;
        });

        volumeSlider.setPrefWidth(160);
        volumeSlider.valueProperty().addListener((obs, oldV, newV) -> {
            if (player != null) {
                player.setVolume(newV.doubleValue() / 100.0);
            }
        });

        HBox controls = new HBox(8,
                openButton,
                playButton,
                pauseButton,
                stopButton,
                currentLabel,
                progressSlider,
                totalLabel,
                new Label("Volume"),
                volumeSlider
        );
        controls.setAlignment(Pos.CENTER_LEFT);

        VBox bottom = new VBox(8, fileLabel, controls);
        bottom.setPadding(new Insets(8));

        BorderPane root = new BorderPane();
        root.setTop(menuBar);
        root.setCenter(videoPane);
        root.setBottom(bottom);

        Scene scene = new Scene(root, 980, 620);
        stage.setTitle("Lab 1 - Task 7 (Media Player)");
        stage.setScene(scene);
        stage.show();
    }

    private void openMedia(Stage stage) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Open media file");
        chooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("Media", "*.mp4", "*.m4v", "*.mp3", "*.wav", "*.m4a"),
                new FileChooser.ExtensionFilter("All files", "*.*")
        );

        File file = chooser.showOpenDialog(stage);
        if (file == null) {
            return;
        }

        fileLabel.setText("File: " + file.getName());

        if (player != null) {
            player.stop();
            player.dispose();
        }

        Media media = new Media(file.toURI().toString());
        player = new MediaPlayer(media);
        mediaView.setMediaPlayer(player);
        player.setVolume(volumeSlider.getValue() / 100.0);

        player.setOnReady(() -> {
            Duration total = player.getTotalDuration();
            totalLabel.setText(format(total));
            currentLabel.setText("00:00");
            progressSlider.setValue(0);
        });

        InvalidationListener timeListener = obs -> updateProgressFromPlayer();
        player.currentTimeProperty().addListener(timeListener);

        player.setOnEndOfMedia(() -> {
            progressSlider.setValue(100);
            Duration total = player.getTotalDuration();
            currentLabel.setText(format(total));
        });

        player.play();
    }

    private void updateProgressFromPlayer() {
        if (player == null) {
            return;
        }

        Duration current = player.getCurrentTime();
        Duration total = player.getTotalDuration();

        currentLabel.setText(format(current));

        if (!userChangingProgress && total != null && total.toMillis() > 0) {
            double percent = (current.toMillis() / total.toMillis()) * 100.0;
            progressSlider.setValue(percent);
        }
    }

    private String format(Duration duration) {
        if (duration == null || duration.isUnknown() || duration.lessThan(Duration.ZERO)) {
            return "00:00";
        }

        int totalSeconds = (int) Math.floor(duration.toSeconds());
        int minutes = totalSeconds / 60;
        int seconds = totalSeconds % 60;
        return String.format("%02d:%02d", minutes, seconds);
    }

    @Override
    public void stop() {
        if (player != null) {
            player.stop();
            player.dispose();
        }
    }
}

