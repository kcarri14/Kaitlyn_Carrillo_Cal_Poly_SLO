import Link from 'next/link';
export default function Job1() {
  return (
    <div >
      <h1><p style={{textAlign: "center"}}><b>Kaitlyn Carrillo</b></p></h1>
      <p style = {{textAlign: "center"}}>(951)-445-1816 | kgcarrillo05@gmail.com | https://github.com/kcarri14/Kaitlyns-Class-projects</p>

      <h2><p style = {{textAlign: "Center"}}><b>Audio Visual Technician for Cal Poly ASI</b></p></h2>
      <p>MCTSSA is the Marine Corps Tactical System Support Activity which is based in Camp Pendleton, CA. MCTSSA is the first Science and Tech Reinvention Lab within the Marine Corp. STRLs are empowered with legsilative authories, including personnel flexibility, minor military construction capabilites, and discretioonary funding control for their directors. </p>
        <ul>
          <p>Dates: June 2025 - September 2025</p> 
          <p>Duties: TBD </p>
        </ul>
      <h4><p style = {{textAlign: "Right"}}><Link href="/"> back </Link></p></h4>

    </div>
  );
}