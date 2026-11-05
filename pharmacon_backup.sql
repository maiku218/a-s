BEGIN TRANSACTION;
DROP TABLE IF EXISTS admin_activity;
CREATE TABLE admin_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action VARCHAR(100) NOT NULL,
            ip_address VARCHAR(45) DEFAULT NULL,
            details TEXT,
            activity_time TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE
        );
INSERT INTO "admin_activity" VALUES(52,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:03:20');
INSERT INTO "admin_activity" VALUES(53,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:03:35');
INSERT INTO "admin_activity" VALUES(54,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:04:08');
INSERT INTO "admin_activity" VALUES(55,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:19:06');
INSERT INTO "admin_activity" VALUES(56,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:23:00');
INSERT INTO "admin_activity" VALUES(57,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:23:16');
INSERT INTO "admin_activity" VALUES(58,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:23:33');
INSERT INTO "admin_activity" VALUES(59,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:24:23');
INSERT INTO "admin_activity" VALUES(60,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:24:43');
INSERT INTO "admin_activity" VALUES(61,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:32:14');
INSERT INTO "admin_activity" VALUES(62,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 12:32:14');
INSERT INTO "admin_activity" VALUES(63,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:32:30');
INSERT INTO "admin_activity" VALUES(64,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 12:32:30');
INSERT INTO "admin_activity" VALUES(65,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:37:22');
INSERT INTO "admin_activity" VALUES(66,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 12:37:23');
INSERT INTO "admin_activity" VALUES(67,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 12:38:46');
INSERT INTO "admin_activity" VALUES(68,14,'Register Cashier','127.0.0.1','Registered cashier: pharmacon','2026-09-09 12:39:53');
INSERT INTO "admin_activity" VALUES(69,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 12:39:58');
INSERT INTO "admin_activity" VALUES(70,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 13:11:23');
INSERT INTO "admin_activity" VALUES(71,14,'Edit Product','127.0.0.1','Edited product: Paracetamol 500mg','2026-09-09 13:27:56');
INSERT INTO "admin_activity" VALUES(72,14,'Edit Product','127.0.0.1','Edited product: Paracetamol 500mg','2026-09-09 16:31:50');
INSERT INTO "admin_activity" VALUES(73,14,'Edit Product','127.0.0.1','Edited product: Amoxicillin 250mg1','2026-09-09 16:32:15');
INSERT INTO "admin_activity" VALUES(74,14,'Delete Product','127.0.0.1','Deleted product: Amoxicillin 250mg1','2026-09-09 16:32:19');
INSERT INTO "admin_activity" VALUES(75,14,'Add New Product','127.0.0.1','sdgasdg - 222 units added','2026-09-09 16:32:41');
INSERT INTO "admin_activity" VALUES(76,14,'Add New Product','127.0.0.1','wfqwrqw - 444 units added','2026-09-09 16:33:01');
INSERT INTO "admin_activity" VALUES(77,14,'Delete Product','127.0.0.1','Deleted product: wfqwrqw','2026-09-09 16:33:10');
INSERT INTO "admin_activity" VALUES(78,14,'Edit Product','127.0.0.1','Edited product: Paracetamol 500mg','2026-09-09 16:35:34');
INSERT INTO "admin_activity" VALUES(79,14,'Edit Product','127.0.0.1','Edited product: Bandage','2026-09-09 16:35:51');
INSERT INTO "admin_activity" VALUES(80,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 18:01:28');
INSERT INTO "admin_activity" VALUES(81,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 18:45:44');
INSERT INTO "admin_activity" VALUES(82,14,'Add New Product','127.0.0.1','asd - 123 units added','2026-09-09 18:46:08');
INSERT INTO "admin_activity" VALUES(83,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 21:18:59');
INSERT INTO "admin_activity" VALUES(84,14,'Delete Product','127.0.0.1','Deleted product: Paracetamol 500mg','2026-09-09 21:19:29');
INSERT INTO "admin_activity" VALUES(85,14,'Delete Product','127.0.0.1','Deleted product: Bandage','2026-09-09 21:19:30');
INSERT INTO "admin_activity" VALUES(86,14,'Delete Product','127.0.0.1','Deleted product: sdgasdg','2026-09-09 21:19:32');
INSERT INTO "admin_activity" VALUES(87,14,'Delete Product','127.0.0.1','Deleted product: asd','2026-09-09 21:19:34');
INSERT INTO "admin_activity" VALUES(88,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 21:19:53');
INSERT INTO "admin_activity" VALUES(89,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 21:20:06');
INSERT INTO "admin_activity" VALUES(90,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 21:20:16');
INSERT INTO "admin_activity" VALUES(91,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-09 21:24:23');
INSERT INTO "admin_activity" VALUES(92,14,'Add New Product','127.0.0.1','asdfasd - 42 units added','2026-09-09 21:25:53');
INSERT INTO "admin_activity" VALUES(93,14,'Edit Product','127.0.0.1','Edited product: asdfasd','2026-09-09 21:26:02');
INSERT INTO "admin_activity" VALUES(94,14,'Delete Product','127.0.0.1','Deleted product: asdfasd','2026-09-09 21:26:11');
INSERT INTO "admin_activity" VALUES(95,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-09 21:27:45');
INSERT INTO "admin_activity" VALUES(96,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-10 07:56:01');
INSERT INTO "admin_activity" VALUES(97,14,'Add New Product','127.0.0.1','Nature Spring 500mL - 22 units added','2026-09-10 14:03:45');
INSERT INTO "admin_activity" VALUES(98,14,'Add New Product','127.0.0.1','Beng-Beng (22g) - 8 units added','2026-09-10 14:05:37');
INSERT INTO "admin_activity" VALUES(99,14,'Add New Product','127.0.0.1','Choco Mucho (30g) - 10 units added','2026-09-10 14:08:21');
INSERT INTO "admin_activity" VALUES(100,14,'Add New Product','127.0.0.1','LM Chicken Sotanghon - 3 units added','2026-09-10 14:10:18');
INSERT INTO "admin_activity" VALUES(101,14,'Add New Product','127.0.0.1','LM Bulalo (40g) - 2 units added','2026-09-10 14:12:55');
INSERT INTO "admin_activity" VALUES(102,14,'Add New Product','127.0.0.1','LM Spicy Batchoy (40g) - 4 units added','2026-09-10 14:16:04');
INSERT INTO "admin_activity" VALUES(103,14,'Add New Product','127.0.0.1','LM Spicy Bulalo (40g) - 4 units added','2026-09-10 14:24:00');
INSERT INTO "admin_activity" VALUES(104,14,'Edit Product','127.0.0.1','Edited product: Nature Spring (500mL)','2026-09-10 14:30:04');
INSERT INTO "admin_activity" VALUES(105,14,'Edit Product','127.0.0.1','Edited product: LM Chicken Sotanghon (28g)','2026-09-10 14:30:46');
INSERT INTO "admin_activity" VALUES(106,14,'Add New Product','127.0.0.1','LM Batchoy (70g) - 2 units added','2026-09-10 14:32:41');
INSERT INTO "admin_activity" VALUES(107,14,'Add New Product','127.0.0.1','LM Jjampong (40g) - 7 units added','2026-09-10 14:33:55');
INSERT INTO "admin_activity" VALUES(108,14,'Add New Product','127.0.0.1','Nissin Seafood (40g) - 3 units added','2026-09-10 14:36:25');
INSERT INTO "admin_activity" VALUES(109,14,'Add New Product','127.0.0.1','Nescafe Original (20g) - 21 units added','2026-09-10 14:43:40');
INSERT INTO "admin_activity" VALUES(110,14,'Add New Product','127.0.0.1','Kopiko Blanca (20g) - 19 units added','2026-09-10 14:45:35');
INSERT INTO "admin_activity" VALUES(111,14,'Add New Product','127.0.0.1','Kopiko Brown (20g) - 7 units added','2026-09-10 14:47:19');
INSERT INTO "admin_activity" VALUES(112,14,'Add New Product','127.0.0.1','Kopiko Black (20g) - 6 units added','2026-09-10 14:48:52');
INSERT INTO "admin_activity" VALUES(113,14,'Add New Product','127.0.0.1','Lipton Tea Bag (2g) - 8 units added','2026-09-10 14:51:21');
INSERT INTO "admin_activity" VALUES(114,14,'Add New Product','127.0.0.1','Milo (24g) - 19 units added','2026-09-10 14:54:24');
INSERT INTO "admin_activity" VALUES(115,14,'Add New Product','127.0.0.1','Quaker Original w/ Milk (40g) - 2 units added','2026-09-10 14:56:01');
INSERT INTO "admin_activity" VALUES(116,14,'Add New Product','127.0.0.1','Quaker Banana & Honey (33g) - 3 units added','2026-09-10 14:56:58');
INSERT INTO "admin_activity" VALUES(117,14,'Add New Product','127.0.0.1','Nescafe Classic (1.9g) - 49 units added','2026-09-10 15:08:34');
INSERT INTO "admin_activity" VALUES(118,14,'Add New Product','127.0.0.1','Nestle Coffee Mate (5g) - 51 units added','2026-09-10 15:11:51');
INSERT INTO "admin_activity" VALUES(119,14,'Add New Product','127.0.0.1','Nestle Bear Brand (33g) - 13 units added','2026-09-10 15:12:56');
INSERT INTO "admin_activity" VALUES(120,14,'Add New Product','127.0.0.1','Birch Tree (33g) - 9 units added','2026-09-10 15:14:35');
INSERT INTO "admin_activity" VALUES(121,14,'Add New Product','127.0.0.1','Alaska Fortified (33g) - 5 units added','2026-09-10 15:16:42');
INSERT INTO "admin_activity" VALUES(122,14,'Add New Product','127.0.0.1','Eden Original (45g) - 4 units added','2026-09-10 15:17:45');
INSERT INTO "admin_activity" VALUES(123,14,'Add New Product','127.0.0.1','Alaska Condensed (38g) - 6 units added','2026-09-10 15:19:58');
INSERT INTO "admin_activity" VALUES(124,14,'Add New Product','127.0.0.1','Star Classic (30g) - 12 units added','2026-09-10 15:22:16');
INSERT INTO "admin_activity" VALUES(125,14,'Add New Product','127.0.0.1','Best Foods Mayo Magic (80ml) - 1 units added','2026-09-10 15:24:00');
INSERT INTO "admin_activity" VALUES(126,14,'Add New Product','127.0.0.1','Tang Orange (19g) - 1 units added','2026-09-10 15:25:08');
INSERT INTO "admin_activity" VALUES(127,14,'Add New Product','127.0.0.1','Tang Grapes (19g) - 9 units added','2026-09-10 15:26:07');
INSERT INTO "admin_activity" VALUES(128,14,'Add New Product','127.0.0.1','Tang Pineapple (19g) - 4 units added','2026-09-10 15:26:58');
INSERT INTO "admin_activity" VALUES(129,14,'Add New Product','127.0.0.1','Nestea Apple (19g) - 7 units added','2026-09-10 15:27:50');
INSERT INTO "admin_activity" VALUES(130,14,'Add New Product','127.0.0.1','Papa Banana Ketchup (25g) - 10 units added','2026-09-10 15:29:37');
INSERT INTO "admin_activity" VALUES(131,14,'Add New Product','127.0.0.1','Maggi Magic Sarap (8g) - 21 units added','2026-09-10 15:30:33');
INSERT INTO "admin_activity" VALUES(132,14,'Add New Product','127.0.0.1','Ajinomoto (24g) - 3 units added','2026-09-10 15:31:34');
INSERT INTO "admin_activity" VALUES(133,14,'Add New Product','127.0.0.1','Ajinomoto (11g) - 12 units added','2026-09-10 15:33:08');
INSERT INTO "admin_activity" VALUES(134,14,'Add New Product','127.0.0.1','Ajinomoto Ginisa (8g) - 16 units added','2026-09-10 15:36:11');
INSERT INTO "admin_activity" VALUES(135,14,'Add New Product','127.0.0.1','Equal Refined Sugar (1/4kg) - 9 units added','2026-09-10 15:37:33');
INSERT INTO "admin_activity" VALUES(136,14,'Add New Product','127.0.0.1','Knorr Sinigang Origina Mix (11g) - 17 units added','2026-09-10 15:39:49');
INSERT INTO "admin_activity" VALUES(137,14,'Add New Product','127.0.0.1','Mama Sitas Oyster Sauce (30g) - 6 units added','2026-09-10 15:41:24');
INSERT INTO "admin_activity" VALUES(138,14,'Add New Product','127.0.0.1','Bioderm Timeless (60g) - 1 units added','2026-09-10 16:06:15');
INSERT INTO "admin_activity" VALUES(139,14,'Add New Product','127.0.0.1','Bioderm Intense Coolness (60g) - 1 units added','2026-09-10 16:07:41');
INSERT INTO "admin_activity" VALUES(140,14,'Add New Product','127.0.0.1','Bioderm Coolness (60g) - 3 units added','2026-09-10 16:08:47');
INSERT INTO "admin_activity" VALUES(141,14,'Add New Product','127.0.0.1','Bioderm Clean White (60g) - 8 units added','2026-09-10 16:10:11');
INSERT INTO "admin_activity" VALUES(142,14,'Add New Product','127.0.0.1','Myra Whitening Papaya Extract (45g) - 2 units added','2026-09-10 16:12:49');
INSERT INTO "admin_activity" VALUES(143,14,'Add New Product','127.0.0.1','Johnsons Blossom (50g) - 1 units added','2026-09-10 16:14:04');
INSERT INTO "admin_activity" VALUES(144,14,'Add New Product','127.0.0.1','Johnsons Milk (50g) - 1 units added','2026-09-10 16:15:37');
INSERT INTO "admin_activity" VALUES(145,14,'Add New Product','127.0.0.1','Silka (65g) - 4 units added','2026-09-10 16:16:42');
INSERT INTO "admin_activity" VALUES(146,14,'Add New Product','127.0.0.1','GreenCross Cool Mountain (55g) - 2 units added','2026-09-10 16:18:41');
INSERT INTO "admin_activity" VALUES(147,14,'Add New Product','127.0.0.1','Safeguard Pure White (65g) - 7 units added','2026-09-10 16:20:02');
INSERT INTO "admin_activity" VALUES(148,14,'Add New Product','127.0.0.1','Perla Papaya (110g) - 6 units added','2026-09-10 16:21:07');
INSERT INTO "admin_activity" VALUES(149,14,'Add New Product','127.0.0.1','Perla Original White (110g) - 5 units added','2026-09-10 16:21:57');
INSERT INTO "admin_activity" VALUES(150,14,'Add New Product','127.0.0.1','Citric - 18 units added','2026-09-10 16:23:08');
INSERT INTO "admin_activity" VALUES(151,14,'Add New Product','127.0.0.1','Surf Bar Kalamansi (120g) - 9 units added','2026-09-10 16:24:08');
INSERT INTO "admin_activity" VALUES(152,14,'Add New Product','127.0.0.1','Surf Bar Cherry Blossom (120g) - 1 units added','2026-09-10 16:25:16');
INSERT INTO "admin_activity" VALUES(153,14,'Add New Product','127.0.0.1','Ariel Sunrise Fresh Liquid (58g) - 4 units added','2026-09-10 16:27:39');
INSERT INTO "admin_activity" VALUES(154,14,'Add New Product','127.0.0.1','Ariel w/ Downy Floral Passion (54g) - 14 units added','2026-09-10 16:33:14');
INSERT INTO "admin_activity" VALUES(155,14,'Add New Product','127.0.0.1','Pride Liquid (60ml) - 15 units added','2026-09-10 16:35:11');
INSERT INTO "admin_activity" VALUES(156,14,'Add New Product','127.0.0.1','Tide Perfect Clean (69g) - 2 units added','2026-09-10 16:37:05');
INSERT INTO "admin_activity" VALUES(157,14,'Add New Product','127.0.0.1','Tide w/ Downy Perfume Fantasy (67g) - 12 units added','2026-09-10 16:43:31');
INSERT INTO "admin_activity" VALUES(158,14,'Add New Product','127.0.0.1','Dove Shampoo Bio Keratin (13.5ml) - 12 units added','2026-09-10 16:57:35');
INSERT INTO "admin_activity" VALUES(159,14,'Add New Product','127.0.0.1','Dove Shampoo Ceramide (13.5ml) - 1 units added','2026-09-10 16:58:29');
INSERT INTO "admin_activity" VALUES(160,14,'Add New Product','127.0.0.1','Head & Shoulder Shampoo Smooth & Silky (12ml) - 9 units added','2026-09-10 16:59:59');
INSERT INTO "admin_activity" VALUES(161,14,'Add New Product','127.0.0.1','Sunsilk Shampoo Smooth & Manageable (15ml) - 7 units added','2026-09-10 17:01:45');
INSERT INTO "admin_activity" VALUES(162,14,'Add New Product','127.0.0.1','Sunsilk Shampoo Strong & Long (15ml) - 10 units added','2026-09-10 17:03:11');
INSERT INTO "admin_activity" VALUES(163,14,'Add New Product','127.0.0.1','Gard Refreshing Menthol (12ml) - 2 units added','2026-09-10 17:04:13');
INSERT INTO "admin_activity" VALUES(164,14,'Add New Product','127.0.0.1','Palmolive Intensive Moisture (15ml) - 5 units added','2026-09-10 17:06:34');
INSERT INTO "admin_activity" VALUES(165,14,'Add New Product','127.0.0.1','Palmolive Ultra Smooth (15ml) - 2 units added','2026-09-10 17:07:44');
INSERT INTO "admin_activity" VALUES(166,14,'Add New Product','127.0.0.1','Palmolive Silky Straight (15ml) - 5 units added','2026-09-10 17:08:51');
INSERT INTO "admin_activity" VALUES(167,14,'Add New Product','127.0.0.1','Dove Shampoo Restorative Oil (12ml) - 13 units added','2026-09-10 17:10:16');
INSERT INTO "admin_activity" VALUES(168,14,'Add New Product','127.0.0.1','Pantene Shampoo Total Damage Care (15ml) - 4 units added','2026-09-10 17:11:33');
INSERT INTO "admin_activity" VALUES(169,14,'Add New Product','127.0.0.1','Creamsilk Hairfall Defense (13ml) - 10 units added','2026-09-10 17:12:52');
INSERT INTO "admin_activity" VALUES(170,14,'Add New Product','127.0.0.1','Creamsilk Standout Straight (13ml) - 20 units added','2026-09-10 17:13:42');
INSERT INTO "admin_activity" VALUES(171,14,'Add New Product','127.0.0.1','Close Up Red Hot (10g) - 6 units added','2026-09-10 17:15:17');
INSERT INTO "admin_activity" VALUES(172,14,'Add New Product','127.0.0.1','Colgate Maximum Cavity Protection (20g) - 16 units added','2026-09-10 17:16:59');
INSERT INTO "admin_activity" VALUES(173,14,'Add New Product','127.0.0.1','Colgate Charcoal Clean (20g) - 9 units added','2026-09-10 17:17:57');
INSERT INTO "admin_activity" VALUES(174,14,'Add New Product','127.0.0.1','Colgate Fresh Confidence (20g) - 13 units added','2026-09-10 17:18:47');
INSERT INTO "admin_activity" VALUES(175,14,'Add New Product','127.0.0.1','Wings Floral Fresh (70g) - 2 units added','2026-09-10 17:20:05');
INSERT INTO "admin_activity" VALUES(176,14,'Add New Product','127.0.0.1','Del w/ Fragarance Pearls (33ml) - 11 units added','2026-09-10 17:22:11');
INSERT INTO "admin_activity" VALUES(177,14,'Add New Product','127.0.0.1','Del Lavender Breeze (22ml) - 1 units added','2026-09-10 17:23:22');
INSERT INTO "admin_activity" VALUES(178,14,'Add New Product','127.0.0.1','Del Blossom Fresh (33ml) - 7 units added','2026-09-10 17:24:15');
INSERT INTO "admin_activity" VALUES(179,14,'Add New Product','127.0.0.1','Downy Kontra Kulob (24ml) - 84902430344876 units added','2026-09-10 17:24:57');
INSERT INTO "admin_activity" VALUES(180,14,'Add New Product','127.0.0.1','Downy Kontra Kulog (24ml) - 8 units added','2026-09-10 17:25:47');
INSERT INTO "admin_activity" VALUES(181,14,'Add New Product','127.0.0.1','Downy Kontra Germa Safeguard (26ml) - 1 units added','2026-09-10 17:26:40');
INSERT INTO "admin_activity" VALUES(182,14,'Add New Product','127.0.0.1','Surf Sun Fresh (65g) - 6 units added','2026-09-10 17:27:21');
INSERT INTO "admin_activity" VALUES(183,14,'Add New Product','127.0.0.1','Surf Kalamansi (57g) - 2 units added','2026-09-10 17:28:07');
INSERT INTO "admin_activity" VALUES(184,14,'Add New Product','127.0.0.1','Surf Purple Blooms (65g)  - 1 units added','2026-09-10 17:29:24');
INSERT INTO "admin_activity" VALUES(185,14,'Add New Product','127.0.0.1','Surf Cherry Blossom (65g) - 6 units added','2026-09-10 17:30:06');
INSERT INTO "admin_activity" VALUES(186,14,'Add New Product','127.0.0.1','Surf Fabric Conditioner Lux Perfumer (25ml) - 13 units added','2026-09-10 17:31:09');
INSERT INTO "admin_activity" VALUES(187,14,'Add New Product','127.0.0.1','Surf Fabric Conditioner Blossom Fresh (40ml)  - 12 units added','2026-09-10 17:31:53');
INSERT INTO "admin_activity" VALUES(188,14,'Add New Product','127.0.0.1','Surf Bar Anti Bacterial (120g) - 2 units added','2026-09-10 17:33:00');
INSERT INTO "admin_activity" VALUES(189,14,'Add New Product','127.0.0.1','Surf Bar Kalamansi (120g) - 2 units added','2026-09-10 17:33:46');
INSERT INTO "admin_activity" VALUES(190,14,'Add New Product','127.0.0.1','Surf Bar Purple Blooms (120g) - 3 units added','2026-09-10 17:34:21');
INSERT INTO "admin_activity" VALUES(191,14,'Add New Product','127.0.0.1','Surf Bar Sun Fresh (120g)  - 3 units added','2026-09-10 17:35:04');
INSERT INTO "admin_activity" VALUES(192,14,'Add New Product','127.0.0.1','Pride Sakura Blossom (40g)  - 11 units added','2026-09-10 17:35:54');
INSERT INTO "admin_activity" VALUES(193,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 02:43:11');
INSERT INTO "admin_activity" VALUES(194,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 10:13:32');
INSERT INTO "admin_activity" VALUES(195,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 10:42:53');
INSERT INTO "admin_activity" VALUES(196,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 10:53:58');
INSERT INTO "admin_activity" VALUES(197,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 10:54:27');
INSERT INTO "admin_activity" VALUES(198,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 11:01:55');
INSERT INTO "admin_activity" VALUES(199,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 11:01:59');
INSERT INTO "admin_activity" VALUES(200,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 11:03:19');
INSERT INTO "admin_activity" VALUES(201,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 11:04:34');
INSERT INTO "admin_activity" VALUES(202,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 11:08:22');
INSERT INTO "admin_activity" VALUES(203,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 12:18:51');
INSERT INTO "admin_activity" VALUES(204,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 12:38:38');
INSERT INTO "admin_activity" VALUES(205,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 12:47:03');
INSERT INTO "admin_activity" VALUES(206,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 12:51:57');
INSERT INTO "admin_activity" VALUES(207,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 13:42:19');
INSERT INTO "admin_activity" VALUES(208,14,'Add New Product','127.0.0.1','LM Pancit Canton Chilimansi (60g) - 5 units added','2026-09-11 13:43:41');
INSERT INTO "admin_activity" VALUES(209,14,'Add New Product','127.0.0.1','LM Pancit Canton Kalamansi (60g) - 2 units added','2026-09-11 13:44:23');
INSERT INTO "admin_activity" VALUES(210,14,'Add New Product','127.0.0.1','LM Pancit Canton Extra Hot (120g) - 2 units added','2026-09-11 13:45:30');
INSERT INTO "admin_activity" VALUES(211,14,'Add New Product','127.0.0.1','LM Pancit Canton Kalamansi (120g) - 6 units added','2026-09-11 13:46:20');
INSERT INTO "admin_activity" VALUES(212,14,'Add New Product','127.0.0.1','LM Pancit Canton Chilimansi (120g) - 2 units added','2026-09-11 13:47:18');
INSERT INTO "admin_activity" VALUES(213,14,'Add New Product','127.0.0.1','LM Pancit Canton Sweet & Spicy (120g) - 2 units added','2026-09-11 13:48:20');
INSERT INTO "admin_activity" VALUES(214,14,'Add New Product','127.0.0.1','LM Noodles Beef (55g) - 10 units added','2026-09-11 13:51:16');
INSERT INTO "admin_activity" VALUES(215,14,'Add New Product','127.0.0.1','LM Noodles Spicy Labuyo (50g) - 4 units added','2026-09-11 13:52:45');
INSERT INTO "admin_activity" VALUES(216,14,'Add New Product','127.0.0.1','Payless Noodles Beef (55g) - 2 units added','2026-09-11 13:53:45');
INSERT INTO "admin_activity" VALUES(217,14,'Add New Product','127.0.0.1','LM Noodles Chicken (55g) - 6 units added','2026-09-11 13:54:36');
INSERT INTO "admin_activity" VALUES(218,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 15:51:02');
INSERT INTO "admin_activity" VALUES(219,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 16:42:12');
INSERT INTO "admin_activity" VALUES(220,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-11 16:45:40');
INSERT INTO "admin_activity" VALUES(221,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-11 16:57:31');
INSERT INTO "admin_activity" VALUES(222,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-19 09:21:53');
INSERT INTO "admin_activity" VALUES(223,14,'Add New Product','127.0.0.1','Bingo Carne Norte (100g) - 3 units added','2026-09-19 11:32:15');
INSERT INTO "admin_activity" VALUES(224,14,'Add New Product','127.0.0.1','Argentina Meat Loaf (170g) - 3 units added','2026-09-19 11:33:30');
INSERT INTO "admin_activity" VALUES(225,14,'Add New Product','127.0.0.1','Argentina Beef Loaf (250g) - 3 units added','2026-09-19 11:36:19');
INSERT INTO "admin_activity" VALUES(226,14,'Add New Product','127.0.0.1','Argentina Beef Loaf (170g) - 3 units added','2026-09-19 11:45:04');
INSERT INTO "admin_activity" VALUES(227,14,'Add New Product','127.0.0.1','Wow Ulam Afritada (155g) - 3 units added','2026-09-19 11:46:45');
INSERT INTO "admin_activity" VALUES(228,14,'Add New Product','127.0.0.1','Wow Ulam Caldereta (155g) - 3 units added','2026-09-19 11:47:53');
INSERT INTO "admin_activity" VALUES(229,14,'Add New Product','127.0.0.1','Wow Ulam Pochero (155g) - 3 units added','2026-09-19 11:48:53');
INSERT INTO "admin_activity" VALUES(230,14,'Add New Product','127.0.0.1','Wow Ulam Adobo (155g) - 3 units added','2026-09-19 11:49:57');
INSERT INTO "admin_activity" VALUES(231,14,'Add New Product','127.0.0.1','Toyo Sardines Spicy (155g) - 3 units added','2026-09-19 11:51:32');
INSERT INTO "admin_activity" VALUES(232,14,'Add New Product','127.0.0.1','Toyo Sardines Original (155g) - 3 units added','2026-09-19 11:52:43');
INSERT INTO "admin_activity" VALUES(233,14,'Add New Product','127.0.0.1','Fresca Sardines Original (155g) - 3 units added','2026-09-19 11:53:39');
INSERT INTO "admin_activity" VALUES(234,14,'Add New Product','127.0.0.1','Fresca Sardines Spicy (155g) - 3 units added','2026-09-19 11:54:59');
INSERT INTO "admin_activity" VALUES(235,14,'Add New Product','127.0.0.1','Ligo Sardines Spicy (155g) - 3 units added','2026-09-19 11:56:34');
INSERT INTO "admin_activity" VALUES(236,14,'Add New Product','127.0.0.1','Toyo Mackerel (155g) - 3 units added','2026-09-19 11:58:02');
INSERT INTO "admin_activity" VALUES(237,14,'Add New Product','127.0.0.1','555 Sardines Spicy (155g) - 3 units added','2026-09-19 11:59:38');
INSERT INTO "admin_activity" VALUES(238,14,'Add New Product','127.0.0.1','555 Sardines Original (155g) - 3 units added','2026-09-19 12:00:37');
INSERT INTO "admin_activity" VALUES(239,14,'Add New Product','127.0.0.1','Virginia Vienna Sausage (70g) - 3 units added','2026-09-19 12:01:49');
INSERT INTO "admin_activity" VALUES(240,14,'Add New Product','127.0.0.1','San Marino Spicy (150g) - 3 units added','2026-09-19 12:03:14');
INSERT INTO "admin_activity" VALUES(241,14,'Add New Product','127.0.0.1','Lucky 7 Carne Norte (150g) - 3 units added','2026-09-19 12:04:28');
INSERT INTO "admin_activity" VALUES(242,14,'Add New Product','127.0.0.1','Century Tuna Spicy (155g) - 3 units added','2026-09-19 12:06:40');
INSERT INTO "admin_activity" VALUES(243,14,'Add New Product','127.0.0.1','555 Tuna Caldereta - 3 units added','2026-09-19 12:07:43');
INSERT INTO "admin_activity" VALUES(244,14,'Add New Product','127.0.0.1','Argentina Corned Beef (150g) - 3 units added','2026-09-19 12:08:52');
INSERT INTO "admin_activity" VALUES(245,14,'Add New Product','127.0.0.1','Star Corned Beef (150g) - 3 units added','2026-09-19 12:09:59');
INSERT INTO "admin_activity" VALUES(246,14,'Add New Product','127.0.0.1','San Marino Original (150g) - 3 units added','2026-09-19 12:18:49');
INSERT INTO "admin_activity" VALUES(247,14,'Add New Product','127.0.0.1','555 Sardines Spicy (425G) - 1 units added','2026-09-19 12:22:05');
INSERT INTO "admin_activity" VALUES(248,14,'Add New Product','127.0.0.1','Hunts Pork & Beans  - 1 units added','2026-09-19 12:27:36');
INSERT INTO "admin_activity" VALUES(249,14,'Add New Product','127.0.0.1','555 Sardines Original (425g) - 1 units added','2026-09-19 12:28:39');
INSERT INTO "admin_activity" VALUES(250,14,'Add New Product','127.0.0.1','Argentina Meat Loaf (250g) - 3 units added','2026-09-19 12:31:37');
INSERT INTO "admin_activity" VALUES(251,14,'Add New Product','127.0.0.1','555 Squid Spicy (155g) - 1 units added','2026-09-19 12:33:44');
INSERT INTO "admin_activity" VALUES(252,14,'Add New Product','127.0.0.1','555 tuna Bicol Express (155g) - 3 units added','2026-09-19 12:34:43');
INSERT INTO "admin_activity" VALUES(253,14,'Add New Product','127.0.0.1','Wow Ulam Adobo (155g) - 3 units added','2026-09-19 12:36:23');
INSERT INTO "admin_activity" VALUES(254,14,'Add New Product','127.0.0.1','Wow Ulam Mechado - 3 units added','2026-09-19 12:37:46');
INSERT INTO "admin_activity" VALUES(255,14,'Add New Product','127.0.0.1','555 Tuna Mechado  - 3 units added','2026-09-19 12:40:13');
INSERT INTO "admin_activity" VALUES(256,14,'Add New Product','127.0.0.1','555 Tuna Afritada (155g) - 3 units added','2026-09-19 12:42:39');
INSERT INTO "admin_activity" VALUES(257,14,'Add New Product','127.0.0.1','Century Tuna Original (155g) - 3 units added','2026-09-19 13:08:50');
INSERT INTO "admin_activity" VALUES(258,14,'Add New Product','127.0.0.1','CDO Karne Norte (150g) - 3 units added','2026-09-19 13:14:36');
INSERT INTO "admin_activity" VALUES(259,14,'Add New Product','127.0.0.1','Del Monte Pineapple Tidbits (137g) - 2 units added','2026-09-19 13:31:09');
INSERT INTO "admin_activity" VALUES(260,14,'Add New Product','127.0.0.1','Del Monte Pineapple Chunks (137g) - 1 units added','2026-09-19 13:35:44');
INSERT INTO "admin_activity" VALUES(261,14,'Add New Product','127.0.0.1','Uni-Pak Tomato Paste (155g) - 3 units added','2026-09-19 13:37:03');
INSERT INTO "admin_activity" VALUES(262,14,'Add New Product','127.0.0.1','Mayon Mushrooms (115g) - 1 units added','2026-09-19 13:40:10');
INSERT INTO "admin_activity" VALUES(263,14,'Add New Product','127.0.0.1','Senorita  - 2 units added','2026-09-19 13:46:13');
INSERT INTO "admin_activity" VALUES(264,14,'Add New Product','127.0.0.1','Alaska Evaporada (140ml) - 1 units added','2026-09-19 13:49:19');
INSERT INTO "admin_activity" VALUES(265,14,'Add New Product','127.0.0.1','Senorita ( Black Beans ) 180g  - 2 units added','2026-09-19 13:50:39');
INSERT INTO "admin_activity" VALUES(266,14,'Add New Product','127.0.0.1','Magnolia ( ALL PURPOSE FLOUR) 200G  - 3 units added','2026-09-19 13:51:49');
INSERT INTO "admin_activity" VALUES(267,14,'Add New Product','127.0.0.1','Hasmine Rice  - 5 units added','2026-09-19 13:53:07');
INSERT INTO "admin_activity" VALUES(268,14,'Add New Product','127.0.0.1','Star Sweet Blend  - 1 units added','2026-09-19 13:54:32');
INSERT INTO "admin_activity" VALUES(269,14,'Add New Product','127.0.0.1','Silver Swan Salted Black Beans (100g) - 2 units added','2026-09-19 13:55:53');
INSERT INTO "admin_activity" VALUES(270,14,'Add New Product','127.0.0.1','Coco Mama Fresh Gata (200ml) - 4 units added','2026-09-19 13:57:28');
INSERT INTO "admin_activity" VALUES(271,14,'Add New Product','127.0.0.1','Silver Swan Soy Sauce (200ml) - 6 units added','2026-09-19 14:00:23');
INSERT INTO "admin_activity" VALUES(272,14,'Add New Product','127.0.0.1','Ufc Tamis Anghang (320g) - 3 units added','2026-09-19 14:10:37');
INSERT INTO "admin_activity" VALUES(273,14,'Add New Product','127.0.0.1','Coke 12oz - 24 units added','2026-09-19 14:14:08');
INSERT INTO "admin_activity" VALUES(274,14,'Add New Product','127.0.0.1','Coke,Sprite,Royal (Litro) - 24 units added','2026-09-19 14:15:13');
INSERT INTO "admin_activity" VALUES(275,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-19 14:15:21');
INSERT INTO "admin_activity" VALUES(276,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-19 14:18:33');
INSERT INTO "admin_activity" VALUES(277,14,'Add New Product','127.0.0.1','Nature Spring (1000ml) - 24 units added','2026-09-19 14:20:01');
INSERT INTO "admin_activity" VALUES(278,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-19 14:20:09');
INSERT INTO "admin_activity" VALUES(279,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-19 14:23:25');
INSERT INTO "admin_activity" VALUES(280,14,'Add New Product','127.0.0.1','Egg - 30 units added','2026-09-19 14:24:52');
INSERT INTO "admin_activity" VALUES(281,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-19 14:26:13');
INSERT INTO "admin_activity" VALUES(282,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-19 19:51:33');
INSERT INTO "admin_activity" VALUES(283,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-19 19:53:08');
INSERT INTO "admin_activity" VALUES(284,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-21 23:29:14');
INSERT INTO "admin_activity" VALUES(285,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-22 14:27:58');
INSERT INTO "admin_activity" VALUES(286,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-22 14:28:15');
INSERT INTO "admin_activity" VALUES(287,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-22 19:33:36');
INSERT INTO "admin_activity" VALUES(288,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-22 22:34:17');
INSERT INTO "admin_activity" VALUES(289,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-23 12:28:14');
INSERT INTO "admin_activity" VALUES(290,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-23 12:28:45');
INSERT INTO "admin_activity" VALUES(291,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-23 12:31:04');
INSERT INTO "admin_activity" VALUES(292,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-23 12:31:28');
INSERT INTO "admin_activity" VALUES(293,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-09-23 13:35:05');
INSERT INTO "admin_activity" VALUES(294,14,'Add New Product','127.0.0.1','Washed Sugar (1/4) - 5 units added','2026-09-23 13:37:57');
INSERT INTO "admin_activity" VALUES(295,14,'Edit Product','127.0.0.1','Edited product: Washed Sugar (1/4)','2026-09-23 13:38:49');
INSERT INTO "admin_activity" VALUES(296,14,'Add New Product','127.0.0.1','Buko - 25 units added','2026-09-23 13:40:09');
INSERT INTO "admin_activity" VALUES(297,14,'Add New Product','127.0.0.1','Cobra - 5 units added','2026-09-23 13:42:55');
INSERT INTO "admin_activity" VALUES(298,14,'Add New Product','127.0.0.1','Sting - 5 units added','2026-09-23 13:43:26');
INSERT INTO "admin_activity" VALUES(299,14,'Add New Product','127.0.0.1','Big (Apple & Orange) - 20 units added','2026-09-23 13:44:09');
INSERT INTO "admin_activity" VALUES(300,14,'Add New Product','127.0.0.1','Big (Strawberry,Guyabano,Grapes) - 30 units added','2026-09-23 13:44:58');
INSERT INTO "admin_activity" VALUES(301,14,'Add New Product','127.0.0.1','Choc-O  - 1 units added','2026-09-23 13:45:32');
INSERT INTO "admin_activity" VALUES(302,14,'Add New Product','127.0.0.1','Yakult - 12 units added','2026-09-23 13:46:03');
INSERT INTO "admin_activity" VALUES(303,14,'Add New Product','127.0.0.1','Dutch Mill (Small) - 5 units added','2026-09-23 13:46:39');
INSERT INTO "admin_activity" VALUES(304,14,'Add New Product','127.0.0.1','Selecta (Fortified Milk) - 3 units added','2026-09-23 13:47:39');
INSERT INTO "admin_activity" VALUES(305,14,'Add New Product','127.0.0.1','Chuckie (Small) - 5 units added','2026-09-23 13:48:16');
INSERT INTO "admin_activity" VALUES(306,14,'Add New Product','127.0.0.1','Milo (Small) - 5 units added','2026-09-23 13:48:48');
INSERT INTO "admin_activity" VALUES(307,14,'Add New Product','127.0.0.1','Calamansi Juice - 10 units added','2026-09-23 13:49:17');
INSERT INTO "admin_activity" VALUES(308,14,'Add New Product','127.0.0.1','C2 (Small) - 10 units added','2026-09-23 13:49:54');
INSERT INTO "admin_activity" VALUES(309,14,'Add New Product','127.0.0.1','C2 (Medium) - 1 units added','2026-09-23 13:50:25');
INSERT INTO "admin_activity" VALUES(310,14,'Add New Product','127.0.0.1','C2 (Big) - 3 units added','2026-09-23 13:50:51');
INSERT INTO "admin_activity" VALUES(311,14,'Add New Product','127.0.0.1','Mogu-mogu - 3 units added','2026-09-23 13:51:59');
INSERT INTO "admin_activity" VALUES(312,14,'Add New Product','127.0.0.1','Swakto - 10 units added','2026-09-23 13:52:46');
INSERT INTO "admin_activity" VALUES(313,14,'Add New Product','127.0.0.1','Curls - 50 units added','2026-09-23 13:53:18');
INSERT INTO "admin_activity" VALUES(314,14,'Add New Product','127.0.0.1','Biscuits  - 30 units added','2026-09-23 13:54:01');
INSERT INTO "admin_activity" VALUES(315,14,'Admin Logout','127.0.0.1','Admin logged out','2026-09-23 19:34:53');
INSERT INTO "admin_activity" VALUES(316,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-01 11:54:28');
INSERT INTO "admin_activity" VALUES(317,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-01 17:30:30');
INSERT INTO "admin_activity" VALUES(318,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-02 12:33:15');
INSERT INTO "admin_activity" VALUES(319,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-02 23:31:03');
INSERT INTO "admin_activity" VALUES(320,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-02 23:31:35');
INSERT INTO "admin_activity" VALUES(321,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 13:08:14');
INSERT INTO "admin_activity" VALUES(322,14,'Add New Product','127.0.0.1','biogesic - 5 units added','2026-10-06 13:16:04');
INSERT INTO "admin_activity" VALUES(323,14,'Delete Product','127.0.0.1','Deleted product: biogesic','2026-10-06 13:16:57');
INSERT INTO "admin_activity" VALUES(324,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-06 13:18:09');
INSERT INTO "admin_activity" VALUES(325,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 13:21:58');
INSERT INTO "admin_activity" VALUES(326,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 13:22:52');
INSERT INTO "admin_activity" VALUES(327,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 13:28:22');
INSERT INTO "admin_activity" VALUES(328,14,'Add New Product','127.0.0.1','Ascorbic Acid + Zinc - 84 units added','2026-10-06 13:29:33');
INSERT INTO "admin_activity" VALUES(329,14,'Add New Product','127.0.0.1','Amlodipine Besilate - 100 units added','2026-10-06 13:30:54');
INSERT INTO "admin_activity" VALUES(330,14,'Add New Product','127.0.0.1','Amlodipine - 100 units added','2026-10-06 13:31:53');
INSERT INTO "admin_activity" VALUES(331,14,'Add New Product','127.0.0.1','Ascorbic Acid + Zinc Myverit C Plus - 100 units added','2026-10-06 13:32:39');
INSERT INTO "admin_activity" VALUES(332,14,'Add New Product','127.0.0.1','Amoxicilin Axmel - 100 units added','2026-10-06 13:33:02');
INSERT INTO "admin_activity" VALUES(333,14,'Add New Product','127.0.0.1','Atorvastatin Atorbet - 100 units added','2026-10-06 13:33:28');
INSERT INTO "admin_activity" VALUES(334,14,'Add New Product','127.0.0.1','Atorvastatin Astat - 100 units added','2026-10-06 13:34:07');
INSERT INTO "admin_activity" VALUES(335,14,'Edit Product','127.0.0.1','Edited product: Atorvastatin Atorbet','2026-10-06 13:34:34');
INSERT INTO "admin_activity" VALUES(336,14,'Add New Product','127.0.0.1','Atorvastatin Calcium Florvast 80 - 100 units added','2026-10-06 13:35:10');
INSERT INTO "admin_activity" VALUES(337,14,'Add New Product','127.0.0.1','Ambroxol - 100 units added','2026-10-06 13:35:39');
INSERT INTO "admin_activity" VALUES(338,14,'Add New Product','127.0.0.1','Multivitamins Vitamin B1 + B6 + B12 - 100 units added','2026-10-06 13:36:33');
INSERT INTO "admin_activity" VALUES(339,14,'Add New Product','127.0.0.1','Colchicine - 100 units added','2026-10-06 13:36:56');
INSERT INTO "admin_activity" VALUES(340,14,'Add New Product','127.0.0.1','Betahistine Hydrochloride - 100 units added','2026-10-06 13:37:27');
INSERT INTO "admin_activity" VALUES(341,14,'Add New Product','127.0.0.1','Celecoxib - 100 units added','2026-10-06 13:37:54');
INSERT INTO "admin_activity" VALUES(342,14,'Add New Product','127.0.0.1','Catrimoxamozole Kathrex - 100 units added','2026-10-06 13:38:29');
INSERT INTO "admin_activity" VALUES(343,14,'Add New Product','127.0.0.1','Cefalexin Exel - 100 units added','2026-10-06 13:39:02');
INSERT INTO "admin_activity" VALUES(344,14,'Add New Product','127.0.0.1','Carvedilol - 100 units added','2026-10-06 13:39:22');
INSERT INTO "admin_activity" VALUES(345,14,'Add New Product','127.0.0.1','Celecoxib - 100 units added','2026-10-06 13:39:54');
INSERT INTO "admin_activity" VALUES(346,14,'Add New Product','127.0.0.1','Calcium Ambical - 100 units added','2026-10-06 13:40:17');
INSERT INTO "admin_activity" VALUES(347,14,'Add New Product','127.0.0.1','Clonidine Hydrochloride Clodin - 100 units added','2026-10-06 13:40:49');
INSERT INTO "admin_activity" VALUES(348,14,'Add New Product','127.0.0.1','Clindamycin Clin-Gen - 100 units added','2026-10-06 13:41:31');
INSERT INTO "admin_activity" VALUES(349,14,'Add New Product','127.0.0.1','Betahistine Hydrochloride Betzine - 100 units added','2026-10-06 13:42:03');
INSERT INTO "admin_activity" VALUES(350,14,'Edit Product','127.0.0.1','Edited product: Celecoxib Emicox','2026-10-06 13:42:47');
INSERT INTO "admin_activity" VALUES(351,14,'Edit Product','127.0.0.1','Edited product: Clonidine Hydrochloride Clodin','2026-10-06 13:43:46');
INSERT INTO "admin_activity" VALUES(352,14,'Add New Product','127.0.0.1','Doxofylline Doxofar - 100 units added','2026-10-06 13:44:58');
INSERT INTO "admin_activity" VALUES(353,14,'Add New Product','127.0.0.1','Omeprazole - 100 units added','2026-10-06 13:45:27');
INSERT INTO "admin_activity" VALUES(354,14,'Add New Product','127.0.0.1','Glimepiride Glimegen - 100 units added','2026-10-06 13:46:03');
INSERT INTO "admin_activity" VALUES(355,14,'Add New Product','127.0.0.1','Paracetamol Flugard - 200 units added','2026-10-06 13:46:40');
INSERT INTO "admin_activity" VALUES(356,14,'Add New Product','127.0.0.1','MX3 - 200 units added','2026-10-06 13:47:11');
INSERT INTO "admin_activity" VALUES(357,14,'Add New Product','127.0.0.1','Metformin Hydrochloride Formet - 200 units added','2026-10-06 13:47:48');
INSERT INTO "admin_activity" VALUES(358,14,'Add New Product','127.0.0.1','Febuxostat Febutor-40 - 100 units added','2026-10-06 13:48:46');
INSERT INTO "admin_activity" VALUES(359,14,'Add New Product','127.0.0.1','Carrvedilol - 100 units added','2026-10-06 13:49:09');
INSERT INTO "admin_activity" VALUES(360,14,'Add New Product','127.0.0.1','Cinnarizine Cinzitab - 100 units added','2026-10-06 13:49:34');
INSERT INTO "admin_activity" VALUES(361,14,'Add New Product','127.0.0.1','Carbocisteine - 100 units added','2026-10-06 13:50:07');
INSERT INTO "admin_activity" VALUES(362,14,'Add New Product','127.0.0.1','Nitrofurantoin Harfurin - 100 units added','2026-10-06 13:50:34');
INSERT INTO "admin_activity" VALUES(363,14,'Add New Product','127.0.0.1','Diphenhydramine Hydrochloride Mucomed - 100 units added','2026-10-06 13:51:20');
INSERT INTO "admin_activity" VALUES(364,14,'Add New Product','127.0.0.1','ORS-5 Replacement Dehydrosol - 100 units added','2026-10-06 13:52:07');
INSERT INTO "admin_activity" VALUES(365,14,'Add New Product','127.0.0.1','Omephrazole - 100 units added','2026-10-06 13:52:31');
INSERT INTO "admin_activity" VALUES(366,14,'Add New Product','127.0.0.1','Symdex-D FORTE - 100 units added','2026-10-06 13:53:32');
INSERT INTO "admin_activity" VALUES(367,14,'Add New Product','127.0.0.1','Symdex-D - 100 units added','2026-10-06 13:53:54');
INSERT INTO "admin_activity" VALUES(368,14,'Add New Product','127.0.0.1','Ranitidine Ranitein - 100 units added','2026-10-06 13:54:21');
INSERT INTO "admin_activity" VALUES(369,14,'Add New Product','127.0.0.1','Clopidogrel - 100 units added','2026-10-06 13:54:43');
INSERT INTO "admin_activity" VALUES(370,14,'Edit Product','127.0.0.1','Edited product: Clopidogrel Clopinova','2026-10-06 13:55:13');
INSERT INTO "admin_activity" VALUES(371,14,'Add New Product','127.0.0.1','Betahistine Hydrochloride BEVERT - 100 units added','2026-10-06 13:55:51');
INSERT INTO "admin_activity" VALUES(372,14,'Add New Product','127.0.0.1','Doxycycline Mydoxy - 100 units added','2026-10-06 13:56:23');
INSERT INTO "admin_activity" VALUES(373,14,'Add New Product','127.0.0.1','Carvedilol Karvidol - 100 units added','2026-10-06 13:56:47');
INSERT INTO "admin_activity" VALUES(374,14,'Add New Product','127.0.0.1','Carvedilol Karvidol - 100 units added','2026-10-06 14:02:03');
INSERT INTO "admin_activity" VALUES(375,14,'Add New Product','127.0.0.1','Erythromycin monphevin - 100 units added','2026-10-06 14:02:57');
INSERT INTO "admin_activity" VALUES(376,14,'Add New Product','127.0.0.1','Rosuvastatin Rosulip-10 - 200 units added','2026-10-06 14:03:28');
INSERT INTO "admin_activity" VALUES(377,14,'Add New Product','127.0.0.1','Irbesartan Irbenov-150 - 100 units added','2026-10-06 14:03:55');
INSERT INTO "admin_activity" VALUES(378,14,'Add New Product','127.0.0.1','Salbutamol Beisol - 100 units added','2026-10-06 14:04:16');
INSERT INTO "admin_activity" VALUES(379,14,'Add New Product','127.0.0.1','Glimepiride Diabeats - 100 units added','2026-10-06 14:04:44');
INSERT INTO "admin_activity" VALUES(380,14,'Add New Product','127.0.0.1','Prednisone Corticosteroid - 100 units added','2026-10-06 14:05:07');
INSERT INTO "admin_activity" VALUES(381,14,'Add New Product','127.0.0.1','Folic Acid Prevena - 100 units added','2026-10-06 14:05:30');
INSERT INTO "admin_activity" VALUES(382,14,'Add New Product','127.0.0.1','Furosemide Diubetic - 100 units added','2026-10-06 14:06:00');
INSERT INTO "admin_activity" VALUES(383,14,'Add New Product','127.0.0.1','Losartan Potassium Natrasol  - 100 units added','2026-10-06 14:06:33');
INSERT INTO "admin_activity" VALUES(384,14,'Add New Product','127.0.0.1','Rosuvastatin Calcium Arvast 20 - 100 units added','2026-10-06 14:07:23');
INSERT INTO "admin_activity" VALUES(385,14,'Add New Product','127.0.0.1','Metronidazole Flagex - 100 units added','2026-10-06 14:07:54');
INSERT INTO "admin_activity" VALUES(386,14,'Add New Product','127.0.0.1','Pioglitazone Hydrochloride GLITO 30 - 150 units added','2026-10-06 14:08:38');
INSERT INTO "admin_activity" VALUES(387,14,'Add New Product','127.0.0.1','Ranitidine Ranitein - 100 units added','2026-10-06 14:08:59');
INSERT INTO "admin_activity" VALUES(388,14,'Add New Product','127.0.0.1','Losatan Pottassium NATRASOL - 100 units added','2026-10-06 14:09:28');
INSERT INTO "admin_activity" VALUES(389,14,'Add New Product','127.0.0.1','Trimetazidine Dihydrochloride TRIMESAPH-35 - 100 units added','2026-10-06 14:10:20');
INSERT INTO "admin_activity" VALUES(390,14,'Add New Product','127.0.0.1','Clindamycin Clin-Gen - 100 units added','2026-10-06 14:10:53');
INSERT INTO "admin_activity" VALUES(391,14,'Add New Product','127.0.0.1','Happy Baby Pants XXL  - 48 units added','2026-10-06 14:12:14');
INSERT INTO "admin_activity" VALUES(392,14,'Add New Product','127.0.0.1','EQ Pants L - 80 units added','2026-10-06 14:13:11');
INSERT INTO "admin_activity" VALUES(393,14,'Add New Product','127.0.0.1','Happy Baby Pants XL - 48 units added','2026-10-06 14:14:20');
INSERT INTO "admin_activity" VALUES(394,14,'Add New Product','127.0.0.1','EQ Pants M - 48 units added','2026-10-06 14:15:08');
INSERT INTO "admin_activity" VALUES(395,14,'Add New Product','127.0.0.1','Happy Baby Pants XXL - 35 units added','2026-10-06 14:16:16');
INSERT INTO "admin_activity" VALUES(396,14,'Add New Product','127.0.0.1','EQ Dry L - 32 units added','2026-10-06 14:17:00');
INSERT INTO "admin_activity" VALUES(397,14,'Add New Product','127.0.0.1','EQ Dry XL - 19 units added','2026-10-06 14:17:36');
INSERT INTO "admin_activity" VALUES(398,14,'Add New Product','127.0.0.1','EQ Dry XXL - 20 units added','2026-10-06 14:18:35');
INSERT INTO "admin_activity" VALUES(399,14,'Add New Product','127.0.0.1','EQ Plus+ Economy & Quality - 30 units added','2026-10-06 14:19:46');
INSERT INTO "admin_activity" VALUES(400,14,'Add New Product','127.0.0.1','EQ Pants XXXL - 40 units added','2026-10-06 14:20:22');
INSERT INTO "admin_activity" VALUES(401,14,'Add New Product','127.0.0.1','EQ Pants XXL - 37 units added','2026-10-06 14:21:05');
INSERT INTO "admin_activity" VALUES(402,14,'Add New Product','127.0.0.1','EQ Pants XL - 48 units added','2026-10-06 14:21:54');
INSERT INTO "admin_activity" VALUES(403,14,'Add New Product','127.0.0.1','Coke 355ml - 120 units added','2026-10-06 14:23:35');
INSERT INTO "admin_activity" VALUES(404,14,'Delete Product','127.0.0.1','Deleted product: Coke 12oz','2026-10-06 14:24:22');
INSERT INTO "admin_activity" VALUES(405,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 14:26:10');
INSERT INTO "admin_activity" VALUES(406,14,'Add New Product','127.0.0.1','Chipd Delight - 20 units added','2026-10-06 14:26:37');
INSERT INTO "admin_activity" VALUES(407,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 14:28:07');
INSERT INTO "admin_activity" VALUES(408,14,'Edit Product','127.0.0.1','Edited product: 555 Tuna Afritada (155g)','2026-10-06 14:28:24');
INSERT INTO "admin_activity" VALUES(409,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 14:29:43');
INSERT INTO "admin_activity" VALUES(410,14,'Add New Product','127.0.0.1','Energen - 30 units added','2026-10-06 14:30:27');
INSERT INTO "admin_activity" VALUES(411,14,'Add New Product','127.0.0.1','Kinck Knocks - 40 units added','2026-10-06 14:30:59');
INSERT INTO "admin_activity" VALUES(412,14,'Add New Product','127.0.0.1','kokokruch - 40 units added','2026-10-06 14:31:38');
INSERT INTO "admin_activity" VALUES(413,14,'Add New Product','127.0.0.1','Star Margarine 100g - 20 units added','2026-10-06 14:33:02');
INSERT INTO "admin_activity" VALUES(414,14,'Add New Product','127.0.0.1','Payless Extra Big Xtra Hot - 20 units added','2026-10-06 14:34:49');
INSERT INTO "admin_activity" VALUES(415,14,'Add New Product','127.0.0.1','Ho - mi Beef - 20 units added','2026-10-06 14:35:42');
INSERT INTO "admin_activity" VALUES(416,14,'Add New Product','127.0.0.1','Ho - mi Chicken - 20 units added','2026-10-06 14:36:35');
INSERT INTO "admin_activity" VALUES(417,14,'Edit Product','127.0.0.1','Edited product: LM Jjampong (40g)','2026-10-06 14:36:58');
INSERT INTO "admin_activity" VALUES(418,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 14:39:12');
INSERT INTO "admin_activity" VALUES(419,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-06 14:41:26');
INSERT INTO "admin_activity" VALUES(420,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-13 13:44:37');
INSERT INTO "admin_activity" VALUES(421,14,'Add New Product','127.0.0.1','pilot - 20 units added','2026-10-13 13:46:03');
INSERT INTO "admin_activity" VALUES(422,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-13 13:46:16');
INSERT INTO "admin_activity" VALUES(423,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-13 14:33:51');
INSERT INTO "admin_activity" VALUES(424,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-13 15:24:36');
INSERT INTO "admin_activity" VALUES(425,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-13 16:18:24');
INSERT INTO "admin_activity" VALUES(426,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-13 17:13:10');
INSERT INTO "admin_activity" VALUES(427,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-13 17:14:17');
INSERT INTO "admin_activity" VALUES(428,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-13 17:49:18');
INSERT INTO "admin_activity" VALUES(429,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-13 17:51:07');
INSERT INTO "admin_activity" VALUES(430,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-13 17:53:12');
INSERT INTO "admin_activity" VALUES(431,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 13:24:20');
INSERT INTO "admin_activity" VALUES(432,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 13:30:16');
INSERT INTO "admin_activity" VALUES(433,14,'Add New Product','127.0.0.1','MIGHTY - 20 units added','2026-10-14 13:31:47');
INSERT INTO "admin_activity" VALUES(434,14,'Add New Product','127.0.0.1','CAMEL - 20 units added','2026-10-14 13:32:08');
INSERT INTO "admin_activity" VALUES(435,14,'Add New Product','127.0.0.1','MARLBORO RED - 20 units added','2026-10-14 13:32:31');
INSERT INTO "admin_activity" VALUES(436,14,'Add New Product','127.0.0.1','MARLBORO BLUE - 20 units added','2026-10-14 13:32:51');
INSERT INTO "admin_activity" VALUES(437,14,'Add New Product','127.0.0.1','CHESTER RED - 20 units added','2026-10-14 13:33:24');
INSERT INTO "admin_activity" VALUES(438,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 13:33:47');
INSERT INTO "admin_activity" VALUES(439,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 13:37:38');
INSERT INTO "admin_activity" VALUES(440,14,'Add New Product','127.0.0.1','FUDGEE BAR - 20 units added','2026-10-14 13:39:14');
INSERT INTO "admin_activity" VALUES(441,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 13:39:33');
INSERT INTO "admin_activity" VALUES(442,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 14:01:55');
INSERT INTO "admin_activity" VALUES(443,14,'Add New Product','127.0.0.1','BIOGESIC - 50 units added','2026-10-14 14:02:54');
INSERT INTO "admin_activity" VALUES(444,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 14:03:08');
INSERT INTO "admin_activity" VALUES(445,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 14:04:30');
INSERT INTO "admin_activity" VALUES(446,14,'Add New Product','127.0.0.1','VITAMILK - 10 units added','2026-10-14 14:05:13');
INSERT INTO "admin_activity" VALUES(447,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 14:06:04');
INSERT INTO "admin_activity" VALUES(448,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 14:12:09');
INSERT INTO "admin_activity" VALUES(449,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 14:16:46');
INSERT INTO "admin_activity" VALUES(450,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-14 23:51:34');
INSERT INTO "admin_activity" VALUES(451,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-14 23:58:24');
INSERT INTO "admin_activity" VALUES(452,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 13:54:14');
INSERT INTO "admin_activity" VALUES(453,14,'Add New Product','127.0.0.1','GEL - 10 units added','2026-10-15 13:54:41');
INSERT INTO "admin_activity" VALUES(454,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 13:54:44');
INSERT INTO "admin_activity" VALUES(455,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 13:58:18');
INSERT INTO "admin_activity" VALUES(456,14,'Add New Product','127.0.0.1','PRITONG BANGUS - 20 units added','2026-10-15 13:58:58');
INSERT INTO "admin_activity" VALUES(457,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 13:59:00');
INSERT INTO "admin_activity" VALUES(458,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 14:01:49');
INSERT INTO "admin_activity" VALUES(459,14,'Add New Product','127.0.0.1','OREO - 10 units added','2026-10-15 14:02:20');
INSERT INTO "admin_activity" VALUES(460,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 14:02:26');
INSERT INTO "admin_activity" VALUES(461,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 14:07:26');
INSERT INTO "admin_activity" VALUES(462,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 14:09:39');
INSERT INTO "admin_activity" VALUES(463,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 14:09:58');
INSERT INTO "admin_activity" VALUES(464,14,'Edit Product','127.0.0.1','Edited product: Wings Floral Fresh (70g)','2026-10-15 14:10:38');
INSERT INTO "admin_activity" VALUES(465,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 14:10:41');
INSERT INTO "admin_activity" VALUES(466,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 14:12:26');
INSERT INTO "admin_activity" VALUES(467,14,'Delete Product','127.0.0.1','Deleted product: Beng-Beng (22g)','2026-10-15 14:14:32');
INSERT INTO "admin_activity" VALUES(468,14,'Add New Product','127.0.0.1','WAFER - 10 units added','2026-10-15 14:42:09');
INSERT INTO "admin_activity" VALUES(469,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 14:42:20');
INSERT INTO "admin_activity" VALUES(470,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-15 15:29:23');
INSERT INTO "admin_activity" VALUES(471,14,'Add New Product','127.0.0.1','PIATTOS,NOVA,VCUT - 30 units added','2026-10-15 15:30:02');
INSERT INTO "admin_activity" VALUES(472,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-15 15:30:05');
INSERT INTO "admin_activity" VALUES(473,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 10:29:24');
INSERT INTO "admin_activity" VALUES(474,14,'Add New Product','127.0.0.1','PLASTIC 4X12 - 20 units added','2026-10-16 10:29:57');
INSERT INTO "admin_activity" VALUES(475,14,'Add New Product','127.0.0.1','Choc-o SMALL - 24 units added','2026-10-16 10:30:37');
INSERT INTO "admin_activity" VALUES(476,14,'Add New Product','127.0.0.1','ASSORTED - 0 units added','2026-10-16 10:31:10');
INSERT INTO "admin_activity" VALUES(477,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 10:31:13');
INSERT INTO "admin_activity" VALUES(478,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 10:40:12');
INSERT INTO "admin_activity" VALUES(479,14,'Add New Product','127.0.0.1','Bombay,Ahos - 20 units added','2026-10-16 10:40:53');
INSERT INTO "admin_activity" VALUES(480,14,'Edit Product','127.0.0.1','Edited product: Bombay,Ahos,Kamatis','2026-10-16 10:43:05');
INSERT INTO "admin_activity" VALUES(481,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 10:43:19');
INSERT INTO "admin_activity" VALUES(482,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 11:09:27');
INSERT INTO "admin_activity" VALUES(483,14,'Add New Product','127.0.0.1','Knorr (chicken,pork,shrimp,beef) - 60 units added','2026-10-16 11:10:40');
INSERT INTO "admin_activity" VALUES(484,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 11:10:42');
INSERT INTO "admin_activity" VALUES(485,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 12:42:37');
INSERT INTO "admin_activity" VALUES(486,14,'Edit Product','127.0.0.1','Edited product: Tide Perfect Clean (69g)','2026-10-16 12:42:56');
INSERT INTO "admin_activity" VALUES(487,14,'Edit Product','127.0.0.1','Edited product: Tide w/ Downy Perfume Fantasy (67g)','2026-10-16 12:43:05');
INSERT INTO "admin_activity" VALUES(488,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 12:43:10');
INSERT INTO "admin_activity" VALUES(489,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 17:09:11');
INSERT INTO "admin_activity" VALUES(490,14,'Add New Product','127.0.0.1','DATU PUTI (VINEGAR) - 20 units added','2026-10-16 17:10:02');
INSERT INTO "admin_activity" VALUES(491,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 17:10:04');
INSERT INTO "admin_activity" VALUES(492,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-16 18:10:15');
INSERT INTO "admin_activity" VALUES(493,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-16 18:11:11');
INSERT INTO "admin_activity" VALUES(494,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-20 13:58:20');
INSERT INTO "admin_activity" VALUES(495,14,'Add New Product','127.0.0.1','CANDY - 100 units added','2026-10-20 13:58:59');
INSERT INTO "admin_activity" VALUES(496,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-20 13:59:02');
INSERT INTO "admin_activity" VALUES(497,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-20 14:00:04');
INSERT INTO "admin_activity" VALUES(498,14,'Add New Product','127.0.0.1','NATURE SPRING DISTILLED (10ltr) - 10 units added','2026-10-20 14:00:48');
INSERT INTO "admin_activity" VALUES(499,14,'Add New Product','127.0.0.1','NATURE SPRING (10ltr) - 10 units added','2026-10-20 14:01:32');
INSERT INTO "admin_activity" VALUES(500,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-20 14:01:35');
INSERT INTO "admin_activity" VALUES(501,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-20 14:03:02');
INSERT INTO "admin_activity" VALUES(502,14,'Add New Product','127.0.0.1','Chocolait (Magnolia) - 8 units added','2026-10-20 14:03:43');
INSERT INTO "admin_activity" VALUES(503,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-20 14:07:56');
INSERT INTO "admin_activity" VALUES(504,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-20 14:51:54');
INSERT INTO "admin_activity" VALUES(505,14,'Stock In','127.0.0.1','Tang Orange (19g) | Added: 24 units | Reason: Stock Addition | Old Stock: 1 | New Stock: 25','2026-10-20 14:53:25');
INSERT INTO "admin_activity" VALUES(506,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-20 14:53:43');
INSERT INTO "admin_activity" VALUES(507,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-20 15:55:42');
INSERT INTO "admin_activity" VALUES(508,14,'Add New Product','127.0.0.1','LOPERAMIDE - 10 units added','2026-10-20 15:56:42');
INSERT INTO "admin_activity" VALUES(509,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-20 15:57:13');
INSERT INTO "admin_activity" VALUES(510,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-23 14:02:20');
INSERT INTO "admin_activity" VALUES(511,14,'Add New Product','127.0.0.1','WIPES - 5 units added','2026-10-23 14:02:44');
INSERT INTO "admin_activity" VALUES(512,14,'Admin Logout','127.0.0.1','Admin logged out','2026-10-23 14:02:49');
INSERT INTO "admin_activity" VALUES(513,14,'Admin Login','127.0.0.1','Admin admin logged in','2026-10-27 12:58:45');
DROP TABLE IF EXISTS admins;
CREATE TABLE admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            security_question VARCHAR(255),
            security_answer VARCHAR(255),
            force_password_change INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );
-- Admin credentials excluded from backup
CREATE TABLE alert_acknowledgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            alert_type VARCHAR(50) NOT NULL,
            action VARCHAR(20) NOT NULL,
            reason TEXT,
            user_id INTEGER NOT NULL,
            user_type VARCHAR(20) NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(alert_type, product_id)
        );
DROP TABLE IF EXISTS alert_logs;
CREATE TABLE alert_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type VARCHAR(50) NOT NULL,
            alert_level VARCHAR(20) NOT NULL,
            product_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            acknowledged_by INTEGER DEFAULT NULL,
            acknowledged_at TEXT NULL DEFAULT NULL,
            dismissed_by INTEGER DEFAULT NULL,
            dismissed_at TEXT NULL DEFAULT NULL,
            dismiss_reason TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(alert_type, product_id)
        );
DROP TABLE IF EXISTS alert_settings;
CREATE TABLE alert_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name VARCHAR(100) NOT NULL UNIQUE,
            setting_value VARCHAR(255) NOT NULL,
            updated_at TEXT DEFAULT (datetime('now', 'localtime'))
        );
INSERT INTO "alert_settings" VALUES(41,'low_stock_threshold','10','2026-09-09 11:58:19');
INSERT INTO "alert_settings" VALUES(42,'critical_stock_threshold','5','2026-09-09 11:58:19');
INSERT INTO "alert_settings" VALUES(43,'expiry_critical_days','7','2026-09-09 11:58:19');
INSERT INTO "alert_settings" VALUES(44,'expiry_warning_days','30','2026-09-09 11:58:19');
DROP TABLE IF EXISTS alert_visibility;
CREATE TABLE alert_visibility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            alert_type VARCHAR(50) NOT NULL,
            admin_id INTEGER NOT NULL,
            is_hidden INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
            UNIQUE(product_id, alert_type, admin_id)
        );
DROP TABLE IF EXISTS cashier_activity;
CREATE TABLE cashier_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashier_id INTEGER NOT NULL,
            login_time TEXT NOT NULL,
            logout_time TEXT DEFAULT NULL,
            ip_address VARCHAR(45) DEFAULT NULL,
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id) ON DELETE CASCADE
        );
INSERT INTO "cashier_activity" VALUES(1,1,'2026-09-09 18:01:44','2026-09-09 21:24:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(2,1,'2026-09-09 21:20:44','2026-09-09 21:24:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(3,1,'2026-09-11 10:46:35','2026-09-11 10:52:24','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(4,1,'2026-09-11 10:52:41','2026-09-11 10:53:48','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(5,1,'2026-09-11 10:54:46','2026-09-11 11:00:06','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(6,1,'2026-09-11 11:02:12','2026-09-11 11:02:57','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(7,1,'2026-09-11 11:05:14','2026-09-11 11:08:02','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(8,1,'2026-09-11 11:25:48','2026-09-11 12:18:42','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(9,1,'2026-09-11 12:38:49','2026-09-11 12:46:50','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(10,1,'2026-09-11 12:52:24','2026-09-11 15:47:09','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(11,1,'2026-09-11 15:47:21','2026-09-11 16:42:06','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(12,1,'2026-09-11 16:40:48','2026-09-11 16:42:06','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(13,1,'2026-09-19 09:20:12','2026-09-19 14:17:55','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(14,1,'2026-09-19 14:16:57','2026-09-19 14:17:55','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(15,1,'2026-09-19 14:20:17','2026-09-19 14:21:31','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(16,1,'2026-09-19 14:26:21','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(17,1,'2026-09-19 19:53:36','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(18,1,'2026-09-21 23:28:14','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(19,1,'2026-09-22 14:28:30','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(20,1,'2026-09-23 12:29:10','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(21,1,'2026-09-23 12:31:44','2026-09-23 19:35:00','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(22,1,'2026-10-01 11:54:42','2026-10-06 13:08:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(23,1,'2026-10-01 17:31:36','2026-10-06 13:08:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(24,1,'2026-10-02 12:33:43','2026-10-06 13:08:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(25,1,'2026-10-02 23:31:54','2026-10-06 13:08:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(26,1,'2026-10-06 13:06:48','2026-10-06 13:08:05','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(27,1,'2026-10-06 13:18:27','2026-10-06 13:19:14','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(28,1,'2026-10-06 13:22:24','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(29,1,'2026-10-06 13:26:43','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(30,1,'2026-10-06 14:25:06','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(31,1,'2026-10-06 14:26:48','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(32,1,'2026-10-06 14:28:42','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(33,1,'2026-10-06 14:37:50','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(34,1,'2026-10-06 14:39:59','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(35,1,'2026-10-13 13:46:29','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(36,1,'2026-10-13 14:34:00','2026-10-13 15:24:30','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(37,1,'2026-10-13 16:18:33','2026-10-13 17:12:31','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(38,1,'2026-10-13 17:14:36','2026-10-13 17:48:59','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(39,1,'2026-10-13 17:51:27','2026-10-13 17:52:45','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(40,1,'2026-10-14 13:24:43','2026-10-14 13:29:54','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(41,1,'2026-10-14 13:34:11','2026-10-14 14:04:11','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(42,1,'2026-10-14 13:39:45','2026-10-14 14:04:11','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(43,1,'2026-10-14 14:03:21','2026-10-14 14:04:11','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(44,1,'2026-10-14 14:06:37','2026-10-14 14:11:56','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(45,1,'2026-10-14 14:17:05','2026-10-14 23:50:59','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(46,1,'2026-10-14 23:51:18','2026-10-14 23:51:23','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(47,1,'2026-10-14 23:58:41','2026-10-15 00:01:16','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(48,1,'2026-10-15 00:04:59','2026-10-15 00:35:16','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(49,1,'2026-10-15 13:55:09','2026-10-15 13:58:02','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(50,1,'2026-10-15 13:59:13','2026-10-15 14:01:33','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(51,1,'2026-10-15 14:02:53','2026-10-15 14:07:17','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(52,1,'2026-10-15 14:10:49','2026-10-15 14:12:16','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(53,1,'2026-10-15 14:42:33','2026-10-15 15:29:13','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(54,1,'2026-10-15 15:30:28','2026-10-16 10:29:13','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(55,1,'2026-10-16 10:31:38','2026-10-16 10:39:46','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(56,1,'2026-10-16 10:43:35','2026-10-16 11:09:19','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(57,1,'2026-10-16 11:11:01','2026-10-16 12:42:22','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(58,1,'2026-10-16 12:43:21','2026-10-16 17:09:01','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(59,1,'2026-10-16 17:10:27','2026-10-16 18:09:52','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(60,1,'2026-10-16 18:11:27','2026-10-20 13:58:11','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(61,1,'2026-10-20 13:54:15','2026-10-20 13:58:11','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(62,1,'2026-10-20 13:59:12','2026-10-20 13:59:50','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(63,1,'2026-10-20 14:02:00','2026-10-20 14:02:50','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(64,1,'2026-10-20 14:08:14','2026-10-20 14:51:43','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(65,1,'2026-10-20 14:53:56','2026-10-20 15:55:31','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(66,1,'2026-10-20 15:57:43','2026-10-23 14:01:58','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(67,1,'2026-10-22 09:56:53','2026-10-23 14:01:58','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(68,1,'2026-10-23 14:03:00','2026-10-27 12:58:39','127.0.0.1');
INSERT INTO "cashier_activity" VALUES(69,1,'2026-10-27 12:58:27','2026-10-27 12:58:39','127.0.0.1');
DROP TABLE IF EXISTS cashiers;
CREATE TABLE cashiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(100),
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            security_question VARCHAR(255),
            security_answer VARCHAR(255),
            force_password_change INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );
-- Cashier credentials excluded from backup
CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(100) NOT NULL,
            description TEXT
        );
INSERT INTO "categories" VALUES(21,'Medical','Medical products and medicines');
INSERT INTO "categories" VALUES(22,'Non-Medical','Supplies and hygiene products');
DROP TABLE IF EXISTS held_transactions;
CREATE TABLE held_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashier_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            cart TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id) ON DELETE CASCADE
        );
DROP TABLE IF EXISTS login_attempts;
CREATE TABLE login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address VARCHAR(45) DEFAULT NULL,
            username_attempted VARCHAR(100) DEFAULT NULL,
            attempted_at TEXT DEFAULT (datetime('now', 'localtime')),
            locked_until TEXT NULL DEFAULT NULL
        );
DROP TABLE IF EXISTS products;
CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(200) NOT NULL,
            barcode VARCHAR(100) DEFAULT NULL,
            category_id INTEGER,
            product_type VARCHAR(50) DEFAULT 'medical',
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            expiration_date TEXT DEFAULT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
INSERT INTO "products" VALUES(39,'Nature Spring (500mL)','4800049720114',21,'Medical',15.0,12,NULL,'2026-09-10 14:03:45');
INSERT INTO "products" VALUES(41,'Choco Mucho (30g)','4800092660634',22,'Non-Medical',12.0,5,'2027-02-02','2026-09-10 14:08:21');
INSERT INTO "products" VALUES(42,'LM Chicken Sotanghon (28g)','4807770271519',22,'Non-Medical',30.0,3,'2027-01-23','2026-09-10 14:10:18');
INSERT INTO "products" VALUES(43,'LM Bulalo (40g)','4807770271175',22,'Non-Medical',26.0,2,'2026-11-01','2026-09-10 14:12:55');
INSERT INTO "products" VALUES(44,'LM Spicy Batchoy (40g)','4807770273810',22,'Non-Medical',26.0,4,'2026-01-19','2026-09-10 14:16:04');
INSERT INTO "products" VALUES(45,'LM Spicy Bulalo (40g)','4807770273612',22,'Non-Medical',26.0,4,'2027-01-26','2026-09-10 14:24:00');
INSERT INTO "products" VALUES(46,'LM Batchoy (70g)','4807770272110',22,'Non-Medical',36.0,2,'2026-12-28','2026-09-10 14:32:41');
INSERT INTO "products" VALUES(47,'LM Jjampong (40g)','4807770272653',22,'Non-Medical',30.0,20,'2027-01-21','2026-09-10 14:33:55');
INSERT INTO "products" VALUES(48,'Nissin Seafood (40g)','4800016552113',22,'Non-Medical',28.0,3,'2027-07-22','2026-09-10 14:36:25');
INSERT INTO "products" VALUES(49,'Nescafe Original (20g)','4800361403764',22,'Non-Medical',10.0,20,'2027-02-28','2026-09-10 14:43:40');
INSERT INTO "products" VALUES(50,'Kopiko Blanca (20g)','8996001414309',22,'Non-Medical',10.0,16,'2027-08-23','2026-09-10 14:45:35');
INSERT INTO "products" VALUES(51,'Kopiko Brown (20g)','8996001410547',22,'Non-Medical',10.0,7,'2027-08-15','2026-09-10 14:47:19');
INSERT INTO "products" VALUES(52,'Kopiko Black (20g)','8996001410226',22,'Non-Medical',10.0,6,'2027-03-02','2026-09-10 14:48:52');
INSERT INTO "products" VALUES(53,'Lipton Tea Bag (2g)','8720608629107',22,'Non-Medical',10.0,8,'2026-10-09','2026-09-10 14:51:21');
INSERT INTO "products" VALUES(54,'Milo (24g)','4800361413480',22,'Non-Medical',11.0,18,'2027-01-31','2026-09-10 14:54:24');
INSERT INTO "products" VALUES(55,'Quaker Original w/ Milk (40g)','4800274410408',22,'Non-Medical',23.0,2,'2026-09-20','2026-09-10 14:56:01');
INSERT INTO "products" VALUES(56,'Quaker Banana & Honey (33g)','4800274310357',22,'Non-Medical',15.0,3,'2027-04-20','2026-09-10 14:56:58');
INSERT INTO "products" VALUES(57,'Nescafe Classic (1.9g)','4800361339568',22,'Non-Medical',5.0,36,'2027-05-31','2026-09-10 15:08:34');
INSERT INTO "products" VALUES(58,'Nestle Coffee Mate (5g)','48025515',22,'Non-Medical',5.0,51,'2027-04-30','2026-09-10 15:11:51');
INSERT INTO "products" VALUES(59,'Nestle Bear Brand (33g)','4800361410816',22,'Non-Medical',14.0,10,'2027-05-31','2026-09-10 15:12:56');
INSERT INTO "products" VALUES(60,'Birch Tree (33g)','748485401492',22,'Non-Medical',13.0,9,'2027-10-31','2026-09-10 15:14:35');
INSERT INTO "products" VALUES(61,'Alaska Fortified (33g)','n/a',22,'Non-Medical',10.0,5,'2026-11-28','2026-09-10 15:16:42');
INSERT INTO "products" VALUES(62,'Eden Original (45g)','7622210892126',22,'Non-Medical',20.0,4,'2026-11-22','2026-09-10 15:17:45');
INSERT INTO "products" VALUES(63,'Alaska Condensed (38g)','4800575142169',22,'Non-Medical',12.0,6,'2026-12-05','2026-09-10 15:19:58');
INSERT INTO "products" VALUES(64,'Star Classic (30g)','4805358279155',22,'Non-Medical',15.0,12,'2026-12-27','2026-09-10 15:22:16');
INSERT INTO "products" VALUES(65,'Best Foods Mayo Magic (80ml)','4808680652757',22,'Non-Medical',30.0,1,'2027-03-21','2026-09-10 15:24:00');
INSERT INTO "products" VALUES(66,'Tang Orange (19g)','7622300559991',22,'Non-Medical',22.0,23,'2027-02-12','2026-09-10 15:25:08');
INSERT INTO "products" VALUES(67,'Tang Grapes (19g)','7622300637996',22,'Non-Medical',22.0,7,'2027-03-25','2026-09-10 15:26:07');
INSERT INTO "products" VALUES(68,'Tang Pineapple (19g)','7622300601768',22,'Non-Medical',22.0,4,'2027-02-12','2026-09-10 15:26:58');
INSERT INTO "products" VALUES(69,'Nestea Apple (19g)','4800361382083',22,'Non-Medical',23.0,6,'2027-01-31','2026-09-10 15:27:50');
INSERT INTO "products" VALUES(70,'Papa Banana Ketchup (25g)','014285004158',22,'Non-Medical',6.0,7,'2027-02-02','2026-09-10 15:29:37');
INSERT INTO "products" VALUES(71,'Maggi Magic Sarap (8g)','48025522',22,'Non-Medical',7.0,19,'2027-01-31','2026-09-10 15:30:33');
INSERT INTO "products" VALUES(72,'Ajinomoto (24g)','4801958342008',22,'Non-Medical',10.0,3,NULL,'2026-09-10 15:31:34');
INSERT INTO "products" VALUES(73,'Ajinomoto (11g)','N/A',22,'Non-Medical',5.0,11,NULL,'2026-09-10 15:33:08');
INSERT INTO "products" VALUES(74,'Ajinomoto Ginisa (8g)','4801958846001',22,'Non-Medical',5.0,16,'275760-08-04','2026-09-10 15:36:11');
INSERT INTO "products" VALUES(75,'Equal Refined Sugar (1/4kg)','4806528802289',22,'Non-Medical',25.0,9,'2026-10-17','2026-09-10 15:37:33');
INSERT INTO "products" VALUES(76,'Knorr Sinigang Origina Mix (11g)','4800888603692',22,'Non-Medical',10.0,17,'2027-05-05','2026-09-10 15:39:49');
INSERT INTO "products" VALUES(77,'Mama Sitas Oyster Sauce (30g)','4804888809474',22,'Non-Medical',8.0,5,'2027-02-17','2026-09-10 15:41:24');
INSERT INTO "products" VALUES(78,'Bioderm Timeless (60g)','4800011783031',22,'Non-Medical',20.0,1,NULL,'2026-09-10 16:06:15');
INSERT INTO "products" VALUES(79,'Bioderm Intense Coolness (60g)','4800011149875',22,'Non-Medical',22.0,1,NULL,'2026-09-10 16:07:41');
INSERT INTO "products" VALUES(80,'Bioderm Coolness (60g)','4800011113937',22,'Non-Medical',20.0,3,NULL,'2026-09-10 16:08:47');
INSERT INTO "products" VALUES(81,'Bioderm Clean White (60g)','4800011795331',22,'Non-Medical',20.0,8,NULL,'2026-09-10 16:10:11');
INSERT INTO "products" VALUES(82,'Myra Whitening Papaya Extract (45g)','4800135000373',22,'Non-Medical',25.0,2,'2027-02-28','2026-09-10 16:12:49');
INSERT INTO "products" VALUES(83,'Johnsons Blossom (50g)','4801010561514',22,'Non-Medical',26.0,1,'2028-12-25','2026-09-10 16:14:04');
INSERT INTO "products" VALUES(84,'Johnsons Milk (50g)','4801010562313',22,'Non-Medical',26.0,1,'2029-02-13','2026-09-10 16:15:37');
INSERT INTO "products" VALUES(85,'Silka (65g)','N\A',22,'Non-Medical',22.0,4,'2029-05-30','2026-09-10 16:16:42');
INSERT INTO "products" VALUES(86,'GreenCross Cool Mountain (55g)','4800047863158',22,'Non-Medical',18.0,2,'2028-04-30','2026-09-10 16:18:41');
INSERT INTO "products" VALUES(87,'Safeguard Pure White (65g)','4902430945554',22,'Non-Medical',25.0,7,'2026-06-10','2026-09-10 16:20:02');
INSERT INTO "products" VALUES(88,'Perla Papaya (110g)','4902430178273',22,'Non-Medical',20.0,6,'2027-05-14','2026-09-10 16:21:07');
INSERT INTO "products" VALUES(89,'Perla Original White (110g)','4902430178259',22,'Non-Medical',20.0,5,'2028-11-18','2026-09-10 16:21:57');
INSERT INTO "products" VALUES(90,'Citric','N\A',22,'Non-Medical',10.0,16,NULL,'2026-09-10 16:23:08');
INSERT INTO "products" VALUES(91,'Surf Bar Kalamansi (120g)','4800888136732',22,'Non-Medical',14.0,9,NULL,'2026-09-10 16:24:08');
INSERT INTO "products" VALUES(92,'Surf Bar Cherry Blossom (120g)','4800888190970',22,'Non-Medical',14.0,1,NULL,'2026-09-10 16:25:16');
INSERT INTO "products" VALUES(93,'Ariel Sunrise Fresh Liquid (58g)','4902430764858',22,'Non-Medical',18.0,2,NULL,'2026-09-10 16:27:39');
INSERT INTO "products" VALUES(94,'Ariel w/ Downy Floral Passion (54g)','4902430764902',22,'Non-Medical',18.0,11,NULL,'2026-09-10 16:33:14');
INSERT INTO "products" VALUES(95,'Pride Liquid (60ml)','4800045411283',22,'Non-Medical',10.0,15,'2028-12-31','2026-09-10 16:35:11');
INSERT INTO "products" VALUES(96,'Tide Perfect Clean (69g)','4902430831406',22,'Non-Medical',18.0,2,NULL,'2026-09-10 16:37:05');
INSERT INTO "products" VALUES(97,'Tide w/ Downy Perfume Fantasy (67g)','4902430884242',22,'Non-Medical',18.0,7,NULL,'2026-09-10 16:43:31');
INSERT INTO "products" VALUES(98,'Dove Shampoo Bio Keratin (13.5ml)','4800888212917',22,'Non-Medical',9.0,12,NULL,'2026-09-10 16:57:35');
INSERT INTO "products" VALUES(99,'Dove Shampoo Ceramide (13.5ml)','4800888212900',22,'Non-Medical',9.0,1,NULL,'2026-09-10 16:58:29');
INSERT INTO "products" VALUES(100,'Head & Shoulder Shampoo Smooth & Silky (12ml)','4902430698658',22,'Non-Medical',8.0,9,NULL,'2026-09-10 16:59:59');
INSERT INTO "products" VALUES(101,'Sunsilk Shampoo Smooth & Manageable (15ml)','4800888169716',22,'Non-Medical',8.0,4,NULL,'2026-09-10 17:01:45');
INSERT INTO "products" VALUES(102,'Sunsilk Shampoo Strong & Long (15ml)','4800888169709',22,'Non-Medical',8.0,10,NULL,'2026-09-10 17:03:11');
INSERT INTO "products" VALUES(103,'Gard Refreshing Menthol (12ml)','8850006536063',22,'Non-Medical',8.0,2,NULL,'2026-09-10 17:04:13');
INSERT INTO "products" VALUES(104,'Palmolive Intensive Moisture (15ml)','8850006493014',22,'Non-Medical',8.0,3,NULL,'2026-09-10 17:06:34');
INSERT INTO "products" VALUES(105,'Palmolive Ultra Smooth (15ml)','8850006493038',22,'Non-Medical',8.0,2,NULL,'2026-09-10 17:07:44');
INSERT INTO "products" VALUES(106,'Palmolive Silky Straight (15ml)','8850006493045',21,'Medical',8.0,5,NULL,'2026-09-10 17:08:51');
INSERT INTO "products" VALUES(107,'Dove Shampoo Restorative Oil (12ml)','4800888154255',22,'Non-Medical',8.0,13,NULL,'2026-09-10 17:10:16');
INSERT INTO "products" VALUES(108,'Pantene Shampoo Total Damage Care (15ml)','4902430698146',22,'Non-Medical',8.0,4,NULL,'2026-09-10 17:11:33');
INSERT INTO "products" VALUES(109,'Creamsilk Hairfall Defense (13ml)','4800888139283',22,'Non-Medical',9.0,7,NULL,'2026-09-10 17:12:52');
INSERT INTO "products" VALUES(110,'Creamsilk Standout Straight (13ml)','4800888139306',22,'Non-Medical',9.0,20,NULL,'2026-09-10 17:13:42');
INSERT INTO "products" VALUES(111,'Close Up Red Hot (10g)','4800888147288',22,'Non-Medical',10.0,6,NULL,'2026-09-10 17:15:17');
INSERT INTO "products" VALUES(112,'Colgate Maximum Cavity Protection (20g)','8850006325216',22,'Non-Medical',10.0,16,NULL,'2026-09-10 17:16:59');
INSERT INTO "products" VALUES(113,'Colgate Charcoal Clean (20g)','6920354832123',22,'Non-Medical',14.0,8,NULL,'2026-09-10 17:17:57');
INSERT INTO "products" VALUES(114,'Colgate Fresh Confidence (20g)','8850006325223',22,'Non-Medical',10.0,13,NULL,'2026-09-10 17:18:47');
INSERT INTO "products" VALUES(115,'Wings Floral Fresh (70g)','8998866635073',22,'Non-Medical',8.0,1,NULL,'2026-09-10 17:20:05');
INSERT INTO "products" VALUES(116,'Del w/ Fragarance Pearls (33ml)','4800047847325',22,'Non-Medical',7.0,9,NULL,'2026-09-10 17:22:11');
INSERT INTO "products" VALUES(117,'Del Lavender Breeze (22ml)','4800047841378',22,'Non-Medical',7.0,1,NULL,'2026-09-10 17:23:22');
INSERT INTO "products" VALUES(118,'Del Blossom Fresh (33ml)','4800047847332',22,'Non-Medical',7.0,1,NULL,'2026-09-10 17:24:15');
INSERT INTO "products" VALUES(119,'Downy Kontra Kulob (24ml)','4902430873703',22,'Non-Medical',9.0,84902430344876,NULL,'2026-09-10 17:24:57');
INSERT INTO "products" VALUES(120,'Downy Kontra Kulog (24ml)','4902430873703',22,'Non-Medical',9.0,4,NULL,'2026-09-10 17:25:47');
INSERT INTO "products" VALUES(121,'Downy Kontra Germa Safeguard (26ml)','4902430344876',22,'Non-Medical',9.0,1,NULL,'2026-09-10 17:26:40');
INSERT INTO "products" VALUES(122,'Surf Sun Fresh (65g)','4800888218544',22,'Non-Medical',9.0,6,NULL,'2026-09-10 17:27:21');
INSERT INTO "products" VALUES(123,'Surf Kalamansi (57g)','4800888151827',22,'Non-Medical',9.0,2,NULL,'2026-09-10 17:28:07');
INSERT INTO "products" VALUES(124,'Surf Purple Blooms (65g) ','4800888199133',22,'Non-Medical',9.0,0,NULL,'2026-09-10 17:29:24');
INSERT INTO "products" VALUES(125,'Surf Cherry Blossom (65g)','4800888221056',22,'Non-Medical',9.0,3,NULL,'2026-09-10 17:30:06');
INSERT INTO "products" VALUES(126,'Surf Fabric Conditioner Lux Perfumer (25ml)','8934868110170',22,'Non-Medical',7.0,13,NULL,'2026-09-10 17:31:09');
INSERT INTO "products" VALUES(127,'Surf Fabric Conditioner Blossom Fresh (40ml) ','8934868115908',22,'Non-Medical',9.0,12,NULL,'2026-09-10 17:31:53');
INSERT INTO "products" VALUES(128,'Surf Bar Anti Bacterial (120g)','4800888219343',22,'Non-Medical',15.0,2,NULL,'2026-09-10 17:33:00');
INSERT INTO "products" VALUES(129,'Surf Bar Kalamansi (120g)','4800888136732',22,'Non-Medical',15.0,2,NULL,'2026-09-10 17:33:46');
INSERT INTO "products" VALUES(130,'Surf Bar Purple Blooms (120g)','4800888199119',22,'Non-Medical',15.0,3,NULL,'2026-09-10 17:34:21');
INSERT INTO "products" VALUES(131,'Surf Bar Sun Fresh (120g) ','4800888136770',22,'Non-Medical',15.0,3,NULL,'2026-09-10 17:35:04');
INSERT INTO "products" VALUES(132,'Pride Sakura Blossom (40g) ','4800045350018',22,'Non-Medical',6.0,11,NULL,'2026-09-10 17:35:54');
INSERT INTO "products" VALUES(133,'LM Pancit Canton Chilimansi (60g)','4807770270291',22,'Non-Medical',14.0,5,'2026-12-24','2026-09-11 13:43:41');
INSERT INTO "products" VALUES(134,'LM Pancit Canton Kalamansi (60g)','4807770270123',22,'Non-Medical',14.0,2,'2026-12-24','2026-09-11 13:44:23');
INSERT INTO "products" VALUES(135,'LM Pancit Canton Extra Hot (120g)','4807770274275',22,'Non-Medical',22.0,2,NULL,'2026-09-11 13:45:30');
INSERT INTO "products" VALUES(136,'LM Pancit Canton Kalamansi (120g)','4807770274275',22,'Non-Medical',22.0,6,'2026-12-21','2026-09-11 13:46:20');
INSERT INTO "products" VALUES(137,'LM Pancit Canton Chilimansi (120g)','4807770274480',22,'Non-Medical',22.0,2,'2026-12-01','2026-09-11 13:47:18');
INSERT INTO "products" VALUES(138,'LM Pancit Canton Sweet & Spicy (120g)','4807770274473',22,'Non-Medical',22.0,2,'2026-12-08','2026-09-11 13:48:20');
INSERT INTO "products" VALUES(139,'LM Noodles Beef (55g)','4807770270017',22,'Non-Medical',11.0,10,'2027-01-25','2026-09-11 13:51:16');
INSERT INTO "products" VALUES(140,'LM Noodles Spicy Labuyo (50g)','4807770272097',22,'Non-Medical',11.0,4,'2027-01-03','2026-09-11 13:52:45');
INSERT INTO "products" VALUES(141,'Payless Noodles Beef (55g)','4800016553332',22,'Non-Medical',11.0,2,'2027-01-06','2026-09-11 13:53:45');
INSERT INTO "products" VALUES(142,'LM Noodles Chicken (55g)','4807770270024',22,'Non-Medical',11.0,6,'2026-12-28','2026-09-11 13:54:36');
INSERT INTO "products" VALUES(143,'Bingo Carne Norte (100g)','4800249053951',22,'Non-Medical',20.0,3,'2027-10-15','2026-09-19 11:32:15');
INSERT INTO "products" VALUES(144,'Argentina Meat Loaf (170g)','748485800233',22,'Non-Medical',28.0,3,'2029-05-06','2026-09-19 11:33:30');
INSERT INTO "products" VALUES(145,'Argentina Beef Loaf (250g)','748485800110',22,'Non-Medical',40.0,3,'2029-02-26','2026-09-19 11:36:19');
INSERT INTO "products" VALUES(146,'Argentina Beef Loaf (170g)','748485800097',22,'Non-Medical',28.0,2,'2029-07-08','2026-09-19 11:45:04');
INSERT INTO "products" VALUES(147,'Wow Ulam Afritada (155g)','748485802077',22,'Non-Medical',26.0,3,'2028-11-13','2026-09-19 11:46:45');
INSERT INTO "products" VALUES(148,'Wow Ulam Caldereta (155g)','748485802084',22,'Non-Medical',26.0,3,'2028-11-04','2026-09-19 11:47:53');
INSERT INTO "products" VALUES(149,'Wow Ulam Pochero (155g)','748485803654',22,'Non-Medical',26.0,3,'2029-02-16','2026-09-19 11:48:53');
INSERT INTO "products" VALUES(150,'Wow Ulam Adobo (155g)','748485802060',22,'Non-Medical',26.0,3,'2028-10-20','2026-09-19 11:49:57');
INSERT INTO "products" VALUES(151,'Toyo Sardines Spicy (155g)','4806508620032',22,'Non-Medical',26.0,3,'2028-10-30','2026-09-19 11:51:32');
INSERT INTO "products" VALUES(152,'Toyo Sardines Original (155g)','4806508620025',22,'Non-Medical',26.0,3,'2026-11-06','2026-09-19 11:52:43');
INSERT INTO "products" VALUES(153,'Fresca Sardines Original (155g)','748485201887',22,'Non-Medical',24.0,3,'2028-02-22','2026-09-19 11:53:39');
INSERT INTO "products" VALUES(154,'Fresca Sardines Spicy (155g)','748485201894',22,'Non-Medical',25.0,3,'2027-11-02','2026-09-19 11:54:59');
INSERT INTO "products" VALUES(155,'Ligo Sardines Spicy (155g)','4800163443036',22,'Non-Medical',27.0,3,'2028-10-10','2026-09-19 11:56:34');
INSERT INTO "products" VALUES(156,'Toyo Mackerel (155g)','4806508620063',22,'Non-Medical',30.0,2,'2028-10-25','2026-09-19 11:58:02');
INSERT INTO "products" VALUES(157,'555 Sardines Spicy (155g)','748485200026',22,'Non-Medical',27.0,3,'2029-05-06','2026-09-19 11:59:38');
INSERT INTO "products" VALUES(158,'555 Sardines Original (155g)','748485200019',22,'Non-Medical',27.0,3,'2028-10-04','2026-09-19 12:00:37');
INSERT INTO "products" VALUES(159,'Virginia Vienna Sausage (70g)','4800088115087',22,'Non-Medical',33.0,3,'2029-03-11','2026-09-19 12:01:49');
INSERT INTO "products" VALUES(160,'San Marino Spicy (150g)','4800249006636',22,'Non-Medical',44.0,3,'2029-05-02','2026-09-19 12:03:14');
INSERT INTO "products" VALUES(161,'Lucky 7 Carne Norte (150g)','748485801728',22,'Non-Medical',23.0,3,'2028-10-28','2026-09-19 12:04:28');
INSERT INTO "products" VALUES(162,'Century Tuna Spicy (155g)','748485100418',22,'Non-Medical',44.0,3,'2029-03-29','2026-09-19 12:06:40');
INSERT INTO "products" VALUES(163,'555 Tuna Caldereta','748485700038',22,'Non-Medical',33.0,3,'2029-04-25','2026-09-19 12:07:43');
INSERT INTO "products" VALUES(164,'Argentina Corned Beef (150g)','748485800431',22,'Non-Medical',40.0,3,'2029-06-10','2026-09-19 12:08:52');
INSERT INTO "products" VALUES(165,'Star Corned Beef (150g)','4808887011852',22,'Non-Medical',38.0,3,'2027-10-28','2026-09-19 12:09:59');
INSERT INTO "products" VALUES(166,'San Marino Original (150g)','4800249006612',22,'Non-Medical',44.0,3,'2029-06-26','2026-09-19 12:18:49');
INSERT INTO "products" VALUES(167,'555 Sardines Spicy (425G)','748485200071',22,'Non-Medical',63.0,1,'2028-07-25','2026-09-19 12:22:05');
INSERT INTO "products" VALUES(168,'Hunts Pork & Beans ','4800022100018',22,'Non-Medical',38.0,1,'2028-02-07','2026-09-19 12:27:36');
INSERT INTO "products" VALUES(169,'555 Sardines Original (425g)','748485200064',22,'Non-Medical',63.0,0,'2028-10-13','2026-09-19 12:28:39');
INSERT INTO "products" VALUES(170,'Argentina Meat Loaf (250g)','748485800448',22,'Non-Medical',40.0,3,'2028-11-18','2026-09-19 12:31:37');
INSERT INTO "products" VALUES(171,'555 Squid Spicy (155g)','748485300092',22,'Non-Medical',52.0,1,'2028-08-28','2026-09-19 12:33:44');
INSERT INTO "products" VALUES(172,'555 tuna Bicol Express (155g)','748485700090',22,'Non-Medical',33.0,3,'2029-04-29','2026-09-19 12:34:43');
INSERT INTO "products" VALUES(173,'Wow Ulam Adobo (155g)','748485802060',22,'Non-Medical',26.0,3,'2028-09-23','2026-09-19 12:36:23');
INSERT INTO "products" VALUES(174,'Wow Ulam Mechado','748485802220',22,'Non-Medical',26.0,3,'2028-10-14','2026-09-19 12:37:46');
INSERT INTO "products" VALUES(175,'555 Tuna Mechado ','748485700045',22,'Non-Medical',33.0,3,'2029-05-21','2026-09-19 12:40:13');
INSERT INTO "products" VALUES(176,'555 Tuna Afritada (155g)','748485700021',22,'Non-Medical',33.0,17,'2029-04-22','2026-09-19 12:42:39');
INSERT INTO "products" VALUES(177,'Century Tuna Original (155g)','00000',22,'Non-Medical',44.0,3,'2029-04-17','2026-09-19 13:08:50');
INSERT INTO "products" VALUES(178,'CDO Karne Norte (150g)','00000',22,'Non-Medical',35.0,3,'2029-04-24','2026-09-19 13:14:36');
INSERT INTO "products" VALUES(179,'Del Monte Pineapple Tidbits (137g)','4800024562258',22,'Non-Medical',42.0,2,'2027-11-01','2026-09-19 13:31:09');
INSERT INTO "products" VALUES(180,'Del Monte Pineapple Chunks (137g)','4800024020642',22,'Non-Medical',42.0,1,'2028-02-01','2026-09-19 13:35:44');
INSERT INTO "products" VALUES(181,'Uni-Pak Tomato Paste (155g)','4800154565013',22,'Non-Medical',30.0,3,'2027-03-21','2026-09-19 13:37:03');
INSERT INTO "products" VALUES(182,'Mayon Mushrooms (115g)','4806508627307',22,'Non-Medical',38.0,1,'2027-06-01','2026-09-19 13:40:10');
INSERT INTO "products" VALUES(183,'Senorita ','4806508624009',22,'Non-Medical',18.0,2,'2029-02-10','2026-09-19 13:46:13');
INSERT INTO "products" VALUES(184,'Alaska Evaporada (140ml)','4800575140158',22,'Non-Medical',25.0,1,'2028-11-05','2026-09-19 13:49:19');
INSERT INTO "products" VALUES(185,'Senorita ( Black Beans ) 180g ','4806508624610',22,'Non-Medical',30.0,2,'2027-07-05','2026-09-19 13:50:39');
INSERT INTO "products" VALUES(186,'Magnolia ( ALL PURPOSE FLOUR) 200G ','4806512230814',22,'Non-Medical',30.0,3,'0202-02-26','2026-09-19 13:51:49');
INSERT INTO "products" VALUES(187,'Hasmine Rice ','0001',22,'Non-Medical',55.0,1,NULL,'2026-09-19 13:53:07');
INSERT INTO "products" VALUES(188,'Star Sweet Blend ','48037433',22,'Non-Medical',40.0,1,'2026-09-30','2026-09-19 13:54:32');
INSERT INTO "products" VALUES(189,'Silver Swan Salted Black Beans (100g)','4800344040122',22,'Non-Medical',20.0,2,'2028-01-27','2026-09-19 13:55:53');
INSERT INTO "products" VALUES(190,'Coco Mama Fresh Gata (200ml)','748485150079',22,'Non-Medical',40.0,4,'2027-09-10','2026-09-19 13:57:27');
INSERT INTO "products" VALUES(191,'Silver Swan Soy Sauce (200ml)','4800344001949',22,'Non-Medical',14.0,6,'2030-03-19','2026-09-19 14:00:23');
INSERT INTO "products" VALUES(192,'Ufc Tamis Anghang (320g)','014285000068',22,'Non-Medical',30.0,3,'2027-01-09','2026-09-19 14:10:37');
INSERT INTO "products" VALUES(194,'Coke,Sprite,Royal (Litro)','0003',22,'Non-Medical',45.0,24,NULL,'2026-09-19 14:15:13');
INSERT INTO "products" VALUES(195,'Nature Spring (1000ml)','4800049720121',22,'Non-Medical',25.0,17,NULL,'2026-09-19 14:20:01');
INSERT INTO "products" VALUES(196,'Egg','0013',22,'Non-Medical',13.0,18,NULL,'2026-09-19 14:24:52');
INSERT INTO "products" VALUES(197,'Washed Sugar (1/4)','0012',22,'Non-Medical',23.0,5,NULL,'2026-09-23 13:37:57');
INSERT INTO "products" VALUES(198,'Buko','0011',22,'Non-Medical',27.0,16,NULL,'2026-09-23 13:40:09');
INSERT INTO "products" VALUES(199,'Cobra','0004',22,'Non-Medical',26.0,5,NULL,'2026-09-23 13:42:55');
INSERT INTO "products" VALUES(200,'Sting','0005',22,'Non-Medical',26.0,5,NULL,'2026-09-23 13:43:26');
INSERT INTO "products" VALUES(201,'Big (Apple & Orange)','0006',22,'Non-Medical',12.0,13,NULL,'2026-09-23 13:44:09');
INSERT INTO "products" VALUES(202,'Big (Strawberry,Guyabano,Grapes)','0007',22,'Non-Medical',15.0,30,NULL,'2026-09-23 13:44:58');
INSERT INTO "products" VALUES(203,'Choc-O ','0008',22,'Non-Medical',25.0,1,NULL,'2026-09-23 13:45:32');
INSERT INTO "products" VALUES(204,'Yakult','0009',22,'Non-Medical',12.0,9,NULL,'2026-09-23 13:46:03');
INSERT INTO "products" VALUES(205,'Dutch Mill (Small)','0010',22,'Non-Medical',14.0,5,NULL,'2026-09-23 13:46:39');
INSERT INTO "products" VALUES(206,'Selecta (Fortified Milk)','0014',22,'Non-Medical',38.0,3,NULL,'2026-09-23 13:47:39');
INSERT INTO "products" VALUES(207,'Chuckie (Small)','0015',22,'Non-Medical',20.0,4,NULL,'2026-09-23 13:48:16');
INSERT INTO "products" VALUES(208,'Milo (Small)','0016',22,'Non-Medical',20.0,5,NULL,'2026-09-23 13:48:48');
INSERT INTO "products" VALUES(209,'Calamansi Juice','0017',22,'Non-Medical',22.0,5,NULL,'2026-09-23 13:49:17');
INSERT INTO "products" VALUES(210,'C2 (Small)','0018',22,'Non-Medical',18.0,10,NULL,'2026-09-23 13:49:54');
INSERT INTO "products" VALUES(211,'C2 (Medium)','0019',22,'Non-Medical',30.0,0,NULL,'2026-09-23 13:50:25');
INSERT INTO "products" VALUES(212,'C2 (Big)','0020',22,'Non-Medical',35.0,2,NULL,'2026-09-23 13:50:51');
INSERT INTO "products" VALUES(213,'Mogu-mogu','0021',22,'Non-Medical',46.0,3,NULL,'2026-09-23 13:51:59');
INSERT INTO "products" VALUES(214,'Swakto','0022',22,'Non-Medical',15.0,6,NULL,'2026-09-23 13:52:46');
INSERT INTO "products" VALUES(215,'Curls','0023',22,'Non-Medical',10.0,45,NULL,'2026-09-23 13:53:18');
INSERT INTO "products" VALUES(216,'Biscuits ','0024',22,'Non-Medical',8.0,28,NULL,'2026-09-23 13:54:01');
INSERT INTO "products" VALUES(218,'Ascorbic Acid + Zinc','4806035208031',21,'Medical',5.0,84,NULL,'2026-10-06 13:29:33');
INSERT INTO "products" VALUES(219,'Amlodipine Besilate','4800338585981',21,'Medical',5.0,100,NULL,'2026-10-06 13:30:54');
INSERT INTO "products" VALUES(220,'Amlodipine','4800301902333',21,'Medical',3.0,100,NULL,'2026-10-06 13:31:53');
INSERT INTO "products" VALUES(221,'Ascorbic Acid + Zinc Myverit C Plus','4806523303736',21,'Medical',4.0,100,NULL,'2026-10-06 13:32:39');
INSERT INTO "products" VALUES(222,'Amoxicilin Axmel','4806523301312',21,'Medical',5.0,100,NULL,'2026-10-06 13:33:02');
INSERT INTO "products" VALUES(223,'Atorvastatin Atorbet','8904180810799',21,'Medical',5.0,200,NULL,'2026-10-06 13:33:28');
INSERT INTO "products" VALUES(224,'Atorvastatin Astat','4806525870311',21,'Medical',5.0,100,NULL,'2026-10-06 13:34:07');
INSERT INTO "products" VALUES(225,'Atorvastatin Calcium Florvast 80','4806524781007',21,'Medical',10.0,100,NULL,'2026-10-06 13:35:10');
INSERT INTO "products" VALUES(226,'Ambroxol','4806529431112',21,'Medical',8.0,100,NULL,'2026-10-06 13:35:39');
INSERT INTO "products" VALUES(227,'Multivitamins Vitamin B1 + B6 + B12','4809015348017',21,'Medical',3.0,100,NULL,'2026-10-06 13:36:33');
INSERT INTO "products" VALUES(228,'Colchicine','4806032400643',21,'Medical',5.0,100,NULL,'2026-10-06 13:36:56');
INSERT INTO "products" VALUES(229,'Betahistine Hydrochloride','8906045605038',21,'Medical',20.0,100,NULL,'2026-10-06 13:37:27');
INSERT INTO "products" VALUES(230,'Celecoxib Emicox','4806037101361',21,'Medical',15.0,200,NULL,'2026-10-06 13:37:54');
INSERT INTO "products" VALUES(231,'Catrimoxamozole Kathrex','4806523302067',21,'Medical',5.0,100,NULL,'2026-10-06 13:38:29');
INSERT INTO "products" VALUES(232,'Cefalexin Exel','4806523301893',21,'Medical',7.0,100,NULL,'2026-10-06 13:39:02');
INSERT INTO "products" VALUES(233,'Carvedilol','8906043325471',21,'Medical',10.0,100,NULL,'2026-10-06 13:39:22');
INSERT INTO "products" VALUES(234,'Celecoxib','8904182011910',21,'Medical',10.0,100,NULL,'2026-10-06 13:39:54');
INSERT INTO "products" VALUES(235,'Calcium Ambical','4806524148015',21,'Medical',3.0,100,NULL,'2026-10-06 13:40:17');
INSERT INTO "products" VALUES(236,'Clonidine Hydrochloride Clodin','4806520352621',21,'Medical',8.0,300,NULL,'2026-10-06 13:40:49');
INSERT INTO "products" VALUES(237,'Clindamycin Clin-Gen','4806523303088',21,'Medical',10.0,100,NULL,'2026-10-06 13:41:31');
INSERT INTO "products" VALUES(238,'Betahistine Hydrochloride Betzine','8906045605038',21,'Medical',20.0,100,NULL,'2026-10-06 13:42:03');
INSERT INTO "products" VALUES(239,'Doxofylline Doxofar','4806530220781',21,'Medical',25.0,100,NULL,'2026-10-06 13:44:58');
INSERT INTO "products" VALUES(240,'Omeprazole','4806525870267',21,'Medical',8.0,100,NULL,'2026-10-06 13:45:27');
INSERT INTO "products" VALUES(241,'Glimepiride Glimegen','8904182012788',21,'Medical',3.0,100,NULL,'2026-10-06 13:46:03');
INSERT INTO "products" VALUES(242,'Paracetamol Flugard','4806505140199',21,'Medical',2.0,200,NULL,'2026-10-06 13:46:40');
INSERT INTO "products" VALUES(243,'MX3','4809013625004',21,'Medical',20.0,200,NULL,'2026-10-06 13:47:11');
INSERT INTO "products" VALUES(244,'Metformin Hydrochloride Formet','4806505142698',21,'Medical',8.0,200,NULL,'2026-10-06 13:47:48');
INSERT INTO "products" VALUES(245,'Febuxostat Febutor-40','4806514634450',21,'Medical',12.0,100,NULL,'2026-10-06 13:48:46');
INSERT INTO "products" VALUES(246,'Carrvedilol','8906043325471',21,'Medical',10.0,100,NULL,'2026-10-06 13:49:09');
INSERT INTO "products" VALUES(247,'Cinnarizine Cinzitab','8904172924374',21,'Medical',3.0,100,NULL,'2026-10-06 13:49:34');
INSERT INTO "products" VALUES(248,'Carbocisteine','4806524148022',21,'Medical',3.0,100,NULL,'2026-10-06 13:50:07');
INSERT INTO "products" VALUES(249,'Nitrofurantoin Harfurin','4800338470973',21,'Medical',6.0,100,NULL,'2026-10-06 13:50:34');
INSERT INTO "products" VALUES(250,'Diphenhydramine Hydrochloride Mucomed','4806520352171',21,'Medical',5.0,100,NULL,'2026-10-06 13:51:20');
INSERT INTO "products" VALUES(251,'ORS-5 Replacement Dehydrosol','4806508841376',21,'Medical',5.0,100,NULL,'2026-10-06 13:52:07');
INSERT INTO "products" VALUES(252,'Omephrazole','4806525176079',21,'Medical',5.0,100,NULL,'2026-10-06 13:52:31');
INSERT INTO "products" VALUES(253,'Symdex-D FORTE','4806502850015',21,'Medical',8.0,100,NULL,'2026-10-06 13:53:32');
INSERT INTO "products" VALUES(254,'Symdex-D','4806502850008',21,'Medical',5.0,97,NULL,'2026-10-06 13:53:54');
INSERT INTO "products" VALUES(255,'Ranitidine Ranitein','4806505140151',21,'Medical',10.0,100,NULL,'2026-10-06 13:54:21');
INSERT INTO "products" VALUES(256,'Clopidogrel Clopinova','4806539570245',21,'Medical',5.0,100,NULL,'2026-10-06 13:54:43');
INSERT INTO "products" VALUES(257,'Betahistine Hydrochloride BEVERT','4806539080416',21,'Medical',15.0,100,NULL,'2026-10-06 13:55:51');
INSERT INTO "products" VALUES(258,'Doxycycline Mydoxy','4806523303095',21,'Medical',5.0,100,NULL,'2026-10-06 13:56:23');
INSERT INTO "products" VALUES(259,'Carvedilol Karvidol','4806505140724',21,'Medical',8.0,100,NULL,'2026-10-06 13:56:47');
INSERT INTO "products" VALUES(260,'Carvedilol Karvidol','4806505140724',21,'Medical',8.0,100,NULL,'2026-10-06 14:02:03');
INSERT INTO "products" VALUES(261,'Erythromycin monphevin','4806529430283',21,'Medical',8.0,100,NULL,'2026-10-06 14:02:57');
INSERT INTO "products" VALUES(262,'Rosuvastatin Rosulip-10','8904180808949',21,'Medical',6.0,200,NULL,'2026-10-06 14:03:28');
INSERT INTO "products" VALUES(263,'Irbesartan Irbenov-150','8901463194393',21,'Medical',10.0,100,NULL,'2026-10-06 14:03:55');
INSERT INTO "products" VALUES(264,'Salbutamol Beisol','4809015348000',21,'Medical',2.0,100,NULL,'2026-10-06 14:04:16');
INSERT INTO "products" VALUES(265,'Glimepiride Diabeats','4806503121343',21,'Medical',5.0,100,NULL,'2026-10-06 14:04:44');
INSERT INTO "products" VALUES(266,'Prednisone Corticosteroid','4806032401336',21,'Medical',3.0,100,NULL,'2026-10-06 14:05:07');
INSERT INTO "products" VALUES(267,'Folic Acid Prevena','4806508841505',21,'Medical',5.0,100,NULL,'2026-10-06 14:05:30');
INSERT INTO "products" VALUES(268,'Furosemide Diubetic','4806520351099',21,'Medical',3.0,100,NULL,'2026-10-06 14:06:00');
INSERT INTO "products" VALUES(269,'Losartan Potassium Natrasol ','4806505142810',21,'Medical',5.0,100,NULL,'2026-10-06 14:06:33');
INSERT INTO "products" VALUES(270,'Rosuvastatin Calcium Arvast 20','8903836003547',21,'Medical',10.0,100,NULL,'2026-10-06 14:07:23');
INSERT INTO "products" VALUES(271,'Metronidazole Flagex','4806523302241',21,'Medical',5.0,100,NULL,'2026-10-06 14:07:54');
INSERT INTO "products" VALUES(272,'Pioglitazone Hydrochloride GLITO 30','8901140112573',21,'Medical',12.0,150,NULL,'2026-10-06 14:08:38');
INSERT INTO "products" VALUES(273,'Ranitidine Ranitein','4806505140144',21,'Medical',5.0,100,NULL,'2026-10-06 14:08:59');
INSERT INTO "products" VALUES(274,'Losatan Pottassium NATRASOL','4806505140687',21,'Medical',6.0,100,NULL,'2026-10-06 14:09:28');
INSERT INTO "products" VALUES(275,'Trimetazidine Dihydrochloride TRIMESAPH-35','8906043325402',21,'Medical',6.0,100,NULL,'2026-10-06 14:10:20');
INSERT INTO "products" VALUES(276,'Clindamycin Clin-Gen','4806523303088',21,'Medical',10.0,100,NULL,'2026-10-06 14:10:53');
INSERT INTO "products" VALUES(277,'Happy Baby Pants XXL ','4802288816122',22,'Non-Medical',15.0,48,'2029-12-02','2026-10-06 14:12:14');
INSERT INTO "products" VALUES(278,'EQ Pants L','4800488960737',22,'Non-Medical',10.0,80,'2028-08-18','2026-10-06 14:13:11');
INSERT INTO "products" VALUES(279,'Happy Baby Pants XL','4802288814128',22,'Non-Medical',12.0,48,'2028-09-10','2026-10-06 14:14:20');
INSERT INTO "products" VALUES(280,'EQ Pants M','4800488960324',22,'Non-Medical',10.0,48,'2028-02-12','2026-10-06 14:15:08');
INSERT INTO "products" VALUES(281,'Happy Baby Pants XXL','4802288815125',22,'Non-Medical',12.0,35,'2028-02-12','2026-10-06 14:16:16');
INSERT INTO "products" VALUES(282,'EQ Dry L','4800488958963',22,'Non-Medical',12.0,32,'2028-12-12','2026-10-06 14:17:00');
INSERT INTO "products" VALUES(283,'EQ Dry XL','4800488958994',22,'Non-Medical',15.0,19,'2029-02-12','2026-10-06 14:17:36');
INSERT INTO "products" VALUES(284,'EQ Dry XXL','4800488958819',22,'Non-Medical',50.0,20,'2028-02-10','2026-10-06 14:18:35');
INSERT INTO "products" VALUES(285,'EQ Plus+ Economy & Quality','4800488959809',22,'Non-Medical',13.5,30,'2028-02-12','2026-10-06 14:19:46');
INSERT INTO "products" VALUES(286,'EQ Pants XXXL','4800488961376',22,'Non-Medical',15.0,40,'2028-01-12','2026-10-06 14:20:22');
INSERT INTO "products" VALUES(287,'EQ Pants XXL','4800488960355',22,'Non-Medical',12.0,37,'2027-02-11','2026-10-06 14:21:05');
INSERT INTO "products" VALUES(288,'EQ Pants XL','4800488960348',22,'Non-Medical',12.0,48,NULL,'2026-10-06 14:21:54');
INSERT INTO "products" VALUES(289,'Coke 355ml','4801981106004',22,'Non-Medical',20.0,100,NULL,'2026-10-06 14:23:35');
INSERT INTO "products" VALUES(290,'Chipd Delight','4800552888066',22,'Non-Medical',14.0,17,NULL,'2026-10-06 14:26:37');
INSERT INTO "products" VALUES(291,'Energen','8996001440124',22,'Non-Medical',10.0,30,NULL,'2026-10-06 14:30:27');
INSERT INTO "products" VALUES(292,'Kinck Knocks','4806517040388',22,'Non-Medical',10.0,40,NULL,'2026-10-06 14:30:59');
INSERT INTO "products" VALUES(293,'kokokruch','4800361328463',22,'Non-Medical',10.0,40,NULL,'2026-10-06 14:31:38');
INSERT INTO "products" VALUES(294,'Star Margarine 100g','48037433',22,'Non-Medical',40.0,20,NULL,'2026-10-06 14:33:02');
INSERT INTO "products" VALUES(295,'Payless Extra Big Xtra Hot','4800016556807',22,'Non-Medical',22.0,20,NULL,'2026-10-06 14:34:49');
INSERT INTO "products" VALUES(296,'Ho - mi Beef','4800110026497',22,'Non-Medical',11.0,20,NULL,'2026-10-06 14:35:42');
INSERT INTO "products" VALUES(297,'Ho - mi Chicken','4800110025995',22,'Non-Medical',11.0,20,NULL,'2026-10-06 14:36:35');
INSERT INTO "products" VALUES(298,'pilot','4902505166457',22,'Non-Medical',50.0,20,NULL,'2026-10-13 13:46:03');
INSERT INTO "products" VALUES(299,'MIGHTY','00000',22,'Non-Medical',10.0,9,NULL,'2026-10-14 13:31:47');
INSERT INTO "products" VALUES(300,'CAMEL','00000',22,'Non-Medical',11.0,1,NULL,'2026-10-14 13:32:08');
INSERT INTO "products" VALUES(301,'MARLBORO RED','00000',22,'Non-Medical',11.0,20,NULL,'2026-10-14 13:32:31');
INSERT INTO "products" VALUES(302,'MARLBORO BLUE','00000',22,'Non-Medical',11.0,16,NULL,'2026-10-14 13:32:51');
INSERT INTO "products" VALUES(303,'CHESTER RED','00000',22,'Non-Medical',9.0,0,NULL,'2026-10-14 13:33:24');
INSERT INTO "products" VALUES(304,'FUDGEE BAR','00000',22,'Non-Medical',10.0,19,NULL,'2026-10-14 13:39:14');
INSERT INTO "products" VALUES(305,'BIOGESIC','00000',21,'Medical',7.0,44,NULL,'2026-10-14 14:02:54');
INSERT INTO "products" VALUES(306,'VITAMILK','00000',22,'Non-Medical',37.0,9,NULL,'2026-10-14 14:05:13');
INSERT INTO "products" VALUES(307,'GEL','00000',22,'Non-Medical',5.0,9,NULL,'2026-10-15 13:54:41');
INSERT INTO "products" VALUES(308,'PRITONG BANGUS','00000',22,'Non-Medical',10.0,19,NULL,'2026-10-15 13:58:58');
INSERT INTO "products" VALUES(309,'OREO','00000',22,'Non-Medical',10.0,8,NULL,'2026-10-15 14:02:20');
INSERT INTO "products" VALUES(310,'WAFER','00000',22,'Non-Medical',4.0,9,NULL,'2026-10-15 14:42:09');
INSERT INTO "products" VALUES(311,'PIATTOS,NOVA,VCUT','00000',22,'Non-Medical',20.0,27,NULL,'2026-10-15 15:30:02');
INSERT INTO "products" VALUES(312,'PLASTIC 4X12','00000',22,'Non-Medical',30.0,19,NULL,'2026-10-16 10:29:57');
INSERT INTO "products" VALUES(313,'Choc-o SMALL','00000',22,'Non-Medical',15.0,20,NULL,'2026-10-16 10:30:37');
INSERT INTO "products" VALUES(314,'ASSORTED','00000',22,'Non-Medical',0.0,0,NULL,'2026-10-16 10:31:10');
INSERT INTO "products" VALUES(315,'Bombay,Ahos,Kamatis','00000',22,'Non-Medical',10.0,18,NULL,'2026-10-16 10:40:53');
INSERT INTO "products" VALUES(316,'Knorr (chicken,pork,shrimp,beef)','00000',22,'Non-Medical',8.0,59,NULL,'2026-10-16 11:10:40');
INSERT INTO "products" VALUES(317,'DATU PUTI (VINEGAR)','00000',22,'Non-Medical',12.0,17,NULL,'2026-10-16 17:10:02');
INSERT INTO "products" VALUES(318,'CANDY','00000',22,'Non-Medical',5.0,98,NULL,'2026-10-20 13:58:59');
INSERT INTO "products" VALUES(319,'NATURE SPRING DISTILLED (10ltr)','00000',22,'Non-Medical',115.0,9,NULL,'2026-10-20 14:00:48');
INSERT INTO "products" VALUES(320,'NATURE SPRING (10ltr)','00000',22,'Non-Medical',105.0,9,NULL,'2026-10-20 14:01:32');
INSERT INTO "products" VALUES(321,'Chocolait (Magnolia)','00000',22,'Non-Medical',30.0,5,NULL,'2026-10-20 14:03:43');
INSERT INTO "products" VALUES(322,'LOPERAMIDE','00000',22,'Non-Medical',3.0,4,NULL,'2026-10-20 15:56:42');
INSERT INTO "products" VALUES(323,'WIPES','00000',22,'Non-Medical',35.0,4,NULL,'2026-10-23 14:02:44');
DROP TABLE IF EXISTS sale_items;
CREATE TABLE sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
INSERT INTO "sale_items" VALUES(7,9,57,1,5.0);
INSERT INTO "sale_items" VALUES(8,10,57,1,5.0);
INSERT INTO "sale_items" VALUES(9,11,57,10,5.0);
INSERT INTO "sale_items" VALUES(10,12,41,1,12.0);
INSERT INTO "sale_items" VALUES(11,13,41,1,12.0);
INSERT INTO "sale_items" VALUES(12,14,41,8,12.0);
INSERT INTO "sale_items" VALUES(13,15,57,1,5.0);
INSERT INTO "sale_items" VALUES(14,16,195,1,25.0);
INSERT INTO "sale_items" VALUES(15,17,156,1,30.0);
INSERT INTO "sale_items" VALUES(16,18,69,1,23.0);
INSERT INTO "sale_items" VALUES(17,19,50,1,10.0);
INSERT INTO "sale_items" VALUES(18,19,101,1,8.0);
INSERT INTO "sale_items" VALUES(19,20,50,1,10.0);
INSERT INTO "sale_items" VALUES(20,20,101,1,8.0);
INSERT INTO "sale_items" VALUES(21,21,50,1,10.0);
INSERT INTO "sale_items" VALUES(22,21,101,1,8.0);
INSERT INTO "sale_items" VALUES(23,22,169,1,63.0);
INSERT INTO "sale_items" VALUES(24,23,113,1,14.0);
INSERT INTO "sale_items" VALUES(25,24,57,1,5.0);
INSERT INTO "sale_items" VALUES(26,25,290,1,14.0);
INSERT INTO "sale_items" VALUES(27,25,41,1,12.0);
INSERT INTO "sale_items" VALUES(28,26,176,1,33.0);
INSERT INTO "sale_items" VALUES(29,27,176,1,33.0);
INSERT INTO "sale_items" VALUES(30,28,176,1,33.0);
INSERT INTO "sale_items" VALUES(31,29,39,3,15.0);
INSERT INTO "sale_items" VALUES(32,30,39,3,15.0);
INSERT INTO "sale_items" VALUES(33,31,298,4,50.0);
INSERT INTO "sale_items" VALUES(34,32,298,2,50.0);
INSERT INTO "sale_items" VALUES(35,33,298,4,50.0);
INSERT INTO "sale_items" VALUES(36,34,298,5,50.0);
INSERT INTO "sale_items" VALUES(37,35,298,2,50.0);
INSERT INTO "sale_items" VALUES(38,36,298,1,50.0);
INSERT INTO "sale_items" VALUES(39,37,57,1,5.0);
INSERT INTO "sale_items" VALUES(40,38,299,3,10.0);
INSERT INTO "sale_items" VALUES(41,39,187,2,55.0);
INSERT INTO "sale_items" VALUES(42,40,214,1,15.0);
INSERT INTO "sale_items" VALUES(43,41,207,1,20.0);
INSERT INTO "sale_items" VALUES(44,41,304,1,10.0);
INSERT INTO "sale_items" VALUES(45,42,73,1,5.0);
INSERT INTO "sale_items" VALUES(46,43,300,2,11.0);
INSERT INTO "sale_items" VALUES(47,44,94,1,18.0);
INSERT INTO "sale_items" VALUES(48,45,54,1,11.0);
INSERT INTO "sale_items" VALUES(49,46,299,1,10.0);
INSERT INTO "sale_items" VALUES(50,47,94,1,18.0);
INSERT INTO "sale_items" VALUES(51,47,120,2,9.0);
INSERT INTO "sale_items" VALUES(52,48,94,1,18.0);
INSERT INTO "sale_items" VALUES(53,48,120,2,9.0);
INSERT INTO "sale_items" VALUES(54,49,305,1,7.0);
INSERT INTO "sale_items" VALUES(55,50,306,1,37.0);
INSERT INTO "sale_items" VALUES(56,51,254,3,5.0);
INSERT INTO "sale_items" VALUES(57,52,198,3,27.0);
INSERT INTO "sale_items" VALUES(58,53,215,1,10.0);
INSERT INTO "sale_items" VALUES(59,54,289,1,20.0);
INSERT INTO "sale_items" VALUES(60,55,302,1,11.0);
INSERT INTO "sale_items" VALUES(61,56,300,1,11.0);
INSERT INTO "sale_items" VALUES(62,56,209,1,22.0);
INSERT INTO "sale_items" VALUES(63,57,195,1,25.0);
INSERT INTO "sale_items" VALUES(64,58,299,1,10.0);
INSERT INTO "sale_items" VALUES(65,59,303,20,9.0);
INSERT INTO "sale_items" VALUES(66,60,198,1,27.0);
INSERT INTO "sale_items" VALUES(67,61,300,1,11.0);
INSERT INTO "sale_items" VALUES(68,61,124,1,9.0);
INSERT INTO "sale_items" VALUES(69,62,209,1,22.0);
INSERT INTO "sale_items" VALUES(70,63,121,1,9.0);
INSERT INTO "sale_items" VALUES(71,64,299,2,10.0);
INSERT INTO "sale_items" VALUES(72,65,300,2,11.0);
INSERT INTO "sale_items" VALUES(73,66,71,1,7.0);
INSERT INTO "sale_items" VALUES(74,67,198,1,27.0);
INSERT INTO "sale_items" VALUES(75,68,201,1,12.0);
INSERT INTO "sale_items" VALUES(76,69,196,2,13.0);
INSERT INTO "sale_items" VALUES(77,70,196,2,13.0);
INSERT INTO "sale_items" VALUES(78,71,307,1,5.0);
INSERT INTO "sale_items" VALUES(79,71,204,1,12.0);
INSERT INTO "sale_items" VALUES(80,72,305,5,7.0);
INSERT INTO "sale_items" VALUES(81,73,289,3,20.0);
INSERT INTO "sale_items" VALUES(82,74,300,1,11.0);
INSERT INTO "sale_items" VALUES(83,75,195,1,25.0);
INSERT INTO "sale_items" VALUES(84,76,308,1,10.0);
INSERT INTO "sale_items" VALUES(85,77,290,1,14.0);
INSERT INTO "sale_items" VALUES(86,78,93,2,18.0);
INSERT INTO "sale_items" VALUES(87,79,201,1,12.0);
INSERT INTO "sale_items" VALUES(88,79,309,1,10.0);
INSERT INTO "sale_items" VALUES(89,80,67,2,22.0);
INSERT INTO "sale_items" VALUES(90,81,115,1,8.0);
INSERT INTO "sale_items" VALUES(91,81,118,1,7.0);
INSERT INTO "sale_items" VALUES(92,82,300,2,11.0);
INSERT INTO "sale_items" VALUES(93,83,310,1,4.0);
INSERT INTO "sale_items" VALUES(94,83,216,1,8.0);
INSERT INTO "sale_items" VALUES(95,84,215,1,10.0);
INSERT INTO "sale_items" VALUES(96,85,204,1,12.0);
INSERT INTO "sale_items" VALUES(97,86,289,2,20.0);
INSERT INTO "sale_items" VALUES(98,87,311,1,20.0);
INSERT INTO "sale_items" VALUES(99,88,158,1,27.0);
INSERT INTO "sale_items" VALUES(100,89,299,1,10.0);
INSERT INTO "sale_items" VALUES(101,90,41,1,12.0);
INSERT INTO "sale_items" VALUES(102,91,312,1,30.0);
INSERT INTO "sale_items" VALUES(103,92,313,2,15.0);
INSERT INTO "sale_items" VALUES(104,93,315,2,10.0);
INSERT INTO "sale_items" VALUES(105,93,77,1,8.0);
INSERT INTO "sale_items" VALUES(106,93,71,1,7.0);
INSERT INTO "sale_items" VALUES(107,94,198,2,27.0);
INSERT INTO "sale_items" VALUES(108,95,316,1,8.0);
INSERT INTO "sale_items" VALUES(109,96,289,3,20.0);
INSERT INTO "sale_items" VALUES(110,97,196,2,13.0);
INSERT INTO "sale_items" VALUES(111,98,300,1,11.0);
INSERT INTO "sale_items" VALUES(112,98,201,1,12.0);
INSERT INTO "sale_items" VALUES(113,99,97,5,18.0);
INSERT INTO "sale_items" VALUES(114,99,118,5,7.0);
INSERT INTO "sale_items" VALUES(115,100,215,1,10.0);
INSERT INTO "sale_items" VALUES(116,101,289,1,20.0);
INSERT INTO "sale_items" VALUES(117,102,216,1,8.0);
INSERT INTO "sale_items" VALUES(118,103,201,1,12.0);
INSERT INTO "sale_items" VALUES(119,103,300,1,11.0);
INSERT INTO "sale_items" VALUES(120,104,198,1,27.0);
INSERT INTO "sale_items" VALUES(121,105,214,1,15.0);
INSERT INTO "sale_items" VALUES(122,106,198,1,27.0);
INSERT INTO "sale_items" VALUES(123,107,289,1,20.0);
INSERT INTO "sale_items" VALUES(124,108,300,1,11.0);
INSERT INTO "sale_items" VALUES(125,109,212,1,35.0);
INSERT INTO "sale_items" VALUES(126,110,201,1,12.0);
INSERT INTO "sale_items" VALUES(127,111,317,1,12.0);
INSERT INTO "sale_items" VALUES(128,111,300,2,11.0);
INSERT INTO "sale_items" VALUES(129,112,309,1,10.0);
INSERT INTO "sale_items" VALUES(130,112,41,1,12.0);
INSERT INTO "sale_items" VALUES(131,112,195,1,25.0);
INSERT INTO "sale_items" VALUES(132,113,289,1,20.0);
INSERT INTO "sale_items" VALUES(133,114,196,3,13.0);
INSERT INTO "sale_items" VALUES(134,115,146,1,28.0);
INSERT INTO "sale_items" VALUES(135,116,195,1,25.0);
INSERT INTO "sale_items" VALUES(136,117,300,2,11.0);
INSERT INTO "sale_items" VALUES(137,118,289,1,20.0);
INSERT INTO "sale_items" VALUES(138,119,289,1,20.0);
INSERT INTO "sale_items" VALUES(139,120,196,3,13.0);
INSERT INTO "sale_items" VALUES(140,121,299,3,10.0);
INSERT INTO "sale_items" VALUES(141,122,300,1,11.0);
INSERT INTO "sale_items" VALUES(142,123,211,1,30.0);
INSERT INTO "sale_items" VALUES(143,123,214,1,15.0);
INSERT INTO "sale_items" VALUES(144,124,300,1,11.0);
INSERT INTO "sale_items" VALUES(145,125,201,1,12.0);
INSERT INTO "sale_items" VALUES(146,126,59,3,14.0);
INSERT INTO "sale_items" VALUES(147,126,215,1,10.0);
INSERT INTO "sale_items" VALUES(148,127,201,1,12.0);
INSERT INTO "sale_items" VALUES(149,128,125,1,9.0);
INSERT INTO "sale_items" VALUES(150,129,317,1,12.0);
INSERT INTO "sale_items" VALUES(151,130,209,1,22.0);
INSERT INTO "sale_items" VALUES(152,131,195,1,25.0);
INSERT INTO "sale_items" VALUES(153,132,300,1,11.0);
INSERT INTO "sale_items" VALUES(154,133,289,1,20.0);
INSERT INTO "sale_items" VALUES(155,134,214,1,15.0);
INSERT INTO "sale_items" VALUES(156,134,176,1,33.0);
INSERT INTO "sale_items" VALUES(157,135,318,2,5.0);
INSERT INTO "sale_items" VALUES(158,136,319,1,115.0);
INSERT INTO "sale_items" VALUES(159,137,321,1,30.0);
INSERT INTO "sale_items" VALUES(160,138,187,1,55.0);
INSERT INTO "sale_items" VALUES(161,139,109,1,9.0);
INSERT INTO "sale_items" VALUES(162,140,125,2,9.0);
INSERT INTO "sale_items" VALUES(163,140,116,2,7.0);
INSERT INTO "sale_items" VALUES(164,141,289,1,20.0);
INSERT INTO "sale_items" VALUES(165,142,302,1,11.0);
INSERT INTO "sale_items" VALUES(166,143,204,1,12.0);
INSERT INTO "sale_items" VALUES(167,144,311,1,20.0);
INSERT INTO "sale_items" VALUES(168,145,289,2,20.0);
INSERT INTO "sale_items" VALUES(169,146,66,2,22.0);
INSERT INTO "sale_items" VALUES(170,147,322,6,3.0);
INSERT INTO "sale_items" VALUES(171,148,195,1,25.0);
INSERT INTO "sale_items" VALUES(172,149,90,2,10.0);
INSERT INTO "sale_items" VALUES(173,150,289,1,20.0);
INSERT INTO "sale_items" VALUES(174,151,209,1,22.0);
INSERT INTO "sale_items" VALUES(175,152,109,2,9.0);
INSERT INTO "sale_items" VALUES(176,153,323,1,35.0);
INSERT INTO "sale_items" VALUES(177,154,104,2,8.0);
INSERT INTO "sale_items" VALUES(178,155,320,1,105.0);
INSERT INTO "sale_items" VALUES(179,156,209,1,22.0);
INSERT INTO "sale_items" VALUES(180,157,39,2,15.0);
INSERT INTO "sale_items" VALUES(181,158,290,1,14.0);
INSERT INTO "sale_items" VALUES(182,159,321,2,30.0);
INSERT INTO "sale_items" VALUES(183,160,313,2,15.0);
INSERT INTO "sale_items" VALUES(184,161,39,1,15.0);
INSERT INTO "sale_items" VALUES(185,162,289,1,20.0);
INSERT INTO "sale_items" VALUES(186,163,187,1,55.0);
INSERT INTO "sale_items" VALUES(187,164,302,2,11.0);
INSERT INTO "sale_items" VALUES(188,165,311,1,20.0);
INSERT INTO "sale_items" VALUES(189,166,215,1,10.0);
INSERT INTO "sale_items" VALUES(190,167,39,1,15.0);
INSERT INTO "sale_items" VALUES(191,168,70,3,6.0);
INSERT INTO "sale_items" VALUES(192,169,317,1,12.0);
INSERT INTO "sale_items" VALUES(193,170,49,1,10.0);
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number VARCHAR(50) UNIQUE NOT NULL,
            cashier_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            sale_status VARCHAR(20) DEFAULT 'Completed',
            product_type VARCHAR(20) DEFAULT 'medical',
            sale_date TEXT DEFAULT (datetime('now', 'localtime')),
            receipt_printed INTEGER DEFAULT 0,
            printed_at TEXT NULL DEFAULT NULL,
            voided_at TEXT NULL DEFAULT NULL,
            voided_by INTEGER NULL DEFAULT NULL,
            void_reason TEXT NULL DEFAULT NULL,
            refunded_at TEXT NULL DEFAULT NULL,
            refunded_by INTEGER NULL DEFAULT NULL,
            refund_reason TEXT NULL DEFAULT NULL,
            original_sale_id INTEGER NULL DEFAULT NULL,
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id)
        );
INSERT INTO "sales" VALUES(3,'REC-001',1,15.0,'Voided','Medical','2026-09-09 11:55:23',0,NULL,'2026-09-09 18:40:01',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(4,'REC-002',1,25.0,'Voided','Non-Medical','2026-09-09 11:55:23',0,NULL,'2026-09-09 18:39:53',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(5,'REC-20260909-4226',1,12.0,'Refunded','Medical','2026-09-09 18:01:59',1,'2026-09-09 18:02:10',NULL,NULL,NULL,'2026-09-09 18:24:42',1,'refund',NULL);
INSERT INTO "sales" VALUES(6,'REC-20260909-4088',1,12.0,'Pending','Medical','2026-09-09 18:02:27',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(7,'REC-20260909-4881',1,12.0,'Voided','Medical','2026-09-09 18:13:11',1,'2026-09-09 18:13:13','2026-09-09 18:24:29',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(8,'REC-20260909-5574',1,12.0,'Voided','Medical','2026-09-09 18:25:06',1,'2026-09-09 18:25:08','2026-09-09 21:22:08',1,'void',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(9,'REC-20260911-1874',1,5.0,'Voided','Non-Medical','2026-09-11 12:45:16',1,'2026-09-11 12:45:20','2026-09-11 12:45:35',1,'void',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(10,'REC-20260911-2846',1,5.0,'Pending','Non-Medical','2026-09-11 12:46:33',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(11,'REC-20260911-6039',1,50.0,'Completed','Non-Medical','2026-09-11 15:48:18',1,'2026-09-11 15:48:23',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(12,'REC-20260911-5272',1,12.0,'Pending','Non-Medical','2026-09-11 15:49:14',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(13,'REC-20260911-4119',1,12.0,'Pending','Non-Medical','2026-09-11 15:49:30',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(14,'REC-20260911-4224',1,96.0,'Voided','Non-Medical','2026-09-11 16:41:19',1,'2026-09-11 16:41:21','2026-09-11 16:41:37',1,'void',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(15,'REC-20260919-6243',1,5.0,'Completed','Non-Medical','2026-09-19 09:21:26',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(16,'REC-20260919-9378',1,25.0,'Completed','Non-Medical','2026-09-19 14:20:42',1,'2026-09-19 14:20:44',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(17,'REC-20260919-6516',1,30.0,'Completed','Non-Medical','2026-09-19 14:26:57',1,'2026-09-19 14:26:59',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(18,'REC-20261002-2008',1,23.0,'Completed','Non-Medical','2026-10-02 13:53:25',1,'2026-10-02 13:53:27',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(19,'REC-20261002-2274',1,18.0,'Completed','Non-Medical','2026-10-02 13:54:10',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(20,'REC-20261002-8558',1,18.0,'Completed','Non-Medical','2026-10-02 13:54:19',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(21,'REC-20261002-3338',1,18.0,'Completed','Non-Medical','2026-10-02 13:55:43',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(22,'REC-20261002-8739',1,63.0,'Completed','Non-Medical','2026-10-02 23:32:41',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(23,'REC-20261006-5623',1,14.0,'Completed','Non-Medical','2026-10-06 13:07:36',1,'2026-10-06 13:07:53',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(24,'REC-20261006-8110',1,5.0,'Completed','Non-Medical','2026-10-06 13:27:06',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(25,'REC-20261006-3911',1,26.0,'Completed','Non-Medical','2026-10-06 14:27:17',1,'2026-10-06 14:27:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(26,'REC-20261006-1254',1,33.0,'Completed','Non-Medical','2026-10-06 14:27:36',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(27,'REC-20261006-2939',1,33.0,'Completed','Non-Medical','2026-10-06 14:28:51',1,'2026-10-06 14:28:52',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(28,'REC-20261006-6237',1,33.0,'Completed','Non-Medical','2026-10-06 14:37:59',1,'2026-10-06 14:38:01',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(29,'REC-20261006-9080',1,45.0,'Completed','Non-Medical','2026-10-06 14:38:36',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(30,'REC-20261006-1998',1,45.0,'Completed','Non-Medical','2026-10-06 14:40:15',1,'2026-10-06 14:40:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(31,'REC-20261013-1947',1,200.0,'Voided','Non-Medical','2026-10-13 13:46:51',1,'2026-10-13 13:46:52','2026-10-13 13:48:22',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(32,'REC-20261013-8559',1,100.0,'Voided','Non-Medical','2026-10-13 13:47:13',1,'2026-10-13 13:47:15','2026-10-13 13:48:17',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(33,'REC-20261013-6709',1,200.0,'Voided','Non-Medical','2026-10-13 13:47:38',1,'2026-10-13 13:47:39','2026-10-13 13:48:08',1,'asdgf',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(34,'REC-20261013-7194',1,250.0,'Voided','Non-Medical','2026-10-13 14:35:50',1,'2026-10-13 14:35:51','2026-10-13 14:36:54',1,'viod',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(35,'REC-20261013-2139',1,100.0,'Voided','Non-Medical','2026-10-13 17:14:49',1,'2026-10-13 17:14:53','2026-10-13 17:42:49',1,'asdad',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(36,'REC-20261013-6914',1,50.0,'Voided','Non-Medical','2026-10-13 17:15:05',1,'2026-10-13 17:15:07','2026-10-13 17:42:44',1,'asd',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(37,'REC-20261013-4728',1,5.0,'Voided','Non-Medical','2026-10-13 17:51:44',1,'2026-10-13 17:51:47','2026-10-13 17:52:21',1,'dcdgcc',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(38,'REC-20261014-8543',1,30.0,'Completed','Non-Medical','2026-10-14 13:35:24',1,'2026-10-14 13:35:26',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(39,'REC-20261014-8015',1,110.0,'Completed','Non-Medical','2026-10-14 13:36:11',1,'2026-10-14 13:36:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(40,'REC-20261014-2842',1,15.0,'Completed','Non-Medical','2026-10-14 13:36:41',1,'2026-10-14 13:36:42',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(41,'REC-20261014-4136',1,30.0,'Completed','Non-Medical','2026-10-14 13:40:19',1,'2026-10-14 13:40:20',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(42,'REC-20261014-9575',1,5.0,'Completed','Non-Medical','2026-10-14 13:41:57',1,'2026-10-14 13:41:58',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(43,'REC-20261014-8041',1,22.0,'Completed','Non-Medical','2026-10-14 13:42:35',1,'2026-10-14 13:42:37',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(44,'REC-20261014-2005',1,18.0,'Completed','Non-Medical','2026-10-14 13:43:06',1,'2026-10-14 13:43:08',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(45,'REC-20261014-2303',1,11.0,'Completed','Non-Medical','2026-10-14 13:43:33',1,'2026-10-14 13:43:35',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(46,'REC-20261014-1959',1,10.0,'Completed','Non-Medical','2026-10-14 13:43:57',1,'2026-10-14 13:43:59',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(47,'REC-20261014-3094',1,36.0,'Completed','Non-Medical','2026-10-14 13:45:06',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(48,'REC-20261014-6690',1,36.0,'Completed','Non-Medical','2026-10-14 13:45:20',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(49,'REC-20261014-9343',1,7.0,'Completed','Medical','2026-10-14 14:03:38',1,'2026-10-14 14:03:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(50,'REC-20261014-9439',1,37.0,'Completed','Non-Medical','2026-10-14 14:07:06',1,'2026-10-14 14:07:08',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(51,'REC-20261014-9693',1,15.0,'Completed','Medical','2026-10-14 14:07:22',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(52,'REC-20261014-1396',1,81.0,'Completed','Non-Medical','2026-10-14 14:07:47',1,'2026-10-14 14:07:49',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(53,'REC-20261014-4000',1,10.0,'Completed','Non-Medical','2026-10-14 14:08:25',1,'2026-10-14 14:08:27',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(54,'REC-20261014-1049',1,20.0,'Completed','Non-Medical','2026-10-14 14:08:46',1,'2026-10-14 14:08:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(55,'REC-20261014-9735',1,11.0,'Completed','Non-Medical','2026-10-14 14:09:17',1,'2026-10-14 14:09:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(56,'REC-20261014-4503',1,33.0,'Completed','Non-Medical','2026-10-14 14:09:48',1,'2026-10-14 14:10:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(57,'REC-20261014-7517',1,25.0,'Completed','Non-Medical','2026-10-14 14:34:25',1,'2026-10-14 14:34:26',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(58,'REC-20261014-7110',1,10.0,'Completed','Non-Medical','2026-10-14 15:14:31',1,'2026-10-14 15:14:33',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(59,'REC-20261014-7940',1,180.0,'Completed','Non-Medical','2026-10-14 15:15:04',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(60,'REC-20261014-2264',1,27.0,'Completed','Non-Medical','2026-10-14 16:17:18',1,'2026-10-14 16:17:19',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(61,'REC-20261014-7908',1,20.0,'Completed','Non-Medical','2026-10-14 16:17:52',1,'2026-10-14 16:17:56',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(62,'REC-20261014-3810',1,22.0,'Completed','Non-Medical','2026-10-14 16:28:19',1,'2026-10-14 16:28:20',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(63,'REC-20261015-7081',1,9.0,'Voided','Non-Medical','2026-10-15 00:06:56',1,'2026-10-15 00:07:30','2026-10-15 00:09:13',1,'Customer changes his/her mind.',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(64,'REC-20261015-4977',1,20.0,'Completed','Non-Medical','2026-10-15 13:48:31',1,'2026-10-15 13:48:33',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(65,'REC-20261015-8937',1,22.0,'Completed','Non-Medical','2026-10-15 13:49:07',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(66,'REC-20261015-5361',1,7.0,'Completed','Non-Medical','2026-10-15 13:49:35',1,'2026-10-15 13:49:36',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(67,'REC-20261015-6045',1,27.0,'Completed','Non-Medical','2026-10-15 13:49:57',1,'2026-10-15 13:49:59',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(68,'REC-20261015-3426',1,12.0,'Completed','Non-Medical','2026-10-15 13:50:27',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(69,'REC-20261015-5369',1,26.0,'Completed','Non-Medical','2026-10-15 13:53:16',1,'2026-10-15 13:53:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(70,'REC-20261015-3968',1,26.0,'Completed','Non-Medical','2026-10-15 13:53:34',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(71,'REC-20261015-1474',1,17.0,'Completed','Non-Medical','2026-10-15 13:55:39',1,'2026-10-15 13:55:40',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(72,'REC-20261015-7041',1,35.0,'Completed','Medical','2026-10-15 13:56:26',1,'2026-10-15 13:56:27',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(73,'REC-20261015-5333',1,60.0,'Completed','Non-Medical','2026-10-15 13:56:53',1,'2026-10-15 13:56:54',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(74,'REC-20261015-7288',1,11.0,'Completed','Non-Medical','2026-10-15 13:57:20',1,'2026-10-15 13:57:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(75,'REC-20261015-5359',1,25.0,'Completed','Non-Medical','2026-10-15 13:57:46',1,'2026-10-15 13:57:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(76,'REC-20261015-4314',1,10.0,'Completed','Non-Medical','2026-10-15 13:59:27',1,'2026-10-15 13:59:28',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(77,'REC-20261015-9526',1,14.0,'Completed','Non-Medical','2026-10-15 13:59:52',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(78,'REC-20261015-2893',1,36.0,'Completed','Non-Medical','2026-10-15 14:00:18',1,'2026-10-15 14:01:06',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(79,'REC-20261015-6258',1,22.0,'Completed','Non-Medical','2026-10-15 14:03:31',1,'2026-10-15 14:04:10',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(80,'REC-20261015-2958',1,44.0,'Completed','Non-Medical','2026-10-15 14:05:03',1,'2026-10-15 14:05:08',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(81,'REC-20261015-7385',1,15.0,'Completed','Non-Medical','2026-10-15 14:11:43',1,'2026-10-15 14:11:45',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(82,'REC-20261015-6796',1,22.0,'Completed','Non-Medical','2026-10-15 14:11:59',1,'2026-10-15 14:12:03',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(83,'REC-20261015-2995',1,12.0,'Completed','Non-Medical','2026-10-15 14:42:50',1,'2026-10-15 14:42:52',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(84,'REC-20261015-7293',1,10.0,'Completed','Non-Medical','2026-10-15 15:13:17',1,'2026-10-15 15:13:19',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(85,'REC-20261015-7107',1,12.0,'Completed','Non-Medical','2026-10-15 15:13:30',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(86,'REC-20261015-3063',1,40.0,'Completed','Non-Medical','2026-10-15 15:25:15',1,'2026-10-15 15:25:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(87,'REC-20261015-8664',1,20.0,'Completed','Non-Medical','2026-10-15 15:30:50',1,'2026-10-15 15:30:51',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(88,'REC-20261016-1370',1,27.0,'Voided','Non-Medical','2026-10-16 08:34:28',1,'2026-10-16 08:34:47','2026-10-16 08:35:44',1,'change of mind',NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(89,'REC-20261016-1045',1,10.0,'Completed','Non-Medical','2026-10-16 10:28:07',1,'2026-10-16 10:28:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(90,'REC-20261016-3156',1,12.0,'Completed','Non-Medical','2026-10-16 10:28:48',1,'2026-10-16 10:28:49',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(91,'REC-20261016-7801',1,30.0,'Completed','Non-Medical','2026-10-16 10:31:58',1,'2026-10-16 10:32:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(92,'REC-20261016-8437',1,30.0,'Completed','Non-Medical','2026-10-16 10:32:40',1,'2026-10-16 10:32:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(93,'REC-20261016-9409',1,35.0,'Completed','Non-Medical','2026-10-16 10:44:02',1,'2026-10-16 10:44:06',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(94,'REC-20261016-6130',1,54.0,'Completed','Non-Medical','2026-10-16 11:09:04',1,'2026-10-16 11:09:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(95,'REC-20261016-2570',1,8.0,'Completed','Non-Medical','2026-10-16 11:11:13',1,'2026-10-16 11:11:15',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(96,'REC-20261016-3074',1,60.0,'Completed','Non-Medical','2026-10-16 12:38:44',1,'2026-10-16 12:38:45',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(97,'REC-20261016-7181',1,26.0,'Completed','Non-Medical','2026-10-16 12:39:11',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(98,'REC-20261016-7339',1,23.0,'Completed','Non-Medical','2026-10-16 12:39:36',1,'2026-10-16 12:39:37',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(99,'REC-20261016-5575',1,125.0,'Completed','Non-Medical','2026-10-16 12:43:56',1,'2026-10-16 12:43:57',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(100,'REC-20261016-6085',1,10.0,'Completed','Non-Medical','2026-10-16 12:47:04',1,'2026-10-16 12:47:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(101,'REC-20261016-9281',1,20.0,'Completed','Non-Medical','2026-10-16 15:01:22',1,'2026-10-16 15:01:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(102,'REC-20261016-7998',1,8.0,'Completed','Non-Medical','2026-10-16 15:02:08',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(103,'REC-20261016-6659',1,23.0,'Completed','Non-Medical','2026-10-16 15:13:03',1,'2026-10-16 15:13:06',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(104,'REC-20261016-3534',1,27.0,'Completed','Non-Medical','2026-10-16 15:19:05',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(105,'REC-20261016-7113',1,15.0,'Completed','Non-Medical','2026-10-16 15:31:22',1,'2026-10-16 15:31:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(106,'REC-20261016-5103',1,27.0,'Completed','Non-Medical','2026-10-16 16:40:52',1,'2026-10-16 16:40:53',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(107,'REC-20261016-8109',1,20.0,'Completed','Non-Medical','2026-10-16 16:41:06',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(108,'REC-20261016-6958',1,11.0,'Completed','Non-Medical','2026-10-16 16:41:19',1,'2026-10-16 16:41:20',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(109,'REC-20261016-9145',1,35.0,'Completed','Non-Medical','2026-10-16 16:42:45',1,'2026-10-16 16:42:47',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(110,'REC-20261016-5387',1,12.0,'Completed','Non-Medical','2026-10-16 16:54:17',1,'2026-10-16 16:54:21',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(111,'REC-20261016-4648',1,34.0,'Completed','Non-Medical','2026-10-16 17:10:50',1,'2026-10-16 17:10:51',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(112,'REC-20261016-9399',1,47.0,'Completed','Non-Medical','2026-10-16 17:30:27',1,'2026-10-16 17:30:29',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(113,'REC-20261016-2198',1,20.0,'Completed','Non-Medical','2026-10-16 17:30:48',1,'2026-10-16 17:30:50',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(114,'REC-20261016-5038',1,39.0,'Completed','Non-Medical','2026-10-16 17:31:08',1,'2026-10-16 17:31:10',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(115,'REC-20261016-1498',1,28.0,'Completed','Non-Medical','2026-10-16 17:50:39',1,'2026-10-16 17:50:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(116,'REC-20261016-2543',1,25.0,'Completed','Non-Medical','2026-10-16 17:51:49',1,'2026-10-16 17:51:50',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(117,'REC-20261016-3325',1,22.0,'Completed','Non-Medical','2026-10-16 18:03:17',1,'2026-10-16 18:03:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(118,'REC-20261016-2854',1,20.0,'Completed','Non-Medical','2026-10-16 18:07:32',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(119,'REC-20261016-9697',1,20.0,'Completed','Non-Medical','2026-10-16 18:09:06',1,'2026-10-16 18:09:09',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(120,'REC-20261016-3636',1,39.0,'Completed','Non-Medical','2026-10-16 18:14:55',1,'2026-10-16 18:14:58',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(121,'REC-20261016-9479',1,30.0,'Completed','Non-Medical','2026-10-16 18:30:50',1,'2026-10-16 18:30:51',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(122,'REC-20261016-9142',1,11.0,'Completed','Non-Medical','2026-10-16 18:53:02',1,'2026-10-16 18:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(123,'REC-20261016-3606',1,45.0,'Completed','Non-Medical','2026-10-16 18:55:52',1,'2026-10-16 18:56:14',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(124,'REC-20261016-2805',1,11.0,'Completed','Non-Medical','2026-10-16 18:57:52',1,'2026-10-16 18:57:54',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(125,'REC-20261016-7707',1,12.0,'Completed','Non-Medical','2026-10-16 19:06:43',1,'2026-10-16 19:06:44',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(126,'REC-20261016-7282',1,52.0,'Completed','Non-Medical','2026-10-16 19:28:01',1,'2026-10-16 19:28:03',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(127,'REC-20261016-8098',1,12.0,'Completed','Non-Medical','2026-10-16 19:33:12',1,'2026-10-16 19:33:14',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(128,'REC-20261016-4878',1,9.0,'Completed','Non-Medical','2026-10-16 19:35:58',1,'2026-10-16 19:36:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(129,'REC-20261020-9139',1,12.0,'Completed','Non-Medical','2026-10-20 13:54:29',1,'2026-10-20 13:54:31',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(130,'REC-20261020-5773',1,22.0,'Completed','Non-Medical','2026-10-20 13:55:03',1,'2026-10-20 13:55:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(131,'REC-20261020-5340',1,25.0,'Completed','Non-Medical','2026-10-20 13:55:19',1,'2026-10-20 13:55:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(132,'REC-20261020-3283',1,11.0,'Completed','Non-Medical','2026-10-20 13:56:19',1,'2026-10-20 13:56:21',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(133,'REC-20261020-7425',1,20.0,'Completed','Non-Medical','2026-10-20 13:56:39',1,'2026-10-20 13:56:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(134,'REC-20261020-6533',1,48.0,'Completed','Non-Medical','2026-10-20 13:57:38',1,'2026-10-20 13:57:49',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(135,'REC-20261020-1784',1,10.0,'Completed','Non-Medical','2026-10-20 13:59:28',1,'2026-10-20 13:59:30',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(136,'REC-20261020-1257',1,115.0,'Completed','Non-Medical','2026-10-20 14:02:21',1,'2026-10-20 14:02:23',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(137,'REC-20261020-2937',1,30.0,'Completed','Non-Medical','2026-10-20 14:08:30',1,'2026-10-20 14:08:32',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(138,'REC-20261020-7533',1,55.0,'Completed','Non-Medical','2026-10-20 14:08:46',1,'2026-10-20 14:08:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(139,'REC-20261020-2080',1,9.0,'Completed','Non-Medical','2026-10-20 14:09:17',1,'2026-10-20 14:09:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(140,'REC-20261020-8346',1,32.0,'Completed','Non-Medical','2026-10-20 14:10:29',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(141,'REC-20261020-7338',1,20.0,'Completed','Non-Medical','2026-10-20 14:10:56',1,'2026-10-20 14:10:57',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(142,'REC-20261020-6515',1,11.0,'Completed','Non-Medical','2026-10-20 14:11:22',1,'2026-10-20 14:11:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(143,'REC-20261020-3885',1,12.0,'Completed','Non-Medical','2026-10-20 14:11:40',1,'2026-10-20 14:11:43',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(144,'REC-20261020-4974',1,20.0,'Completed','Non-Medical','2026-10-20 14:22:05',1,'2026-10-20 14:22:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(145,'REC-20261020-8330',1,40.0,'Completed','Non-Medical','2026-10-20 14:51:16',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(146,'REC-20261020-8834',1,44.0,'Completed','Non-Medical','2026-10-20 14:54:14',1,'2026-10-20 14:54:15',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(147,'REC-20261020-1022',1,18.0,'Completed','Non-Medical','2026-10-20 15:58:36',1,'2026-10-20 15:58:37',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(148,'REC-20261020-1045',1,25.0,'Completed','Non-Medical','2026-10-20 16:33:46',1,'2026-10-20 16:33:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(149,'REC-20261020-9737',1,20.0,'Completed','Non-Medical','2026-10-20 16:34:04',1,'2026-10-20 16:34:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(150,'REC-20261020-9452',1,20.0,'Completed','Non-Medical','2026-10-20 16:57:21',1,'2026-10-20 16:57:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(151,'REC-20261020-8841',1,22.0,'Completed','Non-Medical','2026-10-20 17:01:18',1,'2026-10-20 17:01:19',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(152,'REC-20261023-1780',1,18.0,'Completed','Non-Medical','2026-10-23 14:01:36',1,'2026-10-23 14:01:38',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(153,'REC-20261023-2173',1,35.0,'Completed','Non-Medical','2026-10-23 14:03:59',1,'2026-10-23 14:04:09',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(154,'REC-20261023-4484',1,16.0,'Completed','Non-Medical','2026-10-23 14:05:19',1,'2026-10-23 14:05:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(155,'REC-20261023-2770',1,105.0,'Completed','Non-Medical','2026-10-23 14:06:17',1,'2026-10-23 14:06:21',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(156,'REC-20261023-9413',1,22.0,'Completed','Non-Medical','2026-10-23 14:07:28',1,'2026-10-23 14:07:30',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(157,'REC-20261023-1616',1,30.0,'Completed','Medical','2026-10-23 14:08:29',1,'2026-10-23 14:08:31',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(158,'REC-20261023-1515',1,14.0,'Completed','Non-Medical','2026-10-23 14:09:10',1,'2026-10-23 14:09:12',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(159,'REC-20261023-6304',1,60.0,'Completed','Non-Medical','2026-10-23 14:09:59',1,'2026-10-23 14:10:01',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(160,'REC-20261023-6985',1,30.0,'Completed','Non-Medical','2026-10-23 14:11:06',1,'2026-10-23 14:11:08',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(161,'REC-20261023-9746',1,15.0,'Completed','Medical','2026-10-23 14:12:15',1,'2026-10-23 14:12:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(162,'REC-20261023-4841',1,20.0,'Completed','Non-Medical','2026-10-23 14:13:05',1,'2026-10-23 14:13:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(163,'REC-20261023-3299',1,55.0,'Completed','Non-Medical','2026-10-23 14:14:23',1,'2026-10-23 14:14:25',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(164,'REC-20261023-4689',1,22.0,'Completed','Non-Medical','2026-10-23 14:15:04',1,'2026-10-23 14:15:06',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(165,'REC-20261023-3636',1,20.0,'Completed','Non-Medical','2026-10-23 14:15:50',1,'2026-10-23 14:15:52',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(166,'REC-20261023-4718',1,10.0,'Completed','Non-Medical','2026-10-23 14:16:36',1,'2026-10-23 14:16:38',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(167,'REC-20261023-4857',1,15.0,'Completed','Medical','2026-10-23 14:17:50',1,'2026-10-23 14:17:58',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(168,'REC-20261023-2302',1,18.0,'Completed','Non-Medical','2026-10-23 14:18:29',1,'2026-10-23 14:18:32',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(169,'REC-20261023-1523',1,12.0,'Completed','Non-Medical','2026-10-23 14:19:06',1,'2026-10-23 14:19:08',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "sales" VALUES(170,'REC-20261023-9165',1,10.0,'Completed','Non-Medical','2026-10-23 14:20:16',1,'2026-10-23 14:20:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
DROP TABLE IF EXISTS stock_movements;
CREATE TABLE stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            movement_type VARCHAR(10) NOT NULL,
            quantity INTEGER NOT NULL,
            reason VARCHAR(100),
            movement_date TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );
INSERT INTO "stock_movements" VALUES(11,39,'IN',22,'Stock Addition','2026-09-10 14:03:45');
INSERT INTO "stock_movements" VALUES(13,41,'IN',10,'Stock Addition','2026-09-10 14:08:21');
INSERT INTO "stock_movements" VALUES(14,42,'IN',3,'Stock Addition','2026-09-10 14:10:18');
INSERT INTO "stock_movements" VALUES(15,43,'IN',2,'Stock Addition','2026-09-10 14:12:55');
INSERT INTO "stock_movements" VALUES(16,44,'IN',4,'Stock Addition','2026-09-10 14:16:04');
INSERT INTO "stock_movements" VALUES(17,45,'IN',4,'Stock Addition','2026-09-10 14:24:00');
INSERT INTO "stock_movements" VALUES(18,46,'IN',2,'Stock Addition','2026-09-10 14:32:41');
INSERT INTO "stock_movements" VALUES(19,47,'IN',7,'Stock Addition','2026-09-10 14:33:55');
INSERT INTO "stock_movements" VALUES(20,48,'IN',3,'Stock Addition','2026-09-10 14:36:25');
INSERT INTO "stock_movements" VALUES(21,49,'IN',21,'Stock Addition','2026-09-10 14:43:40');
INSERT INTO "stock_movements" VALUES(22,50,'IN',19,'Stock Addition','2026-09-10 14:45:35');
INSERT INTO "stock_movements" VALUES(23,51,'IN',7,'Stock Addition','2026-09-10 14:47:19');
INSERT INTO "stock_movements" VALUES(24,52,'IN',6,'Stock Addition','2026-09-10 14:48:52');
INSERT INTO "stock_movements" VALUES(25,53,'IN',8,'Stock Addition','2026-09-10 14:51:21');
INSERT INTO "stock_movements" VALUES(26,54,'IN',19,'Stock Addition','2026-09-10 14:54:24');
INSERT INTO "stock_movements" VALUES(27,55,'IN',2,'Stock Addition','2026-09-10 14:56:01');
INSERT INTO "stock_movements" VALUES(28,56,'IN',3,'Stock Addition','2026-09-10 14:56:58');
INSERT INTO "stock_movements" VALUES(29,57,'IN',49,'Stock Addition','2026-09-10 15:08:34');
INSERT INTO "stock_movements" VALUES(30,58,'IN',51,'Stock Addition','2026-09-10 15:11:51');
INSERT INTO "stock_movements" VALUES(31,59,'IN',13,'Stock Addition','2026-09-10 15:12:56');
INSERT INTO "stock_movements" VALUES(32,60,'IN',9,'Stock Addition','2026-09-10 15:14:35');
INSERT INTO "stock_movements" VALUES(33,61,'IN',5,'Stock Addition','2026-09-10 15:16:42');
INSERT INTO "stock_movements" VALUES(34,62,'IN',4,'Stock Addition','2026-09-10 15:17:45');
INSERT INTO "stock_movements" VALUES(35,63,'IN',6,'Stock Addition','2026-09-10 15:19:58');
INSERT INTO "stock_movements" VALUES(36,64,'IN',12,'Stock Addition','2026-09-10 15:22:16');
INSERT INTO "stock_movements" VALUES(37,65,'IN',1,'Stock Addition','2026-09-10 15:24:00');
INSERT INTO "stock_movements" VALUES(38,66,'IN',1,'Stock Addition','2026-09-10 15:25:08');
INSERT INTO "stock_movements" VALUES(39,67,'IN',9,'Stock Addition','2026-09-10 15:26:07');
INSERT INTO "stock_movements" VALUES(40,68,'IN',4,'Stock Addition','2026-09-10 15:26:58');
INSERT INTO "stock_movements" VALUES(41,69,'IN',7,'Stock Addition','2026-09-10 15:27:50');
INSERT INTO "stock_movements" VALUES(42,70,'IN',10,'Stock Addition','2026-09-10 15:29:37');
INSERT INTO "stock_movements" VALUES(43,71,'IN',21,'Stock Addition','2026-09-10 15:30:33');
INSERT INTO "stock_movements" VALUES(44,72,'IN',3,'Stock Addition','2026-09-10 15:31:34');
INSERT INTO "stock_movements" VALUES(45,73,'IN',12,'Stock Addition','2026-09-10 15:33:08');
INSERT INTO "stock_movements" VALUES(46,74,'IN',16,'Stock Addition','2026-09-10 15:36:11');
INSERT INTO "stock_movements" VALUES(47,75,'IN',9,'Stock Addition','2026-09-10 15:37:33');
INSERT INTO "stock_movements" VALUES(48,76,'IN',17,'Stock Addition','2026-09-10 15:39:49');
INSERT INTO "stock_movements" VALUES(49,77,'IN',6,'Stock Addition','2026-09-10 15:41:24');
INSERT INTO "stock_movements" VALUES(50,78,'IN',1,'Stock Addition','2026-09-10 16:06:15');
INSERT INTO "stock_movements" VALUES(51,79,'IN',1,'Stock Addition','2026-09-10 16:07:41');
INSERT INTO "stock_movements" VALUES(52,80,'IN',3,'Stock Addition','2026-09-10 16:08:47');
INSERT INTO "stock_movements" VALUES(53,81,'IN',8,'Stock Addition','2026-09-10 16:10:11');
INSERT INTO "stock_movements" VALUES(54,82,'IN',2,'Stock Addition','2026-09-10 16:12:49');
INSERT INTO "stock_movements" VALUES(55,83,'IN',1,'Stock Addition','2026-09-10 16:14:04');
INSERT INTO "stock_movements" VALUES(56,84,'IN',1,'Stock Addition','2026-09-10 16:15:37');
INSERT INTO "stock_movements" VALUES(57,85,'IN',4,'Stock Addition','2026-09-10 16:16:42');
INSERT INTO "stock_movements" VALUES(58,86,'IN',2,'Stock Addition','2026-09-10 16:18:41');
INSERT INTO "stock_movements" VALUES(59,87,'IN',7,'Stock Addition','2026-09-10 16:20:02');
INSERT INTO "stock_movements" VALUES(60,88,'IN',6,'Stock Addition','2026-09-10 16:21:07');
INSERT INTO "stock_movements" VALUES(61,89,'IN',5,'Stock Addition','2026-09-10 16:21:57');
INSERT INTO "stock_movements" VALUES(62,90,'IN',18,'Stock Addition','2026-09-10 16:23:08');
INSERT INTO "stock_movements" VALUES(63,91,'IN',9,'Stock Addition','2026-09-10 16:24:08');
INSERT INTO "stock_movements" VALUES(64,92,'IN',1,'Stock Addition','2026-09-10 16:25:16');
INSERT INTO "stock_movements" VALUES(65,93,'IN',4,'Stock Addition','2026-09-10 16:27:39');
INSERT INTO "stock_movements" VALUES(66,94,'IN',14,'Stock Addition','2026-09-10 16:33:14');
INSERT INTO "stock_movements" VALUES(67,95,'IN',15,'Stock Addition','2026-09-10 16:35:11');
INSERT INTO "stock_movements" VALUES(68,96,'IN',2,'Stock Addition','2026-09-10 16:37:05');
INSERT INTO "stock_movements" VALUES(69,97,'IN',12,'Stock Addition','2026-09-10 16:43:31');
INSERT INTO "stock_movements" VALUES(70,98,'IN',12,'Stock Addition','2026-09-10 16:57:35');
INSERT INTO "stock_movements" VALUES(71,99,'IN',1,'Stock Addition','2026-09-10 16:58:29');
INSERT INTO "stock_movements" VALUES(72,100,'IN',9,'Stock Addition','2026-09-10 16:59:59');
INSERT INTO "stock_movements" VALUES(73,101,'IN',7,'Stock Addition','2026-09-10 17:01:45');
INSERT INTO "stock_movements" VALUES(74,102,'IN',10,'Stock Addition','2026-09-10 17:03:11');
INSERT INTO "stock_movements" VALUES(75,103,'IN',2,'Stock Addition','2026-09-10 17:04:13');
INSERT INTO "stock_movements" VALUES(76,104,'IN',5,'Stock Addition','2026-09-10 17:06:34');
INSERT INTO "stock_movements" VALUES(77,105,'IN',2,'Stock Addition','2026-09-10 17:07:44');
INSERT INTO "stock_movements" VALUES(78,106,'IN',5,'Stock Addition','2026-09-10 17:08:51');
INSERT INTO "stock_movements" VALUES(79,107,'IN',13,'Stock Addition','2026-09-10 17:10:16');
INSERT INTO "stock_movements" VALUES(80,108,'IN',4,'Stock Addition','2026-09-10 17:11:33');
INSERT INTO "stock_movements" VALUES(81,109,'IN',10,'Stock Addition','2026-09-10 17:12:52');
INSERT INTO "stock_movements" VALUES(82,110,'IN',20,'Stock Addition','2026-09-10 17:13:42');
INSERT INTO "stock_movements" VALUES(83,111,'IN',6,'Stock Addition','2026-09-10 17:15:17');
INSERT INTO "stock_movements" VALUES(84,112,'IN',16,'Stock Addition','2026-09-10 17:16:59');
INSERT INTO "stock_movements" VALUES(85,113,'IN',9,'Stock Addition','2026-09-10 17:17:57');
INSERT INTO "stock_movements" VALUES(86,114,'IN',13,'Stock Addition','2026-09-10 17:18:47');
INSERT INTO "stock_movements" VALUES(87,115,'IN',2,'Stock Addition','2026-09-10 17:20:05');
INSERT INTO "stock_movements" VALUES(88,116,'IN',11,'Stock Addition','2026-09-10 17:22:11');
INSERT INTO "stock_movements" VALUES(89,117,'IN',1,'Stock Addition','2026-09-10 17:23:22');
INSERT INTO "stock_movements" VALUES(90,118,'IN',7,'Stock Addition','2026-09-10 17:24:15');
INSERT INTO "stock_movements" VALUES(91,119,'IN',84902430344876,'Stock Addition','2026-09-10 17:24:57');
INSERT INTO "stock_movements" VALUES(92,120,'IN',8,'Stock Addition','2026-09-10 17:25:47');
INSERT INTO "stock_movements" VALUES(93,121,'IN',1,'Stock Addition','2026-09-10 17:26:40');
INSERT INTO "stock_movements" VALUES(94,122,'IN',6,'Stock Addition','2026-09-10 17:27:21');
INSERT INTO "stock_movements" VALUES(95,123,'IN',2,'Stock Addition','2026-09-10 17:28:07');
INSERT INTO "stock_movements" VALUES(96,124,'IN',1,'Stock Addition','2026-09-10 17:29:24');
INSERT INTO "stock_movements" VALUES(97,125,'IN',6,'Stock Addition','2026-09-10 17:30:06');
INSERT INTO "stock_movements" VALUES(98,126,'IN',13,'Stock Addition','2026-09-10 17:31:09');
INSERT INTO "stock_movements" VALUES(99,127,'IN',12,'Stock Addition','2026-09-10 17:31:53');
INSERT INTO "stock_movements" VALUES(100,128,'IN',2,'Stock Addition','2026-09-10 17:33:00');
INSERT INTO "stock_movements" VALUES(101,129,'IN',2,'Stock Addition','2026-09-10 17:33:46');
INSERT INTO "stock_movements" VALUES(102,130,'IN',3,'Stock Addition','2026-09-10 17:34:21');
INSERT INTO "stock_movements" VALUES(103,131,'IN',3,'Stock Addition','2026-09-10 17:35:04');
INSERT INTO "stock_movements" VALUES(104,132,'IN',11,'Stock Addition','2026-09-10 17:35:54');
INSERT INTO "stock_movements" VALUES(105,57,'OUT',1,'Sale','2026-09-11 12:45:16');
INSERT INTO "stock_movements" VALUES(106,57,'IN',1,'Void Sale','2026-09-11 12:45:35');
INSERT INTO "stock_movements" VALUES(107,57,'OUT',1,'Sale','2026-09-11 12:46:33');
INSERT INTO "stock_movements" VALUES(108,133,'IN',5,'Stock Addition','2026-09-11 13:43:41');
INSERT INTO "stock_movements" VALUES(109,134,'IN',2,'Stock Addition','2026-09-11 13:44:23');
INSERT INTO "stock_movements" VALUES(110,135,'IN',2,'Stock Addition','2026-09-11 13:45:30');
INSERT INTO "stock_movements" VALUES(111,136,'IN',6,'Stock Addition','2026-09-11 13:46:20');
INSERT INTO "stock_movements" VALUES(112,137,'IN',2,'Stock Addition','2026-09-11 13:47:18');
INSERT INTO "stock_movements" VALUES(113,138,'IN',2,'Stock Addition','2026-09-11 13:48:20');
INSERT INTO "stock_movements" VALUES(114,139,'IN',10,'Stock Addition','2026-09-11 13:51:16');
INSERT INTO "stock_movements" VALUES(115,140,'IN',4,'Stock Addition','2026-09-11 13:52:45');
INSERT INTO "stock_movements" VALUES(116,141,'IN',2,'Stock Addition','2026-09-11 13:53:45');
INSERT INTO "stock_movements" VALUES(117,142,'IN',6,'Stock Addition','2026-09-11 13:54:36');
INSERT INTO "stock_movements" VALUES(118,57,'OUT',10,'Sale','2026-09-11 15:48:18');
INSERT INTO "stock_movements" VALUES(119,41,'OUT',1,'Sale','2026-09-11 15:49:14');
INSERT INTO "stock_movements" VALUES(120,41,'OUT',1,'Sale','2026-09-11 15:49:30');
INSERT INTO "stock_movements" VALUES(121,41,'OUT',8,'Sale','2026-09-11 16:41:19');
INSERT INTO "stock_movements" VALUES(122,41,'IN',8,'Void Sale','2026-09-11 16:41:37');
INSERT INTO "stock_movements" VALUES(123,57,'OUT',1,'Sale','2026-09-19 09:21:26');
INSERT INTO "stock_movements" VALUES(124,143,'IN',3,'Stock Addition','2026-09-19 11:32:15');
INSERT INTO "stock_movements" VALUES(125,144,'IN',3,'Stock Addition','2026-09-19 11:33:30');
INSERT INTO "stock_movements" VALUES(126,145,'IN',3,'Stock Addition','2026-09-19 11:36:19');
INSERT INTO "stock_movements" VALUES(127,146,'IN',3,'Stock Addition','2026-09-19 11:45:04');
INSERT INTO "stock_movements" VALUES(128,147,'IN',3,'Stock Addition','2026-09-19 11:46:45');
INSERT INTO "stock_movements" VALUES(129,148,'IN',3,'Stock Addition','2026-09-19 11:47:53');
INSERT INTO "stock_movements" VALUES(130,149,'IN',3,'Stock Addition','2026-09-19 11:48:53');
INSERT INTO "stock_movements" VALUES(131,150,'IN',3,'Stock Addition','2026-09-19 11:49:57');
INSERT INTO "stock_movements" VALUES(132,151,'IN',3,'Stock Addition','2026-09-19 11:51:32');
INSERT INTO "stock_movements" VALUES(133,152,'IN',3,'Stock Addition','2026-09-19 11:52:43');
INSERT INTO "stock_movements" VALUES(134,153,'IN',3,'Stock Addition','2026-09-19 11:53:39');
INSERT INTO "stock_movements" VALUES(135,154,'IN',3,'Stock Addition','2026-09-19 11:54:59');
INSERT INTO "stock_movements" VALUES(136,155,'IN',3,'Stock Addition','2026-09-19 11:56:34');
INSERT INTO "stock_movements" VALUES(137,156,'IN',3,'Stock Addition','2026-09-19 11:58:02');
INSERT INTO "stock_movements" VALUES(138,157,'IN',3,'Stock Addition','2026-09-19 11:59:38');
INSERT INTO "stock_movements" VALUES(139,158,'IN',3,'Stock Addition','2026-09-19 12:00:37');
INSERT INTO "stock_movements" VALUES(140,159,'IN',3,'Stock Addition','2026-09-19 12:01:49');
INSERT INTO "stock_movements" VALUES(141,160,'IN',3,'Stock Addition','2026-09-19 12:03:14');
INSERT INTO "stock_movements" VALUES(142,161,'IN',3,'Stock Addition','2026-09-19 12:04:28');
INSERT INTO "stock_movements" VALUES(143,162,'IN',3,'Stock Addition','2026-09-19 12:06:40');
INSERT INTO "stock_movements" VALUES(144,163,'IN',3,'Stock Addition','2026-09-19 12:07:43');
INSERT INTO "stock_movements" VALUES(145,164,'IN',3,'Stock Addition','2026-09-19 12:08:52');
INSERT INTO "stock_movements" VALUES(146,165,'IN',3,'Stock Addition','2026-09-19 12:09:59');
INSERT INTO "stock_movements" VALUES(147,166,'IN',3,'Stock Addition','2026-09-19 12:18:49');
INSERT INTO "stock_movements" VALUES(148,167,'IN',1,'Stock Addition','2026-09-19 12:22:05');
INSERT INTO "stock_movements" VALUES(149,168,'IN',1,'Stock Addition','2026-09-19 12:27:36');
INSERT INTO "stock_movements" VALUES(150,169,'IN',1,'Stock Addition','2026-09-19 12:28:39');
INSERT INTO "stock_movements" VALUES(151,170,'IN',3,'Stock Addition','2026-09-19 12:31:37');
INSERT INTO "stock_movements" VALUES(152,171,'IN',1,'Stock Addition','2026-09-19 12:33:44');
INSERT INTO "stock_movements" VALUES(153,172,'IN',3,'Stock Addition','2026-09-19 12:34:43');
INSERT INTO "stock_movements" VALUES(154,173,'IN',3,'Stock Addition','2026-09-19 12:36:23');
INSERT INTO "stock_movements" VALUES(155,174,'IN',3,'Stock Addition','2026-09-19 12:37:46');
INSERT INTO "stock_movements" VALUES(156,175,'IN',3,'Stock Addition','2026-09-19 12:40:13');
INSERT INTO "stock_movements" VALUES(157,176,'IN',3,'Stock Addition','2026-09-19 12:42:39');
INSERT INTO "stock_movements" VALUES(158,177,'IN',3,'Stock Addition','2026-09-19 13:08:50');
INSERT INTO "stock_movements" VALUES(159,178,'IN',3,'Stock Addition','2026-09-19 13:14:36');
INSERT INTO "stock_movements" VALUES(160,179,'IN',2,'Stock Addition','2026-09-19 13:31:09');
INSERT INTO "stock_movements" VALUES(161,180,'IN',1,'Stock Addition','2026-09-19 13:35:44');
INSERT INTO "stock_movements" VALUES(162,181,'IN',3,'Stock Addition','2026-09-19 13:37:03');
INSERT INTO "stock_movements" VALUES(163,182,'IN',1,'Stock Addition','2026-09-19 13:40:10');
INSERT INTO "stock_movements" VALUES(164,183,'IN',2,'Stock Addition','2026-09-19 13:46:13');
INSERT INTO "stock_movements" VALUES(165,184,'IN',1,'Stock Addition','2026-09-19 13:49:19');
INSERT INTO "stock_movements" VALUES(166,185,'IN',2,'Stock Addition','2026-09-19 13:50:39');
INSERT INTO "stock_movements" VALUES(167,186,'IN',3,'Stock Addition','2026-09-19 13:51:49');
INSERT INTO "stock_movements" VALUES(168,187,'IN',5,'Stock Addition','2026-09-19 13:53:07');
INSERT INTO "stock_movements" VALUES(169,188,'IN',1,'Stock Addition','2026-09-19 13:54:32');
INSERT INTO "stock_movements" VALUES(170,189,'IN',2,'Stock Addition','2026-09-19 13:55:53');
INSERT INTO "stock_movements" VALUES(171,190,'IN',4,'Stock Addition','2026-09-19 13:57:28');
INSERT INTO "stock_movements" VALUES(172,191,'IN',6,'Stock Addition','2026-09-19 14:00:23');
INSERT INTO "stock_movements" VALUES(173,192,'IN',3,'Stock Addition','2026-09-19 14:10:37');
INSERT INTO "stock_movements" VALUES(175,194,'IN',24,'Stock Addition','2026-09-19 14:15:13');
INSERT INTO "stock_movements" VALUES(176,195,'IN',24,'Stock Addition','2026-09-19 14:20:01');
INSERT INTO "stock_movements" VALUES(177,195,'OUT',1,'Sale','2026-09-19 14:20:42');
INSERT INTO "stock_movements" VALUES(178,196,'IN',30,'Stock Addition','2026-09-19 14:24:52');
INSERT INTO "stock_movements" VALUES(179,156,'OUT',1,'Sale','2026-09-19 14:26:57');
INSERT INTO "stock_movements" VALUES(180,197,'IN',5,'Stock Addition','2026-09-23 13:37:57');
INSERT INTO "stock_movements" VALUES(181,198,'IN',25,'Stock Addition','2026-09-23 13:40:09');
INSERT INTO "stock_movements" VALUES(182,199,'IN',5,'Stock Addition','2026-09-23 13:42:55');
INSERT INTO "stock_movements" VALUES(183,200,'IN',5,'Stock Addition','2026-09-23 13:43:26');
INSERT INTO "stock_movements" VALUES(184,201,'IN',20,'Stock Addition','2026-09-23 13:44:09');
INSERT INTO "stock_movements" VALUES(185,202,'IN',30,'Stock Addition','2026-09-23 13:44:58');
INSERT INTO "stock_movements" VALUES(186,203,'IN',1,'Stock Addition','2026-09-23 13:45:32');
INSERT INTO "stock_movements" VALUES(187,204,'IN',12,'Stock Addition','2026-09-23 13:46:03');
INSERT INTO "stock_movements" VALUES(188,205,'IN',5,'Stock Addition','2026-09-23 13:46:39');
INSERT INTO "stock_movements" VALUES(189,206,'IN',3,'Stock Addition','2026-09-23 13:47:39');
INSERT INTO "stock_movements" VALUES(190,207,'IN',5,'Stock Addition','2026-09-23 13:48:16');
INSERT INTO "stock_movements" VALUES(191,208,'IN',5,'Stock Addition','2026-09-23 13:48:48');
INSERT INTO "stock_movements" VALUES(192,209,'IN',10,'Stock Addition','2026-09-23 13:49:17');
INSERT INTO "stock_movements" VALUES(193,210,'IN',10,'Stock Addition','2026-09-23 13:49:54');
INSERT INTO "stock_movements" VALUES(194,211,'IN',1,'Stock Addition','2026-09-23 13:50:25');
INSERT INTO "stock_movements" VALUES(195,212,'IN',3,'Stock Addition','2026-09-23 13:50:51');
INSERT INTO "stock_movements" VALUES(196,213,'IN',3,'Stock Addition','2026-09-23 13:51:59');
INSERT INTO "stock_movements" VALUES(197,214,'IN',10,'Stock Addition','2026-09-23 13:52:46');
INSERT INTO "stock_movements" VALUES(198,215,'IN',50,'Stock Addition','2026-09-23 13:53:18');
INSERT INTO "stock_movements" VALUES(199,216,'IN',30,'Stock Addition','2026-09-23 13:54:01');
INSERT INTO "stock_movements" VALUES(200,69,'OUT',1,'Sale','2026-10-02 13:53:25');
INSERT INTO "stock_movements" VALUES(201,50,'OUT',1,'Sale','2026-10-02 13:54:10');
INSERT INTO "stock_movements" VALUES(202,101,'OUT',1,'Sale','2026-10-02 13:54:10');
INSERT INTO "stock_movements" VALUES(203,50,'OUT',1,'Sale','2026-10-02 13:54:19');
INSERT INTO "stock_movements" VALUES(204,101,'OUT',1,'Sale','2026-10-02 13:54:19');
INSERT INTO "stock_movements" VALUES(205,50,'OUT',1,'Sale','2026-10-02 13:55:43');
INSERT INTO "stock_movements" VALUES(206,101,'OUT',1,'Sale','2026-10-02 13:55:43');
INSERT INTO "stock_movements" VALUES(207,169,'OUT',1,'Sale','2026-10-02 23:32:41');
INSERT INTO "stock_movements" VALUES(208,113,'OUT',1,'Sale','2026-10-06 13:07:36');
INSERT INTO "stock_movements" VALUES(210,57,'OUT',1,'Sale','2026-10-06 13:27:06');
INSERT INTO "stock_movements" VALUES(211,218,'IN',84,'Stock Addition','2026-10-06 13:29:33');
INSERT INTO "stock_movements" VALUES(212,219,'IN',100,'Stock Addition','2026-10-06 13:30:54');
INSERT INTO "stock_movements" VALUES(213,220,'IN',100,'Stock Addition','2026-10-06 13:31:53');
INSERT INTO "stock_movements" VALUES(214,221,'IN',100,'Stock Addition','2026-10-06 13:32:39');
INSERT INTO "stock_movements" VALUES(215,222,'IN',100,'Stock Addition','2026-10-06 13:33:02');
INSERT INTO "stock_movements" VALUES(216,223,'IN',100,'Stock Addition','2026-10-06 13:33:28');
INSERT INTO "stock_movements" VALUES(217,224,'IN',100,'Stock Addition','2026-10-06 13:34:07');
INSERT INTO "stock_movements" VALUES(218,225,'IN',100,'Stock Addition','2026-10-06 13:35:10');
INSERT INTO "stock_movements" VALUES(219,226,'IN',100,'Stock Addition','2026-10-06 13:35:39');
INSERT INTO "stock_movements" VALUES(220,227,'IN',100,'Stock Addition','2026-10-06 13:36:33');
INSERT INTO "stock_movements" VALUES(221,228,'IN',100,'Stock Addition','2026-10-06 13:36:56');
INSERT INTO "stock_movements" VALUES(222,229,'IN',100,'Stock Addition','2026-10-06 13:37:27');
INSERT INTO "stock_movements" VALUES(223,230,'IN',100,'Stock Addition','2026-10-06 13:37:54');
INSERT INTO "stock_movements" VALUES(224,231,'IN',100,'Stock Addition','2026-10-06 13:38:29');
INSERT INTO "stock_movements" VALUES(225,232,'IN',100,'Stock Addition','2026-10-06 13:39:02');
INSERT INTO "stock_movements" VALUES(226,233,'IN',100,'Stock Addition','2026-10-06 13:39:22');
INSERT INTO "stock_movements" VALUES(227,234,'IN',100,'Stock Addition','2026-10-06 13:39:54');
INSERT INTO "stock_movements" VALUES(228,235,'IN',100,'Stock Addition','2026-10-06 13:40:17');
INSERT INTO "stock_movements" VALUES(229,236,'IN',100,'Stock Addition','2026-10-06 13:40:49');
INSERT INTO "stock_movements" VALUES(230,237,'IN',100,'Stock Addition','2026-10-06 13:41:31');
INSERT INTO "stock_movements" VALUES(231,238,'IN',100,'Stock Addition','2026-10-06 13:42:03');
INSERT INTO "stock_movements" VALUES(232,239,'IN',100,'Stock Addition','2026-10-06 13:44:58');
INSERT INTO "stock_movements" VALUES(233,240,'IN',100,'Stock Addition','2026-10-06 13:45:27');
INSERT INTO "stock_movements" VALUES(234,241,'IN',100,'Stock Addition','2026-10-06 13:46:03');
INSERT INTO "stock_movements" VALUES(235,242,'IN',200,'Stock Addition','2026-10-06 13:46:40');
INSERT INTO "stock_movements" VALUES(236,243,'IN',200,'Stock Addition','2026-10-06 13:47:11');
INSERT INTO "stock_movements" VALUES(237,244,'IN',200,'Stock Addition','2026-10-06 13:47:48');
INSERT INTO "stock_movements" VALUES(238,245,'IN',100,'Stock Addition','2026-10-06 13:48:46');
INSERT INTO "stock_movements" VALUES(239,246,'IN',100,'Stock Addition','2026-10-06 13:49:09');
INSERT INTO "stock_movements" VALUES(240,247,'IN',100,'Stock Addition','2026-10-06 13:49:34');
INSERT INTO "stock_movements" VALUES(241,248,'IN',100,'Stock Addition','2026-10-06 13:50:07');
INSERT INTO "stock_movements" VALUES(242,249,'IN',100,'Stock Addition','2026-10-06 13:50:34');
INSERT INTO "stock_movements" VALUES(243,250,'IN',100,'Stock Addition','2026-10-06 13:51:20');
INSERT INTO "stock_movements" VALUES(244,251,'IN',100,'Stock Addition','2026-10-06 13:52:07');
INSERT INTO "stock_movements" VALUES(245,252,'IN',100,'Stock Addition','2026-10-06 13:52:31');
INSERT INTO "stock_movements" VALUES(246,253,'IN',100,'Stock Addition','2026-10-06 13:53:32');
INSERT INTO "stock_movements" VALUES(247,254,'IN',100,'Stock Addition','2026-10-06 13:53:54');
INSERT INTO "stock_movements" VALUES(248,255,'IN',100,'Stock Addition','2026-10-06 13:54:21');
INSERT INTO "stock_movements" VALUES(249,256,'IN',100,'Stock Addition','2026-10-06 13:54:43');
INSERT INTO "stock_movements" VALUES(250,257,'IN',100,'Stock Addition','2026-10-06 13:55:51');
INSERT INTO "stock_movements" VALUES(251,258,'IN',100,'Stock Addition','2026-10-06 13:56:23');
INSERT INTO "stock_movements" VALUES(252,259,'IN',100,'Stock Addition','2026-10-06 13:56:47');
INSERT INTO "stock_movements" VALUES(253,260,'IN',100,'Stock Addition','2026-10-06 14:02:03');
INSERT INTO "stock_movements" VALUES(254,261,'IN',100,'Stock Addition','2026-10-06 14:02:57');
INSERT INTO "stock_movements" VALUES(255,262,'IN',200,'Stock Addition','2026-10-06 14:03:28');
INSERT INTO "stock_movements" VALUES(256,263,'IN',100,'Stock Addition','2026-10-06 14:03:55');
INSERT INTO "stock_movements" VALUES(257,264,'IN',100,'Stock Addition','2026-10-06 14:04:16');
INSERT INTO "stock_movements" VALUES(258,265,'IN',100,'Stock Addition','2026-10-06 14:04:44');
INSERT INTO "stock_movements" VALUES(259,266,'IN',100,'Stock Addition','2026-10-06 14:05:07');
INSERT INTO "stock_movements" VALUES(260,267,'IN',100,'Stock Addition','2026-10-06 14:05:30');
INSERT INTO "stock_movements" VALUES(261,268,'IN',100,'Stock Addition','2026-10-06 14:06:00');
INSERT INTO "stock_movements" VALUES(262,269,'IN',100,'Stock Addition','2026-10-06 14:06:33');
INSERT INTO "stock_movements" VALUES(263,270,'IN',100,'Stock Addition','2026-10-06 14:07:23');
INSERT INTO "stock_movements" VALUES(264,271,'IN',100,'Stock Addition','2026-10-06 14:07:54');
INSERT INTO "stock_movements" VALUES(265,272,'IN',150,'Stock Addition','2026-10-06 14:08:38');
INSERT INTO "stock_movements" VALUES(266,273,'IN',100,'Stock Addition','2026-10-06 14:08:59');
INSERT INTO "stock_movements" VALUES(267,274,'IN',100,'Stock Addition','2026-10-06 14:09:28');
INSERT INTO "stock_movements" VALUES(268,275,'IN',100,'Stock Addition','2026-10-06 14:10:20');
INSERT INTO "stock_movements" VALUES(269,276,'IN',100,'Stock Addition','2026-10-06 14:10:53');
INSERT INTO "stock_movements" VALUES(270,277,'IN',48,'Stock Addition','2026-10-06 14:12:14');
INSERT INTO "stock_movements" VALUES(271,278,'IN',80,'Stock Addition','2026-10-06 14:13:11');
INSERT INTO "stock_movements" VALUES(272,279,'IN',48,'Stock Addition','2026-10-06 14:14:20');
INSERT INTO "stock_movements" VALUES(273,280,'IN',48,'Stock Addition','2026-10-06 14:15:08');
INSERT INTO "stock_movements" VALUES(274,281,'IN',35,'Stock Addition','2026-10-06 14:16:16');
INSERT INTO "stock_movements" VALUES(275,282,'IN',32,'Stock Addition','2026-10-06 14:17:00');
INSERT INTO "stock_movements" VALUES(276,283,'IN',19,'Stock Addition','2026-10-06 14:17:36');
INSERT INTO "stock_movements" VALUES(277,284,'IN',20,'Stock Addition','2026-10-06 14:18:35');
INSERT INTO "stock_movements" VALUES(278,285,'IN',30,'Stock Addition','2026-10-06 14:19:46');
INSERT INTO "stock_movements" VALUES(279,286,'IN',40,'Stock Addition','2026-10-06 14:20:22');
INSERT INTO "stock_movements" VALUES(280,287,'IN',37,'Stock Addition','2026-10-06 14:21:05');
INSERT INTO "stock_movements" VALUES(281,288,'IN',48,'Stock Addition','2026-10-06 14:21:54');
INSERT INTO "stock_movements" VALUES(282,289,'IN',120,'Stock Addition','2026-10-06 14:23:35');
INSERT INTO "stock_movements" VALUES(283,290,'IN',20,'Stock Addition','2026-10-06 14:26:37');
INSERT INTO "stock_movements" VALUES(284,290,'OUT',1,'Sale','2026-10-06 14:27:17');
INSERT INTO "stock_movements" VALUES(285,41,'OUT',1,'Sale','2026-10-06 14:27:17');
INSERT INTO "stock_movements" VALUES(286,176,'OUT',1,'Sale','2026-10-06 14:27:36');
INSERT INTO "stock_movements" VALUES(287,176,'OUT',1,'Sale','2026-10-06 14:28:51');
INSERT INTO "stock_movements" VALUES(288,291,'IN',30,'Stock Addition','2026-10-06 14:30:27');
INSERT INTO "stock_movements" VALUES(289,292,'IN',40,'Stock Addition','2026-10-06 14:30:59');
INSERT INTO "stock_movements" VALUES(290,293,'IN',40,'Stock Addition','2026-10-06 14:31:38');
INSERT INTO "stock_movements" VALUES(291,294,'IN',20,'Stock Addition','2026-10-06 14:33:02');
INSERT INTO "stock_movements" VALUES(292,295,'IN',20,'Stock Addition','2026-10-06 14:34:49');
INSERT INTO "stock_movements" VALUES(293,296,'IN',20,'Stock Addition','2026-10-06 14:35:42');
INSERT INTO "stock_movements" VALUES(294,297,'IN',20,'Stock Addition','2026-10-06 14:36:35');
INSERT INTO "stock_movements" VALUES(295,176,'OUT',1,'Sale','2026-10-06 14:37:59');
INSERT INTO "stock_movements" VALUES(296,39,'OUT',3,'Sale','2026-10-06 14:38:36');
INSERT INTO "stock_movements" VALUES(297,39,'OUT',3,'Sale','2026-10-06 14:40:15');
INSERT INTO "stock_movements" VALUES(298,298,'IN',20,'Stock Addition','2026-10-13 13:46:03');
INSERT INTO "stock_movements" VALUES(299,298,'OUT',4,'Sale','2026-10-13 13:46:51');
INSERT INTO "stock_movements" VALUES(300,298,'OUT',2,'Sale','2026-10-13 13:47:13');
INSERT INTO "stock_movements" VALUES(301,298,'OUT',4,'Sale','2026-10-13 13:47:38');
INSERT INTO "stock_movements" VALUES(302,298,'IN',4,'Void Sale','2026-10-13 13:48:08');
INSERT INTO "stock_movements" VALUES(303,298,'IN',2,'Void Sale','2026-10-13 13:48:17');
INSERT INTO "stock_movements" VALUES(304,298,'IN',4,'Void Sale','2026-10-13 13:48:22');
INSERT INTO "stock_movements" VALUES(305,298,'OUT',5,'Sale','2026-10-13 14:35:50');
INSERT INTO "stock_movements" VALUES(306,298,'IN',5,'Void Sale','2026-10-13 14:36:55');
INSERT INTO "stock_movements" VALUES(307,298,'OUT',2,'Sale','2026-10-13 17:14:49');
INSERT INTO "stock_movements" VALUES(308,298,'OUT',1,'Sale','2026-10-13 17:15:05');
INSERT INTO "stock_movements" VALUES(309,298,'IN',1,'Void Sale','2026-10-13 17:42:44');
INSERT INTO "stock_movements" VALUES(310,298,'IN',2,'Void Sale','2026-10-13 17:42:49');
INSERT INTO "stock_movements" VALUES(311,57,'OUT',1,'Sale','2026-10-13 17:51:44');
INSERT INTO "stock_movements" VALUES(312,57,'IN',1,'Void Sale','2026-10-13 17:52:21');
INSERT INTO "stock_movements" VALUES(313,299,'IN',20,'Stock Addition','2026-10-14 13:31:47');
INSERT INTO "stock_movements" VALUES(314,300,'IN',20,'Stock Addition','2026-10-14 13:32:08');
INSERT INTO "stock_movements" VALUES(315,301,'IN',20,'Stock Addition','2026-10-14 13:32:31');
INSERT INTO "stock_movements" VALUES(316,302,'IN',20,'Stock Addition','2026-10-14 13:32:51');
INSERT INTO "stock_movements" VALUES(317,303,'IN',20,'Stock Addition','2026-10-14 13:33:24');
INSERT INTO "stock_movements" VALUES(318,299,'OUT',3,'Sale','2026-10-14 13:35:24');
INSERT INTO "stock_movements" VALUES(319,187,'OUT',2,'Sale','2026-10-14 13:36:11');
INSERT INTO "stock_movements" VALUES(320,214,'OUT',1,'Sale','2026-10-14 13:36:41');
INSERT INTO "stock_movements" VALUES(321,304,'IN',20,'Stock Addition','2026-10-14 13:39:14');
INSERT INTO "stock_movements" VALUES(322,207,'OUT',1,'Sale','2026-10-14 13:40:19');
INSERT INTO "stock_movements" VALUES(323,304,'OUT',1,'Sale','2026-10-14 13:40:19');
INSERT INTO "stock_movements" VALUES(324,73,'OUT',1,'Sale','2026-10-14 13:41:57');
INSERT INTO "stock_movements" VALUES(325,300,'OUT',2,'Sale','2026-10-14 13:42:35');
INSERT INTO "stock_movements" VALUES(326,94,'OUT',1,'Sale','2026-10-14 13:43:06');
INSERT INTO "stock_movements" VALUES(327,54,'OUT',1,'Sale','2026-10-14 13:43:33');
INSERT INTO "stock_movements" VALUES(328,299,'OUT',1,'Sale','2026-10-14 13:43:57');
INSERT INTO "stock_movements" VALUES(329,94,'OUT',1,'Sale','2026-10-14 13:45:06');
INSERT INTO "stock_movements" VALUES(330,120,'OUT',2,'Sale','2026-10-14 13:45:06');
INSERT INTO "stock_movements" VALUES(331,94,'OUT',1,'Sale','2026-10-14 13:45:20');
INSERT INTO "stock_movements" VALUES(332,120,'OUT',2,'Sale','2026-10-14 13:45:20');
INSERT INTO "stock_movements" VALUES(333,305,'IN',50,'Stock Addition','2026-10-14 14:02:54');
INSERT INTO "stock_movements" VALUES(334,305,'OUT',1,'Sale','2026-10-14 14:03:39');
INSERT INTO "stock_movements" VALUES(335,306,'IN',10,'Stock Addition','2026-10-14 14:05:13');
INSERT INTO "stock_movements" VALUES(336,306,'OUT',1,'Sale','2026-10-14 14:07:06');
INSERT INTO "stock_movements" VALUES(337,254,'OUT',3,'Sale','2026-10-14 14:07:22');
INSERT INTO "stock_movements" VALUES(338,198,'OUT',3,'Sale','2026-10-14 14:07:47');
INSERT INTO "stock_movements" VALUES(339,215,'OUT',1,'Sale','2026-10-14 14:08:25');
INSERT INTO "stock_movements" VALUES(340,289,'OUT',1,'Sale','2026-10-14 14:08:46');
INSERT INTO "stock_movements" VALUES(341,302,'OUT',1,'Sale','2026-10-14 14:09:17');
INSERT INTO "stock_movements" VALUES(342,300,'OUT',1,'Sale','2026-10-14 14:09:48');
INSERT INTO "stock_movements" VALUES(343,209,'OUT',1,'Sale','2026-10-14 14:09:48');
INSERT INTO "stock_movements" VALUES(344,195,'OUT',1,'Sale','2026-10-14 14:34:25');
INSERT INTO "stock_movements" VALUES(345,299,'OUT',1,'Sale','2026-10-14 15:14:31');
INSERT INTO "stock_movements" VALUES(346,303,'OUT',20,'Sale','2026-10-14 15:15:04');
INSERT INTO "stock_movements" VALUES(347,198,'OUT',1,'Sale','2026-10-14 16:17:18');
INSERT INTO "stock_movements" VALUES(348,300,'OUT',1,'Sale','2026-10-14 16:17:52');
INSERT INTO "stock_movements" VALUES(349,124,'OUT',1,'Sale','2026-10-14 16:17:52');
INSERT INTO "stock_movements" VALUES(350,209,'OUT',1,'Sale','2026-10-14 16:28:19');
INSERT INTO "stock_movements" VALUES(351,121,'OUT',1,'Sale','2026-10-15 00:06:56');
INSERT INTO "stock_movements" VALUES(352,121,'IN',1,'Void Sale','2026-10-15 00:09:13');
INSERT INTO "stock_movements" VALUES(353,299,'OUT',2,'Sale','2026-10-15 13:48:31');
INSERT INTO "stock_movements" VALUES(354,300,'OUT',2,'Sale','2026-10-15 13:49:07');
INSERT INTO "stock_movements" VALUES(355,71,'OUT',1,'Sale','2026-10-15 13:49:35');
INSERT INTO "stock_movements" VALUES(356,198,'OUT',1,'Sale','2026-10-15 13:49:57');
INSERT INTO "stock_movements" VALUES(357,201,'OUT',1,'Sale','2026-10-15 13:50:27');
INSERT INTO "stock_movements" VALUES(358,196,'OUT',2,'Sale','2026-10-15 13:53:16');
INSERT INTO "stock_movements" VALUES(359,196,'OUT',2,'Sale','2026-10-15 13:53:34');
INSERT INTO "stock_movements" VALUES(360,307,'IN',10,'Stock Addition','2026-10-15 13:54:41');
INSERT INTO "stock_movements" VALUES(361,307,'OUT',1,'Sale','2026-10-15 13:55:39');
INSERT INTO "stock_movements" VALUES(362,204,'OUT',1,'Sale','2026-10-15 13:55:39');
INSERT INTO "stock_movements" VALUES(363,305,'OUT',5,'Sale','2026-10-15 13:56:26');
INSERT INTO "stock_movements" VALUES(364,289,'OUT',3,'Sale','2026-10-15 13:56:53');
INSERT INTO "stock_movements" VALUES(365,300,'OUT',1,'Sale','2026-10-15 13:57:20');
INSERT INTO "stock_movements" VALUES(366,195,'OUT',1,'Sale','2026-10-15 13:57:46');
INSERT INTO "stock_movements" VALUES(367,308,'IN',20,'Stock Addition','2026-10-15 13:58:58');
INSERT INTO "stock_movements" VALUES(368,308,'OUT',1,'Sale','2026-10-15 13:59:27');
INSERT INTO "stock_movements" VALUES(369,290,'OUT',1,'Sale','2026-10-15 13:59:52');
INSERT INTO "stock_movements" VALUES(370,93,'OUT',2,'Sale','2026-10-15 14:00:18');
INSERT INTO "stock_movements" VALUES(371,309,'IN',10,'Stock Addition','2026-10-15 14:02:20');
INSERT INTO "stock_movements" VALUES(372,201,'OUT',1,'Sale','2026-10-15 14:03:31');
INSERT INTO "stock_movements" VALUES(373,309,'OUT',1,'Sale','2026-10-15 14:03:31');
INSERT INTO "stock_movements" VALUES(374,67,'OUT',2,'Sale','2026-10-15 14:05:03');
INSERT INTO "stock_movements" VALUES(375,115,'OUT',1,'Sale','2026-10-15 14:11:43');
INSERT INTO "stock_movements" VALUES(376,118,'OUT',1,'Sale','2026-10-15 14:11:43');
INSERT INTO "stock_movements" VALUES(377,300,'OUT',2,'Sale','2026-10-15 14:11:59');
INSERT INTO "stock_movements" VALUES(378,310,'IN',10,'Stock Addition','2026-10-15 14:42:09');
INSERT INTO "stock_movements" VALUES(379,310,'OUT',1,'Sale','2026-10-15 14:42:50');
INSERT INTO "stock_movements" VALUES(380,216,'OUT',1,'Sale','2026-10-15 14:42:50');
INSERT INTO "stock_movements" VALUES(381,215,'OUT',1,'Sale','2026-10-15 15:13:17');
INSERT INTO "stock_movements" VALUES(382,204,'OUT',1,'Sale','2026-10-15 15:13:30');
INSERT INTO "stock_movements" VALUES(383,289,'OUT',2,'Sale','2026-10-15 15:25:15');
INSERT INTO "stock_movements" VALUES(384,311,'IN',30,'Stock Addition','2026-10-15 15:30:02');
INSERT INTO "stock_movements" VALUES(385,311,'OUT',1,'Sale','2026-10-15 15:30:50');
INSERT INTO "stock_movements" VALUES(386,158,'OUT',1,'Sale','2026-10-16 08:34:28');
INSERT INTO "stock_movements" VALUES(387,158,'IN',1,'Void Sale','2026-10-16 08:35:44');
INSERT INTO "stock_movements" VALUES(388,299,'OUT',1,'Sale','2026-10-16 10:28:07');
INSERT INTO "stock_movements" VALUES(389,41,'OUT',1,'Sale','2026-10-16 10:28:48');
INSERT INTO "stock_movements" VALUES(390,312,'IN',20,'Stock Addition','2026-10-16 10:29:57');
INSERT INTO "stock_movements" VALUES(391,313,'IN',24,'Stock Addition','2026-10-16 10:30:37');
INSERT INTO "stock_movements" VALUES(392,314,'IN',0,'Stock Addition','2026-10-16 10:31:10');
INSERT INTO "stock_movements" VALUES(393,312,'OUT',1,'Sale','2026-10-16 10:31:58');
INSERT INTO "stock_movements" VALUES(394,313,'OUT',2,'Sale','2026-10-16 10:32:40');
INSERT INTO "stock_movements" VALUES(395,315,'IN',20,'Stock Addition','2026-10-16 10:40:53');
INSERT INTO "stock_movements" VALUES(396,315,'OUT',2,'Sale','2026-10-16 10:44:02');
INSERT INTO "stock_movements" VALUES(397,77,'OUT',1,'Sale','2026-10-16 10:44:02');
INSERT INTO "stock_movements" VALUES(398,71,'OUT',1,'Sale','2026-10-16 10:44:02');
INSERT INTO "stock_movements" VALUES(399,198,'OUT',2,'Sale','2026-10-16 11:09:04');
INSERT INTO "stock_movements" VALUES(400,316,'IN',60,'Stock Addition','2026-10-16 11:10:40');
INSERT INTO "stock_movements" VALUES(401,316,'OUT',1,'Sale','2026-10-16 11:11:13');
INSERT INTO "stock_movements" VALUES(402,289,'OUT',3,'Sale','2026-10-16 12:38:44');
INSERT INTO "stock_movements" VALUES(403,196,'OUT',2,'Sale','2026-10-16 12:39:11');
INSERT INTO "stock_movements" VALUES(404,300,'OUT',1,'Sale','2026-10-16 12:39:36');
INSERT INTO "stock_movements" VALUES(405,201,'OUT',1,'Sale','2026-10-16 12:39:36');
INSERT INTO "stock_movements" VALUES(406,97,'OUT',5,'Sale','2026-10-16 12:43:56');
INSERT INTO "stock_movements" VALUES(407,118,'OUT',5,'Sale','2026-10-16 12:43:56');
INSERT INTO "stock_movements" VALUES(408,215,'OUT',1,'Sale','2026-10-16 12:47:04');
INSERT INTO "stock_movements" VALUES(409,289,'OUT',1,'Sale','2026-10-16 15:01:22');
INSERT INTO "stock_movements" VALUES(410,216,'OUT',1,'Sale','2026-10-16 15:02:09');
INSERT INTO "stock_movements" VALUES(411,201,'OUT',1,'Sale','2026-10-16 15:13:03');
INSERT INTO "stock_movements" VALUES(412,300,'OUT',1,'Sale','2026-10-16 15:13:03');
INSERT INTO "stock_movements" VALUES(413,198,'OUT',1,'Sale','2026-10-16 15:19:05');
INSERT INTO "stock_movements" VALUES(414,214,'OUT',1,'Sale','2026-10-16 15:31:22');
INSERT INTO "stock_movements" VALUES(415,198,'OUT',1,'Sale','2026-10-16 16:40:52');
INSERT INTO "stock_movements" VALUES(416,289,'OUT',1,'Sale','2026-10-16 16:41:06');
INSERT INTO "stock_movements" VALUES(417,300,'OUT',1,'Sale','2026-10-16 16:41:19');
INSERT INTO "stock_movements" VALUES(418,212,'OUT',1,'Sale','2026-10-16 16:42:45');
INSERT INTO "stock_movements" VALUES(419,201,'OUT',1,'Sale','2026-10-16 16:54:17');
INSERT INTO "stock_movements" VALUES(420,317,'IN',20,'Stock Addition','2026-10-16 17:10:02');
INSERT INTO "stock_movements" VALUES(421,317,'OUT',1,'Sale','2026-10-16 17:10:50');
INSERT INTO "stock_movements" VALUES(422,300,'OUT',2,'Sale','2026-10-16 17:10:50');
INSERT INTO "stock_movements" VALUES(423,309,'OUT',1,'Sale','2026-10-16 17:30:27');
INSERT INTO "stock_movements" VALUES(424,41,'OUT',1,'Sale','2026-10-16 17:30:27');
INSERT INTO "stock_movements" VALUES(425,195,'OUT',1,'Sale','2026-10-16 17:30:27');
INSERT INTO "stock_movements" VALUES(426,289,'OUT',1,'Sale','2026-10-16 17:30:48');
INSERT INTO "stock_movements" VALUES(427,196,'OUT',3,'Sale','2026-10-16 17:31:08');
INSERT INTO "stock_movements" VALUES(428,146,'OUT',1,'Sale','2026-10-16 17:50:39');
INSERT INTO "stock_movements" VALUES(429,195,'OUT',1,'Sale','2026-10-16 17:51:49');
INSERT INTO "stock_movements" VALUES(430,300,'OUT',2,'Sale','2026-10-16 18:03:17');
INSERT INTO "stock_movements" VALUES(431,289,'OUT',1,'Sale','2026-10-16 18:07:32');
INSERT INTO "stock_movements" VALUES(432,289,'OUT',1,'Sale','2026-10-16 18:09:06');
INSERT INTO "stock_movements" VALUES(433,196,'OUT',3,'Sale','2026-10-16 18:14:55');
INSERT INTO "stock_movements" VALUES(434,299,'OUT',3,'Sale','2026-10-16 18:30:50');
INSERT INTO "stock_movements" VALUES(435,300,'OUT',1,'Sale','2026-10-16 18:53:02');
INSERT INTO "stock_movements" VALUES(436,211,'OUT',1,'Sale','2026-10-16 18:55:52');
INSERT INTO "stock_movements" VALUES(437,214,'OUT',1,'Sale','2026-10-16 18:55:52');
INSERT INTO "stock_movements" VALUES(438,300,'OUT',1,'Sale','2026-10-16 18:57:52');
INSERT INTO "stock_movements" VALUES(439,201,'OUT',1,'Sale','2026-10-16 19:06:43');
INSERT INTO "stock_movements" VALUES(440,59,'OUT',3,'Sale','2026-10-16 19:28:01');
INSERT INTO "stock_movements" VALUES(441,215,'OUT',1,'Sale','2026-10-16 19:28:01');
INSERT INTO "stock_movements" VALUES(442,201,'OUT',1,'Sale','2026-10-16 19:33:12');
INSERT INTO "stock_movements" VALUES(443,125,'OUT',1,'Sale','2026-10-16 19:35:58');
INSERT INTO "stock_movements" VALUES(444,317,'OUT',1,'Sale','2026-10-20 13:54:29');
INSERT INTO "stock_movements" VALUES(445,209,'OUT',1,'Sale','2026-10-20 13:55:03');
INSERT INTO "stock_movements" VALUES(446,195,'OUT',1,'Sale','2026-10-20 13:55:19');
INSERT INTO "stock_movements" VALUES(447,300,'OUT',1,'Sale','2026-10-20 13:56:19');
INSERT INTO "stock_movements" VALUES(448,289,'OUT',1,'Sale','2026-10-20 13:56:39');
INSERT INTO "stock_movements" VALUES(449,214,'OUT',1,'Sale','2026-10-20 13:57:38');
INSERT INTO "stock_movements" VALUES(450,176,'OUT',1,'Sale','2026-10-20 13:57:38');
INSERT INTO "stock_movements" VALUES(451,318,'IN',100,'Stock Addition','2026-10-20 13:58:59');
INSERT INTO "stock_movements" VALUES(452,318,'OUT',2,'Sale','2026-10-20 13:59:28');
INSERT INTO "stock_movements" VALUES(453,319,'IN',10,'Stock Addition','2026-10-20 14:00:48');
INSERT INTO "stock_movements" VALUES(454,320,'IN',10,'Stock Addition','2026-10-20 14:01:32');
INSERT INTO "stock_movements" VALUES(455,319,'OUT',1,'Sale','2026-10-20 14:02:21');
INSERT INTO "stock_movements" VALUES(456,321,'IN',8,'Stock Addition','2026-10-20 14:03:43');
INSERT INTO "stock_movements" VALUES(457,321,'OUT',1,'Sale','2026-10-20 14:08:30');
INSERT INTO "stock_movements" VALUES(458,187,'OUT',1,'Sale','2026-10-20 14:08:46');
INSERT INTO "stock_movements" VALUES(459,109,'OUT',1,'Sale','2026-10-20 14:09:17');
INSERT INTO "stock_movements" VALUES(460,125,'OUT',2,'Sale','2026-10-20 14:10:29');
INSERT INTO "stock_movements" VALUES(461,116,'OUT',2,'Sale','2026-10-20 14:10:29');
INSERT INTO "stock_movements" VALUES(462,289,'OUT',1,'Sale','2026-10-20 14:10:56');
INSERT INTO "stock_movements" VALUES(463,302,'OUT',1,'Sale','2026-10-20 14:11:22');
INSERT INTO "stock_movements" VALUES(464,204,'OUT',1,'Sale','2026-10-20 14:11:40');
INSERT INTO "stock_movements" VALUES(465,311,'OUT',1,'Sale','2026-10-20 14:22:05');
INSERT INTO "stock_movements" VALUES(466,289,'OUT',2,'Sale','2026-10-20 14:51:16');
INSERT INTO "stock_movements" VALUES(467,66,'IN',24,'Stock Addition','2026-10-20 14:53:25');
INSERT INTO "stock_movements" VALUES(468,66,'OUT',2,'Sale','2026-10-20 14:54:14');
INSERT INTO "stock_movements" VALUES(469,322,'IN',10,'Stock Addition','2026-10-20 15:56:42');
INSERT INTO "stock_movements" VALUES(470,322,'OUT',6,'Sale','2026-10-20 15:58:36');
INSERT INTO "stock_movements" VALUES(471,195,'OUT',1,'Sale','2026-10-20 16:33:46');
INSERT INTO "stock_movements" VALUES(472,90,'OUT',2,'Sale','2026-10-20 16:34:04');
INSERT INTO "stock_movements" VALUES(473,289,'OUT',1,'Sale','2026-10-20 16:57:21');
INSERT INTO "stock_movements" VALUES(474,209,'OUT',1,'Sale','2026-10-20 17:01:18');
INSERT INTO "stock_movements" VALUES(475,109,'OUT',2,'Sale','2026-10-23 14:01:36');
INSERT INTO "stock_movements" VALUES(476,323,'IN',5,'Stock Addition','2026-10-23 14:02:44');
INSERT INTO "stock_movements" VALUES(477,323,'OUT',1,'Sale','2026-10-23 14:03:59');
INSERT INTO "stock_movements" VALUES(478,104,'OUT',2,'Sale','2026-10-23 14:05:19');
INSERT INTO "stock_movements" VALUES(479,320,'OUT',1,'Sale','2026-10-23 14:06:18');
INSERT INTO "stock_movements" VALUES(480,209,'OUT',1,'Sale','2026-10-23 14:07:28');
INSERT INTO "stock_movements" VALUES(481,39,'OUT',2,'Sale','2026-10-23 14:08:29');
INSERT INTO "stock_movements" VALUES(482,290,'OUT',1,'Sale','2026-10-23 14:09:10');
INSERT INTO "stock_movements" VALUES(483,321,'OUT',2,'Sale','2026-10-23 14:09:59');
INSERT INTO "stock_movements" VALUES(484,313,'OUT',2,'Sale','2026-10-23 14:11:06');
INSERT INTO "stock_movements" VALUES(485,39,'OUT',1,'Sale','2026-10-23 14:12:15');
INSERT INTO "stock_movements" VALUES(486,289,'OUT',1,'Sale','2026-10-23 14:13:05');
INSERT INTO "stock_movements" VALUES(487,187,'OUT',1,'Sale','2026-10-23 14:14:23');
INSERT INTO "stock_movements" VALUES(488,302,'OUT',2,'Sale','2026-10-23 14:15:04');
INSERT INTO "stock_movements" VALUES(489,311,'OUT',1,'Sale','2026-10-23 14:15:50');
INSERT INTO "stock_movements" VALUES(490,215,'OUT',1,'Sale','2026-10-23 14:16:36');
INSERT INTO "stock_movements" VALUES(491,39,'OUT',1,'Sale','2026-10-23 14:17:50');
INSERT INTO "stock_movements" VALUES(492,70,'OUT',3,'Sale','2026-10-23 14:18:29');
INSERT INTO "stock_movements" VALUES(493,317,'OUT',1,'Sale','2026-10-23 14:19:06');
INSERT INTO "stock_movements" VALUES(494,49,'OUT',1,'Sale','2026-10-23 14:20:16');
DROP TABLE IF EXISTS store_settings;
CREATE TABLE store_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key VARCHAR(100) NOT NULL UNIQUE,
            setting_value TEXT,
            updated_at TEXT DEFAULT (datetime('now', 'localtime'))
        );
INSERT INTO "store_settings" VALUES(571,'receipt_header','PHARMACON','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(572,'receipt_subtitle','A''s PharmaHealth & Convenience','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(573,'receipt_footer','Thank you for your purchase!
Please come again.','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(574,'store_name','PharmaCon','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(575,'store_address','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(576,'store_contact','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(577,'return_policy','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(578,'website','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(579,'social_media','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(580,'currency_symbol','₱','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(581,'tax_rate','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(582,'tax_label','Tax','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(583,'discount_amount','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(584,'discount_label','Discount','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(585,'font_size','medium','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(586,'paper_size','80','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(587,'print_alignment','center','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(588,'line_style','dashed','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(589,'show_receipt_number','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(590,'show_date','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(591,'show_cashier','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(592,'show_customer','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(593,'show_medical_items','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(594,'show_logo','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(595,'show_footer','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(596,'show_return_policy','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(597,'show_website','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(598,'show_social','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(599,'show_barcode','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(600,'show_subtotal','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(601,'show_tax','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(602,'show_discount','0','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(603,'show_divider_after_header','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(604,'show_divider_after_items','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(605,'show_divider_after_total','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(606,'show_divider_before_footer','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(607,'tin','','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(608,'vat_status','VAT Registered','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(609,'document_title','SALES INVOICE','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(610,'title_alignment','Center','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(611,'title_style','Bold','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(612,'invoice_prefix','INV-','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(613,'next_invoice_no','0000123','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(614,'invoice_digits','7','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(615,'show_date_time','Both','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(616,'date_format','MMM DD, YYYY','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(617,'time_format','12-hour','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(618,'footer_alignment','Center','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(619,'footer_style','Normal','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(620,'show_item_header','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(621,'show_tax_breakdown','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(622,'show_cashier_name','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(623,'show_payment_method','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(624,'show_change','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(625,'show_separator_lines','1','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(626,'line_spacing','Compact','2026-09-09 11:58:19');
INSERT INTO "store_settings" VALUES(627,'print_density','Normal','2026-09-09 11:58:19');
DROP TABLE IF EXISTS test_table;
CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);
CREATE INDEX idx_ip_attempted ON login_attempts(ip_address, attempted_at);
CREATE INDEX idx_username_attempted ON login_attempts(username_attempted, attempted_at);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('admins',14);
INSERT INTO "sqlite_sequence" VALUES('categories',22);
INSERT INTO "sqlite_sequence" VALUES('store_settings',627);
INSERT INTO "sqlite_sequence" VALUES('alert_settings',44);
INSERT INTO "sqlite_sequence" VALUES('admin_activity',513);
INSERT INTO "sqlite_sequence" VALUES('products',323);
INSERT INTO "sqlite_sequence" VALUES('sales',170);
INSERT INTO "sqlite_sequence" VALUES('sale_items',193);
INSERT INTO "sqlite_sequence" VALUES('cashiers',1);
INSERT INTO "sqlite_sequence" VALUES('stock_movements',494);
INSERT INTO "sqlite_sequence" VALUES('alert_acknowledgments',6);
INSERT INTO "sqlite_sequence" VALUES('alert_logs',3);
INSERT INTO "sqlite_sequence" VALUES('cashier_activity',69);
INSERT INTO "sqlite_sequence" VALUES('held_transactions',3);
COMMIT;