import csv

# ─────────────────────────────────────────────────────────────────────────────
# WHY THESE TWO DATASETS EXIST IN BIGQUERY
#
# vehicles.csv
#   Google Maps has no knowledge of a vehicle's fuel consumption, tank capacity,
#   EV range, or charging time. These are the inputs that make fuel/charge
#   planning precise. Without this table, the agent cannot calculate when the
#   tank runs dry or how far the car goes per charge.
#
# charging_stations.csv
#   Google Maps shows charging station pins but does not expose charger network
#   type (Tesla vs CCS vs CHAdeMO), power output in kW, number of stalls, or
#   typical wait times. These determine whether a stop is 15 minutes or 60
#   minutes — which completely changes the itinerary.
#
#   Gas stations, restaurants, attractions, and route distances are intentionally
#   NOT stored here. Google Maps MCP provides all of that live, with current
#   hours, ratings, and availability — a static CSV would be inferior.
# ─────────────────────────────────────────────────────────────────────────────


# ── TABLE 1: VEHICLES ────────────────────────────────────────────────────────
vehicles = [
    ["make","model","year","fuel_type","city_l_per_100km","highway_l_per_100km",
     "tank_capacity_l","ev_range_km","ev_kwh_per_100km","charge_to_80pct_min",
     "compatible_networks","notes"],
    # Gasoline
    ["Toyota","Camry","2023","gasoline",10.2,7.1,60,"","","","N/A","Common family sedan"],
    ["Toyota","Corolla","2023","gasoline",9.0,6.5,50,"","","","N/A","Compact – very efficient"],
    ["Toyota","RAV4","2023","gasoline",11.0,8.2,55,"","","","N/A","Canada's best-selling SUV"],
    ["Toyota","Highlander","2023","gasoline",12.5,9.5,72,"","","","N/A","3-row SUV – large tank"],
    ["Honda","Civic","2023","gasoline",8.7,6.4,46,"","","","N/A","Compact – excellent efficiency"],
    ["Honda","CR-V","2023","gasoline",10.5,7.9,57,"","","","N/A","Popular compact SUV"],
    ["Honda","Pilot","2023","gasoline",13.1,10.2,70,"","","","N/A","3-row family SUV"],
    ["Ford","F-150","2023","gasoline",14.5,10.8,136,"","","","N/A","Full-size pickup – very large tank"],
    ["Ford","Escape","2023","gasoline",10.8,7.6,57,"","","","N/A","Compact SUV"],
    ["Chevrolet","Silverado 1500","2023","gasoline",15.1,11.2,98,"","","","N/A","Full-size pickup"],
    ["Chevrolet","Equinox","2023","gasoline",11.0,8.5,55,"","","","N/A","Compact SUV"],
    ["Jeep","Grand Cherokee","2023","gasoline",13.2,9.8,93,"","","","N/A","Large SUV – big tank"],
    ["Dodge","Challenger","2023","gasoline",14.7,10.1,72,"","","","N/A","Muscle car – poor highway economy"],
    ["Ram","1500","2023","gasoline",14.8,11.0,98,"","","","N/A","Full-size pickup"],
    ["Nissan","Rogue","2023","gasoline",10.7,8.0,55,"","","","N/A","Popular crossover"],
    ["Subaru","Outback","2023","gasoline",10.5,7.8,74,"","","","N/A","AWD wagon – large tank"],
    ["Subaru","Forester","2023","gasoline",10.2,7.6,63,"","","","N/A","AWD SUV"],
    ["Mazda","CX-5","2023","gasoline",10.4,7.7,58,"","","","N/A","Reliable compact SUV"],
    ["Mazda","3","2023","gasoline",9.0,6.6,51,"","","","N/A","Sporty compact"],
    ["BMW","3 Series","2023","gasoline",10.0,7.0,59,"","","","N/A","Luxury compact"],
    ["Mercedes-Benz","C-Class","2023","gasoline",10.3,7.2,66,"","","","N/A","Luxury sedan"],
    ["Audi","Q5","2023","gasoline",11.2,8.0,75,"","","","N/A","Luxury SUV – large tank"],
    ["Volkswagen","Golf","2023","gasoline",9.1,6.7,50,"","","","N/A","Hatchback – efficient"],
    ["Volvo","XC60","2023","gasoline",11.0,7.8,71,"","","","N/A","Luxury SUV"],
    ["Genesis","GV70","2023","gasoline",11.5,8.3,70,"","","","N/A","Korean luxury SUV"],
    # Hybrid (self-charging – no plug needed)
    ["Toyota","Prius","2023","hybrid",4.8,4.9,43,"","","","N/A","Best highway efficiency in class"],
    ["Toyota","RAV4 Hybrid","2023","hybrid",7.1,6.8,55,"","","","N/A","Self-charging – no plug needed"],
    ["Toyota","Highlander Hybrid","2023","hybrid",8.1,7.0,72,"","","","N/A","3-row hybrid – great range"],
    ["Honda","CR-V Hybrid","2023","hybrid",6.0,5.5,57,"","","","N/A","Strong highway efficiency"],
    ["Ford","F-150 PowerBoost","2023","hybrid",12.0,9.5,136,"","","","N/A","Hybrid pickup – massive range"],
    # Plug-in Hybrid
    ["Toyota","RAV4 Prime","2023","plugin_hybrid",2.8,6.5,55,68,"",45,"CCS","68km EV range then runs on gasoline"],
    ["Ford","Escape PHEV","2023","plugin_hybrid",3.0,7.2,52,56,"",40,"CCS","56km EV range then gasoline"],
    # Electric
    ["Tesla","Model 3","2023","electric","","","",576,14.9,25,"Tesla Supercharger","V3 250kW – ~170km added in 15 min"],
    ["Tesla","Model Y","2023","electric","","","",533,16.3,25,"Tesla Supercharger","Most popular EV in Canada"],
    ["Tesla","Model S","2023","electric","","","",652,17.3,20,"Tesla Supercharger","V3 Supercharger – fastest Tesla charging"],
    ["Tesla","Model X","2023","electric","","","",543,20.0,25,"Tesla Supercharger","Large SUV – higher consumption"],
    ["Tesla","Cybertruck","2024","electric","","","",547,22.5,30,"Tesla Supercharger","AWD – large vehicle, higher draw"],
    ["Hyundai","IONIQ 5","2023","electric","","","",488,17.0,18,"CCS,CHAdeMO","800V – 10-80% in 18 min at 350kW station"],
    ["Hyundai","IONIQ 6","2023","electric","","","",614,14.3,18,"CCS","800V – most efficient Hyundai EV"],
    ["Kia","EV6","2023","electric","","","",504,16.1,18,"CCS","800V – same platform as IONIQ 5"],
    ["Ford","Mustang Mach-E","2023","electric","","","",490,18.0,45,"CCS","DC fast charge to 80% in 45 min"],
    ["Chevrolet","Bolt EV","2023","electric","","","",417,16.1,60,"CCS","Slower DC charging – plan longer stops"],
    ["Volkswagen","ID.4","2023","electric","","","",435,17.6,38,"CCS","DC fast charge to 80% in 38 min"],
    ["Nissan","Leaf","2023","electric","","","",349,17.3,40,"CHAdeMO","Shortest range – needs most stops"],
    ["BMW","iX","2023","electric","","","",452,21.0,35,"CCS","DC fast charge 10-80% in 35 min"],
    ["Volvo","C40 Recharge","2023","electric","","","",438,19.5,37,"CCS","DC fast charge to 80% in 37 min"],
    ["Audi","e-tron","2023","electric","","","",446,24.0,38,"CCS","Higher consumption – larger platform"],
    ["Porsche","Taycan","2023","electric","","","",484,24.8,23,"CCS","800V – 5-80% in 23 min"],
    ["Mercedes-Benz","EQS","2023","electric","","","",770,19.5,31,"CCS","Longest EV range available"],
    ["Rivian","R1T","2023","electric","","","",505,23.0,40,"CCS","Electric pickup – higher consumption"],
    ["Lucid","Air","2023","electric","","","",837,13.2,22,"CCS","Best efficiency and longest range EV"],
]

with open("vehicles.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(vehicles)
print(f"vehicles.csv: {len(vehicles)-1} vehicles")


# ── TABLE 2: EV CHARGING STATIONS ────────────────────────────────────────────
charging_stations = [
    ["station_id","name","city","province","latitude","longitude",
     "network","connector_type","max_power_kw","num_stalls",
     "typical_wait_min","open_24h","indoor_outdoor","amenities"],
    # Toronto area
    [1,"Tesla Supercharger – Toronto Scarborough","Toronto","ON",43.7734,-79.2577,"Tesla","Tesla",250,16,0,1,"outdoor","Food court, Walmart, restaurants"],
    [2,"Tesla Supercharger – Toronto Yorkdale","Toronto","ON",43.7255,-79.4522,"Tesla","Tesla",250,20,5,1,"outdoor","Yorkdale Mall – full dining options"],
    [3,"Tesla Supercharger – Mississauga Heartland","Mississauga","ON",43.5830,-79.7080,"Tesla","Tesla",250,12,5,1,"outdoor","Costco, restaurants, coffee"],
    [4,"Electrify Canada – Pickering Town Centre","Pickering","ON",43.8345,-79.0892,"Electrify Canada","CCS/CHAdeMO",150,6,15,1,"outdoor","Pickering Town Centre mall"],
    [5,"FLO – Toronto Don Mills","Toronto","ON",43.7285,-79.3418,"FLO","CCS/CHAdeMO",50,4,20,1,"outdoor","Shops at Don Mills"],
    [6,"ChargePoint – Oakville Place","Oakville","ON",43.4675,-79.6877,"ChargePoint","CCS",62,4,25,1,"outdoor","Oakville Place Mall, Tim Hortons"],
    # Toronto → Kingston (ON-401 east)
    [7,"Tesla Supercharger – Whitby","Whitby","ON",43.8975,-78.9429,"Tesla","Tesla",150,8,10,1,"outdoor","Tim Hortons, restaurants"],
    [8,"Tesla Supercharger – Port Hope","Port Hope","ON",43.9540,-78.2980,"Tesla","Tesla",150,6,10,1,"outdoor","Tim Hortons"],
    [9,"Electrify Canada – Cobourg","Cobourg","ON",43.9600,-78.1650,"Electrify Canada","CCS/CHAdeMO",150,4,15,1,"outdoor","Walmart, fast food"],
    [10,"Tesla Supercharger – Belleville","Belleville","ON",44.1628,-77.3832,"Tesla","Tesla",250,10,5,1,"outdoor","Quinte Mall – food court, restaurants"],
    [11,"Tesla Supercharger – Kingston","Kingston","ON",44.2298,-76.4919,"Tesla","Tesla",250,12,5,1,"outdoor","Frontenac Mall – restaurants, coffee"],
    [12,"Electrify Canada – Kingston","Kingston","ON",44.2380,-76.5100,"Electrify Canada","CCS/CHAdeMO",150,4,15,1,"outdoor","Cataraqui Centre mall"],
    [13,"ChargePoint – Kingston Downtown","Kingston","ON",44.2312,-76.4860,"ChargePoint","CCS",50,2,25,1,"outdoor","Walk to historic waterfront"],
    # Kingston → Montreal
    [14,"Tesla Supercharger – Gananoque","Gananoque","ON",44.3295,-76.1644,"Tesla","Tesla",150,6,10,1,"outdoor","Near 1000 Islands"],
    [15,"Tesla Supercharger – Brockville","Brockville","ON",44.5895,-75.6871,"Tesla","Tesla",150,8,10,1,"outdoor","McDonald's, Tim Hortons"],
    [16,"Tesla Supercharger – Cornwall","Cornwall","ON",45.0225,-74.7411,"Tesla","Tesla",250,10,5,1,"outdoor","Walmart, Tim Hortons – last ON stop"],
    [17,"FLO – Cornwall","Cornwall","ON",45.0210,-74.7398,"FLO","CCS/CHAdeMO",50,2,20,1,"outdoor","Cornwall Square Mall"],
    [18,"Tesla Supercharger – Vaudreuil-Dorion","Vaudreuil-Dorion","QC",45.3978,-74.0334,"Tesla","Tesla",250,12,5,1,"outdoor","Costco, restaurants – first QC stop"],
    [19,"Electrify Canada – Vaudreuil","Vaudreuil-Dorion","QC",45.4010,-74.0290,"Electrify Canada","CCS/CHAdeMO",150,4,15,1,"outdoor","Near highway exit"],
    # Montreal
    [20,"Tesla Supercharger – Montreal West Island","Montreal","QC",45.4654,-73.8304,"Tesla","Tesla",250,16,5,1,"outdoor","Fairview Pointe-Claire – full dining"],
    [21,"Tesla Supercharger – Montreal Centre","Montreal","QC",45.5017,-73.5673,"Tesla","Tesla",250,16,5,1,"outdoor","Downtown – hotels and restaurants walkable"],
    [22,"Electrify Canada – Montreal Cavendish","Montreal","QC",45.4711,-73.6419,"Electrify Canada","CCS/CHAdeMO",150,6,10,1,"outdoor","Cavendish Mall"],
    [23,"FLO – Montreal Plateau","Montreal","QC",45.5236,-73.5802,"FLO","CCS/CHAdeMO",50,4,20,1,"outdoor","Restaurants and cafes nearby"],
    # Toronto → Ottawa
    [24,"Tesla Supercharger – Ottawa South","Ottawa","ON",45.3491,-75.7554,"Tesla","Tesla",250,12,5,1,"outdoor","Barrhaven – restaurants, grocery"],
    [25,"Tesla Supercharger – Ottawa Gloucester","Ottawa","ON",45.4480,-75.5490,"Tesla","Tesla",250,10,5,1,"outdoor","St. Laurent Shopping Centre"],
    [26,"ChargePoint – Ottawa Rideau","Ottawa","ON",45.4215,-75.6972,"ChargePoint","CCS",50,2,20,1,"indoor","Rideau Centre – warm indoor charging"],
    [27,"FLO – Ottawa Kanata","Ottawa","ON",45.3020,-75.9170,"FLO","CCS/CHAdeMO",50,4,20,1,"outdoor","Tanger Outlets Kanata"],
    # Ottawa → Montreal
    [28,"Tesla Supercharger – Casselman","Casselman","ON",45.3110,-75.0900,"Tesla","Tesla",150,6,10,1,"outdoor","Tim Hortons – compact highway stop"],
    [29,"FLO – Hawkesbury","Hawkesbury","ON",45.6070,-74.6050,"FLO","CCS/CHAdeMO",50,2,20,1,"outdoor","Near ON/QC border"],
    # Montreal → Quebec City (A-40)
    [30,"Tesla Supercharger – Trois-Rivieres","Trois-Rivieres","QC",46.3500,-72.5500,"Tesla","Tesla",250,8,5,1,"outdoor","Natural halfway stop – restaurants"],
    [31,"FLO – Drummondville","Drummondville","QC",45.8800,-72.4900,"FLO","CCS/CHAdeMO",50,2,20,1,"outdoor","Alternate mid-point stop on A-20"],
    [32,"Tesla Supercharger – Quebec City Laurier","Quebec City","QC",46.8065,-71.2141,"Tesla","Tesla",250,10,5,1,"outdoor","Les Galeries de la Capitale mall"],
    [33,"Electrify Canada – Quebec City","Quebec City","QC",46.8100,-71.2200,"Electrify Canada","CCS/CHAdeMO",150,4,10,1,"outdoor","Near highway – quick stop"],
    [34,"FLO – Quebec City Ste-Foy","Quebec City","QC",46.7800,-71.2900,"FLO","CCS/CHAdeMO",50,4,20,1,"indoor","Place Ste-Foy mall – indoor warm stop"],
    # Toronto → Niagara / QEW
    [35,"Tesla Supercharger – Burlington","Burlington","ON",43.3255,-79.7990,"Tesla","Tesla",250,10,5,1,"outdoor","Mapleview Centre mall"],
    [36,"Tesla Supercharger – St. Catharines","St. Catharines","ON",43.1800,-79.2500,"Tesla","Tesla",150,8,10,1,"outdoor","Near Pen Centre mall"],
    [37,"Electrify Canada – Niagara Falls","Niagara Falls","ON",43.0900,-79.0800,"Electrify Canada","CCS/CHAdeMO",150,4,10,1,"outdoor","Near tourist area"],
    # Toronto → Muskoka / ON-400 north
    [38,"Tesla Supercharger – Barrie","Barrie","ON",44.3890,-79.6690,"Tesla","Tesla",250,12,5,1,"outdoor","Georgian Mall – Tim Hortons, restaurants"],
    [39,"FLO – Orillia","Orillia","ON",44.5990,-79.4200,"FLO","CCS/CHAdeMO",50,2,20,1,"outdoor","Costco plaza"],
    [40,"ChargePoint – Gravenhurst","Gravenhurst","ON",44.9200,-79.3700,"ChargePoint","CCS",50,2,25,1,"outdoor","Muskoka Wharf – scenic waterfront stop"],
]

with open("charging_stations.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(charging_stations)
print(f"charging_stations.csv: {len(charging_stations)-1} stations")
