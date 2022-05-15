from fastapi import FastAPI, Path

app = FastAPI()

galaxy = {
	1: {
		"name": "Beta",
		"planets": {
			1: {
				"name": "Omicron",
				"type": "Desert"
			},
			2: {
				"name": "Roggery",
				"type": "Swamp"
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