-- phpMyAdmin SQL Dump
-- version 4.1.12
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 23. Aug 2014 um 21:11
-- Server Version: 5.6.16
-- PHP-Version: 5.5.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `test`
--

DELIMITER $$
--
-- Prozeduren
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `test_multi_sets`()
    DETERMINISTIC
begin
        select user() as first_col;
        select user() as first_col, now() as second_col;
        select user() as first_col, now() as second_col, now() as third_col;
        end$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `benutzer`
--

CREATE TABLE IF NOT EXISTS `benutzer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `vorname` varchar(200) NOT NULL,
  `nachname` varchar(200) NOT NULL,
  `passwort` varchar(200) NOT NULL,
  `salt` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Daten für Tabelle `benutzer`
--

INSERT INTO `benutzer` (`id`, `username`, `vorname`, `nachname`, `passwort`, `salt`) VALUES
(1, 'fapeg', 'Fabian', 'Pegel2', '4a2aaf6515a902b984812a7cdf789a46', 'CXt1AAHez7ltrurt9IWBNRavcVjRTedD'),
(2, 'maria', 'Maria', 'Henkel', 'c24963a4e0c0d609fa5b1cabc54ef3df', 'jtLRyNgrEZgroB1MYlM1KCYVv56f4X9x'),
(3, 'mina', 'Mina', 'Habsaoui', '7ee0eadf11619a5aa97831c4eb030e52', 'FQW9tj0ioHnGr7V6IFULBRBH9JFIGWaP'),
(5, 'test123', 'Fabian', 'Pegel', 'ba77af29d58b08d881acc85781cf7536', 'z7AHTYNNxgHjFAFHoOLviueK6diiRPrR'),
(6, 'max', 'Max', 'Mustermann', '5643247595d981edb5aaed4a22cb968a', 'vNvbJAQItK6cpsGcaJnhuDui0pjEkYye'),
(7, 'Mirinda', 'Maria', 'Henkel', 'c4c10cd20fd5723fbc7207e96f007740', 'pq3GhypaZ7jrigGXinajf6bX48HxKEkT'),
(8, 'dadada', 'Fabian', 'Pegel', 'fe2ab0b16211774c445b70c7c877f0ee', 'n8avpuYPDiClSPSK4ZSWNwLLZvsMtk2h');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `blogeintrag`
--

CREATE TABLE IF NOT EXISTS `blogeintrag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titel` varchar(300) NOT NULL,
  `text` text NOT NULL,
  `datum` varchar(200) NOT NULL,
  `url_titel` varchar(200) NOT NULL,
  `geschriebenvonbenutzername` varchar(200) NOT NULL,
  `tags` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Daten für Tabelle `blogeintrag`
--

INSERT INTO `blogeintrag` (`id`, `titel`, `text`, `datum`, `url_titel`, `geschriebenvonbenutzername`, `tags`) VALUES
(5, 'Forscher suchen Glück in den Genen ', 'Glücklicher als die Menschen in Dänemark fühlt sich laut Umfragen kaum jemand. Warum nur? Ist es der fürsorgliche Sozialstaat? Die neueste Theorie: 5-HTTLPR könnte dafür verantwortlich sein. \r\n[weiterlesen]\r\nDas Glück der Dänen ist schon fast unheimlich. Immer wieder landet das kleine Volk in den Zufriedenheits-Ranglisten ganz oben. Die Europäische Kommission fragt seit Mitte der Siebzigerjahre in ihrem Eurobarometer gelegentlich danach, wie glücklich die Europäer sind. Immer weit vorne: die Dänen. Dem Satz "Ich bin persönlich glücklich mit meinem Leben" stimmten 96 Prozent der Dänen zu; gefragt hatte 2011 die Hamburger Stiftung für Zukunftsfragen in 13 Ländern, nirgendwo sonst war die Quote so hoch.\r\n\r\nAls die Vereinten Nationen 2012 ihren ersten "World Happiness Report" veröffentlichten, verortete dieser die unglücklichsten Menschen in Afrika, die glücklichsten in Nordeuropa - und die allerglücklichsten in Dänemark. Die zweite Auflage 2013 kam zum selben Ergebnis.\r\n\r\nWas macht die Dänen nur so glücklich? Die Erklärungsversuche sind vielfältig: Wohlstand, ein fürsorglicher Sozialstaat, Toleranz gegenüber sich selbst und anderen. Zwei Wissenschaftler der britischen Universität Warwick fügen den Mutmaßungen nun eine Theorie hinzu: Gute Gene. Ist das Glück am Ende angeboren?\r\n\r\n"Es gibt viel Literatur zu den Faktoren für Glück, aber selbst wenn man diese alle berücksichtigt, fehlt am Ende immer noch etwas, eine letzte Erklärung", erläutert der Ökonom Eugenio Proto, warum er den Zusammenhang zwischen dänischen Genen und dänischem Glück nachgeht. Er und sein Mitautor Andrew Oswald haben dafür 143 Länder untersucht. Weil es nicht genug Daten über das Erbgut einzelner Völker gibt, haben sie sich deren "genetischen Abstand", also die Unterschiede zu den Dänen angeschaut. Ihr Ergebnis: Länder, in denen große Unzufriedenheit herrscht, haben einen großen genetischen Abstand zu Dänemark. Andersherum: Je glücklicher eine Nation, desto ähnlicher ist ihr Erbgut dem dänischen. Andere Ähnlichkeiten haben die Autoren herausgerechnet, etwa geografische Nähe, ähnliche Kultur, vergleichbare Sozialsysteme. Es ist eine statistische Untersuchung und keine, die einzelne Gene betrachtet. Einen Schlüssel zur DNA des Glücks liefert sie nicht.\r\nLiebe zählt mehr als Gesundheit\r\n\r\nNur ein Gen haben sich die Autoren genau angesehen: das Serotonin-Transporter-Gen 5-HTTLPR. Dieses gibt es in zwei Ausprägungen, mit kurzem und mit langem Allel. Es existieren Theorien, wonach Träger der kurzen Ausprägung anfälliger für Depressionen sind. Für 30 Länder haben die Autoren den Test gemacht. Ergebnis: In Ländern, die sich in den Umfragen als unzufrieden beschreiben, leben mehr Menschen mit der kurzen Ausprägung des Gens. In Dänemark dagegen trägt der kleinste Anteil jenes mit kurzem Allel.\r\n\r\nWenn die These mit den Glücksgenen stimmt, müsste der Wohnort eine kleinere Rolle spielen als die Herkunft. Haben also US-Amerikaner, deren Vorfahren aus Italien eingewandert sind, ein ähnliches Glücksempfinden, wie es in Italien gemessen wird? Die Statistik gibt laut Proto und Oswald Hinweise darauf, dass es so ist. Dennoch weisen die Autoren darauf hin, man solle die Ergebnisse ihrer Studie mit Vorsicht behandeln. Liegt also das Glück wirklich in den Genen? "Wir sind nicht hundertprozentig sicher, dass ein Zusammenhang besteht", sagt Proto.\r\n\r\nDie Europäische Kommission übrigens hat die Einwohner der EU-Länder 2008 gefragt, wovon ihr Glück abhängt. In allen Ländern wählte die Mehrheit Gesundheit als wichtigstes Kriterium. Nur den Dänen war etwas anderes wichtiger für ihr Glück: die Liebe.', '30.07.2014', 'forscher_suchen_glueck_in_den_genen', 'fapeg', 'glück|dänemark|forschung|artikel'),
(6, 'aRussland verhängt Importstopp für Obst und Gemüse aus Polen', 'Kurz nachdem der Westen Wirtschaftssanktionen beschlossen hat, verbietet Russland die Einfuhr von Obst und Gemüse aus Polen. Die Regierung in Warschau ist ein vehementer Kritiker von Putins Rolle im Ukraine-Konflikt.\r\n[weiterlesen]\r\nMoskau - Offiziell sind Gesundheitsbedenken der Grund: Russland hat inmitten wachsender Spannungen mit dem Westen einen Importstopp für Obst und Gemüse aus Polen verhängt. Die Einfuhr "fast aller" Sorten an Früchten und Gemüse sei vom 1. August an wegen Verstößen gegen die Lebensmittelsicherheit verboten, teilte die Agraraufsicht am Mittwoch in Moskau mit.\r\n\r\nVon der Produktion gehe eine Gefahr für die Verbraucher aus, hieß es in der Mitteilung. So sei in 90 Prozent aller überprüften Äpfel eine unzulässig hohe Belastung mit Pestiziden festgestellt worden. Von dem Verbot betroffen sind zudem unter anderem Birnen, Pflaumen und Kirschen, aber auch Kohl.\r\n\r\nDie polnischen Behörden seien mehrfach verwarnt worden, so die Lebensmittelaufsicht. Beanstandet wurden auch Ungezieferbefall sowie fehlerhafte Lieferdokumente. Bereits am Montag hatte Russland nach der Entdeckung schädlicher Insekten in Einfuhren mit Importverboten gegen Länder der Europäischen Union gedroht.\r\n\r\nRussische Importverbote sind keine Seltenheit\r\n\r\nPolen ist einer der wichtigsten Obst- und Gemüselieferanten für Russland. Nach russischen Angaben lag allein der Import von Äpfeln, Birnen und Quitten aus Polen im vergangenen Jahr bei 776.000 Tonnen im Wert von fast 430 Millionen US-Dollar.\r\n\r\nRussland verhängt häufig Importstopps und führt dafür Gesundheitsbedenken an. Handelspartner sehen hinter solchen Schritten aber oftmals politische Motive. In den vergangenen zwei Monaten untersagte Russland bereits diverse Einfuhren aus der Ukraine und aus Moldau.\r\n\r\nDas aktuelle Importverbot könnte eine Reaktion auf die verschärften Sanktionen sein, die EU und USA am Dienstag beschlossen. Der Westen wirft Russland vor, die Unruhen in der Ostukraine anzuheizen. Zudem vermuten Kommentatoren auch, dass die Regierung in Moskau gezielt Polens Politik in der Ukraine-Krise bestrafen möchte. Polen gilt als einer der wichtigsten Partner der prowestlichen Regierung in Kiew und befürwortet Sanktionen gegen Russland als Strafe für die Unterstützung der Separatisten in der umkämpften Ostukraine.', '30.07.2015', 'russland_verhaengt_importstopp_fuer_obst_und_gemuese_aus_polen', 'fapeg', 'russland|artikel|obst|gemüse'),
(11, ' Baukunst 3200 v. Chr.: Ein Tempel der Steinzeit', 'Sie verfügten zwar nur über steinzeitliche Techniken, aber die Vision der Baumeister am rauen Rand Europas war ihrer Zeit um Jahrtausende voraus. Um 3200 v. Chr. errichteten die Ureinwohner der Orkneys eine monumentale Tempelanlage, die alles Dagewesene übertraf.\r\n[weiterlesen]\r\nAuf dem fruchtbaren Archipel vor der Nordspitze des heutigen Schottland bauten die Bewohner Tausende von Tonnen feinkörnigen Sandstein ab und transportierten ihn mehrere Kilometer weit auf einen grasbewachsenen Hügel mit einem majestätischen Rundblick über die Landschaft. Das handwerkliche Können dieser frühen Architekten war beeindruckend: Die mächtigen Mauern, die sie errichteten, hätten den römischen Legionären alle Ehre gemacht, die etwa 30 Jahrhunderte später rund 650 Kilometer weiter südlich den Hadrianswall bauten.\r\n\r\n Auf unserer Zeitreise springen wir nun fünf Jahrtausende vorwärts und landen an einem milden Sommernachmittag auf einer malerischen Landzunge, dem Ness of Brodgar, unweit von Kirkwall, der Hauptstadt der Orkneys. Hier gräbt ein Team aus Archäologen, Universitätsprofessoren, Studenten und Freiwilligen eine Ansammlung großartiger Gebäude aus, die lange Zeit verschüttet unter einem Acker lagen. Der Archäologe Nick Card, Grabungsleiter am Archäologischen Institut der University of the Highlands and Islands in Kirkwall, sagt, die Entdeckung der Ruinen stelle die britische Vorgeschichte auf den Kopf.\r\n\r\nDie Entdeckung ist deshalb so faszinierend, weil die Ruinen im Herzen einer der dichtesten Ansammlungen prähistorischer Monumente in Großbritannien gefunden wurden. Wenn man heute auf dem Ness steht, hat man mehrere steinzeitliche Kulturdenkmäler im Blick, die zusammen ein Weltkulturerbe bilden, The Heart of Neolithic Orkney. Einen Kilometer entfernt auf einem mit Heidekraut bewachsenen Hügel erhebt sich ein gigantischer, an Tolkiens Romane erinnernder Steinkreis, Ring of Brodgar genannt. Ein zweiter zeremonieller Steinkreis, die Stones of Stenness, ist jenseits des Fahrdamms zu sehen, der zum Ness führt. Und anderthalb Kilometer entfernt thront ein unheimlich wirkender Grabhügel, genannt Maes Howe, ein gewaltiger, über 4500 Jahre alter Kammerbau. Maes Howe ist außerdem auf die Mittelachse und den Eingang des vor kurzem entdeckten Tempels am Ness ausgerichtet.\r\n\r\nBis vor 30 Jahren sah man den Ring of Brodgar, die Stones of Stenness und das Hügelgrab Maes Howe als isolierte Monumente mit unterschiedlichen Entstehungsgeschichten. "Das Ness erzählt uns jetzt, dass hier eine wesentlich stärker zusammenhängende Struktur existierte", sagt Card.\r\n\r\nIm Jahr 1850 fegte ein Sturm in der Bucht von Skaill, an der Westküste der Hauptinsel Mainland, einige Sanddünen weg und legte ein erstaunlich gut erhaltenes steinzeitliches Dorf frei.\r\n\r\nIn den Ruinen fanden sich auch kostbare Handelswaren\r\n\r\nDer erste Hinweis auf weitere erstaunliche Dinge, die im Boden am Ness ruhen, tauchte im Jahr 2002 auf, als eine geophysikalische Studie große, von Menschenhand gemachte Besonderheiten unter der Erdoberfläche aufspürte. Man begann mit Erkundungsgrabungen, aber erst im Jahr 2008 begriffen die Archäologen allmählich, wie groß die Stätte war, auf die sie zufällig gestoßen waren. Bislang sind erst zehn Prozent freigelegt, zahlreiche weitere Steinbauten liegen noch in der Umgebung unter dem Rasen verborgen.\r\n\r\nIn den Ruinen fanden sich auch kostbare Handelswaren wie vulkanisches Glas von so weit entfernten Orten wie der Insel Arran im Westen Schottlands. Diese Artefakte legen nahe, dass die Orkneys an einer etablierten Handelsroute lagen und die Tempelanlage am Ness eine Pilgerstätte gewesen sein könnte.\r\n\r\nFaszinierender noch als Gegenstände, die die Händler mitbrachten, war, was sie wieder mitnahmen: Ideen und Inspiration. Markant bemalte Tonscherben, die am Ness und anderswo gefunden wurden, lassen vermuten, dass die mit Mustern dekorierten Töpfereien, die im neolithischen Britannien verbreitet waren, ihren Ursprung auf den Orkneys hatten. "Das steht völlig im Widerspruch zur gängigen Auffassung, alles Kulturelle müsse aus dem vornehmen Süden gekommen sein, um den barbarischen Norden zu zivilisieren", sagt Roy Towers, Archäologe und Keramikexperte.\r\n\r\nTausend Jahre lang, länger als Westminster Abbey und die Kathedrale von Canterbury stehen, zog die Tempelanlage am Ness die Landschaft und Generationen von Bewohnern der Orkneys in ihren Bann - ein Symbol für Reichtum, Macht und kulturelle Energie. Doch irgendwann um das Jahr 2300 v. Chr. ging alles zu Ende.\r\n\r\nWas immer der Grund war, der uralte Tempel wurde ausgemustert und zum Teil zerstört - ab sichtlich und symbolisch.\r\n\r\nIm Laufe der Jahrhunderte nach der Aufgabe der Tempelanlage am Ness forderten Zeit und Elemente ihren Tribut. Was immer an Steinen der alten vergessenen Mauern noch sichtbar war, wurde von den neuen Siedlern zum Bau ihrer eigenen Häuser und Höfe verwendet. Jetzt waren sie an der Reihe, ihren Teil der Geschichte auf der windgepeitschten Bühne der Orkneys zu spielen.', '17.08.2014', 'baukunst_3200_v._chr.:_ein_tempel_der_steinzeit', 'fapeg', 'artikel|tempel|steinzeit|technik|irland'),
(18, 'Irland und die Kartoffel – eine Art Liebesgeschichte', 'Die Iren gelten nicht nur als Weltmeister im Teetrinken, die globalen Legenden sehen Irland auch noch immer als die Champions des Kartoffelkonsums. Tatsächlich lag der Pro-Kopfverbrauch im 19. Jahrhundert, als das Nahrungsangebot sich auf der verarmten Grünen Insel sehr in Grenzen hielt, bei sagenhaften 2.000 Kilogramm. Damals stand auf dem Speiseplan des einfachen Volkes nur eines: Kartoffel, Kartoffel, und noch mal Kartoffel. Als deshalb ab 1845 mehrere Jahre die Kartoffelernte ausfiel, war die Katastrophe da: Eine Million Menschen starben an den Folgeerkrankungen des Hungers, 1,5 Millionen wanderten notgedrungen aus, die Bevölkerungszahl fiel innerhalb weniger Jahrzehnte von 7 auf 3,8 Millionen.\r\n\r\nDas Trauma der großen Hungersnot (“Famine”) ist auch heute noch gegenwärtig in Irland. Die Kartoffel allerdings hat Ihre zentrale Bedeutung verloren – was eng mit dem hohen Lebensstandard der zu Wohlstand gekommenen Irinnen und Iren zusammen hängt. Heute konsumiert der Durchschnitts-Insulaner noch gut 100 Kilogramm Erdäpfel, weit mehr als Deutsche, Italiener und Franzosen, deutlich weniger allerdings als Polen, Russen, Rumänen oder Ukrainer.\r\n\r\nSo gesehen bleibt Irland ein Kartoffel-verrücktes Land in Westeuropa – und die Aussichten, in einem echt irischen Restaurant eine Lasagne garniert mit Kartoffelsalat, Kartoffelbrei und ein paar Pommes zu bekommen, sind noch immer ganz gut. Auch als Chips (hier: Crisps) werden die Erdknollen in degenerierter Form tonnenweise konsumiert. Die Love Story hält auch dem Wohlstand stand. Der irische Wohlstand dokumentiert sich übrigens auch in Kleinigkeiten: Die großen preiswerten 10- und 20-Kilogramm-Kartoffelsäcke mit der erdigen Rohware sind aus der Mode gekommen. Iren kaufen heutzutage bevorzugt die kleinen Zwei- oder Fünf-Kilo-Beutel mit gewaschenen und kochfertigen Knollen.\r\n\r\nIn diesem Jahr freute sich Irland aufgrund des guten Wetters übrigens über eine außergewöhnlich gute Kartoffelernte und erstmals seit Menschengedenken exportierten irische Farmer wieder beachtliche Mengen ihrer Krummbirnen ins Ausland: Roosters und Kerr Pinks für die Welt. Irland jammert in diesen Jahren viel über den Zustand im eigenen Land. Wer einmal in etwas längeren Zeitläuften denkt, beispielsweise von der Einführung der Patate in Irland im Jahr 1588 bis zur Gegenwart, der kommt ohne Umschweife zum Schluss: Diesem Land und seinen Einwohnern geht es prächtig. Besser als den meisten anderen Menschen weltweit und so gut wie fast nie zuvor. Darauf einen Poitin – destilliert aus Kartoffeln!\r\n(Quelle: http://www.irlandnews.com)', '20.08.2014', 'irland_und_die_kartoffel_1408546310.06', 'Mirinda', 'kartoffel|artikel|irland|glück'),
(19, 'Feuer und Eis', 'Ben & Jerry''s startet 1986 eine landesweite Marketing-Tour mit dem Cow Mobile, das zur Auslieferung von Gratis-Eis verwendet worden war. Dann kommt es zu einem Unglück. Auf der Rückreise brennt das Cow Mobile in der Nähe von Cleveland, Ohio, völlig aus. Zum Glück wurde keiner verletzt. Laut Ben sah es aus „wie das weltgrößte Omelette Surprise“.\r\n(Quelle: http://www.benjerry.de)', '20.08.2014', 'feuer_und_eis_1408547039.89', 'Mirinda', 'irland|artikel|eis|marketing'),
(20, 'Kartoffel Teil 2', 'In Irland wird wirklich zu jedem Gericht die Kartoffel serviert. Dabei hat die Kartoffel verschiedene Formen. Es gibt sehr oft Kartoffel -brei oder gedünstete Kartoffel. Manchmal wird die Kartoffel auch geröstet. Seit ich in Irland war, kann ich keine Kartoffel mehr sehen, ohne in Panik auszubrechen. Die Kartoffel ist mein Feind. Sogar zu Sanwiches wurden Chips aus Kartoffel serviert. Und der Vater einer Freundin aus Dublin ist davon überzeugt, dass ohne Kartoffel kein Essen ein ordentliches Essen ist. Ich dachte, die Kartoffel sei bei den Deutschen das Lieblingsessen, aber die Kartoffel ist bei den Iren noch viel beliebter.', '20.08.2014', 'kartoffel_teil_2_1408550303.74', 'Mirinda', 'irland|artikel|gemüse|kartoffel');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kommentar`
--

CREATE TABLE IF NOT EXISTS `kommentar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `blogeintragid` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(300) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `text` text NOT NULL,
  `datum` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=27 ;

--
-- Daten für Tabelle `kommentar`
--

INSERT INTO `kommentar` (`id`, `blogeintragid`, `name`, `email`, `url`, `text`, `datum`) VALUES
(23, 20, 'fabian', 'fabian@fapeg.com', NULL, 'aha', '21.08.2014 - 14:04 Uhr'),
(24, 20, 'fabian', 'fabian@fapeg.com', NULL, 'test', '21.08.2014 - 14:05 Uhr'),
(25, 19, 'Fabian', 'fabian@fapeg.com', NULL, 'Test2', '21.08.2014 - 14:05 Uhr'),
(26, 20, 'fabian', 'fabian@fapeg.com', 'fapeg.com', 'blablabla', '23.08.2014 - 21:07 Uhr');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
