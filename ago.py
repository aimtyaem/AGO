import os
from openai import AzureOpenAI
from datetime import datetime

# Configuration from sample code
endpoint = "https://ago.openai.azure.com"
model_name = "gpt-4o"
deployment = "gpt-4o"
api_version = "2024-12-01-preview"
subscription_key = ("895wldthT3YtWIfqrJVloEuSW5C3mA7Q14qq00iEpNvJYDfsfTeTJQQJ99BDACHYHv6XJ3w3AAABACOGT1IT")  # From environment

# Initialize client with sample configuration
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Application state and constants
current_scope = None
bill_analysis = None
CONTENT_FILTER_MESSAGE = "Response blocked due to content policy violations. Please modify your input."
SYSTEM_PROMPT = """You are a sustainability expert assistant specializing in carbon footprint reduction.
Provide technical, compliance-focused recommendations with numerical calculations.
Always consider RAI policies in responses."""

def generate_response(prompt):
    """Enhanced response generation with sample parameters"""
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=4096
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if "content_filter" in str(e).lower():
            return CONTENT_FILTER_MESSAGE
        return f"API Error: {str(e)}"

def display_menu():
    """Main menu display"""
    print("\n=== Carbon Footprint Reduction Onboarding ===")
    print("1. Set Sustainability Goal")
    print("2. Process Energy Bill")
    print("3. View Recommendations")
    print("4. Exit")
    return input("Enter your choice: ")

def scope_selection():
    """Scope selection with validation"""
    global current_scope
    print("\nSelect Scope Type:")
    print("1. Scope 1 - Direct Emissions")
    print("2. Scope 2 - Indirect Energy Emissions")
    print("3. Scope 3 - Value Chain Emissions")

    scope_map = {
        "1": "Scope 1 - Direct Emissions",
        "2": "Scope 2 - Indirect Energy Emissions",
        "3": "Scope 3 - Value Chain Emissions"
    }

    while True:
        choice = input("Choose scope (1-3): ")
        current_scope = scope_map.get(choice)
        if current_scope: return current_scope
        print("Invalid selection. Please try again.")

def handle_sustainability_goal():
    """Scope-specific guidance generation"""
    selected_scope = scope_selection()
    prompt = f"""As a sustainability consultant, explain the implementation process for {selected_scope}
    including technical requirements, compliance factors, and monitoring strategies.
    Include 3-5 key performance indicators with formulas."""

    response = generate_response(prompt)
    return response if response != CONTENT_FILTER_MESSAGE else "Content blocked in scope guidance"

def process_energy_file(file_path):
    """Secure file processing with validation"""
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
    """Energy analysis workflow"""
    global bill_analysis
    print("\n=== Energy Bill Analysis ===")
    file_path = input("Enter path to energy bill file: ")

    if not os.path.exists(file_path):
        return "File not found. Please check the path."

    bill_data = process_energy_file(file_path)
    if not bill_data: return "Failed to process file"

    analysis_prompt = f"""Analyze {bill_data['scope']} energy consumption:
    - Date: {bill_data['timestamp']}
    - Usage: {bill_data['kwh']} kWh
    Provide technical analysis including:
    1. CO2e calculation with formula
    2. Industry benchmark comparison
    3. Three optimization strategies
    Format with markdown and LaTeX math."""

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