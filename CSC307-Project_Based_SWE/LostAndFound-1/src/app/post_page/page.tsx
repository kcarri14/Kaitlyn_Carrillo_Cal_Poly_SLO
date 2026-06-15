"use client";
import { useState, ChangeEvent, FormEvent, useEffect } from "react";
import { useRouter } from 'next/navigation';
import { useAuth } from "@clerk/nextjs";
import styles from "@/styles/postpage.module.css";
import { predefinedLocations } from "@/components/Map/map.data";


interface FormData  {
  isLost: boolean,
  bounty: number,
  name: string,
  location: [number, number] | null,
  date: Date,
  event: string,
  description: string,
  tags: string[], 
  images: string[],
  ownerId: number | null,
};


// predefined type tags for dropdown
const predefinedTypeTags:  { id: number; name: string }[] = [
  {id: 1, name: "iPhone" },
  {id: 2, name: "Cell Phone" },
  {id: 3, name: "Computer" },
  {id: 4, name: "Airpods" },
  {id: 5, name: "Headphones" },
  {id: 6, name: "Clothing" },
  {id: 7, name: "Water Bottle" },
  {id: 8, name: "Bag" },
  {id: 9, name: "Jewelery" },
  {id: 10, name: "Glasses" },
  {id: 11, name: "Tablet" },
  {id: 12, name: "Pen Pouch" },
  {id: 13, name: "Mug" },
  {id: 14, name: "Book" },
  {id: 15, name: "Other" },

]
// predefined color tags for dropdown

const predefinedColorTags:  { id: number; name: string }[] = [
  {id: 1, name: "Red" },
  {id: 2, name: "Orange" },
  {id: 3, name: "Yellow" },
  {id: 4, name: "Green" },
  {id: 5, name: "Blue" },
  {id: 6, name: "Purple" },
  {id: 7, name: "Brown" },
  {id: 8, name: "Rainbow" },
  {id: 9, name: "Multi-Colored" },
  {id: 10, name: "Black" },
  {id: 11, name: "White" },
  {id: 12, name: "Gold" },
  {id: 13, name: "Silver" },
  {id: 14, name: "Other" },
]


export default function Home() {
  // sets the color to the teal for the text boxes
  const [colorL, setColorL] = useState<string>("#639393");
  const [colorFile] = useState<string>("#639393");
  const [colorU] = useState<string>("#639393");
  const [colorP, setColorP] = useState<string>("#639393");
  const [selectedTypeTag, setSelectedTypeTag] = useState<string>();
  const [selectedColorTag, setSelectedColorTag] = useState<string>();

  // needed to be able to type in textboxes
  const [text, setText] = useState<string>("");
  const [textT, setTextT] = useState<string>("");
  const [date, setDate] = useState<string>("");
  const [textE, setTextE] = useState<string>("");
  const [textD, setTextD] = useState<string>("");

  // switches the Lost/Found Button
  const [buttonText, setButtonText] = useState("Lost");
  const toggleButtonText = () => {
    setButtonText((prevText) => prevText === "Lost" ? "Found" : "Lost");
  };

  // when lost/found button is pressed it changes colors
  const toggleColor = (color: string, setColor: (color: string) => void) => {
    setColor(color === "#173931" ? "#639393" : "#173931");

  };

  // when post button is pressed it changes colors
  const toggleColorP = (color: string, setColor: (color: string) => void) => {
    setColor(color === "#173931" ? "#639393" : "#173931");
  };

  //handles the selct file for the image upload
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSelectedFile(event.target.files?.[0] || null);
  };
  const handleUpload = () => {
    if (selectedFile) {
      alert(`File uploaded: ${selectedFile.name}`);
    } else {
      alert("No file selected");
    }
  };
  
  //handles the location change 
  const [selectedLocation, setSelectedLocation] = useState<[number, number] | null>(null);
  const handleLocationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOption = predefinedLocations.find(location => location.id === parseInt(e.target.value));
    if (selectedOption) {
      setSelectedLocation(selectedOption.coordinates); 
    }
  };
  
  //handles the type tag change
  const handleTypeTagChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOption = predefinedTypeTags.find(tag => tag.id === parseInt(e.target.value));
    if (selectedOption) {
      setSelectedTypeTag(selectedOption.name); 

  };
}

//handles the Check box for the Event?
  const handleColorTagChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOption = predefinedColorTags.find(tag => tag.id === parseInt(e.target.value));
    if (selectedOption) {
      setSelectedColorTag(selectedOption.name); 

  };
}
//gets the id from the Account table using the clerkId 
const { userId } = useAuth();
const [ownerId, setOwnerId] =useState<number | null>(null); 

useEffect(() => {
  const fetchOwnerId = async () => {
    try {
      const response = await fetch(`/api/Account/?clerkId=${userId}`);
      const data = await response.json();

      
      
      if (data) {
        const owner = data.accounts.find((account: { clerkId: string }) => account.clerkId === userId); 
        setOwnerId(owner.id);  
      } else {
        console.error("Owner ID not found.");
      }
    } catch (error) {
      console.error("Error fetching ownerId:", error);
    }
  };
  if (userId){
    fetchOwnerId();
  }
    
}, [userId]);

//data to be posted in database
const [formData, setFormData] = useState<FormData>({
  isLost: colorL == "#639393",
  bounty: 0,
  name: textT,
  location: selectedLocation,
  date: new Date(),
  event: textE,
  description: textD.trim(),
  tags: [], 
  images: [],
  ownerId: ownerId,
});


useEffect(() => {
  setFormData({
    isLost: colorL === "#639393",
    bounty: parseInt(text) || 0, 
    name: textT,
    location: selectedLocation,
    date: new Date(date), 
    event: textE,
    description: textD.trim(),
    tags: [selectedColorTag, selectedTypeTag].filter(Boolean) as string[], 
    images: [],
    ownerId: ownerId,
  });
}, [colorL, text, textT, selectedLocation, date, textE, textD, selectedTypeTag, selectedColorTag, userId]);


//handles the Check box for the Bounty?
const [isChecked, setIsChecked] = useState(false);
const handleCheckboxChange = () => {
  setIsChecked((prev) => {
    const newChecked = !prev;
    if (!newChecked || isFound == true) {
      setText(""); 
    }
    return newChecked;
  });
}

//handles the Check box for the Event?
const [isCheckedEvent, setIsCheckedEvent] = useState(false);
const handleCheckboxChangeEvent = () => {
  setIsCheckedEvent((prev) => {
    const newChecked = !prev;
    if (!newChecked) {
      setTextE(""); 
    }
    return newChecked;
  });
}

// handles the click for the lost/found button
const [isFound, setIsFound] = useState(false);
const handleClick = ()=> {
  toggleButtonText();
  toggleColor(colorL, setColorL)
  if(colorL == "#173931"){
    setIsFound(false);
  }else{
    setIsFound(true);
  }
  
}

//makes sure bounty can't be negative
const handleBounty = (e: React.ChangeEvent<HTMLInputElement >) => {
  const bounty = e.target.value;
  console.log(bounty)
  if (parseInt(bounty)< 0){
    setText("0");
  }else{
    setText(bounty);
    console.log(bounty)
  }
}

//handles the POST Request for the form 
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setIsSubmitting(true);

    if (textT.trim() === ""|| textD.trim() === ""||!selectedLocation || !date || !selectedTypeTag) {
      alert("Name, Description, Location, date and Type are required!");
      toggleColorP(colorP, setColorP);
      setIsSubmitting(false);
      return;
    }
   
  
    try {
      const response = await fetch("/api/Item", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({Item: formData}),

      });
      const result = await response.json();
      if (response.ok) {
        alert("Item reported successfully");
        router.push('/');
      } else {
        alert(`Error: ${result.error || "Something went wrong"}`);
      }
    } catch (error) {
      console.error("Error submitting the form:", error);
      alert("Error submitting the form. Please try again.");
    }
    if (selectedLocation) {
      console.log('Selected location:', selectedLocation); 
    }
    setIsSubmitting(false);
    setColorP(colorP === "#173931" ? "#639393" : "#173931");
  }
  


  
  return (
    <>
      {/* Report items logo */}
      <div style={{ margin: "8px", textAlign: "center" }}>
        <h1 className={styles.title}>Report Item</h1>
        <form onSubmit={handleSubmit}>
        {/* Button for lost or found items */}
        <div>
          <button id = "LostButton" type = "button"
            onClick={handleClick}
            className={styles.lost_btn}
            style={{
              backgroundColor: colorL,
            }}
          >
            {buttonText}
          </button>
        </div>
        {/* Bounty toggle switch and the textbox for bounty  */}
       
        {!isFound && ( <p className={styles.text}>
          Bounty?
            <label >
              <input type="checkbox" checked={isChecked} onChange={handleCheckboxChange} className={styles.switch} />
              <span className="slider round"></span>
            </label>
            {isChecked && (
            <input
              className={styles.bounty_textbox}
              type="number"
              value={text}
              onChange={handleBounty}
              placeholder="Ex: 5, 10, 20, etc..."

              maxLength = {10}
            />)}
          </p>
          )}
   
        {/* add image section */}
        {/* <div className="p-4 border rounded shadow-md w-64">
          <p>
            Add Image:{" "}
            <input
              type="file"
              onChange={handleFileChange}
              className="mb-2"
              style={{
                backgroundColor: colorFile,
                padding: "20px 20px",
                borderRadius: "16px",
                cursor: "pointer",
              }}
            />
            <button type = "button"
              onClick={handleUpload}
              style={{
                backgroundColor: colorU,
                color: "#a7d9a1",
                padding: "20px 20px",
                borderRadius: "16px",
                margin: "4px",
                cursor: "pointer",
              }}
            >
              Upload
            </button>
          </p>
        </div> */}
        {/* Type text box */}
        <p className={styles.text}>
          Name:<span className={styles.required}>*   </span>
          <input
            type="text"
            value={textT}
            onChange={(e) => setTextT(e.target.value)}
            placeholder="(Ex: iPhone 13, MacBook Pro, Jansport Backpack, etc...)"
            className={styles.name_textbox}
            maxLength = {20}
          />
        </p>
        {/* add type text box */}
        <div>
        <label htmlFor="tags" className={styles.text}>Type:<strong><span className={styles.required}>*</span> </strong></label>
        <select id="tags"  onChange={handleTypeTagChange} className={styles.dropdown}>
          <option value="">Select type tag </option>
          {predefinedTypeTags.map(tag => (
            <option key={tag.id} value={tag.id}>
              {tag.name}
            </option>
          ))}
        </select>
        
      
        {/* location text box */}
        <div>
        <label htmlFor="location" className={styles.text}>Location:<span className={styles.required}>* </span> </label>
        <select id="location" onChange={handleLocationChange} className={styles.dropdown} >
          <option value="">Select a Location</option>
          {predefinedLocations.map(location => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>
      </div>
        {/* color text box */}
        <label htmlFor="tags" className={styles.text}>Color:<strong> <span className={styles.required}>*   </span> </strong></label>
        <select id="tags"  onChange={handleColorTagChange} className={styles.dropdown}>
          <option value="">Select a Color </option>
          {predefinedColorTags.map(tag => (
            <option key={tag.id} value={tag.id}>
              {tag.name}
            </option>
          ))}
        </select>
        {/* set date with calendar */}
        <p className={styles.text}>
          Date Lost/Found:<span className={styles.required}>*</span>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{ marginLeft: "10px" , marginBottom: "20px"}}
            className={styles.dropdown}
            max = {new Date().toISOString().split("T")[0]}
          />
        </p>
        {/* at event toggle switch and the textbox for event */}
        <p className={styles.text}>
          
            At Event?{" "}
            <label >
              <input type="checkbox" checked={isCheckedEvent} onChange={handleCheckboxChangeEvent} className={styles.switch} />
              <span className="slider round"></span>
            </label>
            {isCheckedEvent && (<input
              type="text"
              value={textE}
              onChange={(e) => setTextE(e.target.value)}
              placeholder="Ex: CSA CNYB, Culture Fest, etc..."
              className={styles.event_textbox}
              maxLength = {20}
            />)}
         
        </p>
        {/* description text box */}
        <div className={styles.text}>
          Description:<span className={styles.required}>*  </span>
          <input
            className={styles.description_textbox}
            type="text"
            value={textD}
            onChange={(e) => setTextD(e.target.value)}
            placeholder="(Ex: a hole in the pocket, red sparkly key chain)"
            maxLength = {100}
          />
        </div>
        {/* Post button */}
        <div >
          <button type = "submit"
            onClick={() => toggleColorP(colorP, setColorP)}
            className={styles.lost_btn}
            style={{
              backgroundColor: colorP,
            }} disabled = {isSubmitting}
          >
            {isSubmitting ? "Posting..." : "Post"}
          </button>
        </div>
        </div> 
        </form>
      </div>
    </>
  );
}
