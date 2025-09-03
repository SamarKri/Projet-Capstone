# Capstone — SST Méditerranée (Pipeline optimisé)
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

## Installation (recommandée)
```bash
python -m venv venv
venv\Scripts\activate      # Windows PowerShell

pip install xarray numpy matplotlib folium codecarbon

```

## Exécution 

### Script CLI
```bash
python Capstone.py 
```

## Outputs attendus
- `outputs/summary.json` : Statistiques basiques et métadonnées d'exécution.
- `outputs/SST_Mediterranee_map.html` : Carte interactive Folium (ouvrir dans navigateur).
- `outputs/impact_estimate.json` : Estimation simple des transferts et CO₂ évités.
- `outputs/emissions_codecarbon.csv` : Résultats CodeCarbon (si activé).

## Estimation d'impact détaillée (méthodologie)
Les estimations fournies sont **indicatives** et reposent sur hypothèses simples :  
- Taille du dataset annuel SST (méthode classique) : **~10 Go** (exemple)  
- Extraction optimisée (sous-ensemble spatial + un jour) : **~0.1 Go**  
- Facteur d'émission réseau (approx.) : **0.06 kg CO₂ / Go** (valeur indicative, ADEME-like)  

Calcul :  
```
CO2_full = 10 * 0.06 = 0.6 kg CO2 par extraction complète
CO2_opt  = 0.1 * 0.06 = 0.006 kg CO2 par extraction optimisée
CO2_saved = CO2_full - CO2_opt = 0.594 kg CO2  (~99% de réduction sur cet exemple)
```

> Remarque : ces valeurs varient selon la source des données, la topologie réseau et la mesure précise par l'infrastructure cloud. Pour des analyses précises, corréler les métriques `codecarbon` avec logs cloud (eg. egress bytes, storage API metrics).

## Licence
MIT License — tu es libre d'adapter et de réutiliser ce code pour des fins académiques et non commerciales. 

## Attribution & citation
Si tu utilises ce travail dans un rapport ou une publication, cite le projet :  
*Samar Krimi — Capstone: SST Méditerranée (Green Digital Certificate)*


