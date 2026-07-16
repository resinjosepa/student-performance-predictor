import matplotlib.pyplot as plt
import pandas as pd

features = [
    "G2",
    "Absences",
    "G1",
    "Age",
    "Free Time",
    "School",
    "Health",
    "Family Relation",
    "Travel Time",
    "Dalc"
]

importance = [
    0.855130,
    0.036549,
    0.016583,
    0.010211,
    0.007559,
    0.007036,
    0.006641,
    0.006566,
    0.005636,
    0.005033
]

plt.figure(figsize=(10,6))

plt.barh(features, importance)

plt.title("Top 10 Feature Importance")

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig("static/charts/feature_importance.png")

plt.close()

print("Chart created successfully!")

# -----------------------------
# Grade Distribution
# -----------------------------

df = pd.read_csv("student-por.csv")

plt.figure(figsize=(8,5))

plt.hist(df["G3"], bins=20, edgecolor="black")

plt.title("Distribution of Final Grades")

plt.xlabel("Final Grade (G3)")

plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig("static/charts/grade_distribution.png")

plt.close()

print("All charts created successfully!")