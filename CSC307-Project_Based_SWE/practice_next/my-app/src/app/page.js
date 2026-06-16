'use client'
import Image from "next/image";
import { FaSearch } from "react-icons/fa";
import { FaMapSigns } from "react-icons/fa";
import { LuMessagesSquare } from "react-icons/lu";
import { CgProfile } from "react-icons/cg";
import { FaRegBell } from "react-icons/fa";
import {useState} from 'react'

export default function Home() {
    const [colorL, setColorL] = useState("#CF8E80");
  
    const handleClickLost = () => {
      setColorL(colorL === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorF, setColorF] = useState("#CF8E80");
  
    const handleClickFound = () => {
      setColorF(colorF === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorFile, setColorFile] = useState("#CF8E80");
  
    const handleClickFile = () => {
      setColorL(colorL === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorU, setColorU] = useState("#CF8E80");
  
    const handleClickUpload = () => {
      setColorU(colorU === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorP, setColorP] = useState("#CF8E80");
  
    const handleClickPost = () => {
      setColorP(colorP === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorTag, setColorTag] = useState("#CF8E80");
  
    const handleClickTag = () => {
      setColorTag(colorTag === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };

    const [colorExample, setColorExample] = useState("#CF8E80");
  
    const handleClickExample = () => {
      setColorExample(colorExample === "#7D1D3F" ? "#CF8E80" : "#7D1D3F"); 
    };


  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    
  };

  const handleUpload = () => {
    if (selectedFile) {
      alert(`File uploaded: ${selectedFile.name}`);
    } else {
      alert("No file selected");
    }
  };
  const [text, setText] = useState(""); 

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const [textT, setTextT] = useState(""); 

  const handleChangeType = (event) => {
    setTextT(event.target.value);
  };

  const [textL, setTextL] = useState(""); 
  const handleChangeLocation = (event) => {
    setTextL(event.target.value);
  };

  const [textC, setTextC] = useState(""); 

  const handleChangeColor = (event) => {
    setTextC(event.target.value);
  };

  const [textS, setTextS] = useState(""); 

  const handleChangeSize = (event) => {
    setTextS(event.target.value);
  };

  const [date, setDate] = useState("");

  const handleChangeDate = (event) => {
    setDate(event.target.value); 
  };

  const [textE, setTextE] = useState(""); 

  const handleChangeEvent = (event) => {
    setTextE(event.target.value);
  };

  const [textD, setTextD] = useState(""); 

  const handleChangeDesc = (event) => {
    setTextD(event.target.value);
  };
  
  const [texttags, setTexttags] = useState(""); 

  const handleChangetags = (event) => {
    setTexttags(event.target.value);
  };
  

  return (
    <> 
      <div class="topnav">
      <a href="#home">Lost and Found </a>
      <a href="#home"><CgProfile /></a>
      <a href="#home"><FaRegBell /> </a>
      <a href="#news" class="split"><LuMessagesSquare /></a>
      <a href="#contact" class="split"><FaMapSigns /></a>
      <a href="#about" class="split"><FaSearch /></a>
      </div>
  
      <p style = {{textDecoration: "underline"}}> <b><h1>Report Item </h1></b></p>
    
      <div class="btn-group">
        <button onClick = {handleClickLost} style={{ backgroundColor: colorL, colorL: "#f4ebbe", padding: "10px 20px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }} >Lost</button>
        <button onClick = {handleClickFound} style={{ backgroundColor: colorF, colorF: "#f4ebbe", padding: "10px 20px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }}>Found</button>
    
      </div>
      <p style={{ marginRight: "10px" }}><b>Bounty? <label class="switch"> <input type="checkbox" style={{ marginRight: "10px" }}></input><span class="slider round"></span>If so:</label><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "300px", height: "20px", fontSize: "12px", marginLeft: "10px"}} type="text" 
          value={text} 
          onChange={handleChange} 
          placeholder="Ex: 5, 10, 20, etc..."
          className="custom-input"></input></b></p>
      
      <div className="p-4 border rounded shadow-md w-64">
        <p>Add Image: <input type="file" onChange={handleFileChange} className="mb-2" style={{ backgroundColor: colorFile, colorFile: "#f4ebbe", padding: "20px 20px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }} />
        <button
          onClick={handleUpload}
          className="bg-blue-500 text-white px-4 py-2 rounded"
          style={{ backgroundColor: colorU, color: "#f4ebbe", padding: "20px 20px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }}
        >
          Upload
        </button></p>
        
      </div>
      <p><input  style={{backgroundColor: "#CF8E80",  color: "#f4ebbe", width: "1000px", height: "20px", fontSize: "12px" }} type="text" 
          value={textT} 
          onChange={handleChangeType} 
          placeholder="Type: (Ex: iPhone, Computer, Backpack, etc...)" 
          className="custom-input"></input></p>

      <p><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "300px", height: "20px", fontSize: "12px" }} type="text" 
          value={textL} 
          onChange={handleChangeLocation} 
          placeholder="Location: (Ex: UU, 1901, MAC, etc...)"
          className="custom-input"></input></p>

      <p><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "300px", height: "20px", fontSize: "12px" }} type="text" 
          value={textC} 
          onChange={handleChangeColor} 
          placeholder="Color: (Ex: red, orange, yellow, rainbow, etc...)"
          className="custom-input"></input></p>

      <p><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "300px", height: "20px", fontSize: "12px" }} type="text" 
          value={textS} 
          onChange={handleChangeSize} 
          placeholder="Size: (Ex: S,M,L,XL)"
          className="custom-input"></input></p>

      <p style = {{marginRight: "20px"}}>Date Lost: <input 
          type="date" 
          value={date} 
          onChange={handleChangeDate} 
          className="p-2 border rounded"
          style = {{marginLeft: "10px"}}
        /></p>
      
      <p style={{ marginRight: "10px" }}><b>At Event? <label class="switch"> <input type="checkbox" style={{ marginRight: "10px" }}></input><span class="slider round"></span>If so:</label><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "850px", height: "20px", fontSize: "12px", marginLeft: "10px"}} type="text" 
        value={textE} 
        onChange={handleChangeEvent} 
        placeholder="Ex: CSA CNYB, Culture Fest, etc..."
        className="custom-input"></input></b></p>

      <p><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "850px", height: "100px", fontSize: "12px",textAlign: "left", verticalAlign: "top" }} type="text" 
        value={textD} 
        onChange={handleChangeDesc} 
        placeholder="Description: (Ex: a hole in the pocket, red sparkly key chain)"
        className="custom-input"></input></p>  

      <div class="btn-group">
        <button onClick = {handleClickPost} style={{ backgroundColor: colorP, colorP: "#f4ebbe", padding: "10px 20px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px", marginLeft: "1000px" }} >Post</button>
    
      </div>  

      <p><input  style={{ backgroundColor: "#CF8E80", color: "#f4ebbe", width: "250px", height: "20px", fontSize: "12px",textAlign: "left", verticalAlign: "top" }} type="text" 
          value={texttags} 
          onChange={handleChangetags} 
          placeholder="Add Tag: (Ex: #red, #foundinUU, etc...)"
          className="custom-input"></input></p>  

      <div class="btn-group">
        <button onClick = {handleClickTag} style={{ backgroundColor: colorTag, colorTag: "#f4ebbe", padding: "10px 10px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }} >#Example</button>
        <button onClick = {handleClickExample} style={{ backgroundColor: colorExample, colorExample: "#f4ebbe", padding: "10px 10px", border: "none", borderRadius: "5px", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }}>#tag</button>
    
      </div>

    </>
    
  );
}

//style={{ backgroundColor: "#7D1D3F", border: "none", color: "", padding: '10px', textAlign: "center", textDecoration: "none", display: "inline-block", margin: "4px" , cursor: "pointer", borderRadius: "16px" }}
