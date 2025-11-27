import pandas as pd
import matplotlib.pyplot as plt


def plot_population_vs_fields(df_path: str) -> None:
    """
    
    :param df_path: path to dataframe 
    :return: plots population of city as a dot graph, and tennis fields as histogram, on the same plot.
    """
    # ---- Load your dataset ----
    df = pd.read_csv("data_full.csv")

    # ---- Group by territory ----
    grouped = df.groupby("territory").agg(
        entry_count=("territory", "count"),
        population=("population", "first")
    ).reset_index()

    # ---- Plot ----
    fig, ax1 = plt.subplots(figsize=(10,6))

    # Bar plot for entry count
    bars = ax1.bar(grouped["territory"], grouped["entry_count"], label="Entry Count")
    ax1.set_ylabel("Number of Entries")
    ax1.set_xticklabels(grouped["territory"], rotation=45, ha="right")

    # Second y-axis for population
    ax2 = ax1.twinx()
    dots = ax2.scatter(grouped["territory"], grouped["population"], color="red", label="Population")
    ax2.set_ylabel("Population")

    # ---- Legend ----
    # Combine handles from both axes
    handles = [bars, dots]
    labels = ["Entry Count", "Population"]
    plt.legend(handles, labels, loc="upper left")

    plt.title("Number of Entries per Territory vs Population")
    plt.tight_layout()
    plt.show()


def plot_scatter_tennis_fields_vs_population(csv_path):
    """
    Reads a CSV file of tennis fields and plots a scatter plot:
    X-axis: Population
    Y-axis: Number of tennis fields per area
    """
    # Load CSV
    df = pd.read_csv(csv_path)

    # Aggregate by area
    agg = df.groupby('territory').agg(
        tennis_fields=('id', 'count'),
        population=('population', 'first')  # assuming population is same for each area
    ).reset_index()

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(agg['population'], agg['tennis_fields'], s=100, alpha=0.7, color='teal')

    # Add labels for each point
    for i, row in agg.iterrows():
        plt.text(row['population'], row['tennis_fields'], row['territory'], fontsize=8, ha='right', va='bottom')

    plt.xlabel('Population')
    plt.ylabel('Number of Tennis Fields')
    plt.title('Tennis Fields per Area vs Population')
    plt.grid(True)
    plt.show()


def plot_tennis_fields_vs_population_bubble(csv_path):
    """
    Reads a CSV file of tennis fields and produces a bubble plot:
    X-axis: Population
    Y-axis: Number of tennis fields per area
    Bubble size: Population
    """
    # Load CSV
    df = pd.read_csv(csv_path)

    # Aggregate by area
    agg = df.groupby('territory').agg(
        tennis_fields=('id', 'count'),
        population=('population', 'first')  # population is constant for each area
    ).reset_index()


    # Bubble sizes scaled
    bubble_size = agg['population'] / agg['population'].max() * 2000

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(
        agg['population'],
        agg['tennis_fields'],
        s=bubble_size,
        alpha=0.5,
        linewidths=1,
        edgecolor='black'
    )

    # Add labels
    for _, row in agg.iterrows():
        plt.text(row['population'], row['tennis_fields'], row['territory'],
                 fontsize=8, ha='center', va='center')

    plt.xlabel('Population')
    plt.ylabel('Number of Tennis Fields')
    plt.title('Tennis Fields per Area vs Population (Bubble Plot)')
    plt.grid(True)
    plt.show()



def plot_tennis_field_heatmap(csv_path):
    """
    Reads a CSV containing tennis field locations and produces a 2D heatmap
    of latitude vs longitude using matplotlib.hist2d.
    """
    # Load CSV
    df = pd.read_csv(csv_path)

    # Extract coordinates
    lats = df["latitude"]
    lons = df["longitude"]

    # Plot
    plt.figure(figsize=(8, 8))
    plt.hist2d(lons, lats, bins=30, cmap="hot")
    plt.colorbar(label="Tennis Court Density")

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Heatmap of Tennis Court Density")
    plt.tight_layout()
    plt.show()

plot_population_vs_fields('data_full.csv')
plot_tennis_field_heatmap('data_full.csv')
plot_scatter_tennis_fields_vs_population('data_full.csv')