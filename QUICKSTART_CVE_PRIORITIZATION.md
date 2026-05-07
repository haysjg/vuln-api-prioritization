# Guide de démarrage rapide - Priorisation CVE

## 🚀 Installation en 30 secondes

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer les credentials
export FALCON_CLIENT_ID="votre_client_id"
export FALCON_CLIENT_SECRET="votre_client_secret"

# 3. Tester l'installation
python scripts/test_prioritization.py
```

## ⚡ Utilisation rapide

### Option 1 : Menu interactif (recommandé)

**Linux/Mac :**
```bash
./scripts/run_prioritization.sh
```

**Windows :**
```powershell
.\scripts\run_prioritization.ps1
```

### Option 2 : Ligne de commande directe

```bash
# Top 20 CVE critiques (triage quotidien)
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.severity:['CRITICAL','HIGH']" \
  --top 20 --verbose

# CVE exploitées activement (urgence)
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.exploit_status:>=3" \
  --verbose

# Toutes les CVE avec CVSS >= 7.0
python scripts/prioritize_vulnerabilities.py \
  --min-score 7.0 --verbose
```

## 📊 Résultats

Le script génère **3 fichiers** dans `./reports/` :

- **CSV** - Pour Excel/Google Sheets
- **JSON** - Pour automation/API
- **XLSX** - Excel formaté avec couleurs

## 🎯 Score de priorité

Le score combine **6 facteurs** :

| Facteur | Poids | Description |
|---------|-------|-------------|
| **CVSS** | 10× | Score technique (0-10) |
| **Expert Rating** 🔥 | 0.8× | **Analyse CTI CrowdStrike (le plus important !)** |
| **Exploitation** | 30/level | PoC/exploit public/exploitation active |
| **Exposition** | 0.5/host | Nombre d'hôtes touchés |
| **Criticité** | 50 | Actifs critiques (production, DC, PCI, etc.) |
| **Ancienneté** | 0.1/jour | Jours depuis publication |

**Exemple de calcul :**

CVE-2024-1234 (Expert Rating: HIGH, exploit actif, 50 hosts production, CVSS 9.8, 60 jours) :
```
Score = (9.8 × 10) + (70 × 0.8) + (3 × 30) + (50 × 0.5) + 50 + (60 × 0.1)
      = 98 + 56 + 90 + 25 + 50 + 6
      = 325 points
```

### 🔥 Pourquoi l'Expert Rating est crucial

Le **CrowdStrike Expert Rating** intègre de la threat intelligence que le CVSS seul ne capture pas :
- Exploitation active observée par CrowdStrike
- Usage par des threat actors connus
- Qualité et disponibilité des exploits
- Efficacité des mitigations disponibles

## 🔧 Personnalisation

Modifier `config/prioritization_config.json` pour ajuster les poids.

Exemples de stratégies :
- **CTI-Driven** : Maximum de poids sur Expert Rating et exploitation
- **Aggressive** : Focus sur exploitation active et CTI
- **Balanced** : Équilibré avec forte influence CTI (défaut)
- **Exposure** : Focus sur le volume d'hôtes
- **Severity Only** : CVSS traditionnel minimal

## 📚 Documentation complète

Voir `docs/CVE_PRIORITIZATION.md` pour :
- Tous les champs API disponibles
- Formules détaillées
- Cas d'usage avancés
- Configuration personnalisée
- Dépannage

## 💡 Cas d'usage typiques

### Triage SOC quotidien
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.severity:['CRITICAL','HIGH']" \
  --top 50 \
  --output-prefix daily_triage_$(date +%Y%m%d)
```

### Revue hebdomadaire
```bash
python scripts/prioritize_vulnerabilities.py \
  --min-score 7.0 \
  --output-prefix weekly_$(date +%Y%m%d)
```

### Alerte exploitation active
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.exploit_status:>=3" \
  --output-prefix urgent_$(date +%Y%m%d)
```

### Rapport mensuel complet
```bash
python scripts/prioritize_vulnerabilities.py \
  --output-prefix monthly_$(date +%Y%m) \
  --verbose
```

## ❓ Problèmes courants

### Erreur d'authentification
```bash
# Vérifier les variables
echo $FALCON_CLIENT_ID
echo $FALCON_CLIENT_SECRET
```

### Aucune vulnérabilité retournée
- Vérifier les permissions API : **Vulnerabilities READ**
- Supprimer les filtres : `--filter` et `--min-score`

### Excel non généré
```bash
pip install openpyxl
```

## 🔗 Liens utiles

- [Documentation API CrowdStrike](https://falcon.crowdstrike.com/documentation)
- [FalconPy SDK GitHub](https://github.com/CrowdStrike/falconpy)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)
