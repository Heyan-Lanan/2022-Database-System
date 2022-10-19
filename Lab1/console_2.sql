select Reader.name
from Reader
where Reader.ID NOT IN (
    select Reader_ID
    from Borrow
    );