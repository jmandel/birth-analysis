import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

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

def generate_json_data(df):
    """Generate JSON data for interactive filtering"""
    
    # Define the dimensions we want to capture
    age_ranges = [(15,19), (20,24), (25,29), (30,34), (35,38), (39,42), (43,50)]
    bmi_categories = {
        1: "Underweight",
        2: "Normal",
        3: "Overweight",
        4: "Obese"
    }
    education_levels = {
        1: "8th grade or less",
        2: "9-12th grade, no diploma",
        3: "High school graduate/GED",
        4: "Some college, no degree",
        5: "Associate degree",
        6: "Bachelor's degree",
        7: "Master's degree",
        8: "Doctorate/Professional degree"
    }
    
    # Initialize data structure
    data = {
        "metadata": {
            "age_ranges": age_ranges,
            "bmi_categories": bmi_categories,
            "education_levels": education_levels,
            "delivery_types": [
                "Vaginal Non-Operative-No Induction",
                "Vaginal Non-Operative-Induced",
                "Vaginal Operative-No Induction",
                "Vaginal Operative-Induced",
                "C-Section-No Induction",
                "C-Section-Induced"
            ]
        },
        "data": {}
    }
    
    # Calculate counts for each combination
    for age_range in age_ranges:
        age_key = f"{age_range[0]}-{age_range[1]}"
        data["data"][age_key] = {}
        
        for bmi in bmi_categories.keys():
            data["data"][age_key][str(bmi)] = {}
            
            for edu in education_levels.keys():
                filtered_df = df[
                    (df['mage'].between(age_range[0], age_range[1])) &
                    (df['bmi_r'] == bmi) &
                    (df['education'] == edu) &
                    (df['gestation'].between(34, 42))
                ]
                
                # Skip if no data for this combination
                if len(filtered_df) == 0:
                    continue
                
                weekly_data = {}
                for week in range(34, 43):
                    week_births = filtered_df[filtered_df['gestation'] == week]
                    
                    delivery_counts = {
                        "Vaginal Non-Operative-No Induction": len(week_births[(week_births['me_rout'] == 1) & (week_births['ld_indl'] == 'N')]),
                        "Vaginal Non-Operative-Induced": len(week_births[(week_births['me_rout'] == 1) & (week_births['ld_indl'] == 'Y')]),
                        "Vaginal Operative-No Induction": len(week_births[week_births['me_rout'].isin([2,3]) & (week_births['ld_indl'] == 'N')]),
                        "Vaginal Operative-Induced": len(week_births[week_births['me_rout'].isin([2,3]) & (week_births['ld_indl'] == 'Y')]),
                        "C-Section-No Induction": len(week_births[(week_births['me_rout'] == 4) & (week_births['ld_indl'] == 'N')]),
                        "C-Section-Induced": len(week_births[(week_births['me_rout'] == 4) & (week_births['ld_indl'] == 'Y')])
                    }
                    
                    if sum(delivery_counts.values()) > 0:  # Only include weeks with data
                        weekly_data[str(week)] = delivery_counts
                
                data["data"][age_key][str(bmi)][str(edu)] = weekly_data
    
    return data

def main():
    df = read_natality_data("Nat2023us.txt")
    
    # Generate and save JSON data
    json_data = generate_json_data(df)
    with open('birth_data.json', 'w') as f:
        json.dump(json_data, f)
    
    # Original visualization code can stay...
    fig = analyze_and_plot_deliveries(df)
    fig.savefig('delivery_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()