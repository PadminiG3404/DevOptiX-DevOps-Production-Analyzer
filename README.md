# 🚀 DevOptiX – DevOps Productivity Analyzer

DevOptiX is a modular and intelligent system for analyzing software development and deployment workflows to identify productivity bottlenecks and suggest data-driven improvements. It supports core DevOps and DORA metrics, detects bottlenecks, recommends improvements, visualizes trends, and integrates DORA metrics for high-performance insights. It is built to be extended with real-time integrations and ML-powered insights.

---

## 📌 Features

- 🔍 Workflow bottleneck detection (PR reviews, builds, deployments, etc.)
- 📈 DORA Metrics computation:
  - Deployment Frequency
  - Lead Time for Changes
  - Change Failure Rate (simulated)
  - Mean Time to Recovery (simulated)
- 🤖 Recommendation Engine for team/process improvements
- 📊 Visual analytics (histograms, bottleneck trends)
- 🧪 Synthetic data generation for demo/testing
- 📦 Modular Python architecture
- ✅ Ready for real-time tool integration (GitHub, Jenkins, etc.)
- 🖥️ Streamlit UI (planned)

---

## 📁 Folder Structure

```
DevOptiX/
│
├── generate_data.py # Synthetic task generator
├── compute_metrics.py # Core metrics computation
├── bottleneck_detection.py # Detects process bottlenecks
├── recommendation_engine.py # Task + DORA-based recommendations
├── trend_analysis.py # Trend regression for time-based insights
├── ml_anomaly_detector.py # Machine learning-based anomaly detection
├── visualize.py # Multiple plots and visual analytics
├── export.py # Exports data to CSV/JSON/TXT
├── main.py # Entry point for the full pipeline
└── outputs/ # All generated metrics, plots, and insights
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DevOptiX.git
cd DevOptiX
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Running the tool
```bash
python main.py
```

---

## 📊 Output Artifacts

All outputs are saved in the `outputs/` directory:

### 🔢 Metrics
- `metrics.csv`: All computed metrics per task  
- `dora_metrics.txt`: Overall DORA metrics summary  

### 📦 Bottlenecks & Recommendations
- `bottlenecks.json`: Tasks with bottleneck stages  
- `task_recommendations.json` / `.txt`: Optimization suggestions  
- `dora_recommendations.json` / `.txt`: DORA-based team guidance  

### 🧠 Analysis & Trends
- `trend_regressions.json`: Stage trends over time  
- `anomalies.json`: Detected anomalies in performance  

### 📈 Visual Reports
- `pr_review_time.png`: PR review time distribution  
- `bottleneck_counts.png`: Bottleneck frequency by stage  
- `dora_metrics.png`: Bar chart of DORA metrics  
- `bottlenecks_by_stage_and_team.png`: Heatmap of delays by team/stage  
- `avg_pr_review_time_by_team.png`: Average PR review time per team  
- `lead_time_trend.png`: Sprint-based lead time changes  
- `developer_stage_heatmap.png`: Developer-stage bottleneck heatmap  

---

### 📌 Sample Output

```yaml
🔧 Generating synthetic data...
📊 Computing metrics...
🔍 Detecting bottlenecks...
💡 Generating task-based recommendations...
📈 Computing DORA metrics...
💡 Generating DORA-based recommendations...
📉 Running trend analysis...
🤖 Running anomaly detection...
📤 Exporting outputs...
[EXPORT] Metrics exported to outputs\metrics.csv
[EXPORT] JSON data exported to outputs\bottlenecks.json
[EXPORT] JSON data exported to outputs\task_recommendations.json
[EXPORT] JSON data exported to outputs\dora_recommendations.json
[EXPORT] JSON data exported to outputs\trend_regressions.json
[EXPORT] JSON data exported to outputs\anomalies.json
📊 Plotting insights...
[VISUAL] Saved plot to pr_review_time.png
[VISUAL] Saved bottleneck plot to outputs\bottleneck_counts.png
[VISUAL] Saved DORA metrics plot to outputs\dora_metrics.png
[VISUAL] Saved plot to outputs\bottlenecks_by_stage_and_team.png
[VISUAL] Saved avg stage durations to outputs\avg_pr_review_time_by_team.png
[VISUAL] Saved DORA trends to outputs\lead_time_trend.png
[VISUAL] Saved heatmap to outputs\developer_stage_heatmap.png
✅ Done. Check the 'outputs/' folder for results.

📈 DORA Metrics Summary:
   deployment_frequency_per_day: 8.33
   average_lead_time_hours: 29.0
   change_failure_rate_percent: 23.0
   mean_time_to_restore_hours: 1.59

```

---

## 🛠️ Customization

You can configure or extend:

- **Team structure and number of developers**  
  Edit: `generate_synthetic_tasks()`

- **Stages to track** (e.g., add QA or staging phases)

- **Anomaly logic**  
  Edit: `ml_anomaly_detector.py`

- **Trend depth and sprint granularity**  
  Edit: `trend_analysis.py`

---

## 🧭 Roadmap

- [ ] Real-time ingestion support (from CI/CD logs, GitHub APIs)  
- [ ] Web dashboard with interactive visualizations  
- [ ] Persistent database support for longitudinal studies  
- [ ] Integration with JIRA/GitHub metrics APIs  
- [ ] Role-based recommendations (Dev vs Ops vs Manager)

---

## 👩‍💻 Contributing

Contributions are welcome!  
Feel free to open issues or submit PRs for enhancements, bug fixes, or documentation.

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for full terms.

---

## 🙌 Acknowledgements

Inspired by DORA metrics and DevOps Research & Assessment reports.  
Built for teams aiming to improve visibility and reduce delivery friction.

---

## 💡 Optional Enhancements

Let me know if you'd like:

- A `requirements.txt` auto-generated from your environment  
- Badges (build status, license, Python version, etc.)  
- To convert this into a `docs/` site with Markdown pages or Sphinx


