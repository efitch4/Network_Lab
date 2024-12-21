import tkinter as tk
import tkinter
print(tkinter.Tcl().eval('info library'))



class PaycheckCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Paycheck Calculator")

        # Labels and entry fields for user input
        self.label_hourly_wage = tk.Label(master, text="Hourly Wage:")
        self.label_hourly_wage.grid(row=0, column=0, sticky="w")
        self.entry_hourly_wage = tk.Entry(master)
        self.entry_hourly_wage.grid(row=0, column=1)

        self.label_hours_per_pay_period = tk.Label(master, text="Hours per Pay Period:")
        self.label_hours_per_pay_period.grid(row=1, column=0, sticky="w")
        self.entry_hours_per_pay_period = tk.Entry(master)
        self.entry_hours_per_pay_period.grid(row=1, column=1)

        self.label_sui_rate = tk.Label(master, text="SUI Rate (%):")
        self.label_sui_rate.grid(row=2, column=0, sticky="w")
        self.entry_sui_rate = tk.Entry(master)
        self.entry_sui_rate.grid(row=2, column=1)

        self.label_sdi_rate = tk.Label(master, text="SDI Rate (%):")
        self.label_sdi_rate.grid(row=3, column=0, sticky="w")
        self.entry_sdi_rate = tk.Entry(master)
        self.entry_sdi_rate.grid(row=3, column=1)

        self.label_sui_wage_base = tk.Label(master, text="SUI Wage Base:")
        self.label_sui_wage_base.grid(row=4, column=0, sticky="w")
        self.entry_sui_wage_base = tk.Entry(master)
        self.entry_sui_wage_base.grid(row=4, column=1)

        self.label_sdi_wage_limit = tk.Label(master, text="SDI Wage Limit:")
        self.label_sdi_wage_limit.grid(row=5, column=0, sticky="w")
        self.entry_sdi_wage_limit = tk.Entry(master)
        self.entry_sdi_wage_limit.grid(row=5, column=1)

        # Button to calculate paycheck
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=6, columnspan=2)

        # Label to display result
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=7, columnspan=2)

    def calculate(self):
        try:
            hourly_wage = float(self.entry_hourly_wage.get())
            hours_per_pay_period = float(self.entry_hours_per_pay_period.get())
            sui_rate = float(self.entry_sui_rate.get()) / 100
            sdi_rate = float(self.entry_sdi_rate.get()) / 100
            sui_wage_base = float(self.entry_sui_wage_base.get())
            sdi_wage_limit = float(self.entry_sdi_wage_limit.get())

            # Perform paycheck calculation
            gross_paycheck = hourly_wage * hours_per_pay_period

            # Calculate SUI and SDI deductions
            sui_deduction = min(gross_paycheck * sui_rate, sui_wage_base)
            sdi_deduction = min(gross_paycheck * sdi_rate, sdi_wage_limit)

            total_deductions = sui_deduction + sdi_deduction

            net_pay = gross_paycheck - total_deductions

            # Display the result
            self.result_label.config(text=f"Net Pay: ${net_pay:.2f}")
        except ValueError:
            self.result_label.config(text="Please enter valid numeric values.")

def main():
    root = tk.Tk()
    app = PaycheckCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
