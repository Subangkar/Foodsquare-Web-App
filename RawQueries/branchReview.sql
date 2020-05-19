-- all comments and rating for branch with current user @ top
select comment.branch_id,
       comment.id                       as comment_id,
       account.username                 as user_name,
       account.id                       as user_id,
       rate.rating,
       comment.comment,
       comment.time,
       (select count(liked.user_id)
        from browse_branchcommentreact liked
        where liked.post_id = comment.id
          and liked.liked = true)       as nlikes,
       (select count(disliked.user_id)
        from browse_branchcommentreact disliked
        where disliked.post_id = comment.id
          and disliked.disliked = true) as ndislikes
from browse_branchcomment comment
         left join browse_branchrating rate on rate.branch_id = comment.branch_id and
                                               rate.user_id = comment.user_id
         join accounts_user account on comment.user_id = account.id
where comment.user_id = 1
  and comment.branch_id = 2
UNION
DISTINCT
select *
from (
         select comment.branch_id,
                comment.id                       as comment_id,
                account.username                 as user_name,
                account.id                       as user_id,
                rate.rating,
                comment.comment,
                comment.time,
                (select count(liked.user_id)
                 from browse_branchcommentreact liked
                 where liked.post_id = comment.id
                   and liked.liked = true)       as nlikes,
                (select count(disliked.user_id)
                 from browse_branchcommentreact disliked
                 where disliked.post_id = comment.id
                   and disliked.disliked = true) as ndislikes
         from browse_branchcomment comment
                  left join browse_branchrating rate on rate.branch_id = comment.branch_id and
                                                        rate.user_id = comment.user_id
                  join accounts_user account on comment.user_id = account.id
         where comment.user_id != 1
           and comment.branch_id = 2
         order by time desc
     ) other_comments;


-- avg Branch rating
select avg(rating) as avg_rating
from browse_branchrating
where branch_id = 1;


-- avg Restaurant rating
select avg(rating) as avg_rating
from browse_branchrating
         join accounts_restaurantbranch
              on browse_branchrating.branch_id = accounts_restaurantbranch.id
where accounts_restaurantbranch.restaurant_id = 1;


-- like count of a post
select count(liked.user_id)
from browse_branchcommentreact liked
where liked.post_id = 1
  and liked.liked = true;

-- dislike count of a post
select count(disliked.user_id)
from browse_branchcommentreact disliked
where disliked.post_id = 1
  and disliked.disliked = true;