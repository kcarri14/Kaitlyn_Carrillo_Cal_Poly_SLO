import Link from 'next/link';
export default function Job() {
  return (
    <div >
      <h1><p style={{textAlign: "center"}}><b>Kaitlyn Carrillo</b></p></h1>
      <h2><p style = {{textAlign: "center"}}>(951)-445-1816 | kgcarrillo05@gmail.com | https://github.com/kcarri14/Kaitlyns-Class-projects</p></h2>

      <h1><p style = {{textAlign: "Center"}}><b>Job 1 description</b></p></h1>
      <h1> <Link href="/"> back </Link></h1>
    </div>
  );
}