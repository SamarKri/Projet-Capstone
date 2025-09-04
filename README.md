# 🌊 Capstone - Analyse de la Température de Surface de la Mer (SST) en Méditerranée
**Auteur**: Samar Krimi


## Résumé du projet
Ce dépôt contient un **exemple technique** pour extraire, traiter et visualiser la Sea Surface Temperature (SST) pour la Méditerranée de manière **optimisée et à faible empreinte numérique**. 

Ce code est la version une version complète et cohérente pour mon projet Capstone, il répond à ces exigences :
- Lecture d’un fichier NetCDF Copernicus local.
- Calcul des statistiques SST (mean, min, max, médiane).
- Création d’une carte Folium avec sous-échantillonnage pour éviter des temps de calcul trop longs.
- Suivi de l’empreinte carbone avec CodeCarbon et sauvegarde en impact_estimate.json.

## Contenu du dépôt

- `Capstone.py` : Script Python complet (options CLI).
- `README_GitHub.md` : Ce fichier (version courte).
- `outputs/` : Dossier créé après exécution contenant résumé, carte HTML et estimations d'impact.

## 🛠️  Installation

### Cloner le dépôt
```bash
git clone https://github.com/tonpseudo/Capstone-SST-Project.git
cd Capstone-SST-Project

### Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate      # Windows PowerShell

### Installer les dépendances
pip install -r requirements.txt
```

## Exécution 
```bash
python Capstone.py 
```

## Outputs attendus
- `outputs/summary.json` : Statistiques basiques et métadonnées d'exécution.
- `outputs/SST_Mediterranee_map.html` : Carte interactive Folium (ouvrir dans navigateur).
- `outputs/impact_estimate.json` : Estimation simple des transferts et CO₂ évités.
- `outputs/emissions_codecarbon.csv` : Résultats CodeCarbon (si activé).

## 📂 Structure du Projet
Capstone-SST-Project/
```plaintext
├── outputs/               # Résultats générés automatiquement
│   ├── summary.json
│   ├── SST_Mediterranee_map.html
│   ├── emissions_codecarbon.csv
│   └── impact_estimate.json
│
├── Capstone.py             # Script principal
├── requirements.txt        # Dépendances Python
├── .gitignore
├── README.md
└── LICENSE
```

## Résultats du script
Statistiques SST (Sea Surface Temperature) :
```python
{'mean': 297.25, 'min': 286.62, 'max': 303.95, 'median': 298.34}
```
Moyenne de température : ~297.25 K (~24,1°C)
Minimum : ~286.62 K (~13,5°C)
Maximum : ~303.95 K (~30,8°C)
Médiane : 298.34 K (~25,2°C)
Carte sauvegardée : outputs\SST_Mediterranee_map.html ✅

## Consommation énergétique estimée par CodeCarbon
```yaml
Energy consumed for RAM : 0.000002 kWh
Delta energy consumed for CPU : 0.000024 kWh, power : 140.0 W
Total energy : 0.000025 kWh
CO₂ émis : 0.000014 kg
```

- Consommation totale très faible (25 µWh), normal pour un script Python léger.
- Émissions de CO₂ quasi négligeables (14 mg).
- Fichiers de sortie :
    - emissions_codecarbon.csv → suivi de la consommation
    - impact_estimate.json → estimation CO₂


## Licence
MIT License — tu es libre d'adapter et de réutiliser ce code pour des fins académiques et non commerciales.

*Samar Krimi — Capstone: SST Méditerranée (Green Digital Certificate)*
