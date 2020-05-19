select *
from browse_package
where (select avg(rating) as avg_rating
       from browse_packagerating
       where browse_packagerating.package_id = browse_package.id) >= floor(0)
;
