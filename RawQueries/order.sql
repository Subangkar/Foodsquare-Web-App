-- each branch's month-wise completed delivery count -----
select branch.branch_name                               as name,
       to_char(date_trunc('month', ao.time), 'Month')   as month,
       EXTRACT(month from date_trunc('month', ao.time)) as monthval,
       count(ao.delivery_id)                            as sale
from accounts_restaurantbranch branch
         left join accounts_order ao on branch.id = ao.branch_id and ao.order_status = 'DELIVERED' and
                                        date_part('year', ao.time) = date_part('year', CURRENT_DATE)
where branch.restaurant_id = 2
group by branch.branch_name, date_trunc('month', ao.time);


-- current branch's month-wise completed delivery count -----
select to_char(date_trunc('month', ao.time), 'Month')   as month,
       EXTRACT(month from date_trunc('month', ao.time)) as monthval,
       count(ao.delivery_id)                            as sale
from accounts_restaurantbranch branch
         left join accounts_order ao on branch.id = ao.branch_id and ao.order_status = 'DELIVERED' and
                                        date_part('year', ao.time) = date_part('year', CURRENT_DATE)
where branch.id = 3
group by date_trunc('month', ao.time);


-- each packages's order count in last n months -----
select package.pkg_name as name, sum(order_pack.quantity) as sale
from browse_package package
         join accounts_orderpackagelist order_pack on package.id = order_pack.package_id
         join accounts_order ordr on order_pack.order_id = ordr.id
where ordr.order_status = 'DELIVERED'
  and package.restaurant_id = 2
  and ordr.time >= CURRENT_DATE - INTERVAL '3 months'
group by package.pkg_name
order by sale desc;


-- each packages's order count for a branch in last n months -----
select package.pkg_name as name, sum(order_pack.quantity) as sale
from browse_package package
         join browse_packagebranchdetails branch_pack on package.id = branch_pack.package_id
         join accounts_orderpackagelist order_pack on package.id = order_pack.package_id
         join accounts_order ordr on order_pack.order_id = ordr.id
where ordr.order_status = 'DELIVERED'
  and branch_pack.branch_id = 3
  and ordr.time >= CURRENT_DATE - INTERVAL '3 months'
group by package.pkg_name
order by sale desc;

