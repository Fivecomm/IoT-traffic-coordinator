# INSIGNIA: IoT Traffic Coordinator

A Python-based network resource allocation simulator that optimizes User Equipment (UE) connection density while minimizing collisions using intelligent allocation algorithms.

**Current Version:** v1.0

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Configuration](#configuration)
  - [Batch Processing](#batch-processing)
- [Algorithm Details](#algorithm-details)
- [Output](#output)
- [Examples](#examples)
- [License](#license)
- [Authors & Contact](#authors--contact)
- [Citation](#citation)

---

## Overview

INSIGNIA is a simulator designed for analyzing and optimizing network resource allocation in IoT and cellular networks. It compares a **random allocation algorithm** against an **intelligent allocation algorithm** that minimizes resource collisions and optimizes network load distribution.

### Use Cases
- Network capacity planning for IoT deployments
- Performance analysis of resource allocation strategies
- Connection density optimization
- Network load balancing simulation
- Research in cellular network optimization

---

## Key Features

✅ **Two Allocation Strategies**
- Random allocation (baseline for comparison)
- Intelligent collision-minimizing allocation

✅ **Flexible Configuration**
- Multiple predefined UE profiles (WIOTHUB, WIOTPRESS, WIOTRAD)
- Custom UE type definitions
- Configurable connection time ranges and frequencies
- Scalable number of UEs (from 2,000 to 10,000+)

✅ **Comprehensive Analysis**
- Real-time performance metrics
- Statistical analysis (max, percentile, distribution)
- Load reduction percentage calculation
- Visualization of results

✅ **Data Persistence**
- JSON-based result storage
- Batch processing capabilities
- Easy data export for external analysis

✅ **Visualization**
- Network resource utilization plots
- Load comparison graphs
- Saturation analysis
- Multi-format output (PNG, JSON)

---

## Requirements

- **Python:** 3.8 or higher
- **OS:** Windows, macOS, or Linux
- **Dependencies:** See [requirements.txt](requirements.txt)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Fivecomm/IoT-traffic-coordinator.git
cd IoT-traffic-coordinator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Project Structure

```
INSIGNIA/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── LICENSE                        # License file
├── .gitignore                     # Git ignore rules
│
├── INSIGNIA.py                    # Main entry point
├── INSIGNIA_algorithm.py          # Allocation algorithms (random & optimized)
├── INSIGNIA_objects.py            # Core classes (UE, GroupUE, Grid)
├── INSIGNIA_functions.py          # Utility functions (I/O, plotting, analysis)
├── Configurations_UEs.py          # Predefined UE configurations
│
├── simulation_results/            # Output directory for results
│   └── *.json                     # Simulation result files
│
├── INSIGNIA results/              # INSIGNIA results
│   ├── *.json                     # Archived simulation data
│   ├── raw_sims/                  # Raw simulation outputs
│   └── figuras/                   # Generated figures for INSIGNIA project
│
├── batch.txt                      # Batch processing file list
└── plot_json.py                   # JSON data visualization tool
```

---

## Usage

### Basic Usage

Run the simulator with default configuration:

```bash
python INSIGNIA.py
```

When prompted, press Enter to simulate new data or provide a JSON filename to load existing results:
```
Filename to load (enter to simulate a new one) / 'q' for exiting:
```

### Configuration

#### Predefined Configurations

Edit the configuration parameters in `INSIGNIA.py`:

```python
base_ues = False             # Include background UEs from statistics
plot_1 = True                # Generate comparison plots
plot_2 = True                # Generate detailed analysis plots
print_values = True          # Print statistics to console
save_json_in_file = True     # Save results to JSON
ues = [20000, 25000, 30000]  # UEs to simulate (multiple for batch simulating)
load_from_file = ""          # Leave empty to simulate, or enter filename
```

#### Custom UE Profiles

Define custom UE types in `Configurations_UEs.py`:

```python
my_ue = UE(
    name="CUSTOM_UE",
    connections_per_day=1,           # How many times per day the UE connects
    minutes_connected=10,             # Duration of each connection in minutes
    time_ranges=[(8.00, 18.00)]      # Time windows when UE can connect (HH.MM format)
)

my_group = GroupUE(
    name="Custom Group",
    number_of_ues=1000,              # Number of UEs in this group
    ue_parameters=my_ue
)
```

### Batch Processing

Process multiple simulation results from `batch.txt`:

```python
# In INSIGNIA.py, uncomment batch processing section
filename = "batch.txt"
batches = read_batch_from_file()
process_batch(batches, ues)
```

Each line in `batch.txt` should contain a JSON filename:
```
2000UEs_2024-10-15.09.40.02.755900.json
2500UEs_2024-10-15 09.40.06.294224.json
3000UEs_2024-10-15 09.40.10.636801.json
```

---

## Algorithm Details

### Random Allocation Algorithm
- Randomly selects connection times within allowed time ranges
- Baseline for performance comparison
- Serves as reference point for optimization evaluation

### Intelligent Allocation Algorithm
1. **Validation:** Verifies input types and parameters
2. **Expansion:** Converts GroupUE objects into individual UEs
3. **Prioritization:** Sorts UEs by restrictiveness (fewer time ranges = higher priority)
4. **Placement:** Attempts collision-free placement
5. **Fallback:** Uses min-collision strategy when collision-free placement is impossible

### Collision Minimization Strategy
- Evaluates all possible placement positions
- Counts collisions for each position
- Selects position with minimum collisions
- Reduces peak resource utilization by ~20-40% depending on configuration

---

## Output

### Console Output

```
RANDOM
Max: 45
98%: 42
95: 39
90%: 35
70%: 28
50%: 15

ALGORITHM
Max: 28
98%: 26
95%: 24
90%: 22
70%: 18
50%: 12

LOAD REDUCTION (RANDOM -> ALGORITHM)
Max: 37.78%
98%: 38.1%
...
```

### Generated Files

- **JSON Results:** `simulation_results/*.json`
  - Contains resource allocation data for both algorithms
  - Timestamped for easy tracking
  
- **Plots:** `*.png`
  - Comparison visualizations
  - Resource utilization graphs
  - Saturation analysis charts

- **Graph Data:** `graph*.json`
  - Exportable data for external visualization tools
  - Multiple plot format support

---

## Examples

### Example 1: Single Simulation with Default Config

```bash
python INSIGNIA.py
# Press Enter when prompted to simulate new data
# Results saved to simulation_results/ directory
```

### Example 2: Load and Analyze Previous Results

```bash
python INSIGNIA.py
# Enter: 2000UEs_2024-10-15.09.40.02.755900.json
# Loads and analyzes existing simulation
```

### Example 3: Custom Configuration with 5000 UEs

Edit `INSIGNIA.py`:
```python
ues = [5000]
load_from_file = ""
```

Then run:
```bash
python INSIGNIA.py
```

### Example 4: Batch Processing Multiple Simulations

Ensure `batch.txt` contains filenames, then in `INSIGNIA.py`:
```python
# Uncomment batch processing section at the end
ues = range(2000, 10000, 500)
batches = read_batch_from_file()
process_batch(batches, ues)
```

---

## UE Types and Profiles used for INSIGNIA project

### WIOTHUB
- **Connections/day:** 1
- **Duration:** 5-15 minutes
- **Time ranges:** Early morning (0:00-6:30) and late night (22:00-23:59)
- **Use case:** Hub devices with scheduled synchronization

### WIOTPRESS
- **Connections/day:** 1
- **Duration:** 2 minutes
- **Time ranges:** Any time (24/7)
- **Use case:** Press sensors with real-time reporting

### WIOTRAD
- **Connections/day:** 1
- **Duration:** 5 minutes
- **Time ranges:** Daytime (10:00-18:00 or 8:00-22:00)
- **Use case:** Radiation sensors with operational windows

---

## Configuration Presets

### Config 1: Original Mix
- 1000 WIOTHUBs (5 min each, 0:00-6:30 & 22:00-23:59)
- 1400 WIOTPRESSs (2 min each, 24/7)
- 600 WIOTRADs (5 min each, 10:00-18:00)

### Config 2: Extended Hub Duration
- 1000 WIOTHUBs (15 min each, 0:00-6:30 & 22:00-23:59)
- 1400 WIOTPRESSs (2 min each, 24/7)
- 600 WIOTRADs (5 min each, 10:00-18:00)

### Config 3: Extended Radiation Window
- 1000 WIOTHUBs (5 min each, 0:00-6:30 & 22:00-23:59)
- 1400 WIOTPRESSs (2 min each, 24/7)
- 600 WIOTRADs (5 min each, 8:00-22:00)

### Config 4: 24/7 All Types
- 1000 WIOTHUBs (15 min each, 24/7)
- 1400 WIOTPRESSs (2 min each, 24/7)
- 600 WIOTRADs (5 min each, 24/7)

---

## Performance Metrics

The simulator reports the following metrics for both algorithms:

| Metric | Description |
|--------|-------------|
| **Max** | Maximum resources used in any single time slot |
| **98%** | 98th percentile of resource usage |
| **95%** | 95th percentile of resource usage |
| **90%** | 90th percentile of resource usage |
| **70%** | 70th percentile of resource usage |
| **50%** | 50th percentile (median) of resource usage |
| **Load Reduction %** | Improvement percentage (Random → Algorithm) |

---

## Troubleshooting

### Issue: "File not found" error when loading JSON
**Solution:** Ensure the JSON file exists in `simulation_results/` directory. Use exact filename or press Enter to simulate new data.

### Issue: Plots not displaying
**Solution:** 
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that your system supports graphical output
- Consider saving plots to files instead

### Issue: Out of memory with large simulations
**Solution:**
- Reduce number of UEs
- Process smaller batches
- Increase available system RAM

### Issue: Inconsistent results between runs
**Solution:** This is expected behavior for the random algorithm. Use the same seed or load saved JSON results for reproducibility.

---

## Performance Considerations

- **Simulation Time:** Varies with UE count
  - 2,000 UEs: ~1-2 seconds
  - 5,000 UEs: ~3-5 seconds
  - 10,000 UEs: ~10-15 seconds

- **Memory Usage:** Approximately 50-100 MB for typical simulations

- **Result File Size:** ~100-500 KB per simulation JSON

---

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Use meaningful variable names

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Citation

If you use INSIGNIA in your research, please cite:

```bibtex
@software{insignia2025,
  title={INSIGNIA: IoT-traffic-coordinator},
  author={Cantero, Miguel},
  year={2025},
  url={https://github.com/Fivecomm/IoT-traffic-coordinator}
}
```

---

## Authors & contact

- **Miguel Cantero** - [miguel.cantero@fivecomm.eu](mailto:miguel.cantero@fivecomm.eu)

### Organization
**Fivecomm** - Research and Development  
© 2025 Fivecomm. All rights reserved.

---

## Acknowledgments

- FIVECOMM Research Team
- Contributors and testers
- Open-source community (NumPy, Matplotlib)
