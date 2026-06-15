'use client'
import Image from "next/image";
import Link from 'next/link';
import JobItem from '@/components/jobItem';
//import prisma from '@/lib/prisma';
import {useState} from 'react'
export default function Home() {

  //const jobLis = await prisma.job.findMany();

    let [jobList, setJobList] = useState([{
      id: 1 ,
      name: "Summer Camp Staff  ",
      date: "(2021-2024)"
    },{
      id: 2 ,
      name: "Cal Poly Dining  ",
      date: "(March 2024 - June 2024)",
      description: "test"
    },{
      id: 3 ,
      name: "Cal Poly ASI  ",
      date: "(October 2024-present)",
      description: "test"
    },{
      id: 4 ,
      name: "MCTSSA  ",
      date: "(June 2025 - September 2025)",
      description: "test"
    }]);



  let jobHtml = jobList.map((job) => <JobItem job ={job} key={job.id}></JobItem>);

  function addJob(){
    const newJobList = [...jobList,{
      id: Math.random(),
      name: "New Job",
      desc: "Whoopie",
      date: " 2025"
    }];
    //jobList.push() but still have to do setJobList(jobList) to let react now it as changed
    setJobList(newJobList);
  }

  let skillsList = [{
    name: "Customer Service"
  },{
    name: "Leadership"
  },{
    name: "Communication"    
  },{
    name: "Problem-Solving"
  }];

  let skillsHtml = skillsList.map((skills) =>{
    return (<li><b>
      <span>{skills.name}</span>
      </b></li>);
  });

  let languageList = [{
    name: "C"
  },{
    name: "Python"
  },{
    name: "RISC-V assembly"    
  },{
    name: "SQL"
  },{
    name: "Java"
  },{
    name: "Javascript"
  }];

  let languageHtml = languageList.map((language) =>{
    return (<li>
      <span>{language.name}</span>
    </li>);
  });

  let projectsList = [{
    name: "File System Emulator",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/File_system_emulator",
    desc: "This program emulates a file system like the one on everyone's computers. You can make a direcotry, list the contents of a directory, change directory, and create a file in a directory with this program. It is written in C."
  },{
    name: "Downloader",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/Downloader",
    desc: "This program will use multiple processes to download a collection of files from one's computer. Memory is dynamically allocated to be able to download large file systems like the root. This program was written in C"
  },{
    name: "Virtual World",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/Virtual_World",
    desc:"This program will launch a virtual world that users can interact with and watch how the lumberjack cut down trees and fairies will regrow trees. If the user presses the space bar, the world changes. Monkeys, bananas, and koalas are introduced which change the dynamic completely. This program was written in Java "   
  },{
    name: "Stick Figure Drawing",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/stick_figure_picture",
    desc: "This program is a drawing of a stick figure. This may seem easy but this program was made in RISC-V assembly so it was harder than many may think."
  },{
    name: "Heros v Monsters Game",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/Heros_vs_Monster_Game",
    desc: "This program is a game where you can battle monsters. The user inputs the weapon that could kill the monster. If the weapon is wrong then the game is over. The game also tracks how many weapons you have, how many monsters, you kill and how much money you have made. The money can be used to buy weapons at the store as well. This project was written in Python."
  },{
    name: "Database Creation",
    website: "https://github.com/kcarri14/Kaitlyns-Class-projects/tree/main/CSC_365_Lab_2" ,
    desc: "This project took data from several data sets and insert them into a databases in order to be altered later. Constraints were added to the data sets as well. This project was written in SQL."
  }];

  let projectsHtml = projectsList.map((projects) =>{
    return (<li>
      <span><b>{projects.name}</b></span>
      <p><span>{projects.website}</span></p>
      <ul>
        <li>{projects.desc}</li>
      </ul>
    </li>);
  });

  return (
    <div >
      <h1><p style={{textAlign: "center"}}><b>Kaitlyn Carrillo</b></p></h1>
      <p style = {{textAlign: "center"}}>(951)-445-1816 | kgcarrillo05@gmail.com | https://github.com/kcarri14/Kaitlyns-Class-projects</p>

      <h2><p style = {{textAlign: "left"}}><b>Job Experience</b></p></h2>

      <ul>
        {jobHtml}
      </ul>
      <button onClick={addJob}>Add Job</button>
      <h2><p style = {{textAlign: "left"}}><b>Skills</b></p></h2>
        <ul>
          <li><b>Programming Languages</b></li>
            <ul>
              {languageHtml}
            </ul>
          {skillsHtml}
        </ul>
      <h2><p style = {{textAlign: "left"}}><b>Projects</b></p></h2>
      <ul>
        {projectsHtml}
      </ul>
    </div>
  );
}
