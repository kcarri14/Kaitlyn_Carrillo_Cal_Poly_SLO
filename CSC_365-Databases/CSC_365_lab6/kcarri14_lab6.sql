-- Lab 6
-- kcarri14
-- Mar 5, 2025

USE `BAKERY`;
-- BAKERY-1
-- Find all customers who did not make a purchase between October 5 and October 11 (inclusive) of 2007. Output first and last name in alphabetical order by last name.
Select customers.FirstName, customers.LastName
from customers
where not exists (
    select *
    from receipts
    where receipts.customer = customers.CId and receipts.SaleDate between '2007-10-05' and '2007-10-11');


USE `BAKERY`;
-- BAKERY-2
-- Find the customer(s) who spent the most money at the bakery during October of 2007. Report first, last name and total amount spent (rounded to two decimal places). Sort by last name.
Select customers.FirstName, customers.LastName, ROUND(SUM(goods.price),2) as TotalSpent
from customers join receipts on customers.CId = receipts.Customer join items on items.Receipt = receipts.RNumber
join goods on items.item = goods.GId
where receipts.SaleDate between '2007-10-01' and '2007-10-31'
GROUP BY customers.CId, customers.FirstName, customers.LastName
Having sum(goods.price) = (
    select MAX(TotalSpent) 
    from (select sum(g1.price) as TotalSpent
          from receipts as r1
            join items as i1 on i1.Receipt = r1.RNumber
            join goods as g1 on i1.Item = g1.GId 
            where r1.SaleDate between '2007-10-01' and '2007-10-31' 
            group by r1.customer
    ) as price
)
Order by customers.LastName;


USE `BAKERY`;
-- BAKERY-3
-- Find all customers who did not purchase any eclairs (food type 'Eclair') during October 2007. Report first and last name in alphabetical order by last name.

Select distinct customers.FirstName, customers.LastName
from customers 
left join receipts on receipts.customer = customers.CId 
left join items on items.Receipt = receipts.RNumber
left join goods on items.Item = goods.GId and goods.Food = 'Eclair'
where receipts.SaleDate between '2007-10-01' and '2007-10-31' 
group by customers.CId, customers.FirstName, customers.LastName
having count(goods.GId) = 0
order by customers.LastName;


USE `BAKERY`;
-- BAKERY-4
-- Find the baked good(s) (flavor and food type) responsible for the most total revenue.
Select distinct goods.Flavor, goods.Food
from items 
join goods on items.Item = goods.GId 
group by goods.Flavor, goods.Food
having sum(goods.price) = (select MAX(sumPrice) 
    from (select sum(g1.price) as sumPrice
          from items as i1 
            join goods as g1 on i1.Item = g1.GId 
            group by g1.Flavor, g1.Food
    ) as price
);


USE `BAKERY`;
-- BAKERY-5
-- Find the most popular item, based on number of pastries sold. Report the item (flavor and food) and total quantity sold.
select goods.Flavor, goods.Food, count(items.item) as PopularFoods
from items join goods on items.item = goods.GId 
group by goods.Food, goods.Flavor
having count(items.item) = (select MAX(ItemCount) 
    from (select COUNT(i2.Item) as ItemCount
          from items i2
          join goods g2 on i2.Item = g2.GId
          group by g2.Flavor, g2.Food) as Counts
);


USE `BAKERY`;
-- BAKERY-6
-- Find the date(s) of highest revenue during the month of October, 2007. In case of tie, sort chronologically.
Select distinct receipts.SaleDate
from receipts 
join items on items.Receipt = receipts.RNumber
join goods on items.Item = goods.GId 
where receipts.SaleDate between '2007-10-01' and '2007-10-31' 
group by receipts.SaleDate
having sum(goods.price) = (select MAX(sumPrice) 
    from (select sum(g1.price) as sumPrice
          from receipts as r1
            join items as i1 on i1.Receipt = r1.RNumber
            join goods as g1 on i1.Item = g1.GId 
            where r1.SaleDate between '2007-10-01' and '2007-10-31' 
            group by r1.SaleDate
    ) as price
)
order by receipts.SaleDate;


USE `BAKERY`;
-- BAKERY-7
-- Find the best-selling item(s) (by number of purchases) on the day(s) of highest revenue in October of 2007.  Report flavor, food, and quantity sold. Sort by flavor and food.
with DailyRevenue as (
    select receipts.SaleDate, sum(goods.price) as Total_revenue
    from receipts 
    join items on receipts.RNumber = items.Receipt
    join goods on items.Item = goods.GId
    where receipts.SaleDate between '2007-10-01' and '2007-10-31'
    group by receipts.SaleDate
), maxRevenueDays as (
    select SaleDate
    from DailyRevenue
    where Total_revenue = (select max(Total_revenue) from DailyRevenue)
), BestSelling as (
    select goods.Flavor, goods.Food, Count(*) as qty
    from receipts 
    join items on receipts.RNumber = items.Receipt
    join goods on items.Item = goods.GId
    join maxRevenueDays on maxRevenueDays.SaleDate = receipts.SaleDate
    group by goods.Flavor, goods.Food
)
select Flavor, Food, qty
from BestSelling
where qty = (select max(qty) from BestSelling)
order by Flavor, Food;


USE `BAKERY`;
-- BAKERY-8
-- For every type of Cake report the customer(s) who purchased it the largest number of times during the month of October 2007. Report the name of the pastry (flavor, food type), the name of the customer (first, last), and the quantity purchased. Sort output in descending order on the number of purchases, then in alphabetical order by last name of the customer, then by flavor.
select countItems.Flavor, countItems.Food, countItems.FirstName, countItems.LastName, countItems.qty
from (
    select goods.Flavor, goods.Food, customers.FirstName, customers.LastName, count(*) as qty
            from receipts as r1
            join items on items.Receipt = r1.RNumber
            join goods on items.Item = goods.GId 
            join customers on r1.customer = customers.CId
            where goods.Food = 'Cake' and r1.SaleDate between '2007-10-01' and '2007-10-31' 
            group by goods.Flavor, goods.Food, customers.FirstName, customers.LastName
    ) as countItems
join (
    select Flavor, MAX(qty) as Maxqty
    from (
        select goods.Flavor, goods.Food, customers.FirstName, customers.LastName, count(*) as qty
            from receipts as r1
            join items on items.Receipt = r1.RNumber
            join goods on items.Item = goods.GId 
            join customers on r1.customer = customers.CId
            where goods.Food = 'Cake' and r1.SaleDate between '2007-10-01' and '2007-10-31' 
            group by goods.Flavor, goods.Food, customers.FirstName, customers.LastName
    ) as Purchases
    group by Flavor ) as MaxPurchases 
    on countItems.Flavor = MaxPurchases.Flavor and countItems.qty = MaxPurchases.Maxqty
order by countItems.qty DESC, countItems.LastName ASC, countItems.Flavor ASC;


USE `BAKERY`;
-- BAKERY-9
-- Output the names of all customers who made multiple purchases (more than one receipt) on the latest day in October on which they made a purchase. Report names (last, first) of the customers and the *earliest* day in October on which they made a purchase, sorted in chronological order, then by last name.

select customers.LastName, customers.FirstName, (
    select min(r2.SaleDate)
    from receipts as r2
    where r2.Customer = customers.CId and r2.SaleDate between '2007-10-01' and '2007-10-31' 
    ) as earliest
from receipts join customers on receipts.Customer = customers.CId
where receipts.SaleDate = (
    select max(r1.SaleDate)
    from receipts as r1
    where r1.Customer = receipts.Customer and r1.SaleDate between '2007-10-01' and '2007-10-31' 
    )
group by customers.CId, customers.LastName, customers.FirstName  
having count(receipts.RNumber) > 1
order by earliest ASC, customers.LastName ASC;


USE `BAKERY`;
-- BAKERY-10
-- Find out if sales (in terms of revenue) of Chocolate-flavored items or sales of Croissants (of all flavors) were higher in October of 2007. Output the word 'Chocolate' if sales of Chocolate-flavored items had higher revenue, or the word 'Croissant' if sales of Croissants brought in more revenue.

with chocolateItems as (
    select sum(goods.price) as total_revenue_chocolate
    from receipts 
    join items on receipts.RNumber = items.Receipt
    join goods on items.Item = goods.GId
    where goods.Flavor = 'Chocolate' and receipts.SaleDate between '2007-10-01' and '2007-10-31'
), croissantsItems as (
    select sum(goods.price) as total_revenue_croissants
    from receipts 
    join items on receipts.RNumber = items.Receipt
    join goods on items.Item = goods.GId
    where goods.Food = 'Croissant' and receipts.SaleDate between '2007-10-01' and '2007-10-31')
select 
    case
        when 
            (select total_revenue_chocolate from chocolateItems) >
            (select total_revenue_croissants from croissantsItems)
        then "Chocolate"
        else "Croissant"
    end as HighestCategory;


USE `BAKERY`;
-- BAKERY-11
-- Based on purchase count, which items(s) are more popular on Fridays than Mondays? Report food, flavor, and purchase counts for Monday and Friday as two separate columns. Report a count of 0 if a given item has not been purchased on that day. Sort by food then flavor, both in A-Z order.
select goods.Food, goods.Flavor, (
    select count(items.Item) 
    from receipts 
    join items on receipts.RNumber = items.Receipt
    where items.Item = goods.GId 
    and Weekday(receipts.SaleDate) = 0
    and receipts.SaleDate between '2007-10-01' and '2007-10-31') as MondayCount, 
    ( select count(items.Item) 
    from receipts 
    join items on receipts.RNumber = items.Receipt
    where items.Item = goods.GId 
    and Weekday(receipts.SaleDate) = 4
    and receipts.SaleDate between '2007-10-01' and '2007-10-31') as FridayCount
from goods
where (select count(items.Item) 
    from receipts join items on receipts.RNumber = items.Receipt
    where items.Item = goods.GId 
    and Weekday(receipts.SaleDate) = 0
    and receipts.SaleDate between '2007-10-01' and '2007-10-31' ) <
    ( select count(items.Item) 
    from receipts join items on receipts.RNumber = items.Receipt
    where items.Item = goods.GId 
    and Weekday(receipts.SaleDate) = 4
    and receipts.SaleDate between '2007-10-01' and '2007-10-31')
order by goods.Food, goods.Flavor;


USE `INN`;
-- INN-1
-- Find the most popular room(s) (based on the number of reservations) in the hotel  (Note: if there is a tie for the most popular room, report all such rooms). Report the full name of the room, the room code and the number of reservations.

select rooms.RoomName, rooms.RoomCode, count(reservations.CODE) as popularRoom
from rooms join reservations on reservations.Room = rooms.RoomCode
group by rooms.RoomName, rooms.RoomCode
having count(reservations.CODE) = (
    select Max(RoomRes)
    from ( 
        select count(r1.CODE) as RoomRes
        from rooms as room1 join reservations as r1 on r1.Room = room1.RoomCode
        group by room1.RoomCode) as ResCount
        );


USE `INN`;
-- INN-2
-- Find the room(s) that have been occupied the largest number of days based on all reservations in the database. Report the room name(s), room code(s) and the number of days occupied. Sort by room name.
select rooms.RoomName, rooms.RoomCode, sum(datediff(reservations.CheckOut, reservations.CheckIn)) as popularRoom
from rooms join reservations on reservations.Room = rooms.RoomCode
group by rooms.RoomName, rooms.RoomCode
having sum(datediff(reservations.CheckOut, reservations.CheckIn)) = (
        select Max(daysOccupied)
        from (select sum(datediff(res1.CheckOut, res1.CheckIn)) as daysOccupied
                from rooms as r1 join reservations as res1 on res1.Room = r1.RoomCode
                group by r1.RoomCode) as Occupancy)
Order by rooms.RoomName;


USE `INN`;
-- INN-3
-- For each room, report the most expensive reservation. Report the full room name, dates of stay, last name of the person who made the reservation, daily rate and the total amount paid (rounded to the nearest penny.) Sort the output in descending order by total amount paid.
select rooms.RoomName, reservations.CheckIn, reservations.CheckOut, reservations.LastName, reservations.Rate, 
    round(datediff(reservations.CheckOut, reservations.CheckIn) * reservations.Rate,2) as Expensive
from rooms 
join reservations on reservations.Room = rooms.RoomCode
where (datediff(reservations.CheckOut, reservations.CheckIn) * reservations.Rate)= (
    select Max(datediff(r1.CheckOut, r1.CheckIn) * r1.Rate)
        from reservations as r1 
        where r1.Room = rooms.RoomCode
)
Order by Expensive DESC;


USE `INN`;
-- INN-4
-- For each room, report whether it is occupied or unoccupied on July 4, 2010. Report the full name of the room, the room code, and either 'Occupied' or 'Empty' depending on whether the room is occupied on that day. (the room is occupied if there is someone staying the night of July 4, 2010. It is NOT occupied if there is a checkout on this day, but no checkin). Output in alphabetical order by room code. 
select rooms.RoomName, rooms.RoomCode,
    case 
        when exists (
            select 1
            from reservations
            where reservations.Room = rooms.RoomCode 
            and reservations.CheckIn <= '2010-07-04' 
            and reservations.CheckOut > '2010-07-04'
            )
            then 'Occupied'
        else 'Empty'
    end as Status
from rooms
order by rooms.RoomCode;


USE `INN`;
-- INN-5
-- Find the highest-grossing month (or months, in case of a tie). Report the month name, the total number of reservations and the revenue. For the purposes of the query, count the entire revenue of a stay that commenced in one month and ended in another towards the earlier month. (e.g., a September 29 - October 3 stay is counted as September stay for the purpose of revenue computation). In case of a tie, months should be sorted in chronological order.
with MonthlyRevenue as (
    select date_format(CheckIn, '%m') as MonthDate,
    count(*) as total_reservation,
    sum(datediff(CheckOut, CheckIn) * Rate) as TotalRev
    from reservations
    group by MonthDate
), MaxMonth as (
    select Max(TotalRev) as MaxRevenue from MonthlyRevenue
)
select date_format(str_to_date(MonthDate, '%m'), '%M'), total_reservation, TotalRev
from MonthlyRevenue join MaxMonth on MonthlyRevenue.TotalRev = MaxMonth.MaxRevenue
order by MonthDate;


USE `STUDENTS`;
-- STUDENTS-1
-- Find the teacher(s) with the largest number of students. Report the name of the teacher(s) (last, first) and the number of students in their class.

select teachers.Last, teachers.First, count(list.LastName) as largestClassroom
from teachers join list on teachers.classroom = list.classroom
group by teachers.Last, teachers.First
having count(list.LastName) = (
    select Max(NumberStudent)
    from (
        select count(l.LastName) as NumberStudent
        from teachers as t join list as l on t.classroom = l.classroom
        group by l.classroom) as blah );


USE `STUDENTS`;
-- STUDENTS-2
-- Find the grade(s) with the largest number of students whose last names start with letters 'A', 'B' or 'C' Report the grade and the number of students. In case of tie, sort by grade number.
with CountStudents as (
    select grade, COunt(*) as StudentCount
    from list 
    where LastName like 'A%' or LastName like 'B%' or LastName like 'C%'
    group by grade
), MaxCount as (
    select max(StudentCount) as Max_Count
    from CountStudents
)
select grade, StudentCount
from CountStudents
where StudentCount = (select Max_Count from MaxCount)
order by grade;


USE `STUDENTS`;
-- STUDENTS-3
-- Find all classrooms which have more students in them than the average number of students in a classroom in the school. Report the classroom numbers and the number of student in each classroom. Sort in ascending order by classroom.
select l.classroom, count(l.LastName) as averageStudent
from list as l 
group by l.classroom
having count(l.LastName) > (
    select (count(list.LastName) / count(distinct list.classroom))
    from teachers join list on teachers.classroom = list.classroom
);


USE `STUDENTS`;
-- STUDENTS-4
-- Find all pairs of classrooms with the same number of students in them. Report each pair only once. Report both classrooms and the number of students. Sort output in ascending order by the number of students in the classroom.
select l1.classroom, l2.classroom, sqrt(count(l1.LastName)) as largestClassroom
from list as l1 join list as l2 on l1.classroom != l2.classroom
where (select count(*) from list where list.classroom = l1.classroom) = (select count(*) from list where list.classroom = l2.classroom)
group by l1.classroom, l2.classroom
having l1.classroom < l2.classroom
order by largestClassroom;


USE `STUDENTS`;
-- STUDENTS-5
-- For each grade with more than one classroom, report the grade and the last name of the teacher who teaches the classroom with the largest number of students in the grade. Output results in ascending order by grade.
select distinct list.grade, teachers.Last
from list 
join teachers on list.classroom = teachers.classroom
where list.grade in (
    SELECT list.grade
    FROM list
    GROUP BY list.grade
    having count(distinct list.classroom) > 1 )
and list.classroom = 
    (select l.classroom
    from list as l join teachers as t on l.classroom = t.classroom
    where l.grade = list.grade
    group by l.classroom
    having count(l.LastName) = (
            select Max(NumberStudent)
            from (
                select count(l1.LastName) as NumberStudent
                from list as l1 
                where l1.grade = list.grade
                group by l1.classroom
                ) as blah 
        )
)
order by list.grade;


USE `CSU`;
-- CSU-1
-- Find the campus(es) with the largest enrollment in 2000. Output the name of the campus and the enrollment. Sort by campus name.

select campuses.Campus, enrollments.Enrolled
from campuses join enrollments on campuses.Id = enrollments.CampusId
where enrollments.Year = 2000 and enrollments.Enrolled = (
    select Max(e1.Enrolled)
    from enrollments as e1
    where e1.Year = 2000)
    
order by campuses.Campus;


USE `CSU`;
-- CSU-2
-- Find the university (or universities) that granted the highest average number of degrees per year over its entire recorded history. Report the name of the university, sorted alphabetically.

with avgDegrees as (
    select c.Campus, Avg(d.degrees) as avg_degree
    from campuses as c join degrees as d on c.Id = d.CampusId
    group by c.Campus
), maxAvgDegrees as (
    select max(avg_degree) as MaxAvg
    from avgDegrees
)
select avgDegrees.Campus
from avgDegrees join maxAvgDegrees on avgDegrees.avg_degree = maxAvgDegrees.MaxAvg
order by avgDegrees.Campus;


USE `CSU`;
-- CSU-3
-- Find the university with the lowest student-to-faculty ratio in 2003. Report the name of the campus and the student-to-faculty ratio, rounded to one decimal place. Use FTE numbers for enrollment. In case of tie, sort by campus name.
with EnrollmentRatios as (
    select campuses.Campus, Round(enrollments.FTE/faculty.FTE, 1) as FTEratio
    from campuses 
    join enrollments on enrollments.CampusId = campuses.Id
    join faculty on faculty.CampusId = campuses.Id
    where enrollments.Year = 2003 and faculty.Year = 2003 and faculty.FTE > 0
)    
select Campus, FTEratio
from EnrollmentRatios 
where FTEratio = (select Min(FTEratio) from EnrollmentRatios)
order by Campus;


USE `CSU`;
-- CSU-4
-- Among undergraduates studying 'Computer and Info. Sciences' in the year 2004, find the university with the highest percentage of these students (base percentages on the total from the enrollments table). Output the name of the campus and the percent of these undergraduate students on campus. In case of tie, sort by campus name.
with SumUndergrad as ( 
    select discEnr.CampusId, Sum(discEnr.Ug) as SumUg
    from discEnr
    join disciplines on disciplines.Id = discEnr.Discipline
    where disciplines.Name = 'Computer and Info. Sciences' and discEnr.Year = 2004
    group by discEnr.CampusId
), Total_Enrollment as (
    select enrollments.CampusId, sum(enrollments.enrolled) as Total
    from enrollments
    where enrollments.Year = 2004
    group by enrollments.CampusId
), percentage as (
    select campuses.Campus, Round((SumUndergrad.SumUg * 100)/ Total_Enrollment.Total, 2) as total_percentage
    from campuses 
    join SumUndergrad on campuses.Id = SumUndergrad.CampusId
    join Total_Enrollment on campuses.Id = Total_Enrollment.CampusId
)
select Campus, total_percentage
from percentage
where total_percentage = (select Max(total_percentage) from percentage)
order by Campus;


USE `CSU`;
-- CSU-5
-- For each year between 1997 and 2003 (inclusive) find the university with the highest ratio of total degrees granted to total enrollment (use enrollment numbers). Report the year, the name of the campuses, and the ratio. List in chronological order.
with HighestRatio as (
    select campuses.Campus, degrees.Year, Round(Sum(degrees.degrees)/ Sum(enrollments.enrolled), 4) as Ratio
    from campuses
    join degrees on campuses.Id = degrees.CampusId
    join enrollments on enrollments.CampusId = campuses.Id and degrees.Year = enrollments.Year
    where degrees.Year between 1997 and 2003
    group by campuses.Id, degrees.Year
), MaxRatio as (
    select Year, Max(Ratio) as MaxRatioPercent
    from HighestRatio
    group by Year
) 
select HighestRatio.Year, HighestRatio.Campus, HighestRatio.Ratio
from HighestRatio
join MaxRatio on HighestRatio.Year = MaxRatio.Year and HighestRatio.Ratio = MaxRatio.MaxRatioPercent
order by HighestRatio.Year, HighestRatio.Campus;


USE `CSU`;
-- CSU-6
-- For each campus report the year of the highest student-to-faculty ratio, together with the ratio itself. Sort output in alphabetical order by campus name. Use FTE numbers to compute ratios and round to two decimal places.
with EnrollmentRatios as (
    select campuses.Campus as CampusName, enrollments.Year as EnrolledYear, Round(sum(enrollments.FTE)/NULLIF(SUM(faculty.FTE), 0), 2) as FTEratio
    from campuses 
    join enrollments on enrollments.CampusId = campuses.Id
    join faculty on faculty.CampusId = campuses.Id and faculty.Year = enrollments.Year
    group by CampusName, EnrolledYear
), MaxEnrollmentRatios as (
    select CampusName, Max(FTEratio) as MaxRatio
    from EnrollmentRatios
    group by CampusName) 
select EnrollmentRatios.CampusName, EnrollmentRatios.EnrolledYear, EnrollmentRatios.FTEratio
from MaxEnrollmentRatios join EnrollmentRatios on EnrollmentRatios.CampusName = MaxEnrollmentRatios.CampusName
and EnrollmentRatios.FTEratio = MaxEnrollmentRatios.MaxRatio
order by EnrollmentRatios.CampusName;


USE `CSU`;
-- CSU-7
-- For each year for which the data is available, report the total number of campuses in which student-to-faculty ratio became worse (i.e. more students per faculty) as compared to the previous year. Report in chronological order.

with SFRatio as (
    select campuses.Campus, enrollments.Year, max(enrollments.FTE/faculty.FTE) as ratio
    from campuses 
    join faculty on campuses.Id = faculty.CampusId
    join enrollments on campuses.Id = enrollments.CampusId and faculty.Year = enrollments.Year
    group by campuses.Campus, enrollments.Year
)
select (sf.Year +1) as year1, Count(*)
from SFRatio as sf
where sf.ratio <(
    select max(sf1.ratio)
    from SFRatio as sf1
    where sf.Campus = sf1.Campus and (sf.Year +1) = sf1.Year
    )
group by year1
order by year1;


USE `MARATHON`;
-- MARATHON-1
-- Find the state(s) with the largest number of participants. List state code(s) sorted alphabetically.

select marathon.state
from marathon
group by marathon.state
having count(marathon.LastName) =  (
    select Max(Numberparticipant)
    from (
        select count(marathon.LastName) as Numberparticipant
        from marathon
        group by marathon.state) as blah );


USE `MARATHON`;
-- MARATHON-2
-- Find all towns in Massachusetts (MA) which fielded more female runners than male runners for the race. Include only those towns that fielded at least 1 male runner and at least 1 female runner. Report the names of towns, sorted alphabetically.

select distinct m1.Town
from marathon as m1 
join (
    select Town, count(*) as female
    from marathon
    where marathon.Sex = "F" 
    group by Town) as femaleRunners on m1.Town = femaleRunners.Town
join (
    select Town, count(*) as male
    from marathon
    where marathon.Sex = "M" 
    group by Town) as maleRunners on m1.Town = maleRunners.Town    
where m1.State = "MA"
group by m1.Town
having max(femaleRunners.female) > max(maleRunners.male) 
order by m1.Town;


USE `MARATHON`;
-- MARATHON-3
-- For each state, report the gender-age group with the largest number of participants. Output state, age group, gender, and the number of runners in the group. Report only information for the states where the largest number of participants in a gender-age group is greater than one. Sort in ascending order by state code, age group, then gender.
select marathon.State, marathon.AgeGroup, marathon.Sex, count(marathon.LastName)
from marathon
group by marathon.State, marathon.AgeGroup, marathon.Sex
having count(*) = (
    select max(CountAge)
    from (
        select count(*) as CountAge
        from marathon as m1 
        where m1.State = marathon.State
        group by m1.AgeGroup, m1.Sex ) as blah)
        and count(*) > 1
order by marathon.State ASC, marathon.AgeGroup ASC, marathon.Sex ASC;


USE `MARATHON`;
-- MARATHON-4
-- Find the 30th fastest female runner. Report her overall place in the race, first name, and last name. This must be done using a single SQL query (which may be nested) that DOES NOT use the LIMIT clause. Think carefully about what it means for a row to represent the 30th fastest (female) runner.
select marathon.Place, marathon.FirstName, marathon.LastName
from marathon
where marathon.Sex = "F" and (
    select count(*) 
    from marathon as m1
    where m1.Sex = "F" and m1.Place < marathon.Place) = 29;


USE `MARATHON`;
-- MARATHON-5
-- For each town in Connecticut report the total number of male and the total number of female runners. Both numbers shall be reported on the same line. If no runners of a given gender from the town participated in the marathon, report 0. Sort by number of total runners from each town (in descending order) then by town.

select marathon.Town, count(marathon.Sex = "M" or null) as Men, count(marathon.Sex = "F" or null) as Women
from marathon
where marathon.State = "CT"
group by marathon.Town
order by (count(marathon.LastName)) DESC, marathon.Town;


USE `KATZENJAMMER`;
-- KATZENJAMMER-1
-- Report the first name of the performer who never played accordion.

select Band.FirstName
from Band 
where not exists (
    select 1
    from Instruments 
    where Band.Id = Instruments.Bandmate and Instruments.Instrument = "accordion");


USE `KATZENJAMMER`;
-- KATZENJAMMER-2
-- Report, in alphabetical order, the titles of all instrumental compositions performed by Katzenjammer ("instrumental composition" means no vocals).

select distinct Songs.Title
from Songs 
join Performance on Songs.SongId = Performance.Song 
join Tracklists on Songs.SongId = Tracklists.Song 
join Band on Band.Id = Performance.Bandmate
where Band.FirstName in ('Anne', 'Marianne', 'Solveig', 'Turid')
and Songs.SongId not in (
    select distinct Song
    from Vocals)
order by Songs.Title;


USE `KATZENJAMMER`;
-- KATZENJAMMER-3
-- Report the title(s) of the song(s) that involved the largest number of different instruments played (if multiple songs, report the titles in alphabetical order).
select Songs.Title
from Songs 
join Instruments on Songs.SongId = Instruments.Song
group by Songs.Title
having Count(distinct Instruments.Instrument) = (
    select Max(InstrumentsInSong)
    from (
        select count(distinct Instruments.Instrument) as InstrumentsInSong
        from Songs 
        join Instruments on Songs.SongId = Instruments.Song
        group by Songs.SongId) as blah);


USE `KATZENJAMMER`;
-- KATZENJAMMER-4
-- Find the favorite instrument of each performer. Report the first name of the performer, the name of the instrument, and the number of songs on which the performer played that instrument. Sort in alphabetical order by the first name, then instrument.

with InstrumentCounts as (
    select Band.Id as BandmateId, Band.FirstName, Instruments.Instrument, count(Instruments.Instrument) as countInstruments
    from Band 
    join Instruments on Band.Id = Instruments.Bandmate
    group by Band.Id, Band.FirstName, Instruments.Instrument
), MaxInstruments as (
    select BandmateId, Max(countInstruments) as MaxCount
    from InstrumentCounts
    group by BandmateId)    
select ic.FirstName, ic.Instrument, ic.countInstruments 
from InstrumentCounts as ic 
join MaxInstruments as mi on ic.BandmateId = mi.BandmateId
where ic.countInstruments = mi.MaxCount
order by ic.FirstName, ic.Instrument;


USE `KATZENJAMMER`;
-- KATZENJAMMER-5
-- Find all instruments played ONLY by Anne-Marit. Report instrument names in alphabetical order.
select distinct Instruments.Instrument
from Instruments join Band on Band.Id = Instruments.Bandmate
where Band.FirstName = 'Anne-Marit' and not exists (
    select 1
    from Instruments as i join Band as b on b.Id = i.Bandmate
    where i.Instrument = Instruments.Instrument and b.FirstName != 'Anne-Marit');


USE `KATZENJAMMER`;
-- KATZENJAMMER-6
-- Report, in alphabetical order, the first name(s) of the performer(s) who played the largest number of different instruments.

with InstrumentCounts as (
    select Bandmate, count(distinct Instruments.Instrument) as countInstruments
    from Instruments
    group by Bandmate
), MaxInstruments as (
    select  Max(countInstruments) as MaxCount
    from InstrumentCounts
)    
    
select Band.FirstName
from Band  
join InstrumentCounts as ic on Band.Id = ic.Bandmate
join MaxInstruments as mi on ic.countInstruments = mi.MaxCount
order by Band.FirstName;


USE `KATZENJAMMER`;
-- KATZENJAMMER-7
-- Which instrument(s) was/were played on the largest number of songs? Report just the names of the instruments, sorted alphabetically (note, you are counting number of songs on which an instrument was played, make sure to not count two different performers playing same instrument on the same song twice).
With InstrumentSongCount as (
    select distinct Song, Instrument
    from Instruments),
InstrumentCounts as (
    select Instrument, count(Song) as countSong
    from InstrumentSongCount
    group by Instrument
), MaxInstruments as (
    select  Max(countSong) as MaxCount
    from InstrumentCounts
)      
select Instrument
from InstrumentCounts
where countSong = (select MaxCount from MaxInstruments)
order by Instrument;


USE `KATZENJAMMER`;
-- KATZENJAMMER-8
-- Who spent the most time performing in the center of the stage (in terms of number of songs on which she was positioned there)? Return just the first name of the performer(s), sorted in alphabetical order.

with PerformanceCounts as (
    select Bandmate, count(distinct Song) as countPerformance
    from Performance
    where StagePosition = 'center'
    group by Bandmate
), MaxPerformance as (
    select  Max(countPerformance) as MaxCount
    from PerformanceCounts
)    
    
select Band.FirstName
from Band  
join PerformanceCounts as ic on Band.Id = ic.Bandmate
where countPerformance = (select MaxCount from MaxPerformance)
order by Band.FirstName;


