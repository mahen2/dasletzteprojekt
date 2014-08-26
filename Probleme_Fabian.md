Probleme und Lösungen
=====================

Artikel-URL
-----------

* Bei der URL-Generierung wird der Titel genutzt. Der gleiche Titel darf prinzipiell zweimal vorkommen, der die URL muss aber einmalig sein, deshlab wird eien Unix-Timestamp angehängt, falls es den Titel schon in der DB gibt.
* Der URL-Titel wird leergelassen, wenn Javascript aus ist und der User vergisst, manuell etwas einzutragen. Damit es trotzdem eine eindeutige URL gibt, wird der URL-Titel für den Link aus einem Zufallsstring erzeugt.

Datenbank
---------

* Usernamen müssen einmalig sein, da wir es bei der SQLite-DB nicht hinbekommen haben zwei Spalten unique zu schalten, wird vor Registrierung eine Datenbankabfrage gemacht, ob es den gewünschten Usernamen schon gibt.
* Die Datenbankanbindung per SQLAlchemy erlaubt die Nutzung von verschiedenen Datenbanken. Wir haben mit SQLite entwickelt und am Ende MySQL getestet. hier hat die INSERT-Funktion Probleme gemacht. Die Lösung war das Ersetzen von einfachen Anführungszeichen (') mit Backticks (`). Jetzt funktioniert es in beiden Datenbanken.
* Die Erstellung der MySQL-Tabellen ist anders als bei SQLite, weil es verschiedene Datentypen gibt und die Syntax sich leicht unterscheidet, deshalb haben wir einen Beispiel-SQL-Dump erstellt, die den Test mit einer MySQL-DB einfacher macht.
* Teilweise waren die Seiten nach Abschicken von Text noch auf dem Stand vor dem Abschicken. Dieses Problem haben wir gelöst indem die Daten zur Anzeige frisch aus der DB geholt werden, bevor die Seite gerendert wird und nicht am Anfang der Funktion.

Sonstiges
---------

* Die Internationalisierung funktioniert überall auf der Seite außer bei den WTForms-Fehlermeldungen. Obwohl die gettext-Funktion benutzt wird, kommt nie der übersetzte Text.
* Tags sollen auch aus mehreren Wörtern bestehen können und trotzdem bequem einzugeben sein. Im Interface kann man deshalb verschiedene Tags jeweils in eine neue Zeile eines Textefeldes schreiben. In der DB werden sie dann durch | getrennt gespeichert.
* Diverse Unicode-Probleme, die aber nach rumprobieren mit decode und encode gelöst werden konnten.