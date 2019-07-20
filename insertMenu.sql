INSERT INTO manager_menu(price, menu_img, menu_name)
VALUES('250', 'menu/burger01.jpg', 'Chicken Cheese Burger');

INSERT INTO "django_site" ("id", "name", "domain") VALUES ('1', 'foodsquare.com', 'foodsquare.com');
INSERT INTO "django_site" ("id", "name", "domain") VALUES ('2', 'foodsquare.net', 'foodsquare.net');
INSERT INTO "django_site" ("id", "name", "domain") VALUES ('3', 'localhost', 'localhost');

INSERT INTO "socialaccount_socialapp" ("provider", "name", "client_id", "key", "secret") 
VALUES ('facebook', 'facebook', '2213513975398382', '', '13ff209e35f44dba1091ac0754eae339');

INSERT INTO "accounts_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "is_customer", "is_manager") VALUES ('2', 'pbkdf2_sha256$150000$cCOV1cL9IFaB$0tp4Dnyl8sjLmXwzcVuenf0YgtZV0pSFgplwzK+FLlU=', '2019-06-30 04:08:17.973037', '0', 'pizin', '', '', 'a@b.com', '0', '1', '2019-06-30 04:08:17.363735', '0', '1');
INSERT INTO "accounts_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "is_customer", "is_manager") VALUES ('3', 'pbkdf2_sha256$150000$5OzmRG84ZcPq$8UPs6B4Z1Kv/DCuhbdHnXYsBxItutzjNRzl+fqSMmdU=', '2019-06-30 06:05:54.064516', '0', 'madman', '', '', 'p@q.com', '0', '1', '2019-06-30 06:05:53.445396', '0', '1');

INSERT INTO "accounts_restaurant" ("id", "restaurant_name", "restaurant_key", "trade_license", "restaurantImg", "user_id") VALUES ('1', 'Pizza Inn', '123654', '12345', 'restaurant_img/default.png', '2');
INSERT INTO "accounts_restaurant" ("id", "restaurant_name", "restaurant_key", "trade_license", "restaurantImg", "user_id") VALUES ('2', 'Madchef', '0', '123456764', 'restaurant_img/default.png', '3');

INSERT INTO "browse_ingredient" ("id", "name") VALUES ('1', ' chicken ');
INSERT INTO "browse_ingredient" ("id", "name") VALUES ('2', ' cheese ');

INSERT INTO "browse_package" ("id", "pkg_name", "for_n_persons", "price", "available", "image", "details", "restaurant_id") VALUES ('1', 'Chicken Cheese Burger', '2', '150', '1', 'menu/cuisine1.jpg', 'Good Item', '1');
INSERT INTO "browse_package" ("id", "pkg_name", "for_n_persons", "price", "available", "image", "details", "restaurant_id") VALUES ('2', 'Beef Cheese Burger', '2', '150', '1', 'menu/cuisine6.jpg', 'Good Item', '1');
