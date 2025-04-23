import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Union
import os
from pathlib import Path

def read_local_xml() -> str:
    """Read the local CORPCODE.xml file."""
    # Get the path relative to the current file
    current_dir = Path(__file__).parent
    file_path = current_dir / 'data' / 'CORPCODE.xml'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_corp_code_xml(xml_content: str) -> List[Dict[str, str]]:
    """Parse the XML content and return a list of corporation information."""
    root = ET.fromstring(xml_content)
    corporations = []
    
    for corp in root.findall('.//list'):
        corp_info = {
            'corp_name': corp.findtext('corp_name', ''),
            'corp_code': corp.findtext('corp_code', ''),
            'stock_code': corp.findtext('stock_code', ''),
            'modify_date': corp.findtext('modify_date', '')
        }
        corporations.append(corp_info)
    
    return corporations

def search_corporations(corporations: List[Dict[str, str]], search_term: str) -> List[Dict[str, str]]:
    """Search corporations by name using case-insensitive partial matching."""
    search_term = search_term.lower()
    results = []
    
    for corp in corporations:
        if corp['corp_name'] and search_term in corp['corp_name'].lower():
            results.append(corp)
    
    return results

def main():
    try:
        # Read and parse the XML file
        xml_content = read_local_xml()
        corporations = parse_corp_code_xml(xml_content)
        
        # Get search term from user
        search_term = input("Enter company name to search (Korean or English): ")
        
        # Search for matching corporations
        results = search_corporations(corporations, search_term)
        
        # Display results
        if results:
            print(f"\nFound {len(results)} matching corporations:")
            for corp in results:
                print(f"\nCorporation Code: {corp['corp_code']}")
                print(f"Korean Name: {corp['corp_name']}")
                print(f"Stock Code: {corp['stock_code']}")
                print(f"Last Modified: {corp['modify_date']}")
        else:
            print("No matching corporations found.")
            
    except FileNotFoundError:
        print("Error: CORPCODE.xml file not found in the current directory")
    except ET.ParseError as e:
        print(f"Error parsing the XML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 