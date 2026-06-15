-- Lab 4
-- kcarri14
-- Feb 8, 2025

USE `STUDENTS`;
-- STUDENTS-1
-- Find all students who study in classroom 111. For each student list first and last name. Sort the output by the last name of the student.
SELECT FirstName, LastName
FROM list
WHERE classroom = '111'
ORDER BY LastName
;


USE `STUDENTS`;
-- STUDENTS-2
-- For each classroom report the grade that is taught in it. Report just the classroom number and the grade number. Sort output by classroom in descending order.
SELECT DISTINCT classroom, grade
FROM list
ORDER BY classroom DESC
;


USE `STUDENTS`;
-- STUDENTS-3
-- Find all teachers who teach fifth grade. Report first and last name of the teachers and the room number. Sort the output by room number.
SELECT DISTINCT First, Last, classroom
FROM teachers natural join list
WHERE grade = 5
ORDER BY classroom
;



USE `STUDENTS`;
-- STUDENTS-4
-- Find all students taught by OTHA MOYER. Output first and last names of students sorted in alphabetical order by their last name.
SELECT FirstName, LastName
FROM teachers natural join list
WHERE First = 'OTHA' AND Last = 'MOYER'
ORDER BY LastName
;


USE `STUDENTS`;
-- STUDENTS-5
-- For each teacher teaching grades K through 3, report the grade (s)he teaches. Output teacher last name, first name, and grade. Each name has to be reported exactly once. Sort the output by grade and alphabetically by teacher’s last name for each grade.
SELECT DISTINCT Last, First, grade
FROM teachers natural join list
WHERE grade = 0 OR grade = 1 OR grade =2 Or grade = 3
ORDER BY grade, Last
;


USE `BAKERY`;
-- BAKERY-1
-- Find all chocolate-flavored items on the menu whose price is under $5.00. For each item output the flavor, the name (food type) of the item, and the price. Sort your output in descending order by price.
SELECT DISTINCT Flavor, Food, Price
FROM goods
WHERE price < 5 and Flavor = 'Chocolate'
ORDER BY Price DESC
;


USE `BAKERY`;
-- BAKERY-2
-- Report the prices of the following items (a) any cookie priced above $1.10, (b) any lemon-flavored items, or (c) any apple-flavored item except for the pie. Output the flavor, the name (food type) and the price of each pastry. Sort the output in alphabetical order by the flavor and then pastry name.
SELECT DISTINCT Flavor, Food, Price
FROM goods
WHERE (price > 1.10 and Food = 'Cookie') or (Flavor = 'Lemon') or (Flavor = 'Apple' and not Food = 'pie')
ORDER BY Flavor, Food
;


USE `BAKERY`;
-- BAKERY-3
-- Find all customers who made a purchase on October 3, 2007. Report the name of the customer (last, first). Sort the output in alphabetical order by the customer’s last name. Each customer name must appear at most once.
SELECT DISTINCT LastName, FirstName
FROM customers natural join receipts
WHERE receipts.Customer = customers.CId and SaleDate ='2007-10-03'
ORDER BY LastName
;


USE `BAKERY`;
-- BAKERY-4
-- Find all different cakes purchased on October 4, 2007. Each cake (flavor, food) is to be listed once. Sort output in alphabetical order by the cake flavor.
SELECT DISTINCT Flavor, Food
FROM (items join receipts on items.Receipt = receipts.RNumber) join goods on items.Item = goods.GID
WHERE receipts.SaleDate ='2007-10-04' and goods.Food = 'Cake'
ORDER BY Flavor
;


USE `BAKERY`;
-- BAKERY-5
-- List all purchases by ARIANE CRUZEN on October 25, 2007. For each item purchased, specify its flavor and type, as well as the price. Output the pastries in the order in which they appear on the receipt (each item needs to appear the number of times it was purchased).
SELECT DISTINCT Flavor, Food, Price
FROM customers join receipts on customers.CId = receipts.Customer join items on receipts.RNumber = items.Receipt join goods on goods.GId = items.Item 
WHERE receipts.SaleDate ='2007-10-25' and customers.LastName = 'CRUZEN' and customers.FirstName = 'ARIANE'
;


USE `BAKERY`;
-- BAKERY-6
-- Find all types of cookies purchased by KIP ARNN during the month of October of 2007. Report each cookie type (flavor, food type) exactly once in alphabetical order by flavor.

SELECT DISTINCT Flavor, Food
FROM customers join receipts on customers.CId = receipts.Customer join items on receipts.RNumber = items.Receipt join goods on goods.GId = items.Item 
WHERE receipts.SaleDate between '2007-10-01'and '2007-10-31' and customers.LastName = 'ARNN' and customers.FirstName = 'KIP' and goods.Food = 'cookie'
;


USE `CSU`;
-- CSU-1
-- Report all campuses from Los Angeles county. Output the full name of campus in alphabetical order.
SELECT Campus
FROM campuses
WHERE County = 'Los Angeles'
ORDER BY Campus
;


USE `CSU`;
-- CSU-2
-- For each year between 1994 and 2000 (inclusive) report the number of students who graduated from California Maritime Academy Output the year and the number of degrees granted. Sort output by year.
SELECT degrees.Year, degrees
FROM campuses join degrees on campuses.Id = degrees.CampusId
WHERE Campus = 'California Maritime Academy' and degrees.Year Between 1994 and 2000
ORDER BY Year
;


USE `CSU`;
-- CSU-3
-- Report undergraduate and graduate enrollments (as two numbers) in ’Mathematics’, ’Engineering’ and ’Computer and Info. Sciences’ disciplines for both Polytechnic universities of the CSU system in 2004. Output the name of the campus, the discipline and the number of graduate and the number of undergraduate students enrolled. Sort output by campus name, and by discipline for each campus.
SELECT campuses.Campus, disciplines.Name, discEnr.Gr, discEnr.Ug
FROM (campuses join discEnr on campuses.Id = discEnr.CampusId) join disciplines on disciplines.Id = discEnr.Discipline
WHERE campuses.Campus IN ('California Polytechnic State University-San Luis Obispo','California State Polytechnic University-Pomona') and discEnr.Year = 2004 and disciplines.Name IN ('Mathematics','Engineering', 'Computer and Info. Sciences')
ORDER BY campuses.Campus, disciplines.Name
;


USE `CSU`;
-- CSU-4
-- Report graduate enrollments in 2004 in ’Agriculture’ and ’Biological Sciences’ for any university that offers graduate studies in both disciplines. Report one line per university (with the two grad. enrollment numbers in separate columns), sort universities in descending order by the number of ’Agriculture’ graduate students.
SELECT distinct campuses.Campus, D.Gr , D2.Gr
FROM discEnr as D 
join discEnr as D2 on D.CampusId = D2.CampusId and D.Year = D2.Year
join disciplines on D.Discipline = disciplines.Id 
join campuses on D.CampusId = campuses.Id
WHERE (D.Year = 2004 and D2.Year = 2004) and (D.Discipline = 1 and D2.Discipline = 4) and D.Gr != 0
ORDER BY D.Gr DESC
;


USE `CSU`;
-- CSU-5
-- Find all disciplines and campuses where graduate enrollment in 2004 was at least three times higher than undergraduate enrollment. Report campus names, discipline names, and both enrollment counts. Sort output by campus name, then by discipline name in alphabetical order.
SELECT distinct campuses.Campus, disciplines.Name, discEnr.Ug, discEnr.Gr
FROM discEnr 
join campuses on discEnr.CampusId = campuses.Id
join disciplines on discEnr.discipline = disciplines.Id
WHERE discEnr.Year = '2004' and discEnr.Gr >= 3 * discEnr.Ug
ORDER BY campuses.Campus, disciplines.Name
;


USE `CSU`;
-- CSU-6
-- Report the amount of money collected from student fees (use the full-time equivalent enrollment for computations) at ’Fresno State University’ for each year between 2002 and 2004 inclusively, and the amount of money (rounded to the nearest penny) collected from student fees per each full-time equivalent faculty. Output the year, the two computed numbers sorted chronologically by year.
SELECT distinct fees.year, fees.fee * enrollments.FTE as collected, ROUND((fees.fee * enrollments.FTE) / faculty.FTE, 2) as per
FROM fees
join enrollments on fees.CampusId = enrollments.CampusId and fees.Year = enrollments.Year
join faculty on fees.CampusId = faculty.CampusId and fees.Year = faculty.Year
join campuses on fees.CampusId = campuses.Id
WHERE campuses.Campus = 'Fresno State University' and fees.year Between 2002 and 2004
ORDER BY fees.year
;


USE `CSU`;
-- CSU-7
-- Find all campuses where enrollment in 2003 (use the FTE numbers), was higher than the 2003 enrollment in ’San Jose State University’. Report the name of campus, the 2003 enrollment number, the number of faculty teaching that year, and the student-to-faculty ratio, rounded to one decimal place. Sort output in ascending order by student-to-faculty ratio.
SELECT campuses.Campus, enrollments.FTE, faculty.FTE, ROUND(enrollments.FTE / faculty.FTE, 1) as ratio
FROM campuses
join enrollments on campuses.Id = enrollments.CampusId and enrollments.Year = 2003
join faculty on campuses.Id = faculty.CampusId and faculty.Year = 2003
join enrollments as SJ on SJ.Year = 2003
join campuses as SJ_C on SJ_C.Id = SJ.CampusId
WHERE SJ_C.campus = 'San Jose State University' and enrollments.FTE > SJ.FTE
ORDER BY ratio
;


USE `INN`;
-- INN-1
-- Find all modern rooms with a base price below $160 and two beds. Report room code and full room name, in alphabetical order by the code.
SELECT RoomCode, RoomName
FROM rooms 
WHERE basePrice < 160 and Beds = 2 and decor = 'modern'
ORDER BY RoomCode
;


USE `INN`;
-- INN-2
-- Find all July 2010 reservations (a.k.a., all reservations that both start AND end during July 2010) for the ’Convoke and sanguine’ room. For each reservation report the last name of the person who reserved it, checkin and checkout dates, the total number of people staying and the daily rate. Output reservations in chronological order.
SELECT DISTINCT reservations.LastName, reservations.CheckIn, reservations.CheckOut, reservations.Adults + reservations.Kids AS Guests, reservations.Rate
FROM rooms join reservations on reservations.Room = rooms.RoomCode
WHERE (CheckIn BETWEEN '2010-07-01' AND '2010-07-31') and (CheckOut BETWEEN '2010-07-01' AND '2010-07-31') and  RoomName = 'Convoke and sanguine'
ORDER BY reservations.CheckIN
;


USE `INN`;
-- INN-3
-- Find all rooms occupied on February 6, 2010. Report full name of the room, the check-in and checkout dates of the reservation. Sort output in alphabetical order by room name.
SELECT DISTINCT rooms.RoomName, reservations.CheckIn, reservations.CheckOut
FROM rooms join reservations on rooms.roomCode = reservations.Room
WHERE ('2010-02-06' BETWEEN reservations.CheckIn AND reservations.CheckOut) AND not reservations.CheckOut = '2010-02-06'
ORDER BY rooms.RoomName
;


USE `INN`;
-- INN-4
-- For each stay by GRANT KNERIEN in the hotel, calculate the total amount of money, he paid. Report reservation code, room name (full), checkin and checkout dates, and the total stay cost. Sort output in chronological order by the day of arrival.

SELECT reservations.CODE, rooms.RoomName, reservations.CheckIn, reservations.CheckOut, DATEDIFF(reservations.CheckOut, reservations.CheckIn) * reservations.Rate AS PAID
FROM rooms join reservations on rooms.roomCode = reservations.Room
WHERE reservations.FirstName = 'GRANT' and reservations.LastName = 'KNERIEN'
ORDER BY reservations.CheckIn
;


USE `INN`;
-- INN-5
-- For each reservation that starts on December 31, 2010 report the room name, nightly rate, number of nights spent and the total amount of money paid. Sort output in descending order by the number of nights stayed.
SELECT rooms.RoomName, reservations.Rate, DATEDIFF(reservations.CheckOut, reservations.CheckIn) AS Nights, DATEDIFF(reservations.CheckOut, reservations.CheckIn) * reservations.Rate AS Money
FROM rooms join reservations on rooms.roomCode = reservations.Room
WHERE reservations.CheckIn = '2010-12-31'
ORDER BY Nights DESC
;


USE `INN`;
-- INN-6
-- Report all reservations in rooms with double beds that contained four adults. For each reservation report its code, the room abbreviation, full name of the room, check-in and check out dates. Report reservations in chronological order, then sorted by the three-letter room code (in alphabetical order) for any reservations that began on the same day.
SELECT reservations.CODE, reservations.Room,rooms.RoomName, reservations.CheckIn, reservations.CheckOut
FROM rooms join reservations on rooms.roomCode = reservations.Room
WHERE rooms.bedType = 'double' and reservations.Adults = 4
ORDER BY reservations.CheckIn ASC , reservations.Room
;


USE `MARATHON`;
-- MARATHON-1
-- Report the overall place, running time, and pace of TEDDY BRASEL.
SELECT Place, RunTime, Pace
FROM marathon
WHERE FirstName = 'TEDDY' and LastName = 'BRASEL'
;


USE `MARATHON`;
-- MARATHON-2
-- Report names (first, last), overall place, running time, as well as place within gender-age group for all female runners from QUNICY, MA. Sort output by overall place in the race.
SELECT FirstName, LastName, Place, RunTime, GroupPlace
FROM marathon
WHERE (Town = 'QUNICY' and State = 'MA') and Sex = 'F'
ORDER BY Place ASC
;


USE `MARATHON`;
-- MARATHON-3
-- Find the results for all 34-year old female runners from Connecticut (CT). For each runner, output name (first, last), town and the running time. Sort by time.
SELECT FirstName, LastName, Town, RunTime
FROM marathon
WHERE Age = 34 and Sex = 'F' and State = 'CT'
ORDER BY RunTime
;


USE `MARATHON`;
-- MARATHON-4
-- Find all duplicate bibs in the race. Report just the bib numbers. Sort in ascending order of the bib number. Each duplicate bib number must be reported exactly once.
SELECT DISTINCT M.BibNumber
FROM marathon AS M, marathon as M1
WHERE M.BibNumber = M1.BibNumber and M.FirstName != M1.FirstName
ORDER BY M.BibNumber
;




USE `MARATHON`;
-- MARATHON-5
-- List all runners who took first place and second place in their respective age/gender groups. List gender, age group, name (first, last) and age for both the winner and the runner up (in a single row). Include only age/gender groups with both a first and second place runner. Order the output by gender, then by age group.
SELECT M1.Sex, M2.AgeGroup, M1.FirstName, M1.LastName, M1.Age, M2.FirstName, M2.LastName, M2.Age
FROM marathon as M1 join marathon as M2 on M1.Sex = M2.Sex and M1.AgeGroup = M2.AgeGroup
WHERE M1.GroupPlace = 1 and M2.GroupPlace = 2
ORDER BY Sex, AgeGroup
;


USE `AIRLINES`;
-- AIRLINES-1
-- Find all airlines that have at least one flight out of AXX airport. Report the full name and the abbreviation of each airline. Report each name only once. Sort the airlines in alphabetical order.
SELECT distinct airlines.Name, airlines.Abbr
FROM airlines join flights on airlines.Id = flights.Airline
WHERE flights.Source = 'AXX' 
ORDER BY airlines.Name
;


USE `AIRLINES`;
-- AIRLINES-2
-- Find all destinations served from the AXX airport by Northwest. Re- port flight number, airport code and the full name of the airport. Sort in ascending order by flight number.

SELECT distinct flights.FlightNo, airports.Code, airports.Name
FROM airlines join flights on airlines.Id = flights.Airline join airports on airports.Code = flights.Destination
WHERE flights.Source = 'AXX' and airlines.Abbr = 'Northwest'
ORDER BY flights.FlightNo ASC
;


USE `AIRLINES`;
-- AIRLINES-3
-- Find all *other* destinations that are accessible from AXX on only Northwest flights with exactly one change-over. Report pairs of flight numbers, airport codes for the final destinations, and full names of the airports sorted in alphabetical order by the airport code.
SELECT flights.FlightNo, F2.FlightNo, F2.Destination, airports.Name
FROM flights 
join flights as F2 on flights.Destination = F2.Source
join airports on airports.Code = F2.Destination
WHERE flights.Source = 'AXX' and flights.Airline = 6 and F2.Airline = 6 and flights.Destination != F2.Destination and F2.Destination != 'AXX'
ORDER BY F2.Destination ASC
;


USE `AIRLINES`;
-- AIRLINES-4
-- Report all pairs of airports served by both Frontier and JetBlue. Each airport pair must be reported exactly once (if a pair X,Y is reported, then a pair Y,X is redundant and should not be reported).
SELECT distinct LEAST(F1.Source, F1.Destination), Greatest(F1.Source, F1.Destination)
FROM flights as F1
join flights as F2 on (F1.Source = F2.Source and F1.Destination = F2.Destination)
WHERE F1.Airline = 8 and F2.Airline = 9
;


USE `AIRLINES`;
-- AIRLINES-5
-- Find all airports served by ALL five of the airlines listed below: Delta, Frontier, USAir, UAL and Southwest. Report just the airport codes, sorted in alphabetical order.
SELECT distinct F1.Source
FROM flights as F1
join flights as F2 on F1.Source = F2.Source
join flights as F3 on F1.Source = F3.Source
join flights as F4 on F1.Source = F4.Source
join flights as F5 on F1.Source = F5.Source
WHERE F1.Airline = 3 
and F2.Airline = 9
and F3.Airline = 2
and F4.Airline = 1
and F5.Airline = 4
ORDER BY F1.Source
;


USE `AIRLINES`;
-- AIRLINES-6
-- Find all airports that are served by at least three Southwest flights. Report just the three-letter codes of the airports — each code exactly once, in alphabetical order.
SELECT distinct flights.Destination
FROM flights join airlines on flights.Airline = airlines.Id and airlines.Abbr = 'Southwest'
join flights as F2 
join airlines as A2 on F2.Airline = A2.Id and A2.Abbr = 'Southwest'
join flights as F3
join airlines as A3 on F3.Airline = A3.Id and A3.Abbr = 'Southwest'
WHERE flights.Destination = F2.Destination 
and flights.Destination = F3.Destination 
and F2.Destination = F3.Destination
and flights.Source != F2.Source
and flights.Source != F3.Source
and F2.Source != F3.Source
ORDER BY flights.Destination;


USE `KATZENJAMMER`;
-- KATZENJAMMER-1
-- Report, in order, the tracklist for ’Le Pop’. Output just the names of the songs in the order in which they occur on the album.
SELECT Songs.Title
FROM Tracklists join Albums on Tracklists.Album = Albums.AId join Songs on Tracklists.Song = Songs.SongId
WHERE Albums.Title = 'Le Pop'
ORDER BY Tracklists.Position
;


USE `KATZENJAMMER`;
-- KATZENJAMMER-2
-- List the instruments each performer plays on ’Mother Superior’. Output the first name of each performer and the instrument, sort alphabetically by the first name.
SELECT Band.Firstname, Instruments.Instrument
FROM Instruments join Band on Instruments.Bandmate = Band.Id join Songs on Instruments.Song = Songs.SongId
WHERE Songs.Title = 'Mother Superior'
ORDER BY Band.Firstname
;


USE `KATZENJAMMER`;
-- KATZENJAMMER-3
-- List all instruments played by Anne-Marit at least once during the performances. Report the instruments in alphabetical order (each instrument needs to be reported exactly once).
SELECT distinct Instruments.Instrument
FROM Instruments join Band on Instruments.Bandmate = Band.Id 
WHERE Band.Firstname = 'Anne-Marit'
ORDER BY Instruments.Instrument
;


USE `KATZENJAMMER`;
-- KATZENJAMMER-4
-- Find all songs that featured ukalele playing (by any of the performers). Report song titles in alphabetical order.
SELECT distinct Songs.Title
FROM Instruments join Songs on Instruments.Song = Songs.SongId 
WHERE Instruments.Instrument = 'ukalele'
ORDER BY Songs.Title
;


USE `KATZENJAMMER`;
-- KATZENJAMMER-5
-- Find all instruments Turid ever played on the songs where she sang lead vocals. Report the names of instruments in alphabetical order (each instrument needs to be reported exactly once).
SELECT distinct Instruments.Instrument
FROM Instruments join Vocals on Vocals.Song = Instruments.Song and Vocals.Bandmate = Instruments.Bandmate join Band on Instruments.Bandmate = Band.Id 
WHERE Band.Firstname = 'Turid' and Vocals.VocalType = 'lead'
ORDER BY Instruments.Instrument
;




USE `KATZENJAMMER`;
-- KATZENJAMMER-6
-- Find all songs where the lead vocalist is not positioned center stage. For each song, report the name, the name of the lead vocalist (first name) and her position on the stage. Output results in alphabetical order by the song, then name of band member. (Note: if a song had more than one lead vocalist, you may see multiple rows returned for that song. This is the expected behavior).
SELECT  Songs.Title, Band.Firstname, Performance.StagePosition
FROM Songs join Vocals on Songs.SongId = Vocals.Song join Band on Vocals.Bandmate = Band.Id join Performance on Vocals.Song = Performance.Song and Vocals.Bandmate = Performance.Bandmate 
WHERE Vocals.VocalType = 'lead' and (Performance.StagePosition != 'center' and Performance.StagePosition != 'back')
ORDER BY Songs.Title, Band.Firstname
;




USE `KATZENJAMMER`;
-- KATZENJAMMER-7
-- Find a song on which Anne-Marit played three different instruments. Report the name of the song. (The name of the song shall be reported exactly once)
SELECT distinct Songs.Title
FROM Instruments AS I1 
join Instruments AS I2 on I1.Song = I2.Song and I1.Bandmate = I2.Bandmate and I1.Instrument != I2.Instrument
join Instruments AS I3 on I1.Song = I3.Song and I1.Bandmate = I3.Bandmate and I1.Instrument != I3.Instrument and I2.Instrument != I3.Instrument
join Band on I1.Bandmate = Band.Id 
join Songs on I1.Song = Songs.SongId
WHERE Band.Firstname = 'Anne-Marit' 
;


USE `KATZENJAMMER`;
-- KATZENJAMMER-8
-- Report the positioning of the band during ’A Bar In Amsterdam’. (just one record needs to be returned with four columns (right, center, back, left) containing the first names of the performers who were staged at the specific positions during the song).
SELECT distinct
B1.Firstname AS `Right`, 
B2.Firstname AS Center, 
B3.Firstname AS Back, 
B4.Firstname AS `Left`
FROM Performance as P1
join Band as B1 on B1.Id = P1.Bandmate and P1.StagePosition = 'right'
join Performance as P2 ON P1.Song = P2.Song
join Band as B2 on B2.Id = P2.Bandmate and P2.StagePosition = 'center'
join Performance as P3 ON P1.Song = P3.Song
join Band as B3 on B3.Id = P3.Bandmate and P3.StagePosition = 'back'
join Performance as P4 ON P1.Song = P4.Song
join Band as B4 on B4.Id = P4.Bandmate and P4.StagePosition = 'left'
join Songs on P1.Song = Songs.SongId
WHERE Songs.Title = 'A Bar In Amsterdam' 
;


