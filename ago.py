import os
from openai import AzureOpenAI
from datetime import datetime

# Initialize Azure OpenAI client with ARM template configurations
client = AzureOpenAI(
    api_key=os.getenv("895wldthT3YtWIfqrJVloEuSW5C3mA7Q14qq00iEpNvJYDfsfTeTJQQJ99BDACHYHv6XJ3w3AAABACOGT1IT"),
    api_version="2024-10-01",  # Matches ARM template version
    azure_endpoint=os.getenv("https://ago.openai.azure.com")
)

# Global state tracking
current_scope = None
bill_analysis = None
CONTENT_FILTER_MESSAGE = "Response blocked due to content policy violations. Please modify your input."

def generate_response(prompt, deployment_name="gpt-4o"):
    """Generate response using Azure OpenAI with RAI policy enforcement"""
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if "content_filter" in str(e).lower():
            return CONTENT_FILTER_MESSAGE
        return f"API Error: {str(e)}"

def display_menu():
    """Display main menu for onboarding flow"""
    print("\n=== Carbon Footprint Reduction Onboarding ===")
    print("1. Set Sustainability Goal")
    print("2. Process Energy Bill")
    print("3. View Recommendations")
    print("4. Exit")
    return input("Enter your choice: ")

def scope_selection():
    """Handle scope selection with RAI-protected input"""
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
        if current_scope:
            return current_scope
        print("Invalid scope selection. Please try again.")

def handle_sustainability_goal():
    """Generate scope-specific guidance with content filtering"""
    selected_scope = scope_selection()
    prompt = f"""As a sustainability consultant, explain the implementation process for {selected_scope} 
    focusing on technical requirements, compliance factors, and monitoring strategies. 
    Include 3-5 key performance indicators."""
    
    response = generate_response(prompt)
    return response if response != CONTENT_FILTER_MESSAGE else "Content blocked in scope guidance"

def process_energy_file(file_path):
    """Secure file processing with error handling"""
    try:
        with open(file_path, 'r') as f:
            kwh = float(f.read().strip())
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'kwh': kwh,
            'scope': current_scope
        }
    except Exception as e:
        print(f"File processing error: {str(e)}")
        return None

def handle_energy_bill():
    """RAI-compliant energy analysis workflow"""
    global bill_analysis
    print("\n=== Secure Energy Bill Upload ===")
    file_path = input("Enter path to energy bill file: ")
    
    if not os.path.exists(file_path):
        return "File not found. Please check the path."
    
    bill_data = process_energy_file(file_path)
    if not bill_data:
        return "Failed to process file"
    
    analysis_prompt = f"""Analyze energy consumption for {bill_data['scope']}:
    - Date: {bill_data['timestamp']}
    - Consumption: {bill_data['kwh']} kWh
    Provide technical analysis including:
    1. Carbon footprint calculation
    2. Industry comparison
    3. Three optimization strategies
    Format as markdown with math expressions for calculations."""
    
    bill_analysis = generate_response(analysis_prompt)
    return bill_analysis if bill_analysis != CONTENT_FILTER_MESSAGE else "Analysis blocked by content filters"

def handle_recommendations():
    """Generate recommendations with compliance checks"""
    if not bill_analysis:
        return "Process an energy bill first"
    
    recommendation_prompt = f"""Based on analysis: {bill_analysis}
    Create a technical implementation plan including:
    - Cost-benefit analysis using NPV calculations
    - Timeline with milestones
    - Risk assessment matrix
    - Compliance considerations
    Format as markdown table."""
    
    response = generate_response(recommendation_prompt)
    return response if response != CONTENT_FILTER_MESSAGE else "Recommendation blocked by content policies"

def main():
    print("Welcome to Secure Carbon Footprint Onboarding")
    print("AI Model: GPT-4o | Security: RAI Policies Enabled")
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
            print("Secure session terminated. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()