import style from '@/styles/map.module.css';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useState, useEffect } from "react";
import { getLocationName } from './map.data';

interface Pin {
      id: number;
      isLost: boolean;
      bounty: number;
      date: Date;
      images: string[];
      name: string;
      location: [number, number];
      event: string;
      description: string;
      tags: string[];
  }

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  iconSize: [25,41],
  iconAnchor: [12,41],
  popupAnchor: [1,-34],
  shadowSize: [41,41],
});


function Map(){
   const [MARKER, setMarker] = useState<Pin[]>([]);

   useEffect(() => {
    const fetchMarkers = async () => {
      try {
        const response = await fetch("/api/Item");
        if (!response.ok) throw new Error("not working");
        const data = await response.json();
        const LostItems = data.items.filter((item: Pin) => item.isLost);
        setMarker(LostItems);
      } catch (error){
        console.error("Error fetching pin", error);
      }
    };
    fetchMarkers();

   }, []);

   const groupedMarkers = MARKER.reduce((acc: any, item: Pin) => {
    const key = item.location.join(","); 
    if (!acc[key]) acc[key] = [];
    acc[key].push(item);
    return acc;
  }, {});

  return (
    <div>
    <MapContainer className= {style.map} center={[35.300144622089526, -120.66319674480712]} zoom = {15.5} scrollWheelZoom={true}>
        <TileLayer
    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  />
      
      {Object.keys(groupedMarkers).map((locationKey) => {
          const itemsAtLocation = groupedMarkers[locationKey];
          const location = itemsAtLocation[0].location; 

          return (
            <Marker key={locationKey} position={location} icon={markerIcon}>
              <Popup className= {style.scrollable}>
              < div >
                {itemsAtLocation.map((item: Pin) => (
                  <div key = {item.id}>
                 <strong> Name: {item.name}</strong> <br />
                  Bounty: ${item.bounty}<br />
                  Location: {getLocationName(item.location)}
                  <br />Date: {new Date(item.date).toISOString().split('T')[0]}
              <br /> Details: {item.tags.filter(tag => tag.toLowerCase() !== "other").join(", ")}
              <br /> Event: {item.event}
              <br /> Description: {item.description}
              <hr />
              </div>
                ))}
                </div>
              </Popup>
            </Marker>
          );
        })}
    

    </MapContainer>
    </div>
  );
}

export default Map;
