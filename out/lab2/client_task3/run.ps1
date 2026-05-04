param(
    [string]$JavaFxLib = "C:\soft\javafx-sdk-21.0.10\lib"
)

$modules = "javafx.controls,javafx.graphics"

javac --module-path $JavaFxLib --add-modules $modules AuthClientFx.java
java "-Dprism.order=sw" --module-path $JavaFxLib --add-modules $modules AuthClientFx
