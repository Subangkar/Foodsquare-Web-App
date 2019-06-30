INSERT INTO manager_menu(price, menu_img, menu_name)
VALUES('250', 'menu/burger01.jpg', 'Chicken Cheese Burger');

INSERT INTO "main"."django_site" ("id", "name", "domain") VALUES ('1', 'foodsquare.com', 'foodsquare.com');
INSERT INTO "main"."django_site" ("id", "name", "domain") VALUES ('2', 'foodsquare.net', 'foodsquare.net');
INSERT INTO "main"."django_site" ("id", "name", "domain") VALUES ('3', 'localhost', 'localhost');

INSERT INTO "main"."socialaccount_socialapp" ("provider", "name", "client_id", "key", "secret") 
VALUES ('facebook', 'facebook', '2213513975398382', '', '13ff209e35f44dba1091ac0754eae339');