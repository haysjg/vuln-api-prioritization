#!/usr/bin/env python3
"""
Script to explore the GetVulnerabilities API response structure
and identify fields useful for CVE prioritization.
"""

import os
import json
from falconpy import Intel

def main():
    # Authentication
    client_id = os.getenv('FALCON_CLIENT_ID')
    client_secret = os.getenv('FALCON_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("Error: FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables must be set")
        return

    # Initialize Intel service class
    falcon = Intel(client_id=client_id, client_secret=client_secret)

    # Query for a sample of vulnerabilities to examine the response structure
    print("Querying vulnerabilities to examine response structure...\n")

    # First, query vulnerability IDs (limited to 10 for exploration)
    query_response = falcon.QueryVulnerabilities(limit=10)

    if query_response['status_code'] != 200:
        print(f"Query Error: {query_response['body'].get('errors', [])}")
        return

    vuln_ids = query_response['body']['resources']
    print(f"Found {len(vuln_ids)} vulnerability IDs\n")

    if not vuln_ids:
        print("No vulnerabilities found. Try adjusting query parameters.")
        return

    # Get detailed information for these vulnerabilities
    get_response = falcon.GetVulnerabilities(ids=vuln_ids[:5])  # Get details for first 5

    if get_response['status_code'] != 200:
        print(f"Get Error: {get_response['body'].get('errors', [])}")
        return

    vulnerabilities = get_response['body']['resources']

    if vulnerabilities:
        print("=" * 80)
        print("AVAILABLE FIELDS IN GetVulnerabilities RESPONSE")
        print("=" * 80)

        # Extract all unique fields from all vulnerability records
        all_fields = set()
        sample_vuln = vulnerabilities[0]

        def extract_fields(obj, prefix=''):
            """Recursively extract field names from nested objects"""
            fields = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    field_path = f"{prefix}.{key}" if prefix else key
                    fields.append(field_path)
                    if isinstance(value, dict):
                        fields.extend(extract_fields(value, field_path))
                    elif isinstance(value, list) and value and isinstance(value[0], dict):
                        fields.extend(extract_fields(value[0], field_path))
            return fields

        all_fields = extract_fields(sample_vuln)
        all_fields = sorted(set(all_fields))

        print("\nAll available fields:")
        print("-" * 80)
        for field in all_fields:
            print(f"  - {field}")

        print(f"\nTotal fields: {len(all_fields)}")

        # Show sample vulnerability with actual values
        print("\n" + "=" * 80)
        print("SAMPLE VULNERABILITY DATA")
        print("=" * 80)
        print(json.dumps(sample_vuln, indent=2))

        # Identify fields useful for prioritization
        print("\n" + "=" * 80)
        print("FIELDS RELEVANT FOR CVE PRIORITIZATION")
        print("=" * 80)

        prioritization_fields = {
            'Severity/Impact': [
                'cve.base_score',
                'cve.severity',
                'cve.exploitability_score',
                'cve.impact_score',
                'cve.cvss_v2_base_score',
                'cve.cvss_v3_base_score',
                'cve.exploitability_score_v3',
                'cve.impact_score_v3'
            ],
            'Exploitation Status': [
                'cve.exploit_status',
                'cve.exploited_in_the_wild',
                'cve.exploit_status_to_include',
                'cve.exploit_observed'
            ],
            'Asset Exposure': [
                'apps.product_name_version',
                'apps.vendor',
                'apps.number_of_hosts_affected',
                'host_info.hostname',
                'host_info.local_ip',
                'host_info.groups'
            ],
            'Temporal Factors': [
                'cve.created_timestamp',
                'cve.published_date',
                'cve.exprt_rating',
                'created_on',
                'updated_on'
            ],
            'Remediation': [
                'remediation.action',
                'remediation.reference',
                'cve.vendor_advisory'
            ],
            'Asset Context': [
                'aid',
                'cid',
                'host_info.os_version',
                'host_info.platform_name',
                'host_info.tags'
            ]
        }

        for category, fields in prioritization_fields.items():
            print(f"\n{category}:")
            for field in fields:
                marker = "✓" if field in all_fields else "✗"
                print(f"  {marker} {field}")

    else:
        print("No vulnerability details returned")

if __name__ == "__main__":
    main()
