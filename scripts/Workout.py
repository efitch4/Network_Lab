import tkinter as tk
from tkinter import filedialog, messagebox
import random
import csv
import os

class WorkoutPlanner:
    def __init__(self, master):
        self.master = master
        master.title("Workout Planner")

        self.label_title = tk.Label(master, text="Generate and Export Workout Plan")
        self.label_title.grid(row=0, column=0, columnspan=8, padx=10, pady=10)

        self.generate_button = tk.Button(master, text="Generate and Export Plan", command=self.generate_and_export_plan)
        self.generate_button.grid(row=1, column=0, columnspan=8, padx=10, pady=5)

    def generate_and_export_plan(self):
        weekdays = ["Monday", "Tuesday", "Thursday", "Friday"]
        workouts = ["Legs", "Back", "Shoulders", "Chest"]

        plan = [["Week ending"] + weekdays]
        for month in range(1, 13):
            for week in range(1, 5):
                week_ending = f"{month}/{week * 7 - 1}/2024"
                weekly_plan = [week_ending]
                used_workouts = set()

                for day in range(4):
                    workout = self.get_random_workout(used_workouts, workouts)
                    used_workouts.add(workout)
                    weekly_plan.append(workout)

                plan.append(weekly_plan)

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(plan)

            messagebox.showinfo("Export Successful", "Workout plan exported successfully")
        else:
            messagebox.showwarning("Export Cancelled", "Export cancelled by user")

    def get_random_workout(self, used_workouts, workouts):
        workout = random.choice(workouts)
        while workout in used_workouts:
            workout = random.choice(workouts)
        return workout

root = tk.Tk()
app = WorkoutPlanner(root)
root.mainloop()


