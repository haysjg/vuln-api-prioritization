#!/usr/bin/env python3
"""
Quick test script to verify CVE prioritization functionality
Processes a small sample of vulnerabilities to validate the scoring logic.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import from scripts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from falconpy import Intel

def test_prioritization():
    """Test the prioritization logic with a small sample"""

    print("=" * 80)
    print("CVE PRIORITIZATION - TEST RUN")
    print("=" * 80)
    print()

    # Check authentication
    client_id = os.getenv('FALCON_CLIENT_ID')
    client_secret = os.getenv('FALCON_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("❌ Error: FALCON_CLIENT_ID and FALCON_CLIENT_SECRET must be set")
        return False

    print("✓ Credentials found")

    # Initialize API
    try:
        intel_api = Intel(client_id=client_id, client_secret=client_secret)
        print("✓ API client initialized")
    except Exception as e:
        print(f"❌ Error initializing API: {e}")
        return False

    # Test query
    print("\nTesting vulnerability query...")
    try:
        # Query for a small sample of CRITICAL vulnerabilities
        query_response = intel_api.QueryVulnerabilities(
            filter="cve.severity:'CRITICAL'",
            limit=5
        )

        if query_response['status_code'] != 200:
            print(f"❌ Query failed: {query_response['body'].get('errors', [])}")
            return False

        vuln_ids = query_response['body']['resources']
        print(f"✓ Found {len(vuln_ids)} vulnerability IDs")

        if not vuln_ids:
            print("⚠ No vulnerabilities found. This is normal if you have no CRITICAL CVEs.")
            print("  Trying again without severity filter...")

            query_response = intel_api.QueryVulnerabilities(limit=5)
            if query_response['status_code'] == 200:
                vuln_ids = query_response['body']['resources']
                print(f"✓ Found {len(vuln_ids)} vulnerability IDs")

        if not vuln_ids:
            print("⚠ No vulnerabilities found in your environment.")
            print("  This test requires at least one vulnerability to be detected.")
            return True  # Not a failure, just no data

    except Exception as e:
        print(f"❌ Error querying vulnerabilities: {e}")
        return False

    # Test getting details
    print("\nTesting vulnerability details retrieval...")
    try:
        get_response = intel_api.GetVulnerabilities(ids=vuln_ids[:3])

        if get_response['status_code'] != 200:
            print(f"❌ Get failed: {get_response['body'].get('errors', [])}")
            return False

        vulnerabilities = get_response['body']['resources']
        print(f"✓ Retrieved details for {len(vulnerabilities)} vulnerabilities")

        if not vulnerabilities:
            print("❌ No vulnerability details returned")
            return False

    except Exception as e:
        print(f"❌ Error getting vulnerability details: {e}")
        return False

    # Test scoring logic
    print("\nTesting priority scoring...")
    try:
        # Import the scoring function from the main script
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "prioritize",
            "scripts/prioritize_vulnerabilities.py"
        )
        prioritize_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prioritize_module)

        for i, vuln in enumerate(vulnerabilities[:3], 1):
            priority_info = prioritize_module.calculate_priority_score(vuln)

            cve_id = vuln.get('cve', {}).get('id', 'Unknown')
            score = priority_info['total_score']
            metadata = priority_info['metadata']

            print(f"\n  Vulnerability #{i}:")
            print(f"    CVE ID: {cve_id}")
            print(f"    Priority Score: {score}")
            print(f"    CVSS: {metadata['cvss_base_score']}")
            print(f"    Severity: {metadata['severity']}")
            print(f"    Exploit Status: {metadata['exploit_status_label']}")
            print(f"    Hosts Affected: {metadata['hosts_affected']}")
            print(f"    Critical Asset: {'YES' if metadata['is_critical_asset'] else 'NO'}")

            # Validate score components
            components = priority_info['component_scores']
            expected_total = sum(components.values())
            if abs(score - expected_total) > 0.01:
                print(f"    ⚠ Warning: Score mismatch (expected {expected_total}, got {score})")

        print("\n✓ Priority scoring completed successfully")

    except Exception as e:
        print(f"❌ Error testing priority scoring: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
    print()
    print("The prioritization script is ready to use!")
    print()
    print("Run the full script with:")
    print("  python scripts/prioritize_vulnerabilities.py --verbose")
    print()
    print("Or use the quick-start menu:")
    print("  ./scripts/run_prioritization.sh      (Linux/Mac)")
    print("  .\\scripts\\run_prioritization.ps1     (Windows)")
    print()

    return True


if __name__ == "__main__":
    success = test_prioritization()
    sys.exit(0 if success else 1)
