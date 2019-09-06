select delman.id,
       delman.name,
       delman.user_id,
       delman.address,
       count(delivery.id) as order_cnt,
       sum(delivery.charge) as payment
from accounts_deliveryman delman
         join accounts_delivery delivery on delman.id = delivery.deliveryman_id
         join accounts_order on delivery.id = accounts_order.delivery_id
where accounts_order.time >= date_trunc('month', CURRENT_DATE)
group by delman.id;