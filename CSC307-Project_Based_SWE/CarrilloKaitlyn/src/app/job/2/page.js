import Link from 'next/link';
export default function Job1() {
  return (
    <div >
      <h1><p style={{textAlign: "center"}}><b>Kaitlyn Carrillo</b></p></h1>
      <p style = {{textAlign: "center"}}>(951)-445-1816 | kgcarrillo05@gmail.com | https://github.com/kcarri14/Kaitlyns-Class-projects</p>

      <h2><p style = {{textAlign: "Center"}}><b>Panda Express Worker for Cal Poly Dining</b></p></h2>
      <p>Working at Panda Express showed me the hard work and dedication needed to work in the food industry. I’ve learned customer service and time management during my time at Panda Express</p>
        <ul>
          <p>Dates: March 2024 - June 2024</p> 
          <p>Duties: Served food to customers, cleaned the kitchen before closing, interacted with cusomters in order to take their order, and lead/teach newer staff what to do </p>
        </ul>
      <h4><p style = {{textAlign: "Right"}}><Link href="/"> back </Link></p></h4>

    </div>
  );
}