import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_natality_data(filepath):
    """Read fixed-width natality data file focusing on relevant fields"""
    colspecs = [
        (74, 76),    # MAGER - Mother's age
        (123, 124),  # MEDUC - Mother's Education 
        (286, 287),  # BMI_R (recoded BMI categories)
        (489, 491),  # COMBGEST - Combined Gestation
        (401, 402),  # ME_ROUT - Delivery Route
        (382, 383),  # LD_INDL - Induction
    ]
    
    columns = ['mage', 'education', 'bmi_r', 'gestation', 'me_rout', 'ld_indl']
    
    return pd.read_fwf(
        filepath,
        colspecs=colspecs,
        names=columns,
        dtype={col: 'Int64' if col != 'ld_indl' else 'str' for col in columns}
    )

def analyze_and_plot_deliveries(df):
    """Analyze and visualize delivery methods by week"""
    filtered_df = df[
        (df['mage'].between(39, 42)) &
        (df['bmi_r'] == 2) &
        (df['education'].isin([7, 8])) &
        (df['gestation'].between(34, 42))
    ].copy()
    
    total_population = len(filtered_df)
    print(f"\nTotal population (34+ weeks): {total_population:,}")
    
    # Define delivery categories for both analysis and plotting
    delivery_cats = {
        'Vaginal Non-Operative-No Induction': ['lightblue', '', (1, 'N')],
        'Vaginal Non-Operative-Induced': ['lightblue', '///', (1, 'Y')],
        'Vaginal Operative-No Induction': ['lightgreen', '', ([2,3], 'N')],
        'Vaginal Operative-Induced': ['lightgreen', '///', ([2,3], 'Y')],
        'C-Section-No Induction': ['salmon', '', (4, 'N')],
        'C-Section-Induced': ['salmon', '///', (4, 'Y')]
    }
    
    # Print weekly statistics
    print("\nWeekly Delivery Statistics:")
    for week in range(34, 43):
        week_births = filtered_df[filtered_df['gestation'] == week]
        week_total = len(week_births)
        print(f"\nWeek {week} (Births: {week_total}, {(week_total/total_population)*100:.1f}% of population)")
        
        for label, (_, _, (route, induction)) in delivery_cats.items():
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
            print(f"  {label}: {count} ({prob:.1f}% of population)")
    
    # Create visualization
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # Top plot: Overall weekly probabilities
    weekly_counts = filtered_df['gestation'].value_counts().sort_index()
    weekly_percentages = (weekly_counts / total_population) * 100
    ax1.bar(weekly_counts.index, weekly_percentages, color='lightgray')
    ax1.set_title('Weekly Delivery Probability\nMothers 39-42, Normal BMI, Masters+', pad=20)
    ax1.set_ylabel('Probability of Delivery (%)')
    
    # Bottom plot: Delivery methods
    bottom = np.zeros(len(range(34, 43)))
    
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
    
    max_total_pct = max(bottom)
    ax2.set_ylim(0, max_total_pct * 1.05)
    
    for ax in [ax1, ax2]:
        ax.set_xticks(range(34, 43))
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1f}%'.format(y)))
    
    plt.tight_layout()
    return fig

def main():
    df = read_natality_data("Nat2023us.txt")
    fig = analyze_and_plot_deliveries(df)
    fig.savefig('delivery_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()