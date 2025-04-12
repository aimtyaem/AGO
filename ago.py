import os
import json
from openai import AzureOpenAI
from datetime import datetime

# Configuration - Replace with your actual credentials
endpoint = "https://ago.openai.azure.com"
model_name = "gpt-4o"
deployment = "gpt-4o"
api_version = "2024-12-01-preview"
subscription_key = "895wldthT3YtWIfqrJVloEuSW5C3mA7Q14qq00iEpNvJYDfsfTeTJQQJ99BDACHYHv6XJ3w3AAABACOGT1IT"

# Initialize client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Application state
current_scope = None
bill_analysis = None
CONTENT_FILTER_MESSAGE = "Response blocked due to content policy violations."
SYSTEM_PROMPT = """You are a sustainability expert specializing in Egyptian energy systems.
Provide recommendations specific to Egypt's grid, tariffs, and regional conditions.
Always reference Egyptian Electricity Holding Company (EEHC) standards."""

def process_energy_file(file_path):
    """Process Egyptian energy bills with advanced validation"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            bill_data = json.loads(content)

            if not isinstance(bill_data, dict):
                raise ValueError("Invalid JSON structure - expected dictionary")

            fields = bill_data.get("bill_structure", {}).get("fields", {})
            if "total_kWh" not in fields:
                raise ValueError("Missing required total_kWh field")

            try:
                kwh = float(fields["total_kWh"])
            except (ValueError, TypeError):
                raise ValueError("total_kWh must be a numeric value")

            metadata = {
                'tariff_type': fields.get("tariff_type", "Unknown"),
                'location_type': fields.get("location_type", "Unknown"),
                'billing_period': fields.get("billing_period", "Unknown"),
                'source': bill_data.get("source", "Unknown provider")
            }

            rules = bill_data.get("interpretation_rules", {})

            return {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'kwh': kwh,
                'scope': current_scope,
                'metadata': metadata,
                'rules': rules,
                'optimizations': bill_data.get("optimization_suggestions", {}),
                'units': bill_data.get("units", {})
            }

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except Exception as e:
        print(f"File processing error: {str(e)}")
        return None

def generate_response(user_prompt):
    """Generate AI response with error handling"""
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {str(e)}")
        return CONTENT_FILTER_MESSAGE

def handle_sustainability_goal():
    """Configure sustainability scope with validation"""
    global current_scope
    print("Available Scopes:")
    print("1. Scope 1 (Direct emissions)")
    print("2. Scope 2 (Electricity indirect emissions)")
    print("3. Scope 3 (Value chain emissions)")
    
    choice = input("Select scope (1-3): ").strip()
    scope_map = {
        "1": "Scope 1 - Direct Emissions",
        "2": "Scope 2 - Electricity Indirect",
        "3": "Scope 3 - Value Chain"
    }
    
    if choice in scope_map:
        current_scope = scope_map[choice]
        return f"Scope set to: {current_scope}"
    else:
        current_scope = "Not Specified"
        return "Invalid scope selection - using default analysis"

def handle_energy_bill():
    """Enhanced energy analysis for Egyptian bills"""
    global bill_analysis
    print("\n=== Egyptian Energy Bill Analysis ===")
    file_path = input("Enter path to energy bill file: ").strip()

    if not os.path.exists(file_path):
        return "File not found. Please check the path."

    bill_data = process_energy_file(file_path)
    if not bill_data:
        return "Failed to process file. Ensure it matches Egyptian EEHC format."

    context = f"""
    Egyptian Energy Bill Context:
    - Provider: {bill_data['metadata']['source']}
    - Tariff Type: {bill_data['metadata']['tariff_type']}
    - Location: {bill_data['metadata']['location_type']}
    - Billing Period: {bill_data['metadata']['billing_period']}
    - Emissions Factor: {bill_data['units'].get('emissions_estimate_factor', '0.55 kg CO2/kWh (Egypt default)')}

    Industry Benchmarks:
    - Night Usage Threshold: {bill_data['rules'].get('night_usage_threshold', 0.2)}
    - Average kWh/10k sqft: {bill_data['rules'].get('industry_average_kWh_per_10000_sqft', 12250)}
    """

    analysis_prompt = f"""Analyze this Egyptian {bill_data['scope']} energy consumption:
    {context}
    - Usage: {bill_data['kwh']} kWh
    - Date Processed: {bill_data['timestamp']}

    Provide:
    1. CO2e calculation using Egyptian grid factor
    2. Comparison to EEHC regional benchmarks
    3. Three optimization strategies considering:
       - Egyptian tariff structures
       - {bill_data['metadata']['location_type']} location factors
       - Time-of-use patterns
    4. Flag any usage anomalies per EEHC standards

    Format with markdown tables and Egyptian-specific examples."""

    bill_analysis = generate_response(analysis_prompt)
    return bill_analysis if bill_analysis != CONTENT_FILTER_MESSAGE else "Analysis blocked"

def handle_recommendations():
    """Recommendation generation"""
    if not bill_analysis: return "Process an energy bill first"

    recommendation_prompt = f"""Based on analysis: {bill_analysis}
    Create implementation plan including:
    - NPV calculation with assumptions
    - 12-month timeline
    - Risk matrix
    - Compliance checklist
    Format as markdown table with emojis."""

    response = generate_response(recommendation_prompt)
    return response if response != CONTENT_FILTER_MESSAGE else "Recommendation blocked"

def display_menu():
    """Display main menu and get user choice"""
    print("\nMain Menu:")
    print("1. Configure Sustainability Scope")
    print("2. Analyze Energy Bill")
    print("3. Generate Recommendations")
    print("4. Exit")
    return input("Please select an option (1-4): ").strip()

def main():
    print("Welcome to Carbon Footprint Analysis")
    print(f"AI Model: {model_name} | API: {api_version}")
    while True:
        choice = display_menu()
        if choice == "1":
            print("\n=== Scope Configuration ===")
            print(handle_sustainability_goal())
        elif choice == "2":
            print(handle_energy_bill())
        elif choice == "3":
            print("\n=== Technical Recommendations ===")
            print(handle_recommendations())
        elif choice == "4":
            print("Session ended. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()