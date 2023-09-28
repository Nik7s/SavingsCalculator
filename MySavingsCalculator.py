import tkinter as tk
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


def calculate_details(P, apy, t, d):
    monthly_apy = (1 + apy) ** (1 / 12) - 1
    balance = P
    balances, interests, contributions = [], [], []
    for month in range(int(t * 12)):
        interest = balance * monthly_apy
        balance += interest + d
        balances.append(balance)
        interests.append(interest)
        contributions.append(d if month > 0 else P + d)
    return balances, interests, contributions


def plot_details(balances, t):
    months = np.array([month for month in range(int(t * 12))]).reshape(-1, 1)
    balance_array = np.array(balances).reshape(-1, 1)

    model = LinearRegression()
    model.fit(months, balance_array)

    future_months = np.array([month for month in range(int(t * 12), int(t * 12) + 60)]).reshape(-1, 1)
    future_balance = model.predict(future_months)

    plt.figure(figsize=(10, 6))
    plt.plot(months, balances, label="Total Balance")
    plt.plot(future_months, future_balance, label="Predicted Total Balance", linestyle='dashed')
    plt.xlabel("Months")
    plt.ylabel("Amount ($)")
    plt.title("Investment Growth Over Time with Prediction")
    plt.legend()
    plt.show()


def calculate():
    P = float(entry_P.get())
    d = float(entry_d.get())
    apy = float(entry_apy.get()) / 100
    t = float(entry_t.get())
    balances, interests, contributions = calculate_details(P, apy, t, d)
    final_balance = balances[-1]
    total_contributions = sum(contributions)
    interest_earned = final_balance - total_contributions
    results.set(f"""
    The final amount after {t} years will be: ${final_balance:.2f}
    Interest earned: ${interest_earned:.2f}
    Total contributions (excluding initial deposit): ${total_contributions - P:.2f}
    Initial deposit: ${P:.2f}
    """)
    plot_details(balances, t)


root = tk.Tk()

label_P = tk.Label(root, text="Enter the initial amount:")
label_P.pack()
entry_P = tk.Entry(root)
entry_P.pack()

label_d = tk.Label(root, text="Enter the monthly deposit:")
label_d.pack()
entry_d = tk.Entry(root)
entry_d.pack()

label_apy = tk.Label(root, text="Enter the annual percentage yield (in percentage):")
label_apy.pack()
entry_apy = tk.Entry(root)
entry_apy.pack()

label_t = tk.Label(root, text="Enter the number of years:")
label_t.pack()
entry_t = tk.Entry(root)
entry_t.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

results = tk.StringVar()
results_label = tk.Label(root, textvariable=results)
results_label.pack()

root.mainloop()
