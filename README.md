# Environmental Monitoring & Pollution Control - Demo

## Overview
Simple prototype that predicts air quality category (Good / Moderate / Unhealthy)
from sensor readings using a RandomForest model trained on synthetic data.
Includes a Flask backend and a small web frontend.

## Setup
1. Create virtualenv (optional):
   python -m venv .venv
   source .venv/bin/activate   (Windows: .venv\Scripts\activate)

2. Install requirements:
   pip install -r requirements.txt

3. Train model (generates data and saves model):
   python train_model.py

4. Run web app:
   python app.py

5. Open browser:
   http://127.0.0.1:5000/

## Files
- train_model.py  : builds synthetic dataset and trains model (saves to model/model.pkl)
- app.py          : Flask app with /predict endpoint and web UI
- templates/index.html
- static/script.js
- data/synthetic_air_data.csv
- model/model.pkl

## Notes for submission
- Include the `data/` and `model/` folders produced after running train_model.py
- If you need a single zip, compress the `EnvMonitorProject/` folder:
  zip -r EnvMonitorProject.zip EnvMonitorProject/

Good luck with your submission! If you want, I can:
- convert this into a single zip file structure (I can show the commands),
- or add a short PowerPoint slide (title, problem, approach, dataset, model, results) for final presentation slides.
