import Link from 'next/link';


export default function JobItem({ job }){
    let link = "/job/" +job.id;

    return (<li>
      <span><Link href= {link}>{job.name}</Link></span>
      <span>{job.date}</span>
    </li>);
}