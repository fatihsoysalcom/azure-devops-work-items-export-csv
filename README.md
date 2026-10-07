# Azure DevOps Work Items Export CSV

This example demonstrates how to programmatically fetch Azure DevOps work items using Python and export them to a CSV file. This approach provides a flexible way to extract work item data for analysis or reporting in tools like Microsoft Excel, especially when native Excel add-ins are not available or suitable on platforms like macOS. It connects to your Azure DevOps organization, queries for specific work items, and writes their details to a local CSV file that can be opened in Excel.

## Language

`python`

## How to Run

1. Install the required library: `pip install azure-devops`
2. Set environment variables: `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PROJECT`, and `AZURE_DEVOPS_PAT` (with 'Work Items (Read)' permissions). Alternatively, update the placeholder values directly in the `main.py` script.
3. Run the script: `python main.py`
   A CSV file named `azure_devops_work_items.csv` will be created in the same directory, ready to be opened in Excel.

## Original Article

This example accompanies the Turkish article: [Mac'te Excel ile Azure DevOps İş Öğeleri: Neler Çalışır, Neler Çalışmaz?](https://fatihsoysal.com/blog/macte-excel-ile-azure-devops-is-ogeleri-neler-calisir-neler-calismaz/).

## License

MIT — see [LICENSE](LICENSE).
