from fastapi import FastAPI, Path
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

app = FastAPI()

connector = Connector()

get_systems = sqlalchemy.text(
    "SELECT * FROM Systems WHERE system_id = (:id)",
)
get_planets = sqlalchemy.text(
    "SELECT * FROM Planets WHERE planet_id = (:id)",
)
get_resources = sqlalchemy.text(
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
        result = db_conn.execute(get_systems, id=systemn_id).fetchall()
        return result

@app.get("/planet-by-id/{planet_id}")
def get_planet(planet_id: int = Path(1, description="ID of planet you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_planets, id=planet_id).fetchall()
        return result

@app.get("/resource-by-id/{resource_id}")
def get_resource(resource_id: int = Path(1, description="ID of resource you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_resources, id=resource_id).fetchall()
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
    pool = createConnPool()
    with pool.connect() as db_conn:
        systems = db_conn.execute("SELECT * FROM Systems").fetchall()
        return systems