#!/bin/bash
# Quick start script for CVE prioritization

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "CrowdStrike Falcon - CVE Prioritization"
echo "============================================"
echo

# Check environment variables
if [ -z "$FALCON_CLIENT_ID" ] || [ -z "$FALCON_CLIENT_SECRET" ]; then
    echo -e "${RED}Error: Environment variables not set${NC}"
    echo
    echo "Please set the following environment variables:"
    echo "  export FALCON_CLIENT_ID=\"your_client_id\""
    echo "  export FALCON_CLIENT_SECRET=\"your_client_secret\""
    echo
    exit 1
fi

echo -e "${GREEN}✓ Credentials found${NC}"
echo

# Check Python dependencies
if ! python -c "import falconpy" 2>/dev/null; then
    echo -e "${YELLOW}Warning: falconpy not installed${NC}"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create output directory
mkdir -p reports
echo -e "${GREEN}✓ Output directory ready: ./reports${NC}"
echo

# Menu
echo "Select prioritization mode:"
echo
echo "  1) Top 20 Critical/High CVE (Quick Daily Triage)"
echo "  2) All CVE with CVSS >= 7.0 (Weekly Review)"
echo "  3) Active Exploitation Only (Urgent Response)"
echo "  4) All vulnerabilities (Full Monthly Report)"
echo "  5) Custom filter"
echo
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo
        echo -e "${YELLOW}Running: Top 20 Critical/High CVE${NC}"
        python scripts/prioritize_vulnerabilities.py \
            --filter "cve.severity:['CRITICAL','HIGH']" \
            --top 20 \
            --output-dir ./reports \
            --output-prefix daily_triage_$(date +%Y%m%d) \
            --verbose
        ;;
    2)
        echo
        echo -e "${YELLOW}Running: All CVE with CVSS >= 7.0${NC}"
        python scripts/prioritize_vulnerabilities.py \
            --min-score 7.0 \
            --output-dir ./reports \
            --output-prefix weekly_review_$(date +%Y%m%d) \
            --verbose
        ;;
    3)
        echo
        echo -e "${YELLOW}Running: Active Exploitation Only${NC}"
        python scripts/prioritize_vulnerabilities.py \
            --filter "cve.exploit_status:>=3" \
            --output-dir ./reports \
            --output-prefix active_exploitation_$(date +%Y%m%d) \
            --verbose
        ;;
    4)
        echo
        echo -e "${YELLOW}Running: Full vulnerability scan${NC}"
        python scripts/prioritize_vulnerabilities.py \
            --output-dir ./reports \
            --output-prefix full_report_$(date +%Y%m%d) \
            --verbose
        ;;
    5)
        echo
        read -p "Enter custom FQL filter: " custom_filter
        read -p "Enter minimum CVSS score [0.0]: " min_score
        min_score=${min_score:-0.0}

        echo
        echo -e "${YELLOW}Running: Custom filter${NC}"
        python scripts/prioritize_vulnerabilities.py \
            --filter "$custom_filter" \
            --min-score $min_score \
            --output-dir ./reports \
            --output-prefix custom_$(date +%Y%m%d_%H%M%S) \
            --verbose
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}Prioritization complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo
echo "Reports saved in: ./reports"
echo
ls -lh ./reports/*.{csv,json,xlsx} 2>/dev/null | tail -3
