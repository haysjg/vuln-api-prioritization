# CVE Prioritization Script

Script avancé de priorisation des vulnérabilités CrowdStrike Falcon basé sur plusieurs facteurs de risque.

## 🎯 Objectif

Ce script permet de prioriser intelligemment les CVE détectées dans votre environnement CrowdStrike en calculant un score composite basé sur :

1. **Sévérité CVSS** - Score technique de la vulnérabilité
2. **Expert Rating CrowdStrike** - 🔥 **Analyse CTI par les experts CrowdStrike** (facteur le plus important)
3. **Statut d'exploitation** - Menace réelle (PoC, exploit public, exploitation active)
4. **Exposition** - Nombre d'hôtes affectés
5. **Criticité des actifs** - Importance business des systèmes touchés
6. **Ancienneté** - Âge de la vulnérabilité

## 🚀 Installation

```bash
# Installer les dépendances
pip install falconpy openpyxl

# Configurer les credentials
export FALCON_CLIENT_ID="your_client_id"
export FALCON_CLIENT_SECRET="your_client_secret"
```

## 📊 Utilisation

### Utilisation basique

```bash
# Prioriser toutes les vulnérabilités
python scripts/prioritize_vulnerabilities.py

# Avec sortie verbose
python scripts/prioritize_vulnerabilities.py --verbose
```

### Filtrage avancé

```bash
# Uniquement les CVE CRITICAL et HIGH
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.severity:['CRITICAL','HIGH']"

# CVE avec score CVSS >= 7.0
python scripts/prioritize_vulnerabilities.py --min-score 7.0

# Limiter à 1000 CVE
python scripts/prioritize_vulnerabilities.py --limit 1000

# Top 20 CVE les plus prioritaires
python scripts/prioritize_vulnerabilities.py --top 20
```

### Options de sortie

```bash
# Spécifier le répertoire de sortie
python scripts/prioritize_vulnerabilities.py \
  --output-dir ./reports

# Personnaliser le nom des fichiers
python scripts/prioritize_vulnerabilities.py \
  --output-prefix monthly_vulnerability_review
```

## 📋 Formats de sortie

Le script génère **3 formats** :

### 1. CSV (`vulnerability_prioritization_YYYYMMDD_HHMMSS.csv`)
- Format tableur standard
- Importable dans Excel, Google Sheets
- Colonnes : Rank, Priority Score, CVE ID, CVSS, Severity, Exploit Status, etc.

### 2. JSON (`vulnerability_prioritization_YYYYMMDD_HHMMSS.json`)
- Format structuré pour automation
- Inclut les données brutes complètes
- Utilisable par d'autres scripts/API

### 3. Excel (`vulnerability_prioritization_YYYYMMDD_HHMMSS.xlsx`)
- Fichier Excel formaté avec couleurs
- Color-coding par sévérité :
  - 🔴 CRITICAL (rouge)
  - 🟠 HIGH (orange)
  - 🟡 MEDIUM (jaune)
  - 🟢 LOW (vert)
- Colonnes auto-dimensionnées

## 🧮 Formule de prioritisation

### Score total = Composantes suivantes :

```python
Score = (CVSS × 10) + (Expert Rating × 0.8) + (Exploit Status × 30) +
        (Hosts × 0.5) + (Asset Criticality × 50) + (Age × 0.1)
```

| Composante | Poids | Points max | Description |
|------------|-------|------------|-------------|
| **CVSS** | 10× | 100 | Score CVSS base (0-10) × 10 |
| **Expert Rating** 🔥 | 0.8× | **80** | **CrowdStrike CTI analysis (0-100) × 0.8** |
| **Exploitation** | 30/level | 120 | Statut d'exploitation (0-4) × 30 |
| **Exposition** | 0.5/host | Illimité | Nombre d'hôtes affectés × 0.5 |
| **Criticité actifs** | 50 | 100 | Bonus si actif critique (tags/groups) |
| **Ancienneté** | 0.1/jour | Illimité | Jours depuis publication × 0.1 |

### 🔥 Expert Rating (CrowdStrike CTI) - FACTEUR CLÉ

Le **CrowdStrike Expert Rating** est l'un des facteurs les plus importants car il intègre :

- ✅ Intelligence sur les menaces actives (CTI)
- ✅ Observation d'exploitation par des threat actors connus
- ✅ Disponibilité et qualité des exploits
- ✅ Impact réel observé dans le wild
- ✅ Disponibilité des mitigations

| Expert Rating | Points (sur 100) | Description |
|---------------|------------------|-------------|
| **CRITICAL** | 100 | Menace active critique observée |
| **HIGH** | 70 | Menace sérieuse avec exploitation probable |
| **MEDIUM** | 40 | Risque modéré |
| **LOW** | 10 | Faible priorité |
| **INFORMATIONAL** | 0 | Information uniquement |
| **N/A** | 0 | Pas d'évaluation |

**⚠️ Important** : L'Expert Rating peut parfois différer significativement du score CVSS traditionnel, car il tient compte de facteurs réels que le CVSS ne capture pas (exploitation active, facilité réelle d'exploitation, mitigations disponibles, etc.).

### Détail du statut d'exploitation

| Statut | Label | Points |
|--------|-------|--------|
| 0 | Not Exploited | 0 |
| 1 | PoC Exists | 30 |
| 2 | Public Exploit Available | 60 |
| 3 | Active Exploitation | 90 |
| 4 | Widespread Exploitation | 120 |

### Criticité des actifs

Un actif est considéré **critique** si ses groupes ou tags contiennent :

**Groupes critiques** :
- production, prod, critical, dmz
- domain-controllers, pci, financial
- database, web-servers, public-facing

**Tags critiques** :
- crown-jewels, tier-0, tier-1
- pci-dss, sox, hipaa, gdpr
- critical, high-value, customer-data

## ⚙️ Configuration personnalisée

Modifiez `config/prioritization_config.json` pour ajuster :

### Stratégie "Agressive" (focus exploitation + CTI)
```json
{
  "cvss_weight": 8,
  "expert_rating_weight": 100,
  "exploit_status_weight": 40,
  "hosts_affected_weight": 0.3,
  "asset_criticality_weight": 70,
  "age_weight": 0.15
}
```

### Stratégie "CTI-Driven" (maximum CTI)
```json
{
  "cvss_weight": 5,
  "expert_rating_weight": 120,
  "exploit_status_weight": 50,
  "hosts_affected_weight": 0.3,
  "asset_criticality_weight": 40,
  "age_weight": 0.1
}
```

### Stratégie "Exposition" (focus volume)
```json
{
  "cvss_weight": 10,
  "expert_rating_weight": 60,
  "exploit_status_weight": 20,
  "hosts_affected_weight": 1.5,
  "asset_criticality_weight": 30,
  "age_weight": 0.05
}
```

### Stratégie "Sévérité seule" (CVSS traditionnel)
```json
{
  "cvss_weight": 20,
  "expert_rating_weight": 20,
  "exploit_status_weight": 5,
  "hosts_affected_weight": 0.1,
  "asset_criticality_weight": 10,
  "age_weight": 0.05
}
```

## 📈 Exemple de sortie

```
================================================================================
VULNERABILITY PRIORITIZATION SUMMARY
================================================================================

Showing top 10 of 1,247 total vulnerabilities

Severity Distribution:
  CRITICAL: 87
  HIGH: 324
  MEDIUM: 612
  LOW: 224

Exploitation Status:
  Widespread Exploitation: 5
  Active Exploitation: 23
  Public Exploit Available: 156
  PoC Exists: 421
  Not Exploited: 642

Critical Assets Affected: 143
Total Host Instances Affected: 8,456

================================================================================
TOP PRIORITY VULNERABILITIES
================================================================================

#    Score    CVE ID             CVSS   Severity   Exploit Status            Hosts  Critical
----------------------------------------------------------------------------------------------------
1    287.45   CVE-2024-1234      9.8    CRITICAL   Widespread Exploitation   45     YES
2    245.20   CVE-2024-5678      9.1    CRITICAL   Active Exploitation       67     YES
3    198.30   CVE-2023-9012      8.8    HIGH       Public Exploit Available  123    YES
4    176.55   CVE-2024-3456      9.0    CRITICAL   PoC Exists                234    NO
5    165.80   CVE-2023-7890      7.5    HIGH       Active Exploitation       89     YES
...
```

## 🔍 Cas d'usage

### Triage SOC quotidien
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.severity:['CRITICAL','HIGH']" \
  --top 50 \
  --output-prefix daily_triage_$(date +%Y%m%d)
```

### Revue mensuelle complète
```bash
python scripts/prioritize_vulnerabilities.py \
  --min-score 4.0 \
  --output-dir ./monthly_reports \
  --output-prefix vulnerability_review_$(date +%Y%m) \
  --verbose
```

### Focus exploitation active
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.exploit_status:>=3" \
  --verbose
```

### Audit d'actifs critiques
```bash
# Nécessite modification du script pour filtrer par groupes/tags
python scripts/prioritize_vulnerabilities.py \
  --filter "host_info.groups:*'production'*"
```

## 🔐 Permissions API requises

Le script nécessite les scopes suivants :

- **Vulnerabilities**: `READ`
- **Hosts** (optionnel): `READ` - pour enrichir les données d'actifs

## 📝 Notes importantes

1. **Performance** : Le traitement de milliers de CVE peut prendre plusieurs minutes
2. **Pagination** : Le script gère automatiquement la pagination (5000 IDs par requête)
3. **Batching** : Les détails sont récupérés par lots de 200
4. **Rate limiting** : Respecte les limites de l'API CrowdStrike

## 🛠️ Dépannage

### Erreur d'authentification
```bash
# Vérifier les variables d'environnement
echo $FALCON_CLIENT_ID
echo $FALCON_CLIENT_SECRET

# Tester l'authentification
python scripts/explore_vulnerabilities_api.py
```

### Aucune vulnérabilité retournée
```bash
# Supprimer tous les filtres
python scripts/prioritize_vulnerabilities.py --verbose

# Vérifier les permissions API dans Falcon console
```

### Excel non généré
```bash
# Installer openpyxl
pip install openpyxl
```

## 📚 Ressources

- [CrowdStrike API Documentation](https://falcon.crowdstrike.com/documentation)
- [FalconPy SDK](https://github.com/CrowdStrike/falconpy)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)

## 🤝 Contribution

Pour modifier l'algorithme de priorisation :

1. Éditer `scripts/prioritize_vulnerabilities.py`
2. Modifier la fonction `calculate_priority_score()`
3. Ajuster `SCORING_WEIGHTS` ou charger depuis `config/prioritization_config.json`

## 📄 License

Ce script fait partie du projet API-calls-with-FalconPy.
