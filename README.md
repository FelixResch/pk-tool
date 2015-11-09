# PK-TOOL

Eine nette Gui, die PK-Tutoren während der Übungen unterstützen soll.

![Screenshot](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/screenshot.png)

## Download

Kompilierte Version für Windows 10: [pk-tool.exe](https://github.com/jakobkogler/pk-tool/releases/download/0.1/pk-tool.exe)

## Voraussetzungen ##

* Python 3.4
* PyQt 5.2.1

## Benutzung ##

Das Programm startet man mit `python3 pk-tool.py`. 
Nach dem ersten Start des Programmes muss man ein paar Einstellungen vornehmen.
Den Einstellungs-Dialog findet man unter `Datei - Einstellungen`. 
Dort muss man den Pfad zum PK-Repository angeben, und kann außerdem seinen Usernamen festlegen, um eine bessere Übersicht über seine Gruppen zu bekommen. 

Mit Hilfe von Comboboxen kann man die gewünschte Gruppe auswählen und die gewünschte Übung auswählen. 
Dadurch wird eine interactive Tabelle erstellt. 
Man kann die Anwesenheit eintragen (Häckchen setzen), die Adhoc-Aufgabe bewerten (Zahl zwischen 0 und 100), und auch einen Kommentar eintragen. 

### Eingabe via "Befehlen"

Um keine Zeit beim Namensuchen zu vergäuden, kann man all diese Dinge auch mit "Befehlen" erledigen. 
Die Syntax dafür ist: 

 - `name a`: Der Student `name` ist anwesend. 
 - `name b`: Der Student `name` ist abwesend. 
 - `name zahl`: Der Student `name` bekommt `zahl` Prozent auf den Adhoc-Teil.
 - `name kommentar`: Fügt den Kommentar `kommentar` beim Studenten `name` hinzu. 
 
Dabei genügt es, einen Substring des echten Namens anzugeben. `odo 100` bewertet bei Studenten `Dennis T. Odom` 100%. 
Das funktioniert aber natürlich nur, wenn der Substring nur in einem Namen vorkommt. 

### CSV-Datei exportieren

Jede Änderung wird automatisch gespeichert im PK-Repo-Ordner gespeichert. 
Dabei wird automatisch mit `utf-8` kodiert und Unix Line Endings verwendet (auch unter Windows). 
Nach dem Bearbeiten der Files muss man aber manuell die Dateien ins Git-Repo einchecken und pushen. 

### Neue Tabelle anfangen

Per Klick auf `Datei - Neu` wird eine neue CSV-Datei für die aktuell ausgewählte Gruppe erstellt. 
Diese wird automatisch im richtigen Ordner gespeichert. 

### Sortieren

Jede Spalte kann per Klick auf die Spaltenüberschrift sortiert werden.  

### Neue Studenten der Tabelle hinzufügen

Falls ein Student nicht in der Tabelle erscheint (z.B. weil er aus einer anderen Gruppe ist), kann man per Button-Click eine neue Zeile der Tabelle hinzufügen. 

## Licence ##

Copyright (C) 2015 Jakob Kogler, [MIT License](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/LICENSE.txt)
