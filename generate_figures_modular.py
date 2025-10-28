"""
Modular Figure Generation Script for AS Survey Manuscript
==========================================================

This script is designed to be easily modifiable. Key parameters are at the top
of the script for easy adjustment. Modify colors, sizes, labels, etc. without
digging through the plotting code.

Date: October 28, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Patch
from matplotlib.lines import Line2D
import numpy as np

# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS AS NEEDED
# ============================================================================

# File paths
INPUT_FILE = '/home/david/projects/asp_curriculum/AS Survey Graphs.xlsx'
OUTPUT_DIR = '/home/david/projects/asp_curriculum/'

# Color scheme (modify these to change colors throughout)
COLOR_POSITIVE = '#2C7BB6'      # Blue - for positive/desired outcomes
COLOR_NEGATIVE = '#D7191C'      # Red - for concerns/gaps
COLOR_NEUTRAL = '#FFFFBF'       # Light yellow - for neutral
COLOR_POSITIVE_LIGHT = '#ABD9E9'  # Light blue
COLOR_POSITIVE_LIGHTER = '#D1E5F0'  # Even lighter blue
COLOR_NEGATIVE_LIGHT = '#FDAE61'    # Orange/light red
COLOR_GRAY = '#666666'          # Gray for connecting lines

# Font settings
FONT_FAMILY = 'DejaVu Sans'     # Default font (Arial not available)
TITLE_SIZE = 14
SUBTITLE_SIZE = 12
LABEL_SIZE = 11
TICK_SIZE = 10
ANNOTATION_SIZE = 9

# Figure DPI
DPI = 300  # Publication quality (300-600 recommended)

# Sample size
TOTAL_PROGRAMS = 27

# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def load_data():
    """Load all data from Excel file"""
    data = {
        'interest': pd.read_excel(INPUT_FILE, sheet_name='Interest in AS'),
        'satisfaction': pd.read_excel(INPUT_FILE, sheet_name='Satisfaction scales'),
        'interventions': pd.read_excel(INPUT_FILE, sheet_name='ASP interventions'),
        'barriers': pd.read_excel(INPUT_FILE, sheet_name='Barriers')
    }
    return data

def calculate_interest_career_stats(df):
    """Calculate weighted averages for interest and career placement"""
    # Using midpoint of ranges: 0-25%=12.5%, 26-50%=37.5%, 51-75%=62.5%, 76-100%=87.5%
    midpoints = [12.5, 37.5, 62.5, 87.5]
    
    # Interest counts (from Excel): [11, 10, 5, 1]
    interest_counts = [11, 10, 5, 1]
    career_counts = [20, 4, 3, 0]
    
    avg_interest = sum([m * c for m, c in zip(midpoints, interest_counts)]) / TOTAL_PROGRAMS
    avg_career = sum([m * c for m, c in zip(midpoints, career_counts)]) / TOTAL_PROGRAMS
    
    return avg_interest, avg_career

# ============================================================================
# FIGURE 1: LEADERSHIP PREPAREDNESS GAP
# ============================================================================

def create_figure1(data):
    """Create composite figure with career funnel and satisfaction chart"""
    
    fig = plt.figure(figsize=(12, 8))
    
    # ---- PART A: CAREER FUNNEL ----
    ax1 = plt.subplot(2, 1, 1)
    ax1.axis('off')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    
    # Calculate statistics
    avg_interest, avg_career = calculate_interest_career_stats(data['interest'])
    gap_size = avg_interest - avg_career
    
    # Title
    ax1.text(5, 9.5, 'A. The Career Funnel: Interest vs. Leadership Placement', 
             fontsize=TITLE_SIZE, fontweight='bold', ha='center')
    
    # Interest box
    interest_box = FancyBboxPatch((1, 5.5), 8, 2.5, 
                                   boxstyle="round,pad=0.1",
                                   edgecolor=COLOR_POSITIVE, 
                                   facecolor=COLOR_POSITIVE_LIGHTER,
                                   linewidth=3)
    ax1.add_patch(interest_box)
    ax1.text(5, 7.2, f'{avg_interest:.0f}%', fontsize=48, ha='center', 
             fontweight='bold', color=COLOR_POSITIVE)
    ax1.text(5, 6.3, 'of fellows interested in AS', fontsize=SUBTITLE_SIZE, ha='center')
    ax1.text(5, 5.8, 'at start of fellowship', fontsize=SUBTITLE_SIZE, ha='center')
    
    # Arrow
    arrow = FancyArrowPatch((5, 5.3), (5, 3.7),
                            arrowstyle='->', lw=4, color=COLOR_GRAY,
                            mutation_scale=30)
    ax1.add_patch(arrow)
    
    # Career box
    career_box = FancyBboxPatch((2, 1), 6, 2.5,
                                boxstyle="round,pad=0.1",
                                edgecolor=COLOR_NEGATIVE, 
                                facecolor=COLOR_NEGATIVE_LIGHT,
                                linewidth=3)
    ax1.add_patch(career_box)
    ax1.text(5, 2.7, f'{avg_career:.0f}%', fontsize=48, ha='center', 
             fontweight='bold', color=COLOR_NEGATIVE)
    ax1.text(5, 1.8, 'secured AS leadership', fontsize=SUBTITLE_SIZE, ha='center')
    ax1.text(5, 1.3, 'positions upon graduation', fontsize=SUBTITLE_SIZE, ha='center')
    
    # Gap annotation
    ax1.text(9, 4.5, f'{gap_size:.0f}%\nGAP', fontsize=20, ha='center', 
             fontweight='bold', color=COLOR_NEGATIVE,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                       edgecolor=COLOR_NEGATIVE, linewidth=2))
    
    # ---- PART B: SATISFACTION DIVERGING BAR CHART ----
    ax2 = plt.subplot(2, 1, 2)
    
    # Data from Excel
    categories = [
        'General education/\nbackground knowledge',
        'Ability to use AS in\nclinical practice',
        'Ability to assume a\nleadership role in AS'
    ]
    
    very_satisfied = np.array([9, 10, 3])
    somewhat_satisfied = np.array([14, 15, 12])
    neither = np.array([1, 0, 8])
    somewhat_dissatisfied = np.array([2, 2, 3])
    very_dissatisfied = np.array([1, 0, 1])
    
    # Convert to percentages
    very_satisfied_pct = very_satisfied / TOTAL_PROGRAMS * 100
    somewhat_satisfied_pct = somewhat_satisfied / TOTAL_PROGRAMS * 100
    neither_pct = neither / TOTAL_PROGRAMS * 100
    somewhat_dissatisfied_pct = somewhat_dissatisfied / TOTAL_PROGRAMS * 100
    very_dissatisfied_pct = very_dissatisfied / TOTAL_PROGRAMS * 100
    
    # Calculate positions for diverging layout
    y_pos = np.arange(len(categories))
    bar_height = 0.6

    # Negative side (dissatisfied)
    neg_very = -very_dissatisfied_pct
    neg_somewhat = -somewhat_dissatisfied_pct

    # Positive side (satisfied)
    pos_somewhat = somewhat_satisfied_pct
    pos_very = very_satisfied_pct

    # Calculate starting positions for each section
    # Negative (dissatisfied) - goes LEFT from -(neither/2)
    neutral_half = neither_pct / 2
    dissatisfied_total = somewhat_dissatisfied_pct + very_dissatisfied_pct

    # Plot bars - negative side (very dissatisfied furthest left)
    # Start from -(neutral_half + dissatisfied_total) and go RIGHT
    very_dissatisfied_start = -(neutral_half + dissatisfied_total)
    ax2.barh(y_pos, very_dissatisfied_pct, bar_height, left=very_dissatisfied_start,
             label='Very Dissatisfied', color=COLOR_NEGATIVE,
             edgecolor='black', linewidth=0.5)

    somewhat_dissatisfied_start = very_dissatisfied_start + very_dissatisfied_pct
    ax2.barh(y_pos, somewhat_dissatisfied_pct, bar_height, left=somewhat_dissatisfied_start,
             label='Somewhat Dissatisfied', color=COLOR_NEGATIVE_LIGHT,
             edgecolor='black', linewidth=0.5)

    # Plot neutral bar centered at zero
    ax2.barh(y_pos, neither_pct, bar_height, left=-neutral_half,
             label='Neither', color=COLOR_NEUTRAL, edgecolor='black', linewidth=0.5)

    # Plot bars - positive side starting at neutral_half
    ax2.barh(y_pos, pos_somewhat, bar_height, left=neutral_half,
             label='Somewhat Satisfied', color=COLOR_POSITIVE_LIGHT,
             edgecolor='black', linewidth=0.5)
    ax2.barh(y_pos, pos_very, bar_height, left=neutral_half + pos_somewhat,
             label='Very Satisfied', color=COLOR_POSITIVE,
             edgecolor='black', linewidth=0.5)
    
    # Formatting
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(categories, fontsize=TICK_SIZE)
    ax2.axvline(x=0, color='black', linestyle='-', linewidth=2)
    ax2.set_xlabel('Percentage (%)', fontsize=LABEL_SIZE, fontweight='bold')
    ax2.set_title('B. The Satisfaction Gap: Preparedness Across Competency Levels', 
                  fontsize=TITLE_SIZE, fontweight='bold', pad=15)
    ax2.set_xlim(-60, 100)
    ax2.tick_params(labelsize=TICK_SIZE)
    
    # Legend
    legend_elements = [
        Patch(facecolor=COLOR_NEGATIVE, label='Very Dissatisfied'),
        Patch(facecolor=COLOR_NEGATIVE_LIGHT, label='Somewhat Dissatisfied'),
        Patch(facecolor=COLOR_NEUTRAL, label='Neither'),
        Patch(facecolor=COLOR_POSITIVE_LIGHT, label='Somewhat Satisfied'),
        Patch(facecolor=COLOR_POSITIVE, label='Very Satisfied')
    ]
    ax2.legend(handles=legend_elements, loc='lower left',
              frameon=True, fontsize=ANNOTATION_SIZE)
    
    # Add percentage labels
    for i in range(len(categories)):
        neutral_half_i = neither_pct[i] / 2
        dissatisfied_total_i = somewhat_dissatisfied_pct[i] + very_dissatisfied_pct[i]

        # Negative side total
        if dissatisfied_total_i > 5:
            # Center of dissatisfied section
            dissatisfied_left = -(neutral_half_i + dissatisfied_total_i)
            dissatisfied_center = dissatisfied_left + dissatisfied_total_i / 2
            ax2.text(dissatisfied_center, i, f'{dissatisfied_total_i:.0f}%',
                    ha='center', va='center', fontsize=ANNOTATION_SIZE,
                    fontweight='bold')

        # Neither label (centered at 0)
        if neither_pct[i] > 5:
            ax2.text(0, i, f'{neither_pct[i]:.0f}%',
                    ha='center', va='center', fontsize=ANNOTATION_SIZE,
                    fontweight='bold')

        # Positive side total
        satisfied_total_i = pos_somewhat[i] + pos_very[i]
        if satisfied_total_i > 5:
            satisfied_center = neutral_half_i + satisfied_total_i / 2
            ax2.text(satisfied_center, i, f'{satisfied_total_i:.0f}%',
                    ha='center', va='center', fontsize=ANNOTATION_SIZE,
                    fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}Figure1_Leadership_Gap.pdf',
                dpi=DPI, bbox_inches='tight')
    print("✓ Figure 1 created: Leadership Preparedness Gap")

# ============================================================================
# FIGURE 2: DUMBBELL PLOT FOR ASP INTERVENTIONS
# ============================================================================

def create_figure2(data):
    """Create dumbbell plot comparing curriculum impact"""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Data
    interventions = [
        'Education of residents/faculty',
        'Antibiotic Approval',
        'Guideline Creation',
        'Audit and Feedback',
        'Handshake Rounds',
        'Antibiotic Allergy Assessment',
        'Antibiotic Timeout',
        'None of the above'
    ]
    
    with_curriculum = np.array([76.47, 70.59, 58.82, 58.82, 52.94, 35.29, 17.65, 5.88])
    without_curriculum = np.array([50, 60, 60, 50, 50, 30, 0, 10])
    
    # Sort by gap size
    gaps = np.abs(with_curriculum - without_curriculum)
    sorted_indices = np.argsort(gaps)[::-1]  # Descending order
    
    interventions_sorted = [interventions[i] for i in sorted_indices]
    with_sorted = with_curriculum[sorted_indices]
    without_sorted = without_curriculum[sorted_indices]
    gaps_sorted = gaps[sorted_indices]
    
    y_pos = np.arange(len(interventions_sorted))
    
    # Plot dumbbells
    for i in range(len(interventions_sorted)):
        # Connecting line
        ax.plot([without_sorted[i], with_sorted[i]], [i, i], 
               'o-', color=COLOR_GRAY, linewidth=2, markersize=10,
               markerfacecolor='white', markeredgewidth=2)
        
        # Dots
        ax.plot(with_sorted[i], i, 'o', markersize=12, 
               color=COLOR_POSITIVE, zorder=3)
        ax.plot(without_sorted[i], i, 'o', markersize=12,
               color=COLOR_NEGATIVE, zorder=3)
    
    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(interventions_sorted, fontsize=TICK_SIZE)
    ax.set_xlabel('Percentage of Fellows Participating (%)', 
                 fontsize=LABEL_SIZE, fontweight='bold')
    ax.set_title('Impact of a Formal Curriculum on Fellow Participation\nin AS Interventions',
                fontsize=TITLE_SIZE, fontweight='bold', pad=20)
    ax.set_xlim(-5, 85)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    
    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='With Formal Curriculum',
              markerfacecolor=COLOR_POSITIVE, markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Without Formal Curriculum',
              markerfacecolor=COLOR_NEGATIVE, markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper left',
             frameon=True, fontsize=TICK_SIZE)
    
    # Add gap annotations for all interventions
    for i in range(len(interventions_sorted)):
        gap = gaps_sorted[i]
        mid_point = (with_sorted[i] + without_sorted[i]) / 2
        ax.text(mid_point, i + 0.35, f'Δ{gap:.1f}%',
               ha='center', fontsize=ANNOTATION_SIZE, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}Figure2_ASP_Interventions_Dumbbell.pdf',
               dpi=DPI, bbox_inches='tight')
    print("✓ Figure 2 created: ASP Interventions Dumbbell Plot")

# ============================================================================
# FIGURE 3: BARRIERS TO EDUCATION
# ============================================================================

def create_figure3(data):
    """Create horizontal bar chart of barriers"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Data
    barriers = [
        'Lack of educator time',
        'Lack of materials',
        'None of the above',
        'Lack of AS projects',
        'Lack of time from fellow',
        'Lack of AS interventions'
    ]
    
    percentages = np.array([44.44, 33.33, 22.22, 14.81, 18.52, 7.41])
    
    # Sort from highest to lowest (will be displayed bottom to top, so reverse for top to bottom)
    sorted_indices = np.argsort(percentages)  # Ascending order for top-to-bottom display
    barriers_sorted = [barriers[i] for i in sorted_indices]
    percentages_sorted = percentages[sorted_indices]

    # Plot with single color
    y_pos = np.arange(len(barriers_sorted))
    bars = ax.barh(y_pos, percentages_sorted, color=COLOR_POSITIVE,
                   edgecolor='black', linewidth=1.2, height=0.7)
    
    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(barriers_sorted, fontsize=TICK_SIZE)
    ax.set_xlabel('Percentage of Programs Reporting Barrier (%)',
                 fontsize=LABEL_SIZE, fontweight='bold')
    ax.set_title('Limited Educator Time is the Primary Barrier\nto AS Education',
                fontsize=TITLE_SIZE, fontweight='bold', pad=20)
    ax.set_xlim(0, 55)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    
    # Add value labels
    for i, (bar, pct) in enumerate(zip(bars, percentages_sorted)):
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2,
               f'{pct:.1f}%', ha='left', va='center',
               fontsize=TICK_SIZE, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}Figure3_Barriers.pdf',
               dpi=DPI, bbox_inches='tight')
    print("✓ Figure 3 created: Barriers to Education")

def create_figure3_red(data):
    """Create horizontal bar chart of barriers with red bars"""

    fig, ax = plt.subplots(figsize=(10, 6))

    # Data
    barriers = [
        'Lack of educator time',
        'Lack of materials',
        'None of the above',
        'Lack of AS projects',
        'Lack of time from fellow',
        'Lack of AS interventions'
    ]

    percentages = np.array([44.44, 33.33, 22.22, 14.81, 18.52, 7.41])

    # Sort from highest to lowest (will be displayed bottom to top, so reverse for top to bottom)
    sorted_indices = np.argsort(percentages)  # Ascending order for top-to-bottom display
    barriers_sorted = [barriers[i] for i in sorted_indices]
    percentages_sorted = percentages[sorted_indices]

    # Plot with red color (same as Very Dissatisfied)
    y_pos = np.arange(len(barriers_sorted))
    bars = ax.barh(y_pos, percentages_sorted, color=COLOR_NEGATIVE,
                   edgecolor='black', linewidth=1.2, height=0.7)

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(barriers_sorted, fontsize=TICK_SIZE)
    ax.set_xlabel('Percentage of Programs Reporting Barrier (%)',
                 fontsize=LABEL_SIZE, fontweight='bold')
    ax.set_title('Limited Educator Time is the Primary Barrier\nto AS Education',
                fontsize=TITLE_SIZE, fontweight='bold', pad=20)
    ax.set_xlim(0, 55)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)

    # Add value labels
    for i, (bar, pct) in enumerate(zip(bars, percentages_sorted)):
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2,
               f'{pct:.1f}%', ha='left', va='center',
               fontsize=TICK_SIZE, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}Figure3_Barriers_Red.pdf',
               dpi=DPI, bbox_inches='tight')
    print("✓ Figure 3 (Red version) created: Barriers to Education")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("AS SURVEY MANUSCRIPT - FIGURE GENERATION")
    print("="*70)
    print(f"\nInput file: {INPUT_FILE}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"DPI: {DPI}")
    print(f"Sample size: {TOTAL_PROGRAMS} programs\n")
    
    # Set matplotlib parameters
    plt.rcParams['font.family'] = FONT_FAMILY
    plt.rcParams['font.size'] = TICK_SIZE
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['xtick.major.width'] = 1.2
    plt.rcParams['ytick.major.width'] = 1.2

    # Make PDFs editable in Adobe Illustrator
    plt.rcParams['pdf.fonttype'] = 42   # Embed fonts as TrueType (editable)
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['svg.fonttype'] = 'none'  # For SVGs, keep text as text
    
    # Load data
    print("Loading data...")
    data = load_data()
    print("✓ Data loaded successfully\n")
    
    # Create figures
    print("Creating figures...")
    create_figure1(data)
    create_figure2(data)
    create_figure3(data)
    create_figure3_red(data)

    print("\n" + "="*70)
    print("ALL FIGURES CREATED SUCCESSFULLY!")
    print("="*70)
    print("\nFiles saved to output directory:")
    print("  - Figure1_Leadership_Gap.pdf")
    print("  - Figure2_ASP_Interventions_Dumbbell.pdf")
    print("  - Figure3_Barriers.pdf")
    print("  - Figure3_Barriers_Red.pdf\n")
