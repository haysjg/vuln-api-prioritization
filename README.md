# CrowdStrike Falcon - CVE Prioritization System

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FalconPy](https://img.shields.io/badge/FalconPy-1.6.0+-green.svg)](https://github.com/CrowdStrike/falconpy)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Advanced CVE prioritization system for CrowdStrike Falcon that combines **CVSS scores** with **CrowdStrike Expert Rating** (CTI-based threat intelligence) to provide **risk-based vulnerability prioritization**.

## 🎯 What Makes This Different?

Traditional vulnerability management relies solely on CVSS scores, which don't reflect **real-world exploitation**. This system integrates:

- ✅ **CrowdStrike Expert Rating** - CTI analysis from 25+ trillion security events/week
- ✅ **Active Exploitation Status** - Real-time threat actor activity tracking
- ✅ **Asset Context** - Criticality based on your business (production, domain controllers, PCI, etc.)
- ✅ **Exposure Volume** - Number of affected hosts in your environment
- ✅ **CVSS Technical Score** - Traditional vulnerability severity
- ✅ **Age Factor** - Time since vulnerability disclosure

**Result**: Prioritize vulnerabilities based on **actual risk** to your organization, not just theoretical severity.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/haysjg/vuln-api-prioritization.git
cd vuln-api-prioritization

# Install dependencies
pip install crowdstrike-falconpy openpyxl

# Set up credentials
export FALCON_CLIENT_ID="your_client_id"
export FALCON_CLIENT_SECRET="your_client_secret"

# Test installation
python scripts/test_prioritization.py
```

### Run Prioritization

```bash
# Interactive menu (recommended)
./scripts/run_prioritization.sh          # Linux/Mac
.\scripts\run_prioritization.ps1         # Windows

# Or command line
python scripts/prioritize_vulnerabilities.py --verbose --top 20
```

### Output

The script generates **3 formats**:
- **CSV** - Import into Excel/Google Sheets
- **JSON** - Automation and API integration
- **XLSX** - Excel with color-coding by severity

## 📊 Scoring Formula

```
Priority Score = (CVSS × 10) + (Expert Rating × 0.8) + (Exploitation × 30) +
                 (Hosts × 0.5) + (Asset Criticality × 50) + (Age × 0.1)
```

### Example

**CVE-2024-1234**: CVSS 7.5, Expert Rating CRITICAL, Active Exploitation, 50 hosts, Production servers
```
Score = (7.5 × 10) + (100 × 0.8) + (90) + (25) + (50) + (3)
      = 75 + 80 + 90 + 25 + 50 + 3
      = 323 points → Priority Rank #2
```

**Without Expert Rating**, same CVE would score only 243 points (rank #45).

## 🔥 Why Expert Rating Matters

The **CrowdStrike Expert Rating** is the game-changer:

| Scenario | CVSS | Expert Rating | Traditional Rank | With Expert Rating | Result |
|----------|------|---------------|------------------|--------------------|--------|
| CVE actively exploited by ransomware groups | 7.5 (HIGH) | CRITICAL | #45 | #2 | ✅ **Correctly prioritized** |
| CVE with high CVSS but no exploitation | 9.8 (CRITICAL) | LOW | #3 | #28 | ✅ **Realistically deprioritized** |

👉 **Read more**: [Why Expert Rating is Crucial](docs/EXPERT_RATING_IMPORTANCE.md)

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART_CVE_PRIORITIZATION.md)** - Get started in 5 minutes
- **[Complete Guide](docs/CVE_PRIORITIZATION.md)** - Full documentation with examples
- **[Expert Rating Deep Dive](docs/EXPERT_RATING_IMPORTANCE.md)** - Why CTI-based prioritization matters
- **[API Field Reference](docs/API_FIELDS_REFERENCE.md)** - All available Falcon API fields
- **[Changelog v2.0](CHANGELOG_V2.md)** - Technical details and migration guide

## 🛠️ Features

### Intelligent Scoring
- Multi-factor risk assessment combining 6 data points
- CrowdStrike CTI integration (Expert Rating)
- Customizable scoring weights via JSON config
- 5 pre-built strategies (Balanced, CTI-Driven, Aggressive, Exposure-Focused, Severity-Only)

### Asset Context
- Automatic detection of critical assets (production, domain controllers, PCI, etc.)
- Host group and tag-based criticality
- Customizable asset indicators

### Export & Reporting
- CSV for spreadsheet analysis
- JSON for automation/SOAR integration
- Excel with color-coded severity (Critical=Red, High=Orange, Medium=Yellow, Low=Green)
- Summary statistics and distribution analysis

### Scalability
- Automatic pagination for large environments
- Batch processing (5000 IDs, 200 details per batch)
- Handles 10,000+ vulnerabilities efficiently

## ⚙️ Configuration

Customize scoring weights in `config/prioritization_config.json`:

### Balanced Strategy (Default)
```json
{
  "cvss_weight": 10,
  "expert_rating_weight": 80,
  "exploit_status_weight": 30,
  "hosts_affected_weight": 0.5,
  "asset_criticality_weight": 50,
  "age_weight": 0.1
}
```

### CTI-Driven Strategy (Maximum Threat Intelligence)
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

## 🎯 Use Cases

### Daily SOC Triage
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.severity:['CRITICAL','HIGH']" \
  --top 50
```

### Active Exploitation Response
```bash
python scripts/prioritize_vulnerabilities.py \
  --filter "cve.exploit_status:>=3"
```

### Weekly Vulnerability Review
```bash
python scripts/prioritize_vulnerabilities.py \
  --min-score 7.0 \
  --output-prefix weekly_review_$(date +%Y%m%d)
```

### Monthly Comprehensive Report
```bash
python scripts/prioritize_vulnerabilities.py \
  --verbose \
  --output-prefix monthly_report_$(date +%Y%m)
```

## 🔐 Security

- ✅ No hardcoded credentials
- ✅ Environment variable authentication only
- ✅ `.gitignore` configured to exclude credentials
- ✅ No sensitive data in exports

**Required API Permissions**: `Vulnerabilities: READ`

## 📊 Example Output

```
================================================================================
VULNERABILITY PRIORITIZATION SUMMARY
================================================================================

Severity Distribution:
  CRITICAL: 87
  HIGH: 324
  MEDIUM: 612

Expert Rating Distribution:
  CRITICAL: 23
  HIGH: 156
  MEDIUM: 421

Exploitation Status:
  Widespread Exploitation: 5
  Active Exploitation: 23
  Public Exploit Available: 156

Critical Assets Affected: 143
Total Host Instances Affected: 8,456

================================================================================
TOP PRIORITY VULNERABILITIES
================================================================================

#    Score    CVE ID             CVSS   Severity   Expert     Exploit Status            Hosts
-------------------------------------------------------------------------------------------
1    287.45   CVE-2024-1234      9.8    CRITICAL   CRITICAL   Widespread Exploitation   45
2    245.20   CVE-2024-5678      9.1    CRITICAL   HIGH       Active Exploitation       67
3    198.30   CVE-2023-9012      8.8    HIGH       CRITICAL   Public Exploit Available  123
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Built on [CrowdStrike FalconPy SDK](https://github.com/CrowdStrike/falconpy)
- Leverages CrowdStrike Threat Intelligence
- Inspired by real-world SOC/vulnerability management challenges

## 📞 Support

- **Documentation**: See `/docs` directory
- **Issues**: [GitHub Issues](https://github.com/haysjg/vuln-api-prioritization/issues)
- **CrowdStrike API Docs**: https://falcon.crowdstrike.com/documentation

---

**Version**: 2.0
**Author**: Security Operations Team
**Last Updated**: 2026-05-07

Made with ❤️ to make vulnerability management less painful.
