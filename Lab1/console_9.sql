select	Reader_ID, count(distinct Book_ID) as Book_num
from	Message
where	(to_days(now()) - to_days(borrow_date)) <= 365
group by 	Reader_ID;