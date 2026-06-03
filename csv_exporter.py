"""
CSV exporter for carrier lookup results
"""

import csv
import os
from datetime import datetime
import config
from logger import log_info, log_error

class CSVExporter:
    def __init__(self, output_file=None):
        if output_file is None:
            # Generate default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"results_{timestamp}.csv"
        
        self.output_file = output_file
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Create results directory if it doesn't exist"""
        os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
        self.output_path = os.path.join(config.OUTPUT_DIRECTORY, self.output_file)
    
    def export_results(self, results):
        """Export results to CSV"""
        try:
            log_info(f"Exporting {len(results)} results to CSV...")
            
            with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=config.CSV_COLUMNS)
                
                # Write header
                writer.writeheader()
                
                # Write results
                success_count = 0
                filtered_count = 0
                error_count = 0
                
                for result in results:
                    # Add timestamp if not present
                    if 'timestamp' not in result:
                        result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Count by status
                    status = result.get('status', 'unknown')
                    if status == 'success':
                        success_count += 1
                    elif status == 'filtered':
                        filtered_count += 1
                    else:
                        error_count += 1
                    
                    # Write row
                    row = {col: result.get(col, '') for col in config.CSV_COLUMNS}
                    writer.writerow(row)
            
            log_info(f"CSV exported successfully to: {self.output_path}")
            log_info(f"Results Summary:")
            log_info(f"  - Success (Sky UK): {success_count}")
            log_info(f"  - Filtered (Other carriers): {filtered_count}")
            log_info(f"  - Errors: {error_count}")
            
            return {
                'file': self.output_path,
                'total': len(results),
                'success': success_count,
                'filtered': filtered_count,
                'errors': error_count
            }
            
        except Exception as e:
            log_error(f"Failed to export CSV: {str(e)}")
            return None