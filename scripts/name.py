import sys
import csv
from tabulate import tabulate

def read_csv(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)
            return headers,rows
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)

def main():
    # This will confirm if one command-line argument was used 
    if len(sys.argv) != 2:
        print("Too few command-line arguments" if len(sys.argv) < 2 else "Too many command-line arguments")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith(".csv"):
        print("Not a CSV file")
        sys.exit(1)

    headers, rows = read_csv(filename)

    print(tabulate(rows, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
