import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_natality_data(filepath):
    """Read fixed-width natality data file focusing on BMI-related fields"""
    colspecs = [
        (74, 76),    # MAGER - Mother's age
        (178, 179),  # LBO_REC - Live Birth Order
        (123, 124),  # MEDUC - Mother's Education 
        (286, 287),  # BMI_R (recoded BMI categories)
        (489, 491),  # COMBGEST - Combined Gestation
        (504, 507),  # DBWT - Birth Weight in Grams
        (224, 225),  # PRECARE - Month Prenatal Care Began
        (401, 402),  # ME_ROUT - Delivery Route
        (382, 383),  # LD_INDL - Induction
    ]
    
    columns = ['mage', 'birth_order', 'education', 'bmi_r', 'gestation', 'birthweight', 'prenatal_care', 'me_rout', 'ld_indl']
    
    print(f"Reading data from {filepath}...")
    
    df = pd.read_fwf(
        filepath,
        colspecs=colspecs,
        names=columns,
        dtype={
            'mage': 'Int64',
            'birth_order': 'Int64',
            'education': 'Int64',
            'bmi_r': 'Int64',
            'gestation': 'Int64',
            'birthweight': 'Int64',
            'prenatal_care': 'Int64',
            'me_rout': 'Int64',
            'ld_indl': 'str'
        }
    )
    
    # Add debug printing
    print("\nBMI Category Distribution:")
    print("1 Underweight (<18.5):", len(df[df['bmi_r'] == 1]))
    print("2 Normal (18.5-24.9):", len(df[df['bmi_r'] == 2]))
    print("3 Overweight (25.0-29.9):", len(df[df['bmi_r'] == 3]))
    print("4 Obesity I (30.0-34.9):", len(df[df['bmi_r'] == 4]))
    print("5 Obesity II (35.0-39.9):", len(df[df['bmi_r'] == 5]))
    print("6 Extreme Obesity III (≥40):", len(df[df['bmi_r'] == 6]))
    print("9 Unknown:", len(df[df['bmi_r'] == 9]))
    
    return df

def analyze_normal_bmi_births(df):
    """Analyze births to mothers with normal BMI (category 2)"""
    # Filter for normal BMI using the recoded category
    normal_bmi_df = df[df['bmi_r'] == 2].copy()
    
    print("\nBasic Statistics:")
    print(f"Total births: {len(df):,}")
    print(f"Births to mothers with normal BMI: {len(normal_bmi_df):,}")
    print(f"Percentage of births to mothers with normal BMI: {(len(normal_bmi_df)/len(df))*100:.1f}%")
    
    # No need for pd.cut since we're using pre-categorized BMI values
    
    return normal_bmi_df

def plot_normal_bmi_analysis(df):
    """Create visualizations for normal BMI analysis"""
    # Set up the plotting style
    plt.style.use('seaborn')
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Age distribution
    plt.subplot(2, 2, 1)
    sns.histplot(data=df, x='mage', bins=30)
    plt.title('Age Distribution of Mothers with Normal BMI')
    plt.xlabel('Maternal Age')
    plt.ylabel('Count')
    
    # Education distribution
    plt.subplot(2, 2, 2)
    education_counts = df['education'].value_counts()
    education_counts.plot(kind='bar')
    plt.title('Education Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Birth weight distribution
    plt.subplot(2, 2, 3)
    sns.histplot(data=df, x='birthweight', bins=30)
    plt.title('Birth Weight Distribution')
    plt.xlabel('Birth Weight (grams)')
    plt.ylabel('Count')
    
    # Gestational age distribution
    plt.subplot(2, 2, 4)
    sns.histplot(data=df, x='gestation', bins=30)
    plt.title('Gestational Age Distribution')
    plt.xlabel('Gestational Age (weeks)')
    plt.ylabel('Count')
    
    plt.tight_layout()
    plt.savefig('normal_bmi_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def analyze_advanced_degree_normal_bmi(df):
    # Filter for target population
    filtered_df = df[
        (df['mage'].between(39, 42)) &
        (df['bmi_r'] == 2) &
        (df['education'].isin([7, 8])) &
        (df['gestation'].between(34, 42))
    ].copy()
    
    total_population = len(filtered_df)
    print("\nFiltering summary:")
    print(f"Total population (34+ weeks): {total_population:,}")
    
    # Create delivery categories with updated labels
    delivery_cats = {
        'Vaginal Non-Operative-No Induction': (filtered_df['me_rout'] == 1) & (filtered_df['ld_indl'] == 'N'),
        'Vaginal Non-Operative-Induced': (filtered_df['me_rout'] == 1) & (filtered_df['ld_indl'] == 'Y'),
        'Vaginal Operative-No Induction': (filtered_df['me_rout'].isin([2,3])) & (filtered_df['ld_indl'] == 'N'),
        'Vaginal Operative-Induced': (filtered_df['me_rout'].isin([2,3])) & (filtered_df['ld_indl'] == 'Y'),
        'C-Section-No Induction': (filtered_df['me_rout'] == 4) & (filtered_df['ld_indl'] == 'N'),
        'C-Section-Induced': (filtered_df['me_rout'] == 4) & (filtered_df['ld_indl'] == 'Y')
    }
    
    # Calculate weekly distributions
    weekly_stats = {}
    for week in range(34, 43):
        week_births = filtered_df[filtered_df['gestation'] == week]
        week_total = len(week_births)
        
        stats = {}
        for cat_name, cat_filter in delivery_cats.items():
            count = len(week_births[cat_filter])
            prob = (count / total_population) * 100  # Probability relative to total population
            stats[cat_name] = {'count': count, 'probability': prob}
        weekly_stats[week] = stats
    
    # Print detailed statistics
    print("\nWeekly Delivery Probabilities:")
    for week, stats in weekly_stats.items():
        week_total = sum(s['count'] for s in stats.values())
        print(f"\nWeek {week} (Births: {week_total}, {(week_total/total_population)*100:.1f}% of population)")
        for cat, values in stats.items():
            print(f"  {cat}: {values['count']} ({values['probability']:.1f}% of population)")
    
    return filtered_df

def plot_weekly_deliveries_with_methods(df):
    """Create comprehensive weekly delivery visualization with method breakdowns"""
    filtered_df = df[
        (df['mage'].between(39, 42)) &
        (df['bmi_r'] == 2) &
        (df['education'].isin([7, 8])) &
        (df['gestation'].between(34, 42))
    ].copy()
    
    total_population = len(filtered_df)
    
    # Set up the plot with gridspec
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # Top plot remains the same
    weekly_counts = filtered_df['gestation'].value_counts().sort_index()
    weekly_percentages = (weekly_counts / total_population) * 100
    ax1.bar(weekly_counts.index, weekly_percentages, color='lightgray')
    ax1.set_title('Weekly Delivery Probability\nMothers 39-42, Normal BMI, Masters+', pad=20)
    ax1.set_ylabel('Probability of Delivery (%)')
    
    # Bottom plot: New color/hatch scheme
    delivery_cats = {
        'Spontaneous-No Induction': ['lightblue', '', (1, 'N')],
        'Spontaneous-Induced': ['lightblue', '///', (1, 'Y')],
        'Operative Vaginal-No Induction': ['lightgreen', '', ([2,3], 'N')],
        'Operative Vaginal-Induced': ['lightgreen', '///', ([2,3], 'Y')],
        'Cesarean-No Induction': ['salmon', '', (4, 'N')],
        'Cesarean-Induced': ['salmon', '///', (4, 'Y')]
    }
    
    bottom = np.zeros(len(range(34, 43)))
    
    # Calculate and plot probabilities for each delivery method
    for label, (color, hatch, (route, induction)) in delivery_cats.items():
        weekly_probs = []
        for week in range(34, 43):
            week_births = filtered_df[filtered_df['gestation'] == week]
            if isinstance(route, list):
                count = len(week_births[
                    (week_births['me_rout'].isin(route)) & 
                    (week_births['ld_indl'] == induction)
                ])
            else:
                count = len(week_births[
                    (week_births['me_rout'] == route) & 
                    (week_births['ld_indl'] == induction)
                ])
            prob = (count / total_population) * 100
            weekly_probs.append(prob)
            
        ax2.bar(range(34, 43), weekly_probs, bottom=bottom,
                label=label, color=color, hatch=hatch)
        bottom += weekly_probs
    
    ax2.set_title('Delivery Method Distribution by Week\n(% of Total Population)', pad=20)
    ax2.set_xlabel('Gestational Week')
    ax2.set_ylabel('% of Total Population')
    ax2.legend(bbox_to_anchor=(1.05, 1))
    
    # Set y-axis limit to actual maximum percentage
    max_total_pct = max(bottom)
    ax2.set_ylim(0, max_total_pct * 1.05)
    
    # Formatting
    for ax in [ax1, ax2]:
        ax.set_xticks(range(34, 43))
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1f}%'.format(y)))
    
    plt.tight_layout()
    return fig

def main():
    # Read and analyze data
    filepath = "Nat2023us.txt"  # Update with actual filepath
    df = read_natality_data(filepath)
    
    # Perform analysis
    normal_bmi_df = analyze_normal_bmi_births(df)
    advanced_degree_normal_bmi_df = analyze_advanced_degree_normal_bmi(normal_bmi_df)
    
    # Create visualizations
    plot_normal_bmi_analysis(normal_bmi_df)
    fig = plot_weekly_deliveries_with_methods(df)
    fig.savefig('delivery_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()