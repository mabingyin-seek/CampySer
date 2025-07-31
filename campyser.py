#!/usr/bin/env python3
"""
Campylobacter Serotyping CLI Tool
Analyzes FASTA files against Campylobacter serotype database
"""
import argparse
import os
import sys
import subprocess
import tempfile
import re

class CampySerAnalyzer:
    def __init__(self, blast_db="database/campylobacter_db"):
        self.blast_db = blast_db
        self.serotype_mapping = self._load_serotype_mapping()
    
    def _load_serotype_mapping(self):
        """Load serotype mapping from ser_an.txt"""
        mapping = {}
        if os.path.exists("ser_an.txt"):
            with open("ser_an.txt", "r") as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        serotype = parts[0]
                        accession = parts[1]
                        mapping[accession] = serotype
        return mapping
    
    def run_blast_analysis(self, fasta_file):
        """Run BLAST analysis against the database"""
        print(f"Running BLAST analysis on {fasta_file}...")
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            blast_output = tmp.name
        
        try:
            # Run BLAST
            cmd = [
                "blastn",
                "-query", fasta_file,
                "-db", self.blast_db,
                "-out", blast_output,
                "-outfmt", "6",  # Tabular format
                "-evalue", "1e-10",
                "-max_target_seqs", "5"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"BLAST failed: {result.stderr}")
                return None
            
            # Parse BLAST results
            hits = self._parse_blast_results(blast_output)
            return hits
            
        except FileNotFoundError:
            print("blastn not found. Please install BLAST+ tools.")
            return None
        finally:
            # Clean up temporary file
            if os.path.exists(blast_output):
                os.unlink(blast_output)
    
    def _parse_blast_results(self, blast_output):
        """Parse BLAST tabular output"""
        hits = []
        
        if not os.path.exists(blast_output):
            return hits
        
        with open(blast_output, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('\t')
                    if len(parts) >= 12:
                        subject_id = parts[1]
                        identity = float(parts[2])
                        alignment_length = int(parts[3])  # This is the alignment length
                        # Extract query length from query ID (format: NODE_1_length_312435_cov_1075.888199)
                        query_id = parts[0]
                        if 'length_' in query_id:
                            # Extract length from ID like NODE_1_length_312435_cov_1075.888199
                            length_match = re.search(r'length_(\d+)', query_id)
                            if length_match:
                                query_length = int(length_match.group(1))
                            else:
                                query_length = 23868  # fallback
                        else:
                            query_length = 23868  # fallback
                        
                        coverage = (alignment_length / query_length) * 100  # coverage = alignment_length / query_length
                        evalue = float(parts[10])
                        bitscore = float(parts[11])
                        
                        hits.append({
                            'accession': subject_id,
                            'identity': identity,
                            'coverage': coverage,
                            'evalue': evalue,
                            'bitscore': bitscore,
                            'query_length': query_length,
                            'alignment_length': alignment_length
                        })
        
        # Sort by bitscore (descending)
        hits.sort(key=lambda x: x['bitscore'], reverse=True)
        
        # Output top 5 BLAST results
        print("\nBLAST结果排序后的前五行信息:")
        print("-" * 80)
        print(f"{'序列ID':<20} {'比对序列':<15} {'一致性':<10} {'覆盖度':<10} {'E值':<12} {'比特分数':<10}")
        print("-" * 80)
        
        for i, hit in enumerate(hits[:5], 1):
            print(f"{i:<20} {hit['accession']:<15} {hit['identity']:<10.1f} {hit['coverage']:<10.1f} {hit['evalue']:<12.2e} {hit['bitscore']:<10.1f}")
        
        return hits
    
    def interpret_results(self, blast_hits):
        """Interpret results and determine serotype"""
        serotype_calls = []
        
        if blast_hits:
            for hit in blast_hits:
                # Filter by quality thresholds
                if hit['identity'] >= 95 and hit['coverage'] >= 80:
                    accession = hit['accession']
                    serotype = self.serotype_mapping.get(accession, accession)
                    
                    serotype_calls.append({
                        'method': 'BLAST',
                        'serotype': serotype,
                        'accession': accession,
                        'confidence': 'High',
                        'identity': hit['identity'],
                        'coverage': hit['coverage'],
                        'evalue': hit['evalue']
                    })
        
        return serotype_calls
    
    def analyze_fasta(self, fasta_file):
        """Main analysis function"""
        print(f"Analyzing {fasta_file}...")
        
        # Validate input file
        if not os.path.exists(fasta_file):
            print(f"Error: File {fasta_file} not found")
            return None
        
        # Run BLAST analysis
        blast_hits = self.run_blast_analysis(fasta_file)
        
        # Interpret results
        results = self.interpret_results(blast_hits)
        
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Campylobacter Serotyping Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  campyser.py sample.fasta
  campyser.py sample.fasta --output results.txt
  campyser.py sample.fasta --verbose
  campyser.py sample.fasta --database /path/to/database
        """
    )
    
    parser.add_argument(
        "fasta_file",
        help="Input FASTA file to analyze"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file for results (default: stdout)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--database",
        "-d",
        default="database/campylobacter_db",
        help="BLAST database path (default: database/campylobacter_db)"
    )
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = CampySerAnalyzer(blast_db=args.database)
    
    # Run analysis
    results = analyzer.analyze_fasta(args.fasta_file)
    
    if not results:
        print("No serotype detected")
        sys.exit(1)
    
    # Output results
    output_lines = []
    
    if args.verbose:
        output_lines.append(f"Analysis completed for: {args.fasta_file}")
        output_lines.append(f"Database: {args.database}")
        output_lines.append("-" * 50)
    
    # Best result (highest confidence BLAST hit)
    best_result = results[0]  # Already sorted by bitscore
    
    # Summary
    output_lines.append(f"Predicted Serotype: {best_result['serotype']}")
    output_lines.append(f"Confidence: {best_result['confidence']}")
    output_lines.append(f"Method: {best_result['method']}")
    if 'identity' in best_result:
        output_lines.append(f"Identity: {best_result['identity']:.1f}%")
        output_lines.append(f"Coverage: {best_result['coverage']:.1f}%")
    
    # Detailed results
    if args.verbose:
        output_lines.append("")
        output_lines.append("Detailed Results:")
        output_lines.append("-" * 30)
        
        output_lines.append("BLAST Results:")
        for i, result in enumerate(results[:3], 1):  # Top 3
            output_lines.append(f"  {i}. {result['serotype']} ({result['accession']})")
            output_lines.append(f"     Identity: {result['identity']:.1f}%, Coverage: {result['coverage']:.1f}%")
            output_lines.append(f"     E-value: {result['evalue']:.2e}")
    
    # Output
    output_text = "\n".join(output_lines)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_text)
        print(f"Results saved to {args.output}")
    else:
        print(output_text)

if __name__ == "__main__":
    main()