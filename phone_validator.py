class PhoneValidator:
    def __init__(self):
        self.networks = {
            "MTN": ["024", "054", "055", "059"],
            "Vodafone": ["020", "050"],
            "AirtelTigo": ["026", "056"]
        }
        self.results = {"MTN": [], "Vodafone": [], "AirtelTigo": [], "Unknown": []}
    
    def validate(self, number):
        """Check if number is valid Ghana format"""
        number = number.strip()
        if len(number) != 10:
            return False
        if not number.startswith("0"):
            return False
        if not number.isdigit():
            return False
        return True
    
    def identify_network(self, number):
        """Identify which network a number belongs to"""
        prefix = number[:3]
        for network, prefixes in self.networks.items():
            if prefix in prefixes:
                return network
        return "Unknown"
    
    def process_file(self, filename):
        """Read numbers from file, validate, categorize"""
        try:
            with open(filename, "r") as file:
                numbers = file.readlines()
            
            for number in numbers:
                number = number.strip()
                if self.validate(number):
                    network = self.identify_network(number)
                    self.results[network].append(number)
                else:
                    self.results["Unknown"].append(number)
            
            return True
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return False
    
    def generate_report(self):
        """Print report of results"""
        total = sum(len(v) for v in self.results.values())
        if total == 0:
            print("No numbers processed.")
            return
        
        print("\n=== NETWORK REPORT ===")
        for network, numbers in self.results.items():
            count = len(numbers)
            percentage = (count / total) * 100
            print(f"{network}: {count} ({percentage:.1f}%)")
        print(f"Total: {total} numbers")
    
    def export_report(self, filename="report.txt"):
        """Export report to file"""
        try:
            total = sum(len(v) for v in self.results.values())
            with open(filename, "w") as file:
                file.write("=== NETWORK REPORT ===\n")
                for network, numbers in self.results.items():
                    count = len(numbers)
                    percentage = (count / total) * 100 if total > 0 else 0
                    file.write(f"{network}: {count} ({percentage:.1f}%)\n")
                file.write(f"Total: {total} numbers\n")
            print(f"Report exported to {filename}")
        except:
            print("Error exporting report.")
    
    def view_numbers(self, network=None):
        """View numbers, optionally filtered by network"""
        if network:
            if network in self.results:
                numbers = self.results[network]
                print(f"\n{network} Numbers ({len(numbers)}):")
                for num in numbers:
                    print(f"  {num}")
            else:
                print(f"Network '{network}' not found.")
        else:
            for net, numbers in self.results.items():
                if numbers:
                    print(f"\n{net} ({len(numbers)}):")
                    for num in numbers:
                        print(f"  {num}")


if __name__ == "__main__":
    pv = PhoneValidator()
    
    while True:
        print("\n=== GHANA PHONE VALIDATOR ===")
        print("1. Load Numbers from File")
        print("2. View All Numbers")
        print("3. View by Network")
        print("4. Generate Report")
        print("5. Export Report")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            filename = input("Filename (e.g., numbers.txt): ")
            if pv.process_file(filename):
                print("Numbers processed successfully.")
        
        elif choice == "2":
            pv.view_numbers()
        
        elif choice == "3":
            network = input("Network (MTN/Vodafone/AirtelTigo/Unknown): ")
            pv.view_numbers(network)
        
        elif choice == "4":
            pv.generate_report()
        
        elif choice == "5":
            filename = input("Export filename (e.g., report.txt): ")
            pv.export_report(filename)
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option.")