# Land Management System
![img](https://i.ibb.co/WWjrX6R/Screen-Shot-2021-11-18-at-10-27-42-AM.png)

Helpful SQL Queries:
```
UPDATE landmanagementservice.land_deal_info.owners
SET new_id = GENERATE_UUID()
WHERE new_id is null;
```
```
ALTER TABLE landmanagementservice.land_deal_info.owners
DROP COLUMN id;
```
```
SELECT
  * EXCEPT(new_id),
  new_id AS id
FROM
  landmanagementservice.land_deal_info.owners
```