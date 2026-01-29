#!/usr/bin/env python3
"""
Analysis script for crosslinking between polyallylamine and glutaraldehyde
Analyzes the extent of crosslinking by measuring distances between polymer chains
"""
import os
import sys
import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import matplotlib.pyplot as plt
import argparse

def calculate_contacts(trajectory_file, topology_file, cutoff=0.6):
    """
    Calculate contacts between polyallylamine and glutaraldehyde chains
    
    Parameters:
    -----------
    trajectory_file : str
        Path to trajectory file (.dcd)
    topology_file : str
        Path to topology file (.pdb)
    cutoff : float
        Distance cutoff in nm for defining a contact
        
    Returns:
    --------
    contact_data : dict
        Dictionary containing contact analysis results
    """
    # Load trajectory
    u = mda.Universe(topology_file, trajectory_file)
    
    # Get all atoms
    all_atoms = u.select_atoms("all")
    
    # Try to identify polyallylamine and glutaraldehyde atoms
    # This assumes residue names are set appropriately
    try:
        paa_atoms = u.select_atoms("resname PAA")
        gta_atoms = u.select_atoms("resname GTA")
        
        if len(paa_atoms) == 0 or len(gta_atoms) == 0:
            print("Warning: Could not identify PAA or GTA residues by name")
            print("Attempting to identify by atom count or other means...")
            # Fallback: assume first half is PAA, second half is GTA
            n_atoms = len(all_atoms)
            paa_atoms = all_atoms[:n_atoms//2]
            gta_atoms = all_atoms[n_atoms//2:]
    except:
        # Fallback approach
        n_atoms = len(all_atoms)
        paa_atoms = all_atoms[:n_atoms//2]
        gta_atoms = all_atoms[n_atoms//2:]
    
    print(f"Analyzing trajectory: {trajectory_file}")
    print(f"Number of PAA atoms: {len(paa_atoms)}")
    print(f"Number of GTA atoms: {len(gta_atoms)}")
    print(f"Contact cutoff: {cutoff} nm")
    
    # Calculate contacts over trajectory
    n_frames = len(u.trajectory)
    contacts_per_frame = []
    contact_fraction_per_frame = []
    
    for ts in u.trajectory:
        # Calculate distance matrix between PAA and GTA atoms
        dist_matrix = distances.distance_array(
            paa_atoms.positions,
            gta_atoms.positions,
            box=u.dimensions
        )
        
        # Convert from Angstrom to nm
        dist_matrix = dist_matrix / 10.0
        
        # Count contacts (distances below cutoff)
        n_contacts = np.sum(dist_matrix < cutoff)
        contacts_per_frame.append(n_contacts)
        
        # Calculate fraction of possible contacts
        max_contacts = len(paa_atoms) * len(gta_atoms)
        contact_fraction = n_contacts / max_contacts if max_contacts > 0 else 0
        contact_fraction_per_frame.append(contact_fraction)
    
    # Calculate statistics
    mean_contacts = np.mean(contacts_per_frame)
    std_contacts = np.std(contacts_per_frame)
    mean_fraction = np.mean(contact_fraction_per_frame)
    std_fraction = np.std(contact_fraction_per_frame)
    
    contact_data = {
        'contacts_per_frame': np.array(contacts_per_frame),
        'contact_fraction_per_frame': np.array(contact_fraction_per_frame),
        'mean_contacts': mean_contacts,
        'std_contacts': std_contacts,
        'mean_fraction': mean_fraction,
        'std_fraction': std_fraction,
        'n_frames': n_frames,
        'n_paa_atoms': len(paa_atoms),
        'n_gta_atoms': len(gta_atoms),
        'cutoff': cutoff
    }
    
    return contact_data

def plot_contact_analysis(contact_data, output_prefix):
    """
    Create plots for contact analysis
    
    Parameters:
    -----------
    contact_data : dict
        Dictionary containing contact analysis results
    output_prefix : str
        Prefix for output files
    """
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot 1: Number of contacts over time
    frames = np.arange(len(contact_data['contacts_per_frame']))
    ax1.plot(frames, contact_data['contacts_per_frame'], alpha=0.7)
    ax1.axhline(y=contact_data['mean_contacts'], color='r', linestyle='--', 
                label=f'Mean = {contact_data["mean_contacts"]:.1f} ± {contact_data["std_contacts"]:.1f}')
    ax1.set_xlabel('Frame')
    ax1.set_ylabel('Number of Contacts')
    ax1.set_title('PAA-GTA Contacts Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Contact fraction over time
    ax2.plot(frames, contact_data['contact_fraction_per_frame'], alpha=0.7, color='green')
    ax2.axhline(y=contact_data['mean_fraction'], color='r', linestyle='--',
                label=f'Mean = {contact_data["mean_fraction"]:.4f} ± {contact_data["std_fraction"]:.4f}')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Contact Fraction')
    ax2.set_title('PAA-GTA Contact Fraction Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_contacts.png', dpi=300)
    print(f"Saved plot: {output_prefix}_contacts.png")
    plt.close()
    
    # Create histogram of contacts
    plt.figure(figsize=(8, 6))
    plt.hist(contact_data['contacts_per_frame'], bins=50, alpha=0.7, edgecolor='black')
    plt.axvline(x=contact_data['mean_contacts'], color='r', linestyle='--', 
                label=f'Mean = {contact_data["mean_contacts"]:.1f}')
    plt.xlabel('Number of Contacts')
    plt.ylabel('Frequency')
    plt.title('Distribution of PAA-GTA Contacts')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{output_prefix}_contact_histogram.png', dpi=300)
    print(f"Saved plot: {output_prefix}_contact_histogram.png")
    plt.close()

def save_contact_summary(contact_data, output_file):
    """
    Save contact analysis summary to text file
    
    Parameters:
    -----------
    contact_data : dict
        Dictionary containing contact analysis results
    output_file : str
        Path to output text file
    """
    with open(output_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("CROSSLINKING ANALYSIS SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Cutoff distance: {contact_data['cutoff']} nm\n")
        f.write(f"Number of frames analyzed: {contact_data['n_frames']}\n")
        f.write(f"Number of PAA atoms: {contact_data['n_paa_atoms']}\n")
        f.write(f"Number of GTA atoms: {contact_data['n_gta_atoms']}\n\n")
        
        f.write("CONTACT STATISTICS:\n")
        f.write("-" * 60 + "\n")
        f.write(f"Mean number of contacts: {contact_data['mean_contacts']:.2f} ± {contact_data['std_contacts']:.2f}\n")
        f.write(f"Contact fraction: {contact_data['mean_fraction']:.6f} ± {contact_data['std_fraction']:.6f}\n")
        f.write(f"Contact percentage: {contact_data['mean_fraction']*100:.4f}%\n\n")
        
        f.write(f"Minimum contacts: {np.min(contact_data['contacts_per_frame'])}\n")
        f.write(f"Maximum contacts: {np.max(contact_data['contacts_per_frame'])}\n")
        f.write(f"Median contacts: {np.median(contact_data['contacts_per_frame']):.2f}\n\n")
        
        f.write("=" * 60 + "\n")
    
    print(f"Saved summary: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze crosslinking in polymer simulations')
    parser.add_argument('--traj', required=True, help='Path to trajectory file (.dcd)')
    parser.add_argument('--top', required=True, help='Path to topology file (.pdb)')
    parser.add_argument('--cutoff', type=float, default=0.6, help='Contact cutoff in nm (default: 0.6)')
    parser.add_argument('--output', default='crosslinking_analysis', help='Output prefix (default: crosslinking_analysis)')
    
    args = parser.parse_args()
    
    # Check if files exist
    if not os.path.exists(args.traj):
        print(f"Error: Trajectory file not found: {args.traj}")
        return
    
    if not os.path.exists(args.top):
        print(f"Error: Topology file not found: {args.top}")
        return
    
    print("\n" + "=" * 60)
    print("CROSSLINKING ANALYSIS")
    print("=" * 60 + "\n")
    
    # Calculate contacts
    contact_data = calculate_contacts(args.traj, args.top, args.cutoff)
    
    # Create plots
    plot_contact_analysis(contact_data, args.output)
    
    # Save summary
    save_contact_summary(contact_data, f'{args.output}_summary.txt')
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
