from fastapi import FastAPI, Path
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

app = FastAPI()

connector = Connector()

get_system_by_system = sqlalchemy.text(
    "SELECT * FROM Systems WHERE system_id = (:id)",
)
get_planet_by_system = sqlalchemy.text(
    "SELECT * FROM Planets WHERE system_id = (:id)",
)
get_planet_by_planet = sqlalchemy.text(
    "SELECT * FROM Planets WHERE planet_id = (:id)",
)
get_resource_by_planet = sqlalchemy.text(
    "SELECT * FROM Resources WHERE planet_id = (:id)",
)
get_resource_by_resource = sqlalchemy.text(
    "SELECT * FROM Resources WHERE resource_id = (:id)",
)

# function to return the database connection
def getconn():
    conn = connector.connect(
        "temporal-window-350317:us-east1:empyrion-info",
        "pymysql",
        user="root",
        password="asdfjkl;",
        db="galaxy"
    )
    return conn
def createConnPool():
    return sqlalchemy.create_engine("mysql+pymysql://",creator=getconn,)

@app.get("/")
def home():
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT * FROM SimpleGalaxyInfo").fetchall()
        return {"Message": "Yeah PD, your app is running", "Data": result}

@app.get("/system-by-id/{system_id}")
def get_system(system_id: int = Path(1, description="ID of planetary system you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_system_by_system, id=systemn_id).fetchall()
        return result

@app.get("/planet-by-id/{planet_id}")
def get_planet(planet_id: int = Path(1, description="ID of planet you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_planet_by_planet, id=planet_id).fetchall()
        return result

@app.get("/resource-by-id/{resource_id}")
def get_resource(resource_id: int = Path(1, description="ID of resource you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_resource_by_resource, id=resource_id).fetchall()
        return result

@app.get("/planet-by-name/{planet_name}")
def get_planet_name(planet_name: str = Path("Omicron", description="Listed name of planet")):
	for sector_id in galaxy:
		sector = galaxy[sector_id]
		for planet_id in sector.get("planets"):
			planet = sector.get("planets")[planet_id]
			if planet.get("name").lower() == planet_name.lower():
				return planet

@app.get("/all-galaxy-info")
def get_galaxy_info():
    data = {}
    pool = createConnPool()
    with pool.connect() as db_conn:
        systems = db_conn.execute("SELECT * FROM Systems").fetchall()
        for system in systems:
            system_id = int(system["system_id"])
            planets = db_conn.execute(get_planet_by_system, id=system_id).fetchall()
            for planet in planets:
                planet_id = int(planet["planet_id"])  
                resources = db_conn.execute(get_resource_by_planet, id=planet_id).fetchall()
                return get_resource_info(info_in=resources)

def get_planet_info(info_in: str):
    planet = {}
    planet["system_id"] = info_in["system_id"]
    planet["planet_id"] = info_in["planet_id"]
    planet["planet_name"] = info_in["planet_name"]
    planet["planet_type"] = info_in["planet_type"]
    planet["isStarter"] = info_in["isStarter"]
    return planet

def get_resource_info(info_in: str):
    resources = {}
    i = 0
    for resource in info_in:
        d = {}
        d["resource_id"] = resource["resource_id"]
        d["resource_name"] = resource["resource_name"]
        d["resource_quantity"] = resource["resource_quantity"]
        resources[i] = d
        i += 1
    return resources