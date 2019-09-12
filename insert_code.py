from browse.utils_db import *

insert_package('Chicken Cheese Deluxe', ['Bun', 'Chicken', 'Cheese'], 280, 1, 'Burger', 1)
insert_package('Mr. Perfect', ['Bun', 'Chicken', 'Cheese'], 180, 1, 'Burger', 1)
insert_package('Chicken Cheesegroom', ['Bun', 'Chicken', 'Cheese', 'Mushroom'], 220, 1, 'Burger', 1)

insert_package('Chicken Cheese Burger', ['Bun', 'Chicken', 'Cheese'], 280, 1, 'Burger', 2)
insert_package('Beef Cheese Burger', ['Bun', 'Beef', 'Cheese'], 320, 1, 'Burger', 2)
insert_package('BBQ Pizza', ['Chicken', 'Cheese', 'Onion'], 720, 1, 'Pizza', 2)
insert_package('Vegetable Salad', ['Sauce', 'Tomato', 'Capsicum', 'Onion'], 750, 1, 'Vegetable', 2)
insert_package('Chicken Noodles', ['Sauce', 'Tomato', 'Onion', 'Chicken'], 350, 1, 'Noodles', 2)



from accounts.models import User

post_comment_package(User.objects.get(username='subangkar'), 7, "This is a very good item")
