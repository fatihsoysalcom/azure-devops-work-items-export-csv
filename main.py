import os
import csv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# --- Configuration (replace with your values or set environment variables) ---
# Your Azure DevOps organization URL (e.g., 'https://dev.azure.com/your-organization')
AZURE_DEVOPS_ORG_URL = os.environ.get('AZURE_DEVOPS_ORG_URL', 'https://dev.azure.com/your-organization')
# Your Azure DevOps project name (e.g., 'MyProject')
AZURE_DEVOPS_PROJECT = os.environ.get('AZURE_DEVOPS_PROJECT', 'MyProject')
# Your Personal Access Token (PAT) with Work Items Read permissions
# Generate one at: https://dev.azure.com/{your-organization}/_usersSettings/tokens
AZURE_DEVOPS_PAT = os.environ.get('AZURE_DEVOPS_PAT', 'YOUR_PAT_HERE')

OUTPUT_CSV_FILE = 'azure_devops_work_items.csv'

def main():
    if AZURE_DEVOPS_PAT == 'YOUR_PAT_HERE' or not AZURE_DEVOPS_ORG_URL or not AZURE_DEVOPS_PROJECT:
        print("ERROR: Please set AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PROJECT, and AZURE_DEVOPS_PAT environment variables or update the script.")
        print("       You can generate a PAT at: https://dev.azure.com/{your-organization}/_usersSettings/tokens")
        return

    # Create a connection to the Azure DevOps organization using BasicAuthentication with PAT
    credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
    connection = Connection(base_url=AZURE_DEVOPS_ORG_URL, creds=credentials)

    # Get a client for the Work Item Tracking API to interact with work items
    wit_client = connection.clients.get_work_item_tracking_client()

    print(f"Connecting to Azure DevOps organization: {AZURE_DEVOPS_ORG_URL}")
    print(f"Fetching work items from project: {AZURE_DEVOPS_PROJECT}")

    # Define a Work Item Query Language (WIQL) query to select work items.
    # This query fetches all 'Task', 'Bug', and 'User Story' work items in the specified project.
    # Customize the WHERE clause to filter by type, state, iteration, etc., as needed for your Excel report.
    wiql_query = f"""
        SELECT
            [System.Id],
            [System.WorkItemType],
            [System.Title],
            [System.State],
            [System.AssignedTo],
            [System.CreatedDate]
        FROM
            WorkItems
        WHERE
            [System.TeamProject] = '{AZURE_DEVOPS_PROJECT}'
            AND [System.WorkItemType] IN ('Task', 'Bug', 'User Story')
        ORDER BY
            [System.Id]
    """

    try:
        # Execute the WIQL query to get a list of work item references (IDs and URLs)
        query_results = wit_client.query_by_wiql(wiql={'query': wiql_query}).work_items

        if not query_results:
            print("No work items found matching the query.")
            return

        # Extract just the work item IDs from the query results
        work_item_ids = [wi.id for wi in query_results]

        # Define the specific fields you want to export. These will become your CSV columns.
        # This allows you to control the data structure for Excel analysis.
        fields_to_export = [
            'System.Id',
            'System.WorkItemType',
            'System.Title',
            'System.State',
            'System.AssignedTo',
            'System.CreatedDate',
            'System.Description'
        ]
        # Fetch the full details for the identified work items, including the specified fields
        work_items = wit_client.get_work_items(ids=work_item_ids, fields=fields_to_export)

        # Prepare data for CSV export, which Excel can easily open and format.
        csv_data = []
        # Create CSV header from the last part of the field names (e.g., 'Id', 'WorkItemType')
        csv_header = [field.split('.')[-1] for field in fields_to_export]
        csv_data.append(csv_header)

        for item in work_items:
            row = []
            for field in fields_to_export:
                # Retrieve the value for each field, defaulting to an empty string if not found
                value = item.fields.get(field, '')
                # Special handling for 'AssignedTo' field to get just the display name
                if field == 'System.AssignedTo' and isinstance(value, dict):
                    row.append(value.get('displayName', ''))
                else:
                    row.append(str(value))
            csv_data.append(row)

        # Write the collected data to a CSV file.
        # This file can then be opened directly in Excel on any OS (including Mac) for viewing, filtering, and analysis.
        with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)

        print(f"Successfully exported {len(work_items)} work items to '{OUTPUT_CSV_FILE}'.")
        print(f"You can now open '{OUTPUT_CSV_FILE}' in Excel for viewing and analysis.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PROJECT, and AZURE_DEVOPS_PAT are correct and the PAT has 'Work Items (Read)' permissions.")

if __name__ == '__main__':
    main()
