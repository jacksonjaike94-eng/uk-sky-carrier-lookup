#!/usr/bin/env python3
"""
UK Sky Carrier Lookup System - Main CLI Application
Lookup UK phone numbers and identify Sky UK Limited carriers
"""

import argparse
import sys
import os
from datetime import datetime
from carrier_lookup import CarrierLookup
from csv_exporter import CSVExporter
from logger import log_info, log_error, log_warning

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='UK Sky Carrier Lookup - Identify Sky UK Limited phone numbers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python lookup.py --input numbers.txt --output results.csv
  python lookup.py --input numbers.txt --output results.csv --delay 10
  python lookup.py --input numbers.txt --output results.csv --no-filter
        '''
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file with phone numbers (one per line)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Output CSV file (default: results_TIMESTAMP.csv)'
    )
    
    parser.add_argument(
        '--delay', '-d',
        type=int,
        default=None,
        help='Delay between requests in seconds (default: 8)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='results',
        help='Output directory (default: results)'
    )
    
    parser.add_argument(
        '--no-filter',
        action='store_true',
        help='Disable Sky UK filtering (return all carriers)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    return parser.parse_args()

def validate_input_file(input_file):
    """Validate input file exists"""
    if not os.path.exists(input_file):
        log_error(f"Input file not found: {input_file}")
        return False
    
    if not os.path.isfile(input_file):
        log_error(f"Input path is not a file: {input_file}")
        return False
    
    return True

def main():
    """Main application entry point"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate input file
        if not validate_input_file(args.input):
            sys.exit(1)
        
        # Update config if custom values provided
        import config
        if args.delay:
            config.DELAY_BETWEEN_REQUESTS = args.delay
        
        if args.no_filter:
            config.ENABLED_FILTERING = False
        
        if args.debug:
            config.DEBUG = True
        
        # Initialize lookup system
        log_info("=" * 60)
        log_info("UK Sky Carrier Lookup System Started")
        log_info("=" * 60)
        
        lookup_system = CarrierLookup()
        
        # Start browser
        if not lookup_system.start():
            log_error("Failed to initialize browser")
            sys.exit(1)
        
        try:
            # Process input file
            results = lookup_system.process_file(args.input)
            
            if results is None:
                log_error("Failed to process input file")
                sys.exit(1)
            
            # Export results to CSV
            exporter = CSVExporter(args.output)
            export_result = exporter.export_results(results)
            
            if export_result:
                log_info("=" * 60)
                log_info("Processing Complete!")
                log_info("=" * 60)
                log_info(f"Output file: {export_result['file']}")
                log_info(f"Total numbers: {export_result['total']}")
                log_info(f"Sky UK Limited: {export_result['success']}")
                log_info(f"Other carriers: {export_result['filtered']}")
                log_info(f"Errors: {export_result['errors']}")
            else:
                log_error("Failed to export results")
                sys.exit(1)
        
        finally:
            # Close browser
            lookup_system.close()
    
    except KeyboardInterrupt:
        log_warning("\nOperation cancelled by user")
        sys.exit(130)
    
    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()