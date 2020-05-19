-- avg package rating
select avg(rating) as avg_rating
from browse_packagerating
where package_id = 1;

-- package user count by star
select rating, count(distinct user_id)
from browse_packagerating
where package_id = 1
group by rating;

-- all comments and rating with current user @ top
select comment.package_id,
       comment.id                       as comment_id,
       account.username                 as user_name,
       account.id                       as user_id,
       rate.rating,
       comment.comment,
       comment.time,
       (select count(liked.user_id)
        from browse_packagecommentreact liked
        where liked.post_id = comment.id
          and liked.liked = true)       as nlikes,
       (select count(disliked.user_id)
        from browse_packagecommentreact disliked
        where disliked.post_id = comment.id
          and disliked.disliked = true) as ndislikes
from browse_packagecomment comment
         left join browse_packagerating rate on rate.package_id = comment.package_id and
                                                rate.user_id = comment.user_id
         join accounts_user account on comment.user_id = account.id
where comment.user_id = 2
  and comment.package_id = 7
UNION
DISTINCT
select *
from (
         select comment.package_id,
                comment.id                       as comment_id,
                account.username                 as user_name,
                account.id                       as user_id,
                rate.rating,
                comment.comment,
                comment.time,
                (select count(liked.user_id)
                 from browse_packagecommentreact liked
                 where liked.post_id = comment.id
                   and liked.liked = true)       as nlikes,
                (select count(disliked.user_id)
                 from browse_packagecommentreact disliked
                 where disliked.post_id = comment.id
                   and disliked.disliked = true) as ndislikes
         from browse_packagecomment comment
                  left join browse_packagerating rate on rate.package_id = comment.package_id and
                                                         rate.user_id = comment.user_id
                  join accounts_user account on comment.user_id = account.id
         where comment.user_id != 2
           and comment.package_id = 7
         order by time desc
     ) other_comments;

-- -- better for single user
select comment.package_id,
       comment.id                                   as comment_id,
       comment.user_id,
       (select rate.rating
        from browse_packagerating rate
        where rate.user_id = comment.user_id
          and rate.package_id = comment.package_id) as rating,
       comment.comment,
       comment.time,
       (select count(distinct liked.user_id)
        from browse_packagecommentreact liked
        where liked.post_id = comment.id
          and liked.liked = true)                   as nlikes,
       (select count(distinct disliked.user_id)
        from browse_packagecommentreact disliked
        where disliked.post_id = comment.id
          and disliked.disliked = true)             as ndislikes
from browse_packagecomment comment
where comment.user_id = 1;


-- like count of a post
select count(liked.user_id)
from browse_packagecommentreact liked
where liked.post_id = 1
  and liked.liked = true;

-- dislike count of a post
select count(disliked.user_id)
from browse_packagecommentreact disliked
where disliked.post_id = 1
  and disliked.disliked = true;