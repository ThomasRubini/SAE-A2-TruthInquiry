SET FOREIGN_KEY_CHECKS=0;

INSERT INTO `T_ANSWER` (`ANSWER_ID`, `QA_TYPE`, `NPC_ID`, `TEXT_LID`) VALUES
(1, 0, 1, 1),
(2, 0, 1, 2),
(3, 1, 1, 3),
(4, 1, 1, 4),
(5, 0, 2, 6),
(6, 0, 2, 7),
(7, 1, 2, 8),
(8, 1, 2, 9),
(9, 0, 3, 11),
(10, 0, 3, 12),
(11, 1, 3, 13),
(12, 1, 3, 14),
(13, 0, 4, 16),
(14, 0, 4, 17),
(15, 1, 4, 18),
(16, 1, 4, 19),
(17, 0, 5, 21),
(18, 0, 5, 22),
(19, 1, 5, 23),
(20, 1, 5, 24),
(21, 0, 6, 26),
(22, 0, 6, 27),
(23, 1, 6, 28),
(24, 1, 6, 29),
(25, 0, 7, 31),
(26, 0, 7, 32),
(27, 1, 7, 33),
(28, 1, 7, 34),
(29, 0, 8, 36),
(30, 0, 8, 37),
(31, 1, 8, 38),
(32, 1, 8, 39);

INSERT INTO `T_LOCALE` (`TEXT_ID`, `LANG`, `TEXT`) VALUES
(0, 'FR', 'Le Médecin'),
(1, 'FR', 'Il y avait {SALLE} ça m\'a intrigué.'),
(2, 'FR', '{SALLE} avait l\'air sympa donc j\'y suis allé.'),
(3, 'FR', 'Il me semble qu\'il y avait {NPC}.'),
(4, 'FR', 'Je suis pratiquement sûr que j\'étais avec {NPC}.'),
(5, 'FR', 'Le Diplomate'),
(6, 'FR', 'Je profitais d\'une collation dans {SALLE}.'),
(7, 'FR', 'J\'admirais la décoration subtile de {SALLE} ... je m\'en inspirerais pour chez moi.'),
(8, 'FR', 'Je m\'instruisais auprès de {NPC}.'),
(9, 'FR', 'Avec {NPC} pour exposer nos différents points de vus sur divers sujets.'),
(10, 'FR', 'Le Combattant'),
(11, 'FR', '{SALLE} nous a servi de salle de duel.'),
(12, 'FR', 'J\'ai festoillé dans {SALLE}.'),
(13, 'FR', 'On faisait un bras de fer avec {NPC}.'),
(14, 'FR', '{NPC} et moi nous sommes engagés dans une joute verbale des plus palpitante.'),
(15, 'FR', 'La Duchesse'),
(16, 'FR', 'Pour votre gouverne je me trouvais dans {SALLE}.'),
(17, 'FR', 'Si vous voulez le savoir ... j\'étais en train de me reposer dans {SALLE}.'),
(18, 'FR', '{NPC} me tenait compagnie.'),
(19, 'FR', 'J\'étais avec {NPC}.'),
(20, 'FR', 'La Diva'),
(21, 'FR', '{SALLE} me semblait être la plus belle pièce de la maison.'),
(22, 'FR', 'Je buvais un verre dans {SALLE}.'),
(23, 'FR', 'Je profitais de la compagnie de {NPC}.'),
(24, 'FR', 'J\'étais avec {NPC} à partager une délicieuse conversation ainsi qu\'une coupe de champagne.'),
(25, 'FR', 'La Parieuse'),
(26, 'FR', 'J\'avais monté une table de jeu dans {SALLE}.'),
(27, 'FR', '{SALLE} est tout de même plus agréable une fois changé(e), en casino.'),
(28, 'FR', 'Vous saviez que {NPC} était incroyable avec des cartes à la main ?'),
(29, 'FR', 'Si vous tenez à votre argent ne jouez jamais au poker avec {NPC}.'),
(30, 'FR', 'L\'Agent'),
(31, 'FR', 'On pouvait me retrouver dans {SALLE}.'),
(32, 'FR', '{SALLE}'),
(33, 'FR', 'J\'étais avec {NPC} au moment des faits.'),
(34, 'FR', '{NPC}'),
(35, 'FR', 'La Voyageuse'),
(36, 'FR', '{SALLE} me semblait un bon endroit pour me poser'),
(37, 'FR', '{SALLE} me rappelait mes voyages.'),
(38, 'FR', 'Nous organisions notre prochain voyage avec {NPC}.'),
(39, 'FR', 'Avec {NPC} on parlait des lieux que l’on avait visités. C’était très instructif.'),
(100, 'FR', 'Ce manoir est plutôt grand ... vous pouvez me dire où vous étiez?'),
(101, 'FR', 'Vous étiez où au moment des faits?'),
(102, 'FR', 'Dans quelle salle étiez-vous pendant que le coffre était subtilisé ?'),
(105, 'FR', 'Etiez-vous seul au moment des faits ?'),
(106, 'FR', 'Quelqu’un peu valider vous alibi pour la soirée ?'),
(107, 'FR', 'Vous étiez accompagné ce soir-là ?'),
(110, 'FR', 'Un maintien rigide des traits du visage, un regard de travers. Une crispation des sourcils et parfois des rides autour de la bouche. Ces caractéristiques sont synonymes d\'incompréhension ou de peur de ce que peut nous annoncer la personne en face.'),
(111, 'FR', 'Un visage décontracté et ouvert, les muscles des joues contractés qui laissent apparaître un sourire. On le détermine aussi par des yeux plissés en accord avec les sourcils qui marquent la différence avec un faux sourire où les sourcils ne sont pas contractés. Cela montre une complicité avec l\'interlocuteur ou un moyen de ne pas laisser paraître ses réelles émotions.'),
(112, 'FR', 'Des sourcils contractés et resserrés vers le centre du visage auxquels s\'ajoute un regard vide ou fuyant de l\'interlocuteur, soit en fermant les yeux soit en évitant un contact visuel. Ces caractéristiques témoignent d\'un sentiment puissant ou du fait d\'être atteint par les propos ou accusations de son interlocuteur.'),
(113, 'FR', 'Un visage crispé qui s\'accompagne habituellement de sourcils froncés, un regard perdu qui se détourne de celui de son interlocuteur. Cela s\'accompagne souvent de mouvements de la tête et de la bouche en se mordant les lèvres par exemple. Tout cela traduit une difficulté de concentration ou une peur de ce qu\'annonce ou peut nous annoncer l\'interlocuteur en face.'),
(114, 'FR', 'Généralement par des yeux écarquillés et un haussement des sourcils. Cela peut également se distinguer par une bouche ouverte ou, au contraire, des dents serrées et parfois par un relâchement du visage. Ces caractéristiques correspondent à un choc, une incompréhension ou encore un étonnement de ce que voit ou entend la personne.'),
(120, 'FR', 'méfiant(e),'),
(121, 'FR', 'heureux(se),'),
(122, 'FR', 'triste'),
(123, 'FR', 'stressé(e),'),
(124, 'FR', 'surpris(e),'),
(130, 'FR', 'Le salon'),
(131, 'FR', 'La salle de réception'),
(132, 'FR', 'Le hall d\'entrée'),
(133, 'FR', 'La cuisine'),
(134, 'FR', 'La chambre du maître'),
(135, 'FR', 'Le jardin');

INSERT INTO `T_NPC` (`NPC_ID`, `NAME_LID`) VALUES
(1, 0),
(2, 5),
(3, 10),
(4, 15),
(5, 20),
(6, 25),
(7, 30),
(8, 35);

INSERT INTO `T_PLACE` (`PLACE_ID`, `NAME_LID`) VALUES
(1, 130),
(2, 131),
(3, 132),
(4, 133),
(5, 134),
(6, 135);

INSERT INTO `T_QUESTION` (`QUESTION_ID`, `QUESTION_TYPE`, `TEXT_LID`) VALUES
(1, 0, 100),
(2, 0, 101),
(3, 0, 102),
(4, 1, 105),
(5, 1, 106),
(6, 1, 107);

INSERT INTO `T_REACTION` (`REACTION_ID`, `NPC_ID`, `TRAIT_ID`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 8, 1),
(9, 1, 2),
(10, 2, 2),
(11, 3, 2),
(12, 4, 2),
(13, 5, 2),
(14, 6, 2),
(15, 7, 2),
(16, 8, 2),
(17, 1, 3),
(18, 2, 3),
(19, 3, 3),
(20, 4, 3),
(21, 5, 3),
(22, 6, 3),
(23, 7, 3),
(24, 8, 3),
(25, 1, 4),
(26, 2, 4),
(27, 3, 4),
(28, 4, 4),
(29, 5, 4),
(30, 6, 4),
(31, 7, 4),
(32, 8, 4),
(33, 1, 5),
(34, 2, 5),
(35, 3, 5),
(36, 4, 5),
(37, 5, 5),
(38, 6, 5),
(39, 7, 5),
(40, 8, 5);

INSERT INTO `T_TRAIT` (`TRAIT_ID`, `NAME_LID`,`DESC_LID`) VALUES
(1, 120, 110),
(2, 121, 111),
(3, 122, 112),
(4, 123, 113),
(5, 124, 114);

SET FOREIGN_KEY_CHECKS=1;