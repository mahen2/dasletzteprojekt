Datenbankentwurf
================

blogeintrag (id, titel, datum, text, geschriebenvonbenutzername)
kommentar (id, blogeintragid, name, email, url, text)
foto (id, dateipfad, hochgeladenvonbenutzername)
benutzer (benutzername, Vorname, Nachname, passwort)

------------------------

evtl., wenn wir müssen:
-----------------------

rolle (id, name)
gehoertzurolle (benutzername, rollenid)
tags () // für jeden tag einen eintrag?
taggehoertzueintrag ???