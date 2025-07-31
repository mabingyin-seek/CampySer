#!/usr/bin/env python3
"""
Sequence downloader and database builder for Campylobacter serotyping
"""
import os
import time
import subprocess
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def parse_accession_numbers(file_path):
    """Parse accession numbers from ser_an.txt file"""
    accession_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines[1:]:  # Skip header
        line = line.strip()
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                serotype = parts[0]
                accession = parts[1]
                accession_data.append({
                    'serotype': serotype,
                    'accession': accession
                })
    
    return accession_data

def download_sequences(accession_data, email="ma786074771@gmail.com"):
    """Download sequences using Entrez"""
    Entrez.email = email
    
    sequences = []
    failed_downloads = []
    
    for item in accession_data:
        accession = item['accession']
        serotype = item['serotype']
        
        print(f"Downloading {accession} ({serotype})...")
        
        try:
            # Try to download the sequence
            handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            handle.close()
            
            # Add serotype information to the record
            record.description = f"{serotype} - {record.description}"
            record.id = accession
            record.name = serotype.replace('/', '_')
            
            sequences.append(record)
            print(f"Successfully downloaded {accession}")
            
            # Add delay to avoid overloading NCBI servers
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Failed to download {accession}: {str(e)}")
            failed_downloads.append(accession)
    
    return sequences, failed_downloads

def build_blast_database(fasta_file, db_name="database/campylobacter_db"):
    """Build BLAST database from FASTA file"""
    print(f"Building BLAST database: {db_name}")
    
    # Run makeblastdb command
    cmd = [
        "makeblastdb",
        "-in", fasta_file,
        "-dbtype", "nucl",
        "-out", db_name,
        "-title", "Campylobacter Serotypes Database"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"BLAST database created successfully: {db_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building BLAST database: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("makeblastdb not found. Please install BLAST+ tools.")
        return False

def save_fasta_files(sequences, output_dir="sequences"):
    """Save sequences as FASTA files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter out sequences with undefined content
    valid_sequences = []
    for record in sequences:
        try:
            # Check if sequence is defined
            str(record.seq)
            valid_sequences.append(record)
        except:
            print(f"Skipping sequence {record.id} - undefined content")
    
    print(f"Saving {len(valid_sequences)} valid sequences out of {len(sequences)} total")
    
    # Save all sequences in one file
    with open(os.path.join(output_dir, "all_sequences.fasta"), "w") as f:
        SeqIO.write(valid_sequences, f, "fasta")
    
    # Save individual sequences
    for record in valid_sequences:
        filename = f"{record.name}.fasta"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            SeqIO.write([record], f, "fasta")
    
    print(f"FASTA files saved to {output_dir}")
    return valid_sequences

def main():
    # Parse accession numbers
    accession_data = parse_accession_numbers("ser_an.txt")
    print(f"Found {len(accession_data)} accession numbers")
    
    # Download sequences
    sequences, failed_downloads = download_sequences(accession_data)
    print(f"Successfully downloaded {len(sequences)} sequences")
    
    if failed_downloads:
        print(f"Failed to download {len(failed_downloads)} sequences:")
        for acc in failed_downloads:
            print(f"  - {acc}")
    
    # Save sequences as FASTA
    valid_sequences = save_fasta_files(sequences)
    
    # Build BLAST database
    fasta_file = "sequences/all_sequences.fasta"
    blast_success = build_blast_database(fasta_file)
    
    print("\nDatabase building completed!")
    print(f"BLAST database: {'✓' if blast_success else '✗'}")

if __name__ == "__main__":
    main()