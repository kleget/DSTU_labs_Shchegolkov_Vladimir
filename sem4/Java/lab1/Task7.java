import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.File;

public class Task7 extends Application {

    private MediaPlayer player;
    private MediaView mediaView;
    private Label fileLabel;
    private Label totalLabel;
    private Label currentLabel;
    private Slider volumeSlider;

    @Override
    public void start(Stage stage) {
        mediaView = new MediaView();

        fileLabel = new Label("File: -");
        totalLabel = new Label("Total: 00:00");
        currentLabel = new Label("Current: 00:00");

        Button openBtn = new Button("Open");
        Button playBtn = new Button("Play");
        Button pauseBtn = new Button("Pause");
        Button stopBtn = new Button("Stop");

        openBtn.setOnAction(e -> openFile(stage));
        playBtn.setOnAction(e -> {
            if (player != null) {
                player.play();
            }
        });
        pauseBtn.setOnAction(e -> {
            if (player != null) {
                player.pause();
            }
        });
        stopBtn.setOnAction(e -> {
            if (player != null) {
                player.stop();
            }
        });

        volumeSlider = new Slider(0, 100, 50);
        volumeSlider.valueProperty().addListener((obs, oldV, newV) -> {
            if (player != null) {
                player.setVolume(newV.doubleValue() / 100.0);
            }
        });

        HBox controls = new HBox(10, openBtn, playBtn, pauseBtn, stopBtn, new Label("Volume"), volumeSlider);
        controls.setPadding(new Insets(10));

        VBox infoBox = new VBox(5, fileLabel, totalLabel, currentLabel);
        infoBox.setPadding(new Insets(10));

        BorderPane root = new BorderPane();
        root.setTop(infoBox);
        root.setCenter(mediaView);
        root.setBottom(controls);

        Scene scene = new Scene(root, 900, 600);
        stage.setTitle("Task 7 - Media Player");
        stage.setScene(scene);
        stage.show();
    }

    private void openFile(Stage stage) {
        FileChooser chooser = new FileChooser();
        chooser.setTitle("Open Media File");
        chooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("Video/Audio", "*.mp4", "*.mp3", "*.m4a", "*.wav")
        );
        File file = chooser.showOpenDialog(stage);
        if (file == null) {
            return;
        }

        if (player != null) {
            player.stop();
            player.dispose();
        }

        Media media = new Media(file.toURI().toString());
        player = new MediaPlayer(media);
        mediaView.setMediaPlayer(player);

        fileLabel.setText("File: " + file.getName());
        totalLabel.setText("Total: --:--");
        currentLabel.setText("Current: 00:00");

        player.setOnReady(() -> {
            totalLabel.setText("Total: " + formatTime(player.getTotalDuration()));
            player.setVolume(volumeSlider.getValue() / 100.0);
        });

        player.currentTimeProperty().addListener((obs, oldV, newV) -> {
            currentLabel.setText("Current: " + formatTime(newV));
        });
    }

    private String formatTime(Duration duration) {
        if (duration == null || duration.isUnknown()) {
            return "--:--";
        }
        int totalSeconds = (int) Math.floor(duration.toSeconds());
        int hours = totalSeconds / 3600;
        int minutes = (totalSeconds % 3600) / 60;
        int seconds = totalSeconds % 60;
        if (hours > 0) {
            return String.format("%d:%02d:%02d", hours, minutes, seconds);
        }
        return String.format("%02d:%02d", minutes, seconds);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
