import Link from 'next/link';
export default function Job1() {
    let yearList = [{
        year: 2021,
        position: "Shooting Sports CIT",
        description: "I worked at the Rifle/Pistol Range helping out the staff and scouts",
        duties: "Refilling bullet boxes, heling scouts aim and shoot the score them needed, serve food at the dining hall, leading troops throughout the week, and providing customer service when needed "
      },{
        year: 2022,
        position: "Archery Staff",
        description: "I worked at the Archery range as a staff who helped the archery director.",
        duties: "Lead classes, fix arrows and targets, watch the range, make sure safety protocols were followed, serve food at the dining hall, leading troops throughout the week, and providing customer service when needed "
      },{
        year: 2023,
        position: "Archery Staff",
        description: "I worked at the Archery range as a staff who helped the archery director.",
        duties: "Lead classes, fix arrows and targets, watch the range, make sure safety protocols were followed, serve food at the dining hall, leading troops throughout the week, and providing customer service when needed" 
      },{
        year: 2024,
        position: "Archery Director",
        description: "I worked at the Archery range as director who was in charge of the archery range and staff who were working on the range.",
        duties: "Teach classes, watch the range, make sure safety protocols were followed, make sure my staff were ok mentally, physically and emotionally, in charge of my patrol of staff that made sure that other camp duties were being done, serve food at the dining hall, leading troops throughout the week, and providing customer service when needed "
      }];
    
      let YearHtml = yearList.map((year) =>{
        return (<li>
          <span><b>Year: </b>{year.year}</span>
          <span><p><b>Position: </b>{year.position}</p></span>
          <span><p><b>Description: </b>{year.description}</p></span>
          <span><p><b>Duties: </b>{year.duties}</p></span>
        </li>);
      });
  return (
    <div >
      <h1><p style={{textAlign: "center"}}><b>Kaitlyn Carrillo</b></p></h1>
      <p style = {{textAlign: "center"}}>(951)-445-1816 | kgcarrillo05@gmail.com | https://github.com/kcarri14/Kaitlyns-Class-projects</p>
      <img src="IMG_6047.jpeg" alt="SSRLV"></img>
      <h2><p style = {{textAlign: "Center"}}><b>Archery Staff/Director at Schoepe Scout Reservation at Lost Valley</b></p></h2>
      <p>Being a part of the amazing Lost Valley staff has changed my life for the better. I have learned leadership skills, communication skills, time management skills, and managerial skills. Being a summer camp counselor has helped me developed into the person I am today.</p>
        <ul>
            {YearHtml}
        </ul>
      <h4><p style = {{textAlign: "Right"}}><Link href="/"> back </Link></p></h4>

    </div>
  );
}