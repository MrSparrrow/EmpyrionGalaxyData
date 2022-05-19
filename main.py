from fastapi import FastAPI, Path
from google.cloud.sql.connector import Connector, IPTypes
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text

meta = MetaData()
app = FastAPI()

connector = Connector()


insert_into_system = text(
    "INSERT INTO System (system_name, system_class) VALUES (:x, :y);"
)
get_system_by_system_name = text(
    "SELECT * FROM Systems WHERE system_name = :name;"
)
get_system_by_system = text(
    "SELECT * FROM Systems WHERE system_id = :id;",
)
get_planet_by_system = text(
    "SELECT * FROM Planets WHERE system_id = :id;",
)
get_planet_by_planet = text(
    "SELECT * FROM Planets WHERE planet_id = :id;",
)
get_resource_by_planet = text(
    "SELECT * FROM Resources WHERE planet_id = :id;",
)
get_resource_by_resource = text(
    "SELECT * FROM Resources WHERE resource_id = :id;",
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
    return create_engine("mysql+pymysql://",creator=getconn,)

@app.get("/")
def home():
    return {"Message": "Yeah PD, your app is running", "Data": get_galaxy_info()}

@app.get("/system-by-id/{system_id}")
def get_system(system_id: int = Path(1, description="ID of planetary system you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_system_by_system, id=system_id).fetchall()
        pool.dispose()
        return result

@app.get("/planet-by-id/{planet_id}")
def get_planet(planet_id: int = Path(1, description="ID of planet you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_planet_by_planet, id=planet_id).fetchall()
        pool.dispose()
        return result

@app.get("/resource-by-id/{resource_id}")
def get_resource(resource_id: int = Path(1, description="ID of resource you want", ge=1)):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(get_resource_by_resource, id=resource_id).fetchall()
        pool.dispose()
        return result

@app.get("/all-galaxy-info")
def get_galaxy_info():
    pool = createConnPool()
    with pool.connect() as db_conn:
        systems = {}
        i = 0
        db_data = db_conn.execute("SELECT * FROM Systems").fetchall()
        for system in db_data:
            d = {}
            system_id = int(system["system_id"])
            d["system_id"] = system_id
            d["system_name"] = system["system_name"]
            d["system_class"] = system["system_class"]
            d["planets"] = get_planet_info(system_id)
            systems[i] = d
            i += 1
        return systems

def get_planet_info(system_id: str):
    pool = createConnPool()
    with pool.connect() as db_conn:
        planets = {}
        i = 0
        db_data = db_conn.execute(get_planet_by_system, id=system_id).fetchall()
        for planet in db_data:
            d = {}
            planet_id = int(planet["planet_id"])
            d["planet_id"] = planet_id
            d["planet_name"] = planet["planet_name"]
            d["planet_type"] = planet["planet_type"]
            d["isStarter"] = planet["isStarter"]
            d["resources"] = get_resource_info(planet_id)
            planets[i] = d
            i += 1
        return planets

def get_resource_info(planet_id: int):    
    pool = createConnPool()
    with pool.connect() as db_conn:
        resources = {}
        i = 0
        db_data = db_conn.execute(get_resource_by_planet, id=planet_id).fetchall()
        for resource in db_data:
            d = {}
            resource_id = int(resource["resource_id"])
            d["resource_id"] = resource_id
            d["resource_name"] = resource["resource_name"]
            d["resource_quantity"] = resource["resource_quantity"]
            resources[i] = d
            i += 1
        return resources


#DB side
system = Table(
   'Systems', meta, 
   Column('system_id', Integer, primary_key = True), 
   Column('system_name', String), 
   Column('system_class', String),
)
#APi side
class System(BaseModel):
    system_name: str
    system_class: str
    
@app.post("/system")
async def add_system(info: System):
    pool = createConnPool()
    with pool.connect() as db_conn:
        result = db_conn.execute(system.insert(), 
            {'system_name': info.system_name, 'system_class': info.system_class}
        )
        result = db_conn.execute(get_system_by_system_name, name=info.system_name).fetchall()
        pool.dispose()
        return result
