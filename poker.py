import pandas as pd
from datetime import date
from pandas.errors import EmptyDataError
import matplotlib.pyplot as plt
# 1. Initialize or Load Database
try:
    df = pd.read_csv('poker_log.csv', parse_dates=['Date'])
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'GameType', 'Stakes', 'BuyIn', 'CashOut', 'Net'])

def add_session(game_type, stakes, buyin, cashout):
    """Adds a new session to the log."""
    global df
    net = cashout - buyin
    new_session = {
        'Date': date.today(),
        'GameType': game_type,
        'Stakes': stakes,
        'BuyIn': buyin,
        'CashOut': cashout,
        'Net': net
    }
    df = pd.concat([df, pd.DataFrame([new_session])], ignore_index=True)
    df.to_csv('poker_log.csv', index=False)
    print(f"Session added! Net: ${net}")
#If Showing error type  (Date,GameType,Stakes,BuyIn,CashOut,Net) into the expty csv file then code will run

def show_stats():
    """Displays total profit and history."""
    if df.empty:
        print("No sessions logged yet.")
        return
    total_net = df['Net'].sum()
    print("\n--- Poker Statistics ---")
    print(f"Total Sessions: {len(df)}")
    print(f"Total Bankroll: ${total_net}")
    print("\nSession History:")
    print(df.to_string(index=False))
    
def plot_bankroll():
    """Plots cumulative profit over time."""
    if df.empty:
        print("No sessions logged yet.")
        return
    
    d = df.copy()
    d['Date'] = pd.to_datetime(d['Date'], errors='coerce')
    d = d.dropna(subset=['Date'])
    d = d.sort_values(['Date']).reset_index(drop=True)
    d['Cumulative'] = d['Net'].cumsum()
    
    # Create larger figure with better proportions
    plt.figure(figsize=(12, 6))
    
    # Color the line based on profit/loss
    colors = ['green' if x >= 0 else 'red' for x in d['Cumulative']]
    
    # Plot with styling
    plt.plot(d['Date'], d['Cumulative'], marker='o', linewidth=2.5, 
             markersize=8, color='#2E86AB', markerfacecolor='white', 
             markeredgewidth=2, markeredgecolor='#2E86AB')
    
    # Add a zero line for reference
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    
    # Fill area under curve
    plt.fill_between(d['Date'], d['Cumulative'], 0, 
                     where=(d['Cumulative'] >= 0), alpha=0.3, color='green', label='Profit')
    plt.fill_between(d['Date'], d['Cumulative'], 0, 
                     where=(d['Cumulative'] < 0), alpha=0.3, color='red', label='Loss')
    
    # Styling
    plt.title("Poker Bankroll Tracker", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Date", fontsize=12, fontweight='bold')
    plt.ylabel("Cumulative Profit ($)", fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='best')
    
    # Format y-axis to show dollar signs
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Show the win rate
    wins = len(d[d['Net'] > 0])
    total = len(d)
    win_rate = (wins / total) * 100
    plt.text(0.02, 0.98, f'Win Rate: {win_rate:.1f}%', 
             transform=ax.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
   
    plt.tight_layout()
    plt.show()


# --- Usage ---
#once added make a note so not added twice
#add_session("cash", "25/50", 20, 50)
#add_session("cash", "25/50", 20, 55)
#add_session("cash", "25/50", 20, 35)
#add_session("cash", "25/50", 20, 74)
#add_session("cash", "25/50", 40, 72)
#add_session("cash", "25/50", 20, 63)
#add_session("cash", "25/50", 30, 0)


show_stats()
plot_bankroll()