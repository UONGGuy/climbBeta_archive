# CLI tool for development purposes - manually run data pipeline for dev purposes given json file

import argparse
from app.models.enums import generate_enums
from database.seed import populate_database

def main():
    parser = argparse.ArgumentParser(description="Manual ingestion tool for ClimbBeta.")
    parser.add_argument("--json", required=True, help="Path to the JSON file.")
    parser.add_argument("--validate", action="store_true", help="Validate the JSON file.")
    args = parser.parse_args()

    if args.validate:
        print(f"Validating JSON file: {args.json}")
        # Add validation logic here

    print(f"Generating enums from {args.json}")
    generate_enums(args.json, "app/models/enums.py")

    print(f"Populating database from {args.json}")
    populate_database(args.json)

if __name__ == "__main__":
    main()