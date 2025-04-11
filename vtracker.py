import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load JSON configuration
with open('impactchart.json', 'r') as f:
    config = json.load(f)

# Sample data (replace with pd.read_csv() for real data)
data = {
    "store_id": ["Store1", "Store2", "Store3"],
    "location": ["Cairo", "Alexandria", "Giza"],
    "monthly_kWh": [1000, 1200, 1100],
    "current_fixture_type": ["Incandescent", "Incandescent", "Incandescent"],
    "proposed_fixture_type": ["LED", "LED", "LED"],
    "energy_cost_per_kWh": [0.1, 0.1, 0.1],
    "maintenance_cost_annual": [50, 60, 55]
}
df = pd.DataFrame(data)

# Process calculations from JSON
calc_vars = {}
for calc in config["interpretation"]["calculations"]:
    name = calc["name"]
    if "value" in calc:
        calc_vars[name] = calc["value"]  # Directly store static values
    elif "formula" in calc:
        formula = calc["formula"]
        # Fix formula syntax (replace sum() and add @ for variables)
        formula = formula.replace("sum(monthly_kWh)", "monthly_kWh")
        # Inject @ prefix for variables in calc_vars
        for var in calc_vars:
            formula = formula.replace(var, f"@{var}")
        df[name] = df.eval(formula, local_dict=calc_vars)

# Generate visualizations
figures = []
for viz in config["visualizations"]:
    if viz["type"] == "bar_chart":
        fig = go.Figure()
        for y_field, label in zip(viz["y_fields"], viz["labels"]):
            # Evaluate formula with @ variables
            y_values = df.eval(y_field.replace("led_energy_savings_percent", "@led_energy_savings_percent"), 
                            local_dict=calc_vars)
            fig.add_trace(go.Bar(
                x=df[viz["x_field"]],
                y=y_values,
                name=label
            ))
        fig.update_layout(barmode="group", title=viz["title"])
        figures.append(fig)
    
    elif viz["type"] == "line_chart":
        # Calculate aggregated savings
        annual_savings = df["annual_cost_savings"].sum()
        y_values = [annual_savings * (i+1) for i in range(3)]
        fig = px.line(x=viz["x_values"], y=y_values, title=viz["title"], markers=True)
        figures.append(fig)
    
    elif viz["type"] == "pie_chart":
        # Calculate total emissions
        total_reduction = df["emissions_reduction_kg"].sum()
        total_remaining = (df["annual_energy_consumption"].sum() * 0.55 * 
                          (1 - calc_vars["led_energy_savings_percent"]))
        fig = px.pie(
            names=[seg["label"] for seg in viz["segments"]],
            values=[total_reduction, total_remaining],
            title=viz["title"]
        )
        figures.append(fig)

# Display figures
for fig in figures:
    fig.show()