-- Lab 5
-- kcarri14
-- Feb 20, 2025

USE `BAKERY`;
-- BAKERY-1
-- For each flavor which is found in more than two types of items offered at the bakery, report the flavor, the average price (rounded to the nearest penny) of an item of this flavor, and the total number of different items of this flavor on the menu. Sort the output in ascending order by the average price.
SELECT Flavor, ROUND(AVG(Price), 2) as AvgPrice, Count(DISTINCT Food) as DistinctItems
FROM goods
GROUP BY Flavor
HAVING Count(DISTINCT Food) > 2
ORDER BY AvgPrice
;


USE `BAKERY`;
-- BAKERY-2
-- Find the total amount of money the bakery earned in October 2007 from selling eclairs. Report just the amount.
SELECT ROUND(SUM(Price),2)
FROM goods 
    join items on goods.GId = items.Item  and goods.Food = "Eclair"
    join receipts on items.Receipt = receipts.RNumber
;


USE `BAKERY`;
-- BAKERY-3
-- For each visit by NATACHA STENZ output the receipt number, sale date, total number of items purchased, and amount paid, rounded to the nearest penny. Sort by the amount paid, greatest to least.
SELECT distinct receipts.RNumber, receipts.SaleDate, COUNT(items.Item), Round(SUM(goods.Price),2) as TotalPrice
FROM customers 
    join receipts on receipts.Customer = customers.CId and customers.LastName = 'STENZ' and customers.FirstName = "NATACHA"
    join items on receipts.RNumber = items.Receipt
    join goods on items.Item = goods.GID
GROUP BY receipts.RNumber, receipts.SaleDate
Order by TotalPrice DESC;


USE `BAKERY`;
-- BAKERY-4
-- For the week starting October 8, report the day of the week (Monday through Sunday), the date, total number of purchases (receipts), the total number of pastries purchased, and the overall daily revenue rounded to the nearest penny. Report results in chronological order.
SELECT DAYNAME(SaleDate), SaleDate, Count( DISTINCT items.Receipt), Count(items.Item), ROUND(SUM(goods.Price), 2)
FROM receipts 
    join items on items.Receipt = receipts.RNumber
    join goods on items.Item = goods.GID
WHERE SaleDate >= '2007-10-08' and SaleDate <= '2007-10-14'
GROUP BY SaleDate
ORDER BY SaleDate
;


USE `BAKERY`;
-- BAKERY-5
-- Report all dates on which fewer than three tarts were purchased, sorted in chronological order.
SELECT SaleDate
FROM receipts
    join items on items.Receipt = receipts.RNumber
    join goods on goods.GId = items.Item and goods.Food = 'tart'
GROUP BY SaleDate
Having Count(items.Item) < 3
ORDER BY SaleDate
;


USE `STUDENTS`;
-- STUDENTS-1
-- Report the last and first names of teachers who have between seven and eight (inclusive) students in their classrooms. Sort output in alphabetical order by the teacher's last name.
SELECT teachers.Last, teachers.First
FROM teachers natural join list
GROUP BY teachers.classroom
Having Count(teachers.classroom) BETWEEN 7 and 8
ORDER BY teachers.Last;


USE `STUDENTS`;
-- STUDENTS-2
-- For each grade, report the grade, the number of classrooms in which it is taught, and the total number of students in the grade. Sort the output by the number of classrooms in descending order, then by grade in ascending order.

SELECT list.grade, COUNT(Distinct list.classroom) as classroomCount, Count(list.classroom)
FROM list
GROUP BY list.grade
Order By classroomCount DESC,  list.grade ASC;


USE `STUDENTS`;
-- STUDENTS-3
-- For each Kindergarten (grade 0) classroom, report classroom number along with the total number of students in the classroom. Sort output in the descending order by the number of students.
SELECT list.classroom, Count(list.classroom) as students
FROM list 
where list.grade = 0
GROUP BY list.classroom
Order by students DESC;


USE `STUDENTS`;
-- STUDENTS-4
-- For each fourth grade classroom, report the classroom number and the last name of the student who appears last (alphabetically) on the class roster. Sort output by classroom.
SELECT list.classroom, MAX(list.LastName) as students
FROM list 
where list.grade = 4
GROUP BY list.classroom
Order by list.classroom;


USE `AIRLINES`;
-- AIRLINES-1
-- Find all airports with exactly 19 outgoing flights. Report airport code, the full name of the airport, and the number of different airlines that have outgoing flights from the airport. Sort in alphabetical order by airport code.
SELECT airports.Code, airports.Name, Count(distinct flights.airline)
FROM airports join flights on airports.Code = flights.Destination
Group by airports.Code
Having Count(flights.Destination) = 19
Order by airports.Code;


USE `AIRLINES`;
-- AIRLINES-2
-- Find the number of airports from which airport APN can be reached with exactly one transfer. Make sure to exclude APN itself from the count. Report just the number.
SELECT Count(distinct F1.source)
FROM flights as F1 join flights as F2 on F1.Destination = F2.Source
Where F2.Destination = 'APN' and F1.Source != 'APN';


USE `AIRLINES`;
-- AIRLINES-3
-- Find the number of airports from which airport AET can be reached with at most one transfer. Make sure to exclude AET itself from the count. Report just the number.
SELECT Count(distinct F1.source)
FROM flights as F1 join flights as F2 on F1.Destination = F2.Source
Where (F2.Destination = 'AET' or F1.Destination = 'AET') and F1.Source != 'AET';


USE `AIRLINES`;
-- AIRLINES-4
-- For each airline, report the total number of airports from which it has at least one outgoing flight. Report the full name of the airline and the number of airports computed. Report the results sorted by the number of airports in descending order. In case of tie, sort by airline name A-Z.
SELECT airlines.Name, Count(distinct flights.Source) as NumAirports
FROM flights 
join airlines  on flights.Airline =  airlines.Id 
Group by airlines.Name
Order by NumAirports DESC, airlines.Name ASC
;


USE `CSU`;
-- CSU-1
-- For each campus that averaged more than $2,500 in fees between the years 2000 and 2005 (inclusive), report the campus name and total of fees for this six year period. Sort in ascending order by fee.
SELECT campuses.Campus, SUM(fees.fee) as AverageFee
FROM campuses join fees on campuses.Id = fees.CampusId
Where fees.Year between 2000 and 2005
Group by campuses.Campus
Having AVG(fees.fee) > 2500 
Order by AverageFee ASC
;


USE `CSU`;
-- CSU-2
-- For each campus for which data exists for more than 60 years, report the campus name along with the average, minimum and maximum enrollment (over all years). Sort your output by average enrollment.
SELECT campuses.Campus, AVG(enrollments.Enrolled) as Average, MIN(enrollments.Enrolled), MAX(enrollments.Enrolled)
FROM campuses join enrollments on campuses.Id = enrollments.CampusId
GROUP BY campuses.Campus
Having COUNT(enrollments.Year) > 60
ORDER BY Average
;


USE `CSU`;
-- CSU-3
-- For each campus in LA and Orange counties report the campus name and total number of degrees granted between 1998 and 2002 (inclusive). Sort the output in descending order by the number of degrees.

SELECT campuses.Campus, SUM(degrees.degrees) as totaldegrees
FROM campuses join degrees on campuses.Id = degrees.CampusId
WHERE campuses.County IN ('Los Angeles', 'Orange') and degrees.year BETWEEN 1998 and 2002
GROUP BY campuses.Campus
ORDER BY totaldegrees DESC
;


USE `CSU`;
-- CSU-4
-- For each campus that had more than 20,000 enrolled students in 2004, report the campus name and the number of disciplines for which the campus had non-zero graduate enrollment. Sort the output in alphabetical order by the name of the campus. (Exclude campuses that had no graduate enrollment at all.)
SELECT campuses.Campus, COUNT(discEnr.Discipline) as numDisciplines
FROM campuses 
    join enrollments on campuses.Id = enrollments.CampusId 
    join discEnr on campuses.Id = discEnr.CampusId
WHERE enrollments.Year = 2004 
    and enrollments.Enrolled > 20000 
    and discEnr.Year = 2004 
    and discEnr.Gr > 0
GROUP BY campuses.Campus
ORDER BY campuses.Campus
;


USE `INN`;
-- INN-1
-- For each room, report the full room name, total revenue (number of nights times per-night rate), and the average revenue per stay. In this summary, include only those stays that began in the months of September, October and November of calendar year 2010. Sort output in descending order by total revenue. Output full room names.
SELECT rooms.RoomName, SUM(DATEDIFF(reservations.CheckIn, reservations.Checkout) * reservations.Rate * -1) as SumReservation, 
ROUND(AVG(DATEDIFF(reservations.CheckIn, reservations.Checkout) * reservations.Rate * -1), 2) as AvgReservation
FROM rooms join reservations on rooms.RoomCode = reservations.Room
WHERE reservations.CheckIn BETWEEN '2010-09-01' AND '2010-11-30'
GROUP BY rooms.RoomName
ORDER BY SumReservation DESC;


USE `INN`;
-- INN-2
-- Report the total number of reservations that ended on Fridays, and the total revenue they brought in.
SELECT COUNT(*), SUM(DATEDIFF(reservations.CheckIn, reservations.Checkout) * reservations.Rate * -1)
FROM reservations
WHERE DAYOFWEEK(reservations.CheckOut) = 6;


USE `INN`;
-- INN-3
-- List each day of the week. For each day, compute the total number of reservations that began on that day, and the total revenue for these reservations. Report days of week as Monday, Tuesday, etc. Order days from Sunday to Saturday.
SELECT DAYNAME(reservations.CheckIn) as Day, COUNT(*), SUM(DATEDIFF(reservations.CheckIn, reservations.Checkout) * reservations.Rate * -1) as SumTotal
FROM reservations
GROUP BY Day
ORDER BY FIELD(Day, 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');


USE `INN`;
-- INN-4
-- For each room list full room name and report the highest markup against the base price and the largest markdown (discount). Report markups and markdowns as the signed difference between the base price and the rate. Sort output in descending order beginning with the largest markup. In case of identical markup/down sort by room name A-Z. Report full room names.
SELECT rooms.RoomName, Max( reservations.Rate - rooms.basePrice ) as MarkUp, Min( reservations.Rate - rooms.basePrice ) as MarkDown
FROM rooms join reservations on rooms.RoomCode = reservations.Room
GROUP BY rooms.RoomName
ORDER BY MarkUp DESC, rooms.roomName;


USE `INN`;
-- INN-5
-- For each room report how many nights in calendar year 2010 the room was occupied. Report the room code, the full name of the room, and the number of occupied nights. Sort in descending order by occupied nights. (Note: this should be number of nights during 2010. Some reservations extend beyond December 31, 2010. The ”extra” nights in 2011 must be deducted).
SELECT rooms.RoomCode, rooms.RoomName, SUM(DATEDIFF(LEAST(reservations.CheckOut, '2010-12-31'), GREATEST(reservations.CheckIn, '2010-01-01' )) ) + 1 as Nights
FROM rooms join reservations on rooms.RoomCode = reservations.Room
WHERE reservations.CheckOut > '2010-01-01' and reservations.CheckIn < '2011-01-01'
GROUP BY rooms.RoomCode, rooms.RoomName
ORDER BY Nights DESC;


USE `KATZENJAMMER`;
-- KATZENJAMMER-1
-- For each performer, report first name and how many times she sang lead vocals on a song. Sort output in descending order by the number of leads. In case of tie, sort by performer first name (A-Z.)
SELECT Band.Firstname as BandName, COUNT(Vocals.VocalType) as Voc
FROM Band join Vocals on Band.Id = Vocals.Bandmate
WHERE Vocals.VocalType = 'lead'
GROUP BY BandName
ORDER BY Voc DESC;


USE `KATZENJAMMER`;
-- KATZENJAMMER-2
-- Report how many different instruments each performer plays on songs from the album 'Le Pop'. Include performer's first name and the count of different instruments. Sort the output by the first name of the performers.
SELECT Band.Firstname as BandName, COUNT(distinct Instruments.Instrument) as Instru
FROM Albums 
    join Tracklists on Albums.AId = Tracklists.Album 
    join Songs on Songs.SongId = Tracklists.Song
    join Instruments on Instruments.Song = Songs.SongId
    join Band on Band.Id = Instruments.Bandmate
WHERE Albums.Title = 'Le Pop'
GROUP BY BandName
ORDER BY BandName;


USE `KATZENJAMMER`;
-- KATZENJAMMER-3
-- List each stage position along with the number of times Turid stood at each stage position when performing live. Sort output in ascending order of the number of times she performed in each position.

SELECT Performance.StagePosition as Perform, COUNT(Performance.StagePosition) as StagePos
FROM
    Performance join Band on Band.Id = Performance.Bandmate
WHERE Band.Firstname = 'Turid'
GROUP BY Perform
ORDER BY StagePos ASC;


USE `KATZENJAMMER`;
-- KATZENJAMMER-4
-- Report how many times each performer (other than Anne-Marit) played bass balalaika on the songs where Anne-Marit was positioned on the left side of the stage. List performer first name and a number for each performer. Sort output alphabetically by the name of the performer.

SELECT B1.Firstname as BandName, COUNT(*) as Instru
FROM Instruments 
    join Band as B1 on B1.Id = Instruments.Bandmate
    join Performance on Performance.Song = Instruments.Song
    join Band as B2 on  B2.Id = Performance.Bandmate 
WHERE Instruments.Instrument = 'bass balalaika' 
    and B1.Firstname != 'Anne-Marit' 
    and B2.Firstname = 'Anne-Marit'
    and Performance.StagePosition = 'left' 
GROUP BY BandName
ORDER BY BandName;


USE `KATZENJAMMER`;
-- KATZENJAMMER-5
-- Report all instruments (in alphabetical order) that were played by three or more people.
SELECT Instruments.Instrument as Instru
FROM Instruments
GROUP BY Instru
Having COUNT(distinct Instruments.Bandmate) >= 3
ORDER BY Instru ASC;


USE `KATZENJAMMER`;
-- KATZENJAMMER-6
-- For each performer, list first name and report the number of songs on which they played more than one instrument. Sort output in alphabetical order by first name of the performer
SELECT Band.Firstname as BandName, COUNT(distinct i1.Song) as MultiInstru
FROM Band 
    join Instruments as i1 on Band.Id = i1.Bandmate
    join Instruments as i2 on i1.Song = i2.Song and i1.Bandmate = i2.Bandmate and i1.Instrument != i2.Instrument
GROUP BY Band.Firstname

ORDER BY Band.Firstname;


USE `MARATHON`;
-- MARATHON-1
-- List each age group and gender. For each combination, report total number of runners, the overall place of the best runner and the overall place of the slowest runner. Output result sorted by age group and sorted by gender (F followed by M) within each age group.
SELECT AgeGroup, Sex, Count(AgeGroup), MIN(Place), MAX(Place)
FROM marathon
GROUP BY AgeGroup, Sex
ORDER BY AgeGroup, Sex;


USE `MARATHON`;
-- MARATHON-2
-- Report the total number of gender/age groups for which both the first and the second place runners (within the group) are from the same state.
SELECT COUNT(Distinct m1.AgeGroup)
FROM marathon as m1  join marathon as m2 on m1.AgeGroup = m2.AgeGroup
WHERE m1.GroupPlace = 1 
    and m2.GroupPlace = 2 
    and m1.State =m2.State
    and m1.Sex = m2.Sex;


USE `MARATHON`;
-- MARATHON-3
-- For each full minute, report the total number of runners whose pace was between that number of minutes and the next. In other words: how many runners ran the marathon at a pace between 5 and 6 mins, how many at a pace between 6 and 7 mins, and so on.
SELECT Floor(TIME_TO_SEC(Pace)/60) as MarathonPace, Count(Pace)
FROM marathon
GROUP BY MarathonPace;


USE `MARATHON`;
-- MARATHON-4
-- For each state with runners in the marathon, report the number of runners from the state who finished in top 10 in their gender-age group. If a state did not have runners in top 10, do not output information for that state. Report state code and the number of top 10 runners. Sort in descending order by the number of top 10 runners, then by state A-Z.
SELECT State, Count(*) as Top10
FROM marathon
WHERE GroupPlace <= 10
GROUP BY State
ORDER BY Top10 DESC, State;


USE `MARATHON`;
-- MARATHON-5
-- For each Connecticut town with three or fewer participants in the race, report the town name and average time of its runners in the race computed in seconds. Output the results sorted by the average time (lowest average time first).
SELECT Town, ROUND(AVG(TIME_TO_SEC(RunTime)),1) as AvgRun
FROM marathon
WHERE State = 'CT'
GROUP BY Town
Having Count(Firstname) <= 3
ORDER BY AvgRun;

