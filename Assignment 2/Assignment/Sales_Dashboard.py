"""Interactive sales dashboard for exploring a Google Drive CSV file."""

# Add-ons used to report the load time, print timestamps, and check export filenames.
from datetime import datetime
import os
import time

# Pandas reads the CSV, builds the analysis tables, and writes Excel output.
import pandas as pd


# Keep each report's required columns together so startup checks and report guards agree.
ANALYTICS_REQUIRED_FIELDS = {
    "Total sales by region and order type": (
        "sales_region",
        "order_type",
        "quantity",
        "unit_price",
    ),
    "Average sales by region with average sales by state and sale type": (
        "sales_region",
        "customer_state",
        "order_type",
        "quantity",
        "unit_price",
    ),
    "Sales by customer type and order type by state": (
        "customer_type",
        "order_type",
        "customer_state",
        "quantity",
        "unit_price",
    ),
    "Total sales quantity and price by region and product": (
        "sales_region",
        "produce_name",
        "quantity",
        "unit_price",
    ),
    "Total sales quantity and price by customer type": (
        "order_type",
        "customer_type",
        "quantity",
        "unit_price",
    ),
    "Maximum and minimum sales price by category": ("product_category", "unit_price"),
    "Number of unique employees by region": ("sales_region", "employee_id"),
}

# Store completed tables here so the menu can list and display them later.
stored_results = {}


def load_csv(filepath):
    """Load and validate sales data, replace missing values, and report load details."""
    # Tell the user loading has started before the network read begins.
    print("Loading sales_data.csv from Google Drive...", flush=True)
    # Start a timer so the load duration can be reported after a successful read.
    start_time = time.perf_counter()

    # Read the remote or local CSV; stop the program if reading fails.
    try:
        df = pd.read_csv(filepath)
    except Exception as error:
        raise SystemExit(f"Error: Could not load sales_data.csv: {error}")

    # Reject files with no rows or columns because they cannot support the dashboard.
    if df.empty or len(df.columns) == 0:
        raise SystemExit("Error: sales_data.csv contains no usable data.")

    # Trim header whitespace so field checks match the expected column names.
    df.columns = [str(column).strip() for column in df.columns]
    # A blank or duplicate header makes it unclear which column an analysis should use.
    for column in df.columns:
        if not column:
            raise SystemExit("Error: sales_data.csv contains a blank column name.")
    if len(df.columns) != len(set(df.columns)):
        raise SystemExit("Error: sales_data.csv contains duplicate column names.")

    # Remember numeric columns before filling nulls so their numeric types can be restored.
    numeric_columns = list(df.select_dtypes(include="number").columns)
    # Use zero for missing cells across text and numeric fields.
    df = df.astype(object).fillna(0)
    # These known measures may have been read as text; convert them to numbers too.
    for column in ("quantity", "unit_price", "employee_id", "sale_price"):
        if column not in numeric_columns:
            numeric_columns.append(column)
    # Invalid numeric cells become zero so later calculations and pivots can proceed.
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    # Report when loading completed, how long it took, and the fields available.
    load_time = time.perf_counter() - start_time
    loaded_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"sales_data.csv loaded successfully at {loaded_at}.")
    print(f"Load time: {load_time:.2f} seconds.")
    print(f"Number of rows: {len(df)}")
    print("Available columns: " + ", ".join(str(column) for column in df.columns))
    return df


def display_initial_rows(data):
    """Ask the user how many initial rows to show and print them.

    An empty response skips the preview. Accepts a positive integer or 'all';
    invalid entries are reported and the user is re-prompted.
    """
    # Avoid asking for a range when the file contains no records.
    if data.empty:
        print("No rows are available to display.")
        return

    # Repeat the prompt until the user skips, asks for all rows, or gives a valid count.
    while True:
        response = input(
            "\nEnter rows to display:\n"
            f"- Enter a number 1 to {len(data)}\n"
            "- To see all rows, enter 'all'\n"
            "- To skip preview, press Enter\n"
            "Your choice: "
        ).strip().lower()

        # Enter means the user wants to skip the data preview.
        if not response:
            return

        # Show all records only when the user explicitly enters "all".
        if response == "all":
            pd.set_option("display.max_rows", None)
            print(data)
            offer_excel_export(data, "Sales data")
            return

        # Reject words and other non-integer input without ending the dashboard.
        try:
            num_rows = int(response)
        except ValueError:
            print(
                f"Invalid input '{response}'. Enter a number from 1 to {len(data)}, "
                "'all', or press Enter to skip."
            )
            continue

        # Restrict the row count to the actual number of loaded records.
        if not 1 <= num_rows <= len(data):
            print(f"Invalid number. Enter a number from 1 to {len(data)}.")
            continue

        # Display exactly the requested leading rows and offer to export that preview.
        preview = data.head(num_rows)
        print(preview)
        offer_excel_export(preview, "Sales data preview")
        return


def offer_excel_export(results, result_name):
    """Offer to save a displayed DataFrame as an Excel workbook."""
    # Ask for an explicit yes/no before creating a file.
    while True:
        response = input(
            f"\nWould you like to export these {result_name.lower()} results to Excel? (y/n): "
        ).strip().lower()
        if response in {"n", "no"}:
            return
        if response in {"y", "yes"}:
            break
        print("Please enter 'y' or 'n'.")

    # Require a filename, use the Excel extension, and avoid silently overwriting.
    while True:
        filename = input("Enter a filename for the Excel file (.xlsx): ").strip()
        if not filename:
            print("A filename is required.")
            continue
        if not filename.lower().endswith(".xlsx"):
            filename = filename + ".xlsx"
        if os.path.exists(filename):
            print("That file already exists. Choose a different filename.")
            continue
        break

    # Reset the index so pivot row labels become ordinary Excel columns.
    try:
        excel_results = results.reset_index()
        # Excel interprets formula-like text as formulas, so escape those cell values.
        excel_results.columns = [str(column) for column in excel_results.columns]
        for column in excel_results.columns:
            excel_results[column] = excel_results[column].map(escape_excel_text)
        excel_results.to_excel(filename, sheet_name="Results", index=False)
    except Exception as error:
        print(f"Could not export results to '{filename}': {error}")
        return

    # Confirm the destination only after the workbook was written successfully.
    print(f"Results exported to: {filename}")


def escape_excel_text(value):
    """Prevent text values from being interpreted as formulas by spreadsheet apps."""
    # Prefix suspicious leading characters so spreadsheet programs treat text as text.
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    # Leave ordinary text and numeric cells unchanged.
    return value


def store_result(result_name, result):
    """Keep the latest standard analysis or a separately named custom pivot."""
    # Preserve every custom configuration by assigning it the next unused number.
    if result_name == "Custom pivot table":
        number = 1
        while f"{result_name} {number}" in stored_results:
            number += 1
        result_name = f"{result_name} {number}"
    # Replace earlier versions of standard reports and store a snapshot of the table.
    stored_results[result_name] = result.copy()
    return result_name


def show_stored_results(data=None):
    """Display every pivot table generated during this dashboard session."""
    # Tell the user when there are no reports to display yet.
    if not stored_results:
        print("\nNo analysis results have been stored yet.")
        return

    print("\n--- Stored Analysis Results ---")
    # Print each saved report name followed by its complete table.
    for result_name, result in stored_results.items():
        print(f"\n{result_name}:")
        print(result)


def show_employees_by_region(data):
    """Print the number of unique employees in each sales region."""
    # Do not attempt this report when one of its grouping/count fields is absent.
    if not report_requirements_met(
        data, "Number of unique employees by region"
    ):
        return

    # Work on a copy so report cleanup does not modify the source sales DataFrame.
    report_data = data.copy()
    # Treat any remaining blank employee IDs consistently when counting distinct IDs.
    report_data["employee_id"] = report_data["employee_id"].replace("", 0)
    # Build one row per region and count distinct employee identifiers.
    counts = pd.pivot_table(
        report_data,
        index="sales_region",
        values="employee_id",
        aggfunc="nunique",
        dropna=False,
    )
    # Give the output column a label that explains the distinct-count result.
    counts = counts.rename(columns={"employee_id": "unique_employees"})
    # Save the pivot before printing so it can also appear in the stored-results menu.
    store_result("Number of unique employees by region", counts)
    # Print the report and offer the same table as an Excel workbook.
    print("\nNumber of employees by region:")
    print(counts)
    offer_excel_export(counts, "employee counts by region")


def missing_required_fields(data, required_fields):
    """Return required column names that are absent from the loaded data."""
    # Keep only required names that are not present in the DataFrame headers.
    return [field for field in required_fields if field not in data.columns]


def warn_about_missing_analytics_fields(data):
    """Explain which built-in analyses may be unavailable because of missing columns."""
    # Record missing fields by report so one startup warning can explain all gaps.
    missing_analytics = {}
    for analytics, fields in ANALYTICS_REQUIRED_FIELDS.items():
        missing = missing_required_fields(data, fields)
        if missing:
            missing_analytics[analytics] = missing

    # Skip the warning when every built-in report has its required fields.
    if missing_analytics:
        print(
            "\nWarning: Some dashboard analytics may not work because required "
            "columns are missing:"
        )
        for analytics, missing in missing_analytics.items():
            print(f"- {analytics}: {', '.join(missing)}")


def report_requirements_met(data, analytics_name):
    """Print a useful message and return whether an analysis has all its columns."""
    # Look up the columns this analysis needs in the central requirements table.
    required_fields = ANALYTICS_REQUIRED_FIELDS[analytics_name]
    # Return False after explaining the missing fields; callers then safely stop.
    missing = missing_required_fields(data, required_fields)
    if missing:
        print(
            f"Cannot run '{analytics_name}'. Missing required columns: "
            + ", ".join(missing)
        )
        return False
    return True


def numeric_column(data, column):
    """Convert a report field to numbers, treating invalid values as zero."""
    # Coerce bad text to missing values, then replace those values with zero.
    return pd.to_numeric(data[column], errors="coerce").fillna(0)


def sales_amount(data):
    """Return each row's sales value, calculated as quantity multiplied by unit price."""
    # Calculate row-level revenue using numeric-safe quantity and unit-price values.
    return numeric_column(data, "quantity") * numeric_column(data, "unit_price")


def show_total_sales_by_region_and_order_type(data):
    """Print sales revenue totals for each region and order type."""
    # Check required fields before constructing the sales pivot.
    if not report_requirements_met(data, "Total sales by region and order type"):
        return

    # Copy the input so the derived sales column is not added to the shared source data.
    report_data = data.copy()
    # Calculate revenue for each order as quantity multiplied by unit price.
    report_data["sales"] = sales_amount(data)
    # Sum revenue by region, with a separate output column for each order type.
    report = report_data.pivot_table(
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    # Save, print, and optionally export the completed pivot table.
    store_result("Total sales by region and order type", report)
    print("\nTotal sales by region and order type:")
    print(report.round(2))
    offer_excel_export(report, "sales by region and order type")


def get_user_selection(options, prompt, required=False, single=False):
    """Prompt for comma-separated option numbers and return the chosen options.

    Re-prompts on invalid input. An empty entry returns [] unless required.
    """
    # Avoid displaying an empty numbered list when there are no choices available.
    if not options:
        print(f"{prompt}\nNo options are available for this selection.")
        return []

    # Keep asking until the response satisfies the required selection rules.
    while True:
        # Number each available field or aggregation for simple CLI selection.
        print(prompt)
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
        # Allow Enter only for optional choices; required steps must be completed.
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        # Convert comma-separated choices to integers and catch malformed entries.
        try:
            indexes = [int(item.strip()) for item in choice.split(",")]
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
            continue

        # Reject empty tokens and numbers that do not refer to listed choices.
        if not indexes or any(i < 1 or i > len(options) for i in indexes):
            print(f"Each number must be between 1 and {len(options)}.")
            continue

        # Convert menu numbers to option names and remove duplicate selections.
        selected = list(dict.fromkeys(options[i - 1] for i in indexes))
        # Aggregation selection must contain one operation, not several.
        if single and len(selected) != 1:
            print("Please select exactly one option.")
            continue
        return selected


def generate_custom_pivot_table(data):
    """Interactively configure and display a pivot table from available sales fields."""
    # Keep the generated sales-price field local to this custom-pivot operation.
    pivot_data = data.copy()
    # Offer nonnumeric fields for grouping and numeric fields for calculations.
    numeric_options = list(pivot_data.select_dtypes(include="number").columns)
    row_options = list(pivot_data.select_dtypes(exclude="number").columns)
    # A pivot table needs at least one categorical row grouping.
    if not row_options:
        print("No categorical columns are available to group the data.")
        return
    # Ask which fields define the rows; at least one row field is mandatory.
    rows = get_user_selection(
        row_options,
        "\nSelect rows:",
        required=True,
    )

    # Only offer column groupings not already selected as row groupings.
    column_options = [column for column in row_options if column not in rows]
    columns = get_user_selection(
        column_options,
        "\nSelect columns (optional; press Enter for no grouping):",
    )

    # Identifiers are not meaningful measures, so keep them out of value choices.
    value_options = [
        column
        for column in numeric_options
        if column not in {"order_number", "employee_id"}
    ]
    # Add calculated sale_price as a measure when the source has quantity and price.
    if "sale_price" not in pivot_data.columns and {"quantity", "unit_price"}.issubset(
        pivot_data.columns
    ):
        pivot_data["sale_price"] = sales_amount(pivot_data)
        value_options.append("sale_price")
    elif "sale_price" in pivot_data.columns and "sale_price" not in value_options:
        pivot_data["sale_price"] = numeric_column(pivot_data, "sale_price")
        value_options.append("sale_price")

    # Stop before prompting if there are no numeric measures to aggregate.
    if not value_options:
        print("No numeric columns available to aggregate.")
        return
    # Let the user select one or more numeric measures.
    values = get_user_selection(
        value_options,
        "\nSelect values:",
        required=True,
    )

    # Restrict aggregation to operations supported by the custom pivot interface.
    aggregation_options = ["sum", "mean", "count"]
    aggregation = get_user_selection(
        aggregation_options,
        "\nSelect aggregation function:",
        required=True,
        single=True,
    )[0]

    # Validate that all selected labels still exist before building the pivot.
    if any(field not in pivot_data.columns for field in rows + columns + values):
        print("Could not create the pivot table: a selected field is no longer available.")
        return

    # Create the pivot and report common data/selection errors without crashing.
    try:
        pivot_table = pd.pivot_table(
            pivot_data,
            index=rows,
            columns=columns if columns else None,
            values=values,
            aggfunc=aggregation,
            fill_value=0,
        )
    except (KeyError, TypeError, ValueError) as error:
        print(f"Could not create the pivot table: {error}")
        return
    # Empty output is not useful to save, so report it and return.
    if pivot_table.empty:
        print("The selected fields produced an empty pivot table.")
        return

    # Assign every custom pivot a unique name so later pivots do not overwrite it.
    stored_name = store_result("Custom pivot table", pivot_table)
    # Display the result and offer to export the same table to Excel.
    print("\nCustom pivot table:")
    print(pivot_table)
    offer_excel_export(pivot_table, stored_name.lower())


def show_average_sales_by_region(data):
    """Pivot average sales (quantity * unit_price) by region, with state and sale type sub-columns."""
    # Do not run this report unless all grouping and calculation fields exist.
    if not report_requirements_met(
        data,
        "Average sales by region with average sales by state and sale type",
    ):
        return

    # Add calculated order revenue to a copy, keeping the source data unchanged.
    sales = data.copy()
    sales["sales"] = sales_amount(data)
    # Average revenue by sales region and nested state/order-type columns.
    pivot_table = pd.pivot_table(
        sales,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
    )
    # Keep the pivot for later display, then print it and offer Excel export.
    store_result(
        "Average sales by region with average sales by state and sale type",
        pivot_table,
    )
    print("\nAverage sales by region, by state and sale type:")
    print(pivot_table.round(2))
    offer_excel_export(pivot_table, "average sales by region, state, and order type")


def show_sales_by_customer_type_order_type_and_state(data):
    """Print sales revenue grouped by customer type, order type, and state."""
    # Check every field used for row groups, state columns, and revenue.
    if not report_requirements_met(
        data, "Sales by customer type and order type by state"
    ):
        return

    # Calculate row-level revenue on a copy of the input DataFrame.
    report_data = data.copy()
    report_data["sales"] = sales_amount(data)
    # Use customer/order type as nested rows and state as pivot columns.
    report = report_data.pivot_table(
        index=["customer_type", "order_type"],
        columns="customer_state",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    # Save the result, display it, and offer an Excel copy.
    store_result("Sales by customer type and order type by state", report)
    print("\nSales by customer type and order type by state:")
    print(report.round(2))
    offer_excel_export(report, "sales by customer type, order type, and state")


def show_sales_quantity_and_price_by_region_and_product(data):
    """Print total quantity and calculated sales revenue for each region and product."""
    # Stop with a useful warning if grouping or numeric fields are unavailable.
    if not report_requirements_met(
        data, "Total sales quantity and price by region and product"
    ):
        return

    # Prepare a copy with normalized quantities and calculated per-row revenue.
    report_data = data.copy()
    report_data["quantity"] = numeric_column(data, "quantity")
    report_data["sales"] = sales_amount(data)
    # Sum quantity and revenue for each region/product combination.
    report = pd.pivot_table(
        report_data,
        index=["sales_region", "produce_name"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
        dropna=False,
    )
    # Save, display, and offer to export the grouped totals.
    store_result("Total sales quantity and price by region and product", report)
    print("\nTotal sales quantity and price by region and product:")
    print(report.round(2))
    offer_excel_export(report, "sales quantity and price by region and product")


def show_sales_quantity_and_price_by_customer_type(data):
    """Print total quantity and calculated sales revenue for each customer type."""
    # Check required customer/order and measure fields before making the report.
    if not report_requirements_met(
        data, "Total sales quantity and price by customer type"
    ):
        return

    # Normalize quantities and calculate revenue on a separate working DataFrame.
    report_data = data.copy()
    report_data["quantity"] = numeric_column(data, "quantity")
    report_data["sales"] = sales_amount(data)
    # Sum both measures within each order-type/customer-type group.
    report = pd.pivot_table(
        report_data,
        index=["order_type", "customer_type"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
        dropna=False,
    )
    # Keep this result with the other analytics and offer the same table as Excel.
    store_result("Total sales quantity and price by order and customer type", report)
    print("\nTotal sales quantity and price by order and customer type:")
    print(report.round(2))
    offer_excel_export(report, "sales quantity and price by order and customer type")


def show_min_max_sales_price_by_category(data):
    """Print the minimum and maximum unit sales price for each product category."""
    # A missing category or price field makes this report unavailable.
    if not report_requirements_met(data, "Maximum and minimum sales price by category"):
        return

    # Normalize prices on a copy before calculating category statistics.
    report_data = data.copy()
    report_data["unit_price"] = numeric_column(data, "unit_price")
    # Pivot each category to show its minimum and maximum unit price.
    report = pd.pivot_table(
        report_data,
        index="product_category",
        values="unit_price",
        aggfunc=["min", "max"],
        dropna=False,
    )
    # Save, print, and optionally export the min/max table.
    store_result("Maximum and minimum sales price by category", report)
    print("\nMaximum and minimum sales price by category:")
    print(report.round(2))
    offer_excel_export(report, "minimum and maximum sales price by category")


def exit_program(data=None):
    """Print a goodbye message and stop the program."""
    # Use a normal zero exit status when the user chooses the Exit menu item.
    print("Exiting the program. Goodbye!")
    raise SystemExit(0)


# This tuple pairs each displayed menu label with the function to execute.
menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Total sales by region and order_type", show_total_sales_by_region_and_order_type),
    ("Average sales by region, by state and sale type", show_average_sales_by_region),
    (
        "Sales by customer type and order type by state",
        show_sales_by_customer_type_order_type_and_state,
    ),
    (
        "Total sales quantity and price by region and product",
        show_sales_quantity_and_price_by_region_and_product,
    ),
    (
        "Total sales quantity and price by customer type",
        show_sales_quantity_and_price_by_customer_type,
    ),
    ("Max and min sales price of sales by category", show_min_max_sales_price_by_category),
    ("Number of unique employees by region", show_employees_by_region),
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Display all stored results", show_stored_results),
    ("Exit the program", exit_program),
)


def display_menu():
    """Show the menu and return a valid selection as an index into menu_options."""
    # Redisplay the menu until the user enters one of its listed numbers.
    while True:
        # Show completed report names so users can see what has already been run.
        if stored_results:
            print("\nCompleted analyses:")
            for result_name in stored_results:
                print(f"  - {result_name}")
        else:
            print("\nCompleted analyses: none yet")

        print("\n--- Sales Data Dashboard ---")
        # Generate the menu from the tuple so options can be reordered in one place.
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"  {number}. {description}")

        choice = input(
            f"Select an option (1-{len(menu_options)}), or press Ctrl+C to quit: "
        ).strip()
        # Accept only an integer in the menu's valid range and return its zero-based index.
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection '{choice}'. Please enter a number from 1 to {len(menu_options)}.")


def main():
    """Load the Drive data, report missing analytics fields, and run the menu loop."""
    # Ask Pandas to show every row and column when a full table is requested.
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    # Use the required Drive file, then load it and warn about unavailable analytics.
    csv_file = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
    sales_data = load_csv(csv_file)
    warn_about_missing_analytics_fields(sales_data)

    # Run the chosen menu action with the loaded DataFrame until exit or interruption.
    try:
        while True:
            # Get the selected action from the menu tuple and pass it the data.
            selection = display_menu()
            _, action = menu_options[selection]
            action(sales_data)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")


if __name__ == "__main__":
    main()