from fastapi import FastAPI, Path

app = FastAPI()

galaxy = {
	1: {
		"name": "Beta",
		"planets": {
			1: {
				"name": "Omicron",
				"type": "Desert",
				"moons": {
					1: {
						"name": "Omicron moon"
					},
					2: {
						"name": "Omicron moon 1"
					}
				},
				"resources": [
					"iron",
					"copper",
					"silicon"
				]
			},
			2: {
				"name": "Roggery",
				"type": "Swamp",
				"moons": {
					1: {
						"name": "Roggery moon"
					},
					2: {
						"name": "Roggery moon 1"
					}
				}
			}
		}
	},
	2: {
		"name": "Delta",
		"planets": {
			1: {
				"name": "Akua",
				"type": "Temperate"
			},
			2: {
				"name": "Rogue",
				"type": "Dead"
			}
		}
	}
}


@app.get("/")
def home():
	return {"TODO": "README?"}

@app.get("/system-by-id/{system_id}")
def get_system(system_id: int = Path(1, description="ID of planetary system you want", ge=1)):
	return galaxy[system_id]

@app.get("/planet-by-name/{planet_name}")
def get_planet(planet_name: str = Path("Omicron", description="Listed name of planet")):
	for sector_id in galaxy:
		sector = galaxy[sector_id]
		for planet_id in sector.get("planets"):
			planet = sector.get("planets")[planet_id]
			if planet.get("name") == planet_name:
				return planet