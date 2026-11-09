from fastapi import FastAPI
from pydantic import BaseModel
from model import run_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    pic50_min: float
    pic50_max: float
    atom_min: float
    atom_max: float
    logP_min: float
    logP_max: float


@app.post("/predict")
def predict(data: InputData):
    try:
        # MENJALANKAN MODEL BARU 
        raw_results = run_model(
            pic50_min=data.pic50_min,
            pic50_max=data.pic50_max,
            atom_min=int(data.atom_min),
            atom_max=int(data.atom_max),
            logP_min=data.logP_min,
            logP_max=data.logP_max
        )

        print("RAW MODEL OUTPUT:", raw_results)

        # === NORMALISASI KE FORMAT MODEL LAMA ===
        results = []
        for item in raw_results:

            props = item.get("properties", {})

            results.append({
                "smiles": item.get("smiles"),
                "justification": item.get("justification", "No justification available"),
                "score": item.get("score", None),
                "pIC50": props.get("pic50"),
                "pic50": props.get("pic50"),
                "logP": props.get("logP"),
                "logp": props.get("logP"),
                "atoms": props.get("atom_count"),
                "atom_count": props.get("atom_count"),
                "image": item.get("image")
            })

        return {
            "success": True,
            "results": results,
            "count": len(results),
            "raw_results": raw_results,  
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "success": False,
            "error": str(e),
            "results": []
        }


@app.get("/health")
def health_check():
    return {"status": "ok"}
