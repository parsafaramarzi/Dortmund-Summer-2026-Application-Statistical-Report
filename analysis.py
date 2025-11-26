import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import scikit_posthocs as sp

# ==============================================================================
# --- Task A: Descriptive Analysis Functions ---
# ==============================================================================
def read_data():
    # Reads the dataset and performs initial structural cleaning.
    dataset = pd.read_csv(
        'cycling.txt',
        delim_whitespace=True,
        quotechar='"'
    )
    return dataset

def give_summary_statistics(dataset):
    # Generates and prints three main summary tables.
    print("\n" + "#"*80 + "\nTASK A: DESCRIPTIVE STATISTICS TABLES" + "\n" + "#"*80)

    # Summary 1: Points by Rider Class and Stage Class
    summary_stats = dataset.groupby(['rider_class', 'stage_class'])['points'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).reset_index()
    print("\n--- Summary 1: Points by Rider Class and Stage Class (Table 1) ---")
    print(summary_stats.to_string(float_format='{:0.2f}'.format))
    summary_stats.to_csv('output/rider_stage_points_summary.csv', index=False)

    # Summary 2: Overall Summary Statistics for Points by Rider Class
    overall_rider_summary = dataset.groupby('rider_class')['points'].agg(['count', 'mean', 'median', 'std']).sort_values(by='mean', ascending=False)
    print("\n--- Summary 2: Overall Points by Rider Class (Table 2) ---")
    print(overall_rider_summary.to_string(float_format='{:0.2f}'.format))
    overall_rider_summary.to_csv('output/overall_rider_points_summary.csv', index=True)

    # Summary 3: Points by Stage and Stage Class
    stage_summary = dataset.groupby(['stage', 'stage_class'])['points'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).reset_index()
    stage_summary['stage_num'] = stage_summary['stage'].str.replace('X', '', regex=False).astype(int)
    stage_summary = stage_summary.sort_values(by='stage_num').drop(columns=['stage_num'])
    print("\n--- Summary 3: Points by Stage and Stage Class (Context Table) ---")
    print(stage_summary.to_string(float_format='{:0.2f}'.format))
    stage_summary.to_csv('output/stage_stageclass_points_summary.csv', index=False)

    return {
        'summary_rider_stage': summary_stats,
        'summary_overall_rider': overall_rider_summary,
        'summary_stage': stage_summary
    }

# VISUALIZATION FUNCTIONS (Reordered for optimal report narrative)

def generate_total_points_histogram(dataset):
    # Figure 1: Displays overall distribution (for justifying non-parametric tests).
    df_total = dataset.groupby(['all_riders', 'rider_class'])['points'].sum().reset_index()
    df_total.rename(columns={'points': 'total_points'}, inplace=True)
    df_total.to_csv('output/rider_total_points.csv', index=False)

    print("\n" + "#"*80 + "\nGenerating Figure 1: Histogram of Total Points (Non-Normality Proof)" + "\n" + "#"*80)
    
    plt.figure(figsize=(9, 6))
    sns.histplot(
        data=df_total,
        x='total_points',
        bins=20,
        kde=True,
        color='maroon'
    )
    plt.xlabel('Total Tour Points Scored')
    plt.ylabel('Number of Riders')
    plt.tight_layout()
    plt.savefig('output/figure1_histogram_total_points.png')
    plt.show()

def generate_comparative_boxplot(dataset):
    # Figure 2: Mandatory Comparative Box Plot (RQ1 & RQ2).
    stage_order = ['flat', 'hills', 'mount']
    dataset['stage_class'] = pd.Categorical(dataset['stage_class'], categories=stage_order, ordered=True)

    print("\n" + "#"*80 + "\nGenerating Figure 2: Comparative Box Plot (Stage Performance)" + "\n" + "#"*80)
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))

    sns.boxplot(
        x='rider_class',
        y='points',
        hue='stage_class',
        data=dataset,
        palette="viridis"
    )

    plt.xlabel('Rider Class')
    plt.ylabel('Stage Points Awarded')
    plt.legend(title='Stage Type', bbox_to_anchor=(1.05, 1), loc=2)
    plt.tight_layout()
    plt.savefig('output/figure2_comparative_boxplot.png')
    plt.show()
    
def generate_mean_points_barplot(dataset):
    # Figure 3: Mean Points Bar Plot (Magnitude of Performance).
    mean_points_summary = dataset.groupby(['rider_class', 'stage_class'])['points'].mean().reset_index()
    stage_order = ['flat', 'hills', 'mount']
    mean_points_summary['stage_class'] = pd.Categorical(mean_points_summary['stage_class'], categories=stage_order, ordered=True)

    print("\n" + "#"*80 + "\nGenerating Figure 3: Mean Points Bar Plot (Magnitude)" + "\n" + "#"*80)
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    sns.barplot(
        x='rider_class',
        y='points',
        hue='stage_class',
        data=mean_points_summary,
        palette="viridis",
    )

    plt.xlabel('Rider Class')
    plt.ylabel('Mean Stage Points')
    plt.legend(title='Stage Type', bbox_to_anchor=(1.05, 1), loc=2)
    plt.tight_layout()
    plt.savefig('output/figure3_mean_points_barplot.png')
    plt.show()

def total_points_boxplot_by_rider_class(dataset):
    # Figure 4: Box Plot of Total Tour Points by Rider Class (Overall Hierarchy).
    df_total = dataset.groupby(['all_riders', 'rider_class'])['points'].sum().reset_index()
    df_total.rename(columns={'points': 'total_points'}, inplace=True)
    
    order = df_total.groupby('rider_class')['total_points'].mean().sort_values(ascending=False).index

    print("\n" + "#"*80 + "\nGenerating Figure 4: Box Plot of Total Tour Points (Overall Hierarchy)" + "\n" + "#"*80)
    sns.set_style("whitegrid")
    plt.figure(figsize=(9, 6))
    sns.boxplot(
    x='rider_class',
    y='total_points',
    data=df_total,
    order=order,
    palette="rocket"
    )

    plt.xlabel('Rider Class')
    plt.ylabel('Total Tour Points Scored')
    plt.tight_layout()
    plt.savefig('output/figure4_total_points_boxplot.png')
    plt.show()

def total_points_by_stage_bar_chart(dataset):
    # Figure 5: Total Points by Stage Bar Chart (Context/Validation).
    print("\n" + "#"*80 + "\nGenerating Figure 5: Total Points by Stage (Context)" + "\n" + "#"*80)
    total_points_summary = dataset.groupby(['stage', 'stage_class'])['points'].sum().reset_index()
    total_points_summary['stage_num'] = total_points_summary['stage'].str.replace('X', '', regex=False).astype(int)
    total_points_summary = total_points_summary.sort_values(by='stage_num')

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))

    sns.barplot(
        x='stage',
        y='points',
        hue='stage_class',
        data=total_points_summary,
        palette={'flat': 'green', 'hills': 'blue', 'mount': 'red'},
        dodge=False
    )

    plt.xlabel('Stage Number (X)')
    plt.ylabel('Total Points Awarded (Sum)')
    plt.legend(title='Stage Type', bbox_to_anchor=(1.05, 1), loc=2)
    plt.tight_layout()
    plt.savefig('output/figure5_total_points_by_stage.png')
    plt.show()

# ==============================================================================
# --- Task B: Hypothesis Testing Functions ---
# ==============================================================================
def perform_levene_tests(dataset):
    # Task B, Step 1: Tests for homogeneity of variances.
    print("\n" + "#"*80 + "\nTASK B, STEP 1: LEVENE'S TEST (ASSUMPTION CHECK)" + "\n" + "#"*80)

    groups_rider = [dataset['points'][dataset['rider_class'] == c].dropna() for c in dataset['rider_class'].unique()]
    levene_rider = stats.levene(*groups_rider, center='median')
    print("\n--- Levene's Test for Rider Class ---")
    print(f"Test Statistic (W): {levene_rider.statistic:.4f}, P-value: {levene_rider.pvalue:.10f}")
    
    groups_stage = [dataset['points'][dataset['stage_class'] == c].dropna() for c in dataset['stage_class'].unique()]
    levene_stage = stats.levene(*groups_stage, center='median')
    print("\n--- Levene's Test for Stage Class ---")
    print(f"Test Statistic (W): {levene_stage.statistic:.4f}, P-value: {levene_stage.pvalue:.10f}")
    
    print("#"*80 + "\nLevene's tests complete. Results confirm the need for non-parametric tests." + "\n" + "#"*80)
    return {'rider_class_pvalue': levene_rider.pvalue, 'stage_class_pvalue': levene_stage.pvalue}

def kruskal_wallis_rider_class(dataset):
    # Task B, Step 2: Main test for RQ1 (Rider Class).
    print("\n" + "#"*80 + "\nTASK B, STEP 2: KRUSKAL-WALLIS (Rider Class / RQ1)" + "\n" + "#"*80)
    rider_groups = [dataset['points'][dataset['rider_class'] == c].dropna() for c in dataset['rider_class'].unique()]
    h_statistic, p_value = stats.kruskal(*rider_groups)
    print(f"H-Statistic: {h_statistic:.4f}, P-value: {p_value:.10f}")
    return {'H_statistic': h_statistic, 'p_value': p_value}

def dunn_posthoc_rider_class(dataset):
    # Task B, Step 3: Post-Hoc test for RQ1 (Rider Class).
    print("\n" + "#"*80 + "\nTASK B, STEP 3: DUNN'S POST-HOC (Rider Class / RQ1)" + "\n" + "#"*80)
    dunn_results = sp.posthoc_dunn(a=dataset, val_col='points', group_col='rider_class', p_adjust='bonferroni')
    print("\n--- Post-Hoc P-value Matrix (Rider Class) ---")
    print(dunn_results.to_string(float_format='{:0.8f}'.format))
    return dunn_results

def kruskal_wallis_stage_class(dataset):
    # Task B, Step 4: Main test for RQ2 (Stage Class).
    print("\n" + "#"*80 + "\nTASK B, STEP 4: KRUSKAL-WALLIS (Stage Class / RQ2)" + "\n" + "#"*80)
    stage_groups = [dataset['points'][dataset['stage_class'] == c].dropna() for c in dataset['stage_class'].unique()]
    h_statistic, p_value = stats.kruskal(*stage_groups)
    print(f"H-Statistic: {h_statistic:.4f}, P-value: {p_value:.10f}")
    return {'H_statistic': h_statistic, 'p_value': p_value}

def dunn_posthoc_stage_class(dataset):
    # Task B, Step 5: Post-Hoc test for RQ2 (Stage Class).
    print("\n" + "#"*80 + "\nTASK B, STEP 5: DUNN'S POST-HOC (Stage Class / RQ2)" + "\n" + "#"*80)
    dunn_results = sp.posthoc_dunn(a=dataset, val_col='points', group_col='stage_class', p_adjust='bonferroni')
    print("\n--- Post-Hoc P-value Matrix (Stage Class) ---")
    print(dunn_results.to_string(float_format='{:0.8f}'.format))
    return dunn_results

# ==============================================================================
# MAIN EXECUTION FLOW
# ==============================================================================
def run_analysis():

    # 1. Data Loading
    dataset = read_data()
    print("\n" + "#"*80 + "\nDATASET INFO" + "\n" + "#"*80)
    dataset.info()

    df_total = dataset.groupby(['all_riders', 'rider_class'])['points'].sum().reset_index()
    df_total.rename(columns={'points': 'total_points'}, inplace=True)
    df_total.to_csv('output/rider_total_points.csv', index=False)
    
    # --- TASK A: DESCRIPTIVE ANALYSIS ---
    descriptive_summaries = give_summary_statistics(dataset)
    
    # Visualizations (Figure 1-5, in logical report order)
    generate_total_points_histogram(dataset)        # Figure 1 (Justifies methods)
    generate_comparative_boxplot(dataset)            # Figure 2 (Core RQ comparison)
    generate_mean_points_barplot(dataset)            # Figure 3 (Magnitude)
    total_points_boxplot_by_rider_class(dataset)    # Figure 4 (Overall Hierarchy)
    total_points_by_stage_bar_chart(dataset)         # Figure 5 (Context)

    # --- TASK B: HYPOTHESIS TESTING ---
    levene_results = perform_levene_tests(dataset)

    # Part 1: Rider Class (RQ1)
    kw_rider_results = kruskal_wallis_rider_class(dataset)
    dunn_rider_results = dunn_posthoc_rider_class(dataset)

    # Part 2: Stage Class (RQ2)
    kw_stage_results = kruskal_wallis_stage_class(dataset)
    dunn_stage_results = dunn_posthoc_stage_class(dataset)

    return {
        'descriptive': descriptive_summaries,
        'df_total': df_total,
        'levene': levene_results,
        'kw_rider': kw_rider_results,
        'dunn_rider': dunn_rider_results,
        'kw_stage': kw_stage_results,
        'dunn_stage': dunn_stage_results,
        'image_paths': [
            'output/figure1_histogram_total_points.png',
            'output/figure2_comparative_boxplot.png',
            'output/figure3_mean_points_barplot.png',
            'output/figure4_total_points_boxplot.png',
            'output/figure5_total_points_by_stage.png'
        ]
    }
    
# Call the main function to execute the full analysis
if __name__ == '__main__':
    print("Running full analysis and generating image files. Data is prepared for report generation.")
    run_analysis()