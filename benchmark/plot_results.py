import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

plt.figure(figsize=(8, 5))
plt.bar(df["test"], df["throughput_ops_sec"])
plt.title("Throughput by scenario")
plt.xlabel("Scenario")
plt.ylabel("Operations per second")
plt.tight_layout()
plt.savefig("throughput.png")

plt.figure(figsize=(8, 5))
plt.bar(df["test"], df["p95_latency_ms"])
plt.title("P95 latency by scenario")
plt.xlabel("Scenario")
plt.ylabel("Latency (ms)")
plt.tight_layout()
plt.savefig("p95_latency.png")