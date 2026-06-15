

export const predefinedLocations:  { id: number; name: string; coordinates: [number, number] }[] = [
    {id: 1, name: "UU", coordinates: [35.3002, -120.6588] },
    {id: 2, name: "Rec Center", coordinates: [35.29840142552443, -120.660412048814] },
    {id: 3, name: "Dexter Lawn", coordinates: [35.300639, -120.663291] },
    {id: 4, name: "Orfalea College of Business", coordinates: [35.300320, -120.665241] },
    {id: 5, name: "Football Field", coordinates: [35.298342, -120.665087] },
    {id: 6, name: "yak?ityutyu Dorms", coordinates: [35.29771842506693, -120.65525147864066] },
    {id: 7, name: "Yosemite Hall Dorms", coordinates: [35.29807421600944, -120.65372843047085] },
    {id: 8, name: "Sierra Madre Dorms", coordinates: [35.29910503304359, -120.65494239127132] },
    {id: 9, name: "Red Bricks Dorms", coordinates: [35.30112455348416, -120.6572162270777] },
    {id: 10, name: "North Mountain Dorms", coordinates: [35.30282953829097, -120.65819415501423] },
    {id: 11, name: "Cerro Vista Apartments", coordinates: [35.30479151031942, -120.65708689457455] },
    {id: 12, name: "PCV", coordinates: [35.30836180357595, -120.65871169319334] },
    {id: 13, name: "Baker and Science Buildings", coordinates: [35.30107240291507, -120.66021167751809] },
    {id: 14, name: "Computer Science and Engineering West", coordinates: [35.30000819503057, -120.66248865217173] },
    {id: 15, name: "Library", coordinates: [35.301809581184436, -120.66347603846904] },
    {id: 16, name: "College of Engineering", coordinates: [35.3025765776128, -120.664772261461] },
    {id: 17, name: "College of Liberal Arts", coordinates: [35.30235762122505, -120.66070691269212] },
  ]
  

export const getLocationName = (coordinates: [number, number]) => {
    const tolerance = 0.0001; // Adjust tolerance as needed
  
    const location = predefinedLocations.find(
      (loc) =>
        Math.abs(loc.coordinates[0] - coordinates[0]) < tolerance &&
        Math.abs(loc.coordinates[1] - coordinates[1]) < tolerance
    );
  
    return location ? location.name : "Unknown Location";
};