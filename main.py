from fastapi import FastAPI, Path
from google.cloud.sql.connector import Connector, IPTypes
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text

meta = MetaData()
app = FastAPI()

connector = Connector()


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
get_planet_by_planet_name = text(
    "SELECT * FROM Planets WHERE planet_name = :name;",
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
systems = Table(
   'Systems', meta, 
   Column('system_id', Integer, primary_key = True), 
   Column('system_name', String), 
   Column('system_class', String),
)
planets = Table(
   'Planets', meta, 
   Column('planet_id', Integer, primary_key = True), 
   Column('system_id', Integer), 
   Column('planet_name', String),
   Column('planet_type', String),
   Column('is_starter', bool),
)

#API side
class System(BaseModel):
    system_id: int = Field(default = 0, ge=0)
    system_name: str
    system_class: str
class Planet(BaseModel):
    system_id: int = Field(default = 0, ge=0)
    planet_id: int = Field(default = 0, ge=0)    
    planet_name: str
    planet_type: str
    is_starter: bool
    
@app.post("/system")
async def add_system(info: System):
    pool = createConnPool()
    with pool.connect() as db_conn:
        if info.system_id > 0:
            idCheck = db_conn.execute(get_system_by_system, id=info.system_id).fetchall()
            if idCheck:
                db_conn.execute(systems.update().where(systems.c.system_id==info.system_id).values(system_name=info.system_name, system_class=info.system_class))
                return db_conn.execute(get_system_by_system, id=info.system_id).fetchall()
            else:
                return "System with ID [%s] not found"%info.system_id
        else:
            result = db_conn.execute(systems.insert(), 
                {'system_name': info.system_name, 'system_class': info.system_class}
            )
            result = db_conn.execute(get_system_by_system_name, name=info.system_name).fetchall()
            pool.dispose()
            return result

@app.post("/planet")
async def add_planet(info: Planet):
    pool = createConnPool()
    with pool.connect() as db_conn:
        if info.system_id > 0 and info.planet_id == 0:
            idCheck = db_conn.execute(get_system_by_system, id=info.system_id).fetchall()
            if idCheck:
                db_conn.execute(planets.insert(), 
                    {'system_id': info.system_id, 'planet_name': info.planet_name, 'planet_type':info.planet_type, 'is_starter':info.is_starter}
                )
                return db_conn.execute(get_planet_by_planet_name, name=info.planet_name).fetchall()
            else:
                return "System with ID [%s] not found"%info.system_id
        elif info.system_id == 0 and info.planet_id > 0:
            idCheck = db_conn.execute(get_planet_by_planet, id=info.planet_id).fetchall()
            if idCheck:
                db_conn.execute(planets.update().where(planets.c.planet_id==info.planet_id).values(planet_name=info.planet_name, planet_type=info.planet_type, is_starter=info.is_starter))
                return db_conn.execute(get_planet_by_planet, id=info.planet_id).fetchall()
            else:
                return "Planet with ID [%s] not found"%info.planet_id
        else:
            return "Must provide ID for either system or planet"
