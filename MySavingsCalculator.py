# Import necessary libraries
import tkinter as tk
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# calculate_details function calculates the details of the investment over time.
# P: initial amount, apy: annual percentage yield, t: time in years, d: monthly deposit
def calculate_details(P, apy, t, d):
    # calculate the monthly APY
    monthly_apy = (1 + apy) ** (1 / 12) - 1
    balance = P
    # Initialize empty lists for balances, interests, and contributions.
    balances, interests, contributions = [], [], []
    for month in range(int(t * 12)):  # Loop for each month in t years
        interest = balance * monthly_apy  # Calculate the interest
        balance += interest + d  # Update the balance
        balances.append(balance)
        interests.append(interest)
        contributions.append(d if month > 0 else P + d)
    return balances, interests, contributions  # Return the lists

# plot_details function plots the growth of the investment and prediction.
# balances: list of balances over time, t: time in years
def plot_details(balances, t):
    months = np.array([month for month in range(int(t * 12))]).reshape(-1, 1)
    balance_array = np.array(balances).reshape(-1, 1)

    model = LinearRegression()
    model.fit(months, balance_array)  # Fit a linear regression model

    # Predict future balance for next 5 years (60 months)
    future_months = np.array([month for month in range(int(t * 12), int(t * 12) + 60)]).reshape(-1, 1)
    future_balance = model.predict(future_months)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(months, balances, label="Total Balance")
    plt.plot(future_months, future_balance, label="Predicted Total Balance", linestyle='dashed')
    plt.xlabel("Months")
    plt.ylabel("Amount ($)")
    plt.title("Investment Growth Over Time with Prediction")
    plt.legend()
    plt.show()

# calculate function handles the calculations and plotting
def calculate():
    # Retrieve the values from the entry widgets
    P = float(entry_P.get())
    d = float(entry_d.get())
    apy = float(entry_apy.get()) / 100
    t = float(entry_t.get())
    # Call the calculate_details function
    balances, interests, contributions = calculate_details(P, apy, t, d)
    final_balance = balances[-1]
    total_contributions = sum(contributions)
    interest_earned = final_balance - total_contributions
    # Set the result string
    results.set(f"""
    The final amount after {t} years will be: ${final_balance:.2f}
    Interest earned: ${interest_earned:.2f}
    Total contributions (excluding initial deposit): ${total_contributions - P:.2f}
    Initial deposit: ${P:.2f}
    """)
    plot_details(balances, t)  # Call the plot_details function

# Create the main window
root = tk.Tk()

# Create and pack the widgets for initial amount
label_P = tk.Label(root, text="Enter the initial amount:")
label_P.pack()
entry_P = tk.Entry(root)
entry_P.pack()

# Create and pack the widgets for monthly deposit
label_d = tk.Label(root, text="Enter the monthly deposit:")
label_d.pack()
entry_d = tk.Entry(root)
entry_d.pack()

# Create and pack the widgets for APY
label_apy = tk.Label(root, text="Enter the annual percentage yield (in percentage):")
label_apy.pack()
entry_apy = tk.Entry(root)
entry_apy.pack()

# Create and pack the widgets for number of years
label_t = tk.Label(root, text="Enter the number of years:")
label_t.pack()
entry_t = tk.Entry(root)
entry_t.pack()

# Create and pack the calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

# Create and pack the results label
results = tk.StringVar()
results_label = tk.Label(root, textvariable=results)
results_label.pack()

# Start the Tkinter event loop
root.mainloop()
