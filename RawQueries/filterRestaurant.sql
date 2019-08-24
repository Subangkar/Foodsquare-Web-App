-- For Filtering Restaurant

select accounts_restaurant.*
from accounts_restaurant
         join browse_package on accounts_restaurant.id = browse_package.restaurant_id
         join browse_ingredientlist on browse_package.id = browse_ingredientlist.package_id
         join browse_ingredient on browse_ingredientlist.ingredient_id = browse_ingredient.id
where lower(browse_ingredient.name) like '%%' || lower('bu') || '%%'
   or lower(browse_package.pkg_name) like '%%' || lower('bu') || '%%'
union
distinct
select accounts_restaurant.*
from accounts_restaurant
where lower(accounts_restaurant.restaurant_name) like '%%' || lower('bu') || '%%';

--


-- For Filtering Branch

select distinct accounts_restaurantbranch.*
from accounts_restaurantbranch
         join accounts_restaurant on accounts_restaurantbranch.restaurant_id = accounts_restaurant.id
         join browse_package on accounts_restaurant.id = browse_package.restaurant_id
         join browse_ingredientlist on browse_package.id = browse_ingredientlist.package_id
         join browse_ingredient on browse_ingredientlist.ingredient_id = browse_ingredient.id
where lower(browse_package.category) like '%%' || lower('bu') || '%%'
   or lower(accounts_restaurant.restaurant_name) like '%%' || lower('bu') || '%%'
   or lower(accounts_restaurantbranch.branch_name) like '%%' || lower('bu') || '%%';
--


select accounts_restaurant.*
from accounts_restaurant
where lower(accounts_restaurant.restaurant_name) LIKE '%%' || lower('tak') || '%%';
