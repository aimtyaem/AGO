import os
from openai import AzureOpenAI
from datetime import datetime

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("895wldthT3YtWIfqrJVloEuSW5C3mA7Q14qq00iEpNvJYDfsfTeTJQQJ99BDACHYHv6XJ3w3AAABACOGT1IT"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("https://ago.openai.azure.com")
)

# Global variables to track state
current_scope = None
bill_analysis = None

def generate_response(prompt, deployment_name="gpt-35-turbo"):
    """Generate response using Azure OpenAI."""
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def display_menu():
    """Display main menu for onboarding flow."""
    print("\n=== Carbon Footprint Reduction Onboarding ===")
    print("1. Set Sustainability Goal")
    print("2. Process Energy Bill")
    print("3. View Recommendations")
    print("4. Exit")
    return input("Enter your choice: ")

def scope_selection():
    """Handle scope selection with sub-menu"""
    global current_scope
    print("\nSelect Scope Type:")
    print("1. Scope 1 - Direct Emissions")
    print("2. Scope 2 - Indirect Energy Emissions")
    print("3. Scope 3 - Value Chain Emissions")
    choice = input("Choose scope (1-3): ")

    scope_map = {
        "1": "Scope 1 - Direct Emissions",
        "2": "Scope 2 - Indirect Energy Emissions",
        "3": "Scope 3 - Value Chain Emissions"
    }

    current_scope = scope_map.get(choice, "Unknown Scope")
    return current_scope

def handle_sustainability_goal():
    """Handle sustainability goal selection."""
    selected_scope = scope_selection()
    prompt = f"""A retail company selects '{selected_scope}' as their primary sustainability goal.
    Explain the onboarding process and key focus areas for this scope in 3-5 bullet points."""
    return generate_response(prompt)

def process_energy_file(file_path):
    """Simulate file processing with timestamp"""
    try:
        with open(file_path, 'r') as f:
            kwh = float(f.read().strip())
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'kwh': kwh,
            'scope': current_scope
        }
    except Exception as e:
        print(f"File error: {str(e)}")
        return None

def handle_energy_bill():
    """Handle energy bill upload and analysis"""
    global bill_analysis
    print("\n=== Energy Bill Upload ===")
    file_path = input("Enter path to energy bill file: ")

    if not file_path:
        return "No file selected"

    bill_data = process_energy_file(file_path)
    if not bill_data:
        return "Failed to process file"

    # Generate analysis prompt
    analysis_prompt = f"""Energy bill analysis for {bill_data['scope']}:
    - Date: {bill_data['timestamp']}
    - Consumption: {bill_data['kwh']} kWh
    Explain what this energy usage means for the selected scope, identify potential issues,
    and suggest 3 immediate actions. Format as markdown bullets."""

    bill_analysis = generate_response(analysis_prompt)
    return bill_analysis

def handle_recommendations():
    """Generate recommendations based on analysis"""
    if not bill_analysis:
        return "Please process an energy bill first"

    recommendation_prompt = f"""Based on this analysis:
    {bill_analysis}

    Create a detailed LED transition recommendation including:
    - Implementation steps
    - Cost-benefit analysis
    - ROI timeline
    - Environmental impact
    Format as markdown sections."""

    return generate_response(recommendation_prompt)

def main():
    print("Welcome to Carbon Footprint Reduction Onboarding!")
    while True:
        choice = display_menu()
        if choice == "1":
            print("\n=== Sustainability Goal Setup ===")
            print(handle_sustainability_goal())
        elif choice == "2":
            print(handle_energy_bill())
        elif choice == "3":
            print("\n=== Efficiency Recommendations ===")
            print(handle_recommendations())
        elif choice == "4":
            print("Exiting onboarding system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
