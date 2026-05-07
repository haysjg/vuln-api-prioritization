# Référence complète des champs - API GetVulnerabilities

## 📋 Vue d'ensemble

Cette référence liste TOUS les champs disponibles dans l'API CrowdStrike Falcon `GetVulnerabilities`.

Les champs marqués **⭐** sont particulièrement utiles pour la priorisation des CVE.

---

## 🔑 Champs principaux

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `id` | string | Identifiant unique de la vulnérabilité | |
| `cid` | string | Customer ID | |
| `aid` | string | Agent ID (hôte) | |
| `created_on` | timestamp | Date de création | |
| `updated_on` | timestamp | Dernière mise à jour | ⭐ Temporel |

---

## 🛡️ Objet CVE (cve.*)

### Identification

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `cve.id` | string | CVE ID (ex: CVE-2024-1234) | ⭐ Identité |
| `cve.description` | string | Description de la vulnérabilité | |
| `cve.cwe_id` | string | Common Weakness Enumeration ID | |
| `cve.references` | array | Liens et références | |

### Scores de sévérité

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`cve.base_score`** | float | **Score CVSS de base (0-10)** | ⭐⭐⭐ Score principal |
| **`cve.severity`** | string | **Sévérité (CRITICAL/HIGH/MEDIUM/LOW)** | ⭐⭐⭐ Classification |
| **`cve.cvss_v3_base_score`** | float | **Score CVSS version 3** | ⭐⭐ Score moderne |
| `cve.cvss_v2_base_score` | float | Score CVSS version 2 (legacy) | |

### Scores détaillés

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`cve.exploitability_score`** | float | **Facilité d'exploitation (0-10)** | ⭐⭐ Impact technique |
| **`cve.impact_score`** | float | **Impact potentiel (0-10)** | ⭐⭐ Impact technique |
| `cve.exploitability_score_v3` | float | Score d'exploitabilité CVSS v3 | |
| `cve.impact_score_v3` | float | Score d'impact CVSS v3 | |

### Vecteur d'attaque

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `cve.vector` | string | Vecteur CVSS (ex: AV:N/AC:L/PR:N/UI:N) | ⭐ Contexte |
| `cve.attack_vector` | string | Vecteur d'attaque (Network/Adjacent/Local) | |
| `cve.attack_complexity` | string | Complexité (Low/High) | |
| `cve.privileges_required` | string | Privilèges requis (None/Low/High) | |
| `cve.user_interaction` | string | Interaction utilisateur (None/Required) | |

### Exploitation (CRITIQUE pour priorisation)

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`cve.exploit_status`** | integer | **Statut d'exploitation (0-4)** | ⭐⭐⭐ Menace réelle |
| `cve.exploit_status_to_include` | array | Statuts inclus | |
| `cve.exploit_observed` | boolean | Exploitation observée | ⭐⭐ Alerte |
| `cve.exploited_in_the_wild` | boolean | Exploitée "in the wild" | ⭐⭐⭐ Alerte critique |

**Valeurs de exploit_status :**
- `0` = Non exploitée
- `1` = PoC (Proof of Concept) existe
- `2` = Exploit public disponible
- `3` = Exploitation active observée
- `4` = Exploitation massive (ransomware, etc.)

### Dates et temporalité

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`cve.published_date`** | timestamp | **Date de publication du CVE** | ⭐⭐ Ancienneté |
| `cve.created_timestamp` | timestamp | Date de création | |
| `cve.modified_date` | timestamp | Dernière modification | |

### Évaluation experte

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`cve.exprt_rating`** | string | **Rating des experts CrowdStrike (CTI)** | ⭐⭐⭐ Intel CTI |
| `cve.vendor_advisory` | array | Avis officiels du vendeur | ⭐ Remédiation |

**Valeurs de exprt_rating :**
- `CRITICAL` = 100 points - Menace active critique, exploitation massive observée
- `HIGH` = 70 points - Menace sérieuse avec exploitation probable ou active
- `MEDIUM` = 40 points - Risque modéré
- `LOW` = 10 points - Faible priorité
- `INFORMATIONAL` = 0 points - Information uniquement
- `N/A` = 0 points - Pas d'évaluation disponible

**🔥 L'Expert Rating est l'un des facteurs les plus importants** car il incorpore :
- Intelligence sur les menaces actives (CTI)
- Observation d'exploitation par des threat actors
- Qualité et facilité d'exploitation réelle
- Impact observé dans le wild
- Disponibilité des mitigations

---

## 💻 Applications affectées (apps[])

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `apps[].product_name` | string | Nom du produit | |
| `apps[].product_name_version` | string | Produit + version | ⭐ Identification |
| `apps[].vendor` | string | Éditeur du logiciel | ⭐ Identification |
| **`apps[].number_of_hosts_affected`** | integer | **Nombre d'hôtes touchés** | ⭐⭐⭐ Exposition |
| `apps[].category` | string | Catégorie d'application | |

### Remédiation par application

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `apps[].remediation.action` | string | Action recommandée | ⭐⭐ Action |
| `apps[].remediation.reference` | string | Référence pour patch/update | ⭐⭐ Action |
| `apps[].remediation.ids` | array | IDs de remédiation | |

---

## 🖥️ Informations sur l'hôte (host_info.*)

### Identification

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `host_info.hostname` | string | Nom de l'hôte | ⭐ Identification |
| `host_info.local_ip` | string | Adresse IP locale | |
| `host_info.external_ip` | string | Adresse IP publique | |
| `host_info.mac_address` | string | Adresse MAC | |

### Système d'exploitation

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`host_info.platform_name`** | string | **Plateforme (Windows/Linux/Mac)** | ⭐⭐ Contexte OS |
| `host_info.os_version` | string | Version du système | ⭐ Version |
| `host_info.os_build` | string | Build du système | |
| `host_info.kernel_version` | string | Version du kernel | |

### Contexte business (ESSENTIEL pour priorisation)

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| **`host_info.groups`** | array | **Groupes d'hôtes** | ⭐⭐⭐ Criticité |
| **`host_info.tags`** | array | **Tags custom (criticité business)** | ⭐⭐⭐ Criticité |
| `host_info.site_name` | string | Nom du site/datacenter | ⭐ Géographie |
| `host_info.ou` | string | Organizational Unit (AD) | ⭐ Structure |

**Exemples de groupes/tags critiques :**
- `production`, `prod-servers`
- `domain-controllers`, `dc`
- `pci-dss`, `sox`, `hipaa`
- `crown-jewels`, `tier-0`
- `database-servers`, `web-servers`
- `customer-facing`, `dmz`

### Agent et gestion

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `host_info.agent_version` | string | Version de l'agent Falcon | |
| `host_info.agent_load_flags` | string | Flags de chargement | |
| `host_info.service_provider` | string | Fournisseur cloud | |
| `host_info.first_seen` | timestamp | Première détection | |
| `host_info.last_seen` | timestamp | Dernière vue | |

---

## 🩹 Remédiation globale (remediation.*)

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `remediation.ids` | array | Liste d'IDs de remédiation | |
| `remediation.reference` | string | URL ou référence | ⭐⭐ Documentation |
| `remediation.action` | string | Action (patch/update/mitigate) | ⭐⭐ Action |
| `remediation.available` | boolean | Remédiation disponible | ⭐ Status |

---

## 📊 Métadonnées de réponse (meta.*)

| Champ | Type | Description | Priorisation |
|-------|------|-------------|--------------|
| `meta.pagination.offset` | string | Offset pour pagination | |
| `meta.pagination.limit` | integer | Limite par page | |
| `meta.pagination.total` | integer | Total de résultats | |
| `meta.query_time` | float | Temps de requête (ms) | |
| `meta.trace_id` | string | ID de trace pour debug | |

---

## 🎯 Matrice de priorisation recommandée

### Niveau 1 : CRITIQUE (Score > 250)
- ✅ Exploitation active (`exploit_status >= 3`)
- ✅ CVSS >= 9.0
- ✅ Actifs critiques (`host_info.groups/tags`)
- ✅ Nombreux hôtes affectés (>50)

### Niveau 2 : HAUTE (Score 150-250)
- ✅ Exploit public disponible (`exploit_status = 2`)
- ✅ CVSS 7.0-8.9
- ✅ Actifs production
- ✅ Ancienneté > 90 jours

### Niveau 3 : MOYENNE (Score 50-150)
- ✅ PoC existe (`exploit_status = 1`)
- ✅ CVSS 4.0-6.9
- ✅ Quelques hôtes affectés

### Niveau 4 : BASSE (Score < 50)
- ✅ Non exploitée (`exploit_status = 0`)
- ✅ CVSS < 4.0
- ✅ Peu d'exposition

---

## 🔍 Filtres FQL utiles

### Par sévérité
```
cve.severity:['CRITICAL','HIGH']
```

### Par exploitation
```
cve.exploit_status:>=3
cve.exploited_in_the_wild:true
```

### Par score CVSS
```
cve.base_score:>=7.0
cve.cvss_v3_base_score:>=9.0
```

### Par plateforme
```
host_info.platform_name:'Windows'
host_info.platform_name:['Linux','Mac']
```

### Par groupes
```
host_info.groups:*'production'*
host_info.groups:*'domain-controllers'*
```

### Combinaisons
```
cve.severity:'CRITICAL'+cve.exploit_status:>=2+host_info.groups:*'prod'*
```

---

## 📚 Ressources

- **API Swagger** : https://assets.falcon.crowdstrike.com/support/api/swagger.html
- **FalconPy Docs** : https://github.com/CrowdStrike/falconpy/wiki
- **CVSS Calculator** : https://www.first.org/cvss/calculator/3.1

---

## 💡 Conseils d'utilisation

1. **Toujours combiner plusieurs facteurs** - Ne jamais se baser uniquement sur CVSS
2. **Prioriser l'exploitation active** - `exploit_status >= 3` doit être traité en urgence
3. **Contextualiser par business** - Utiliser `host_info.groups` et `tags`
4. **Surveiller les Expert Ratings** - Les analystes CrowdStrike apportent de l'intel CTI
5. **Automatiser la priorisation** - Utiliser le script `prioritize_vulnerabilities.py`

---

*Généré pour le projet API-calls-with-FalconPy*
