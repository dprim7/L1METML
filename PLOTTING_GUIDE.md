# L1METML Plotting Documentation

## Overview

The L1METML project provides enhanced plotting functionality through a new `evaluation.py` module that consolidates distributed plotting functions while keeping all legacy code completely untouched.

## Enhanced Evaluation Module

The new `evaluation.py` module provides:
- Consolidated plotting interface through `plotting.py` backend
- Full backwards compatibility with legacy code
- Enhanced documentation and error handling
- Multiple evaluation modes

### Recommended Usage

```python
from evaluation import evaluate_model_performance

# Enhanced evaluation with consolidated plots
results = evaluate_model_performance(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Legacy Compatibility

```python
from evaluation import legacy_compatible_test

# Drop-in replacement for original test() function
legacy_compatible_test(Yr_test, predict_test, PUPPI_pt, path_out)
```

## Original Distribution of Plotting Functions (Preserved)

### 1. train.py (UNCHANGED)
**Functions (preserved as-is):**
- `test()` (lines 529-567): Original orchestration of post-training plotting
- `MakeEdgeHist()` (lines 417-433): Edge feature histograms for graph networks

**Status:** All legacy code remains untouched and fully functional

### 2. utils.py (UNCHANGED)
**Functions (preserved as-is):**
- `MakePlots()` (lines 68-575): Main plotting function generating:
  - Resolution plots (X, Y, Pt, Phi)
  - Response plots showing ML vs PUPPI performance
  - Error analysis with statistical significance
  - Multi-panel comparison plots
- `Make1DHists()` (lines 577-627): 1D histogram distributions

**Status:** All original functions remain in utils.py and are fully functional

### 3. Write_MET_binned_histogram.py (UNCHANGED)
**Functions (preserved as-is):**
- `MET_rel_error_opaque()`: Relative error comparison plots
- `MET_binned_predict_mean_opaque()`: Binned prediction vs truth plots  
- `Phi_abs_error_opaque()`: Phi absolute error comparison
- `Pt_abs_error_opaque()`: Pt absolute error comparison
- `extract_result()`: Save prediction arrays for analysis

**Status:** All original functions remain in Write_MET_binned_histogram.py and are fully functional

### 4. rate_test.py (UNCHANGED)
**Functions (preserved as-is):**
- ROC curve generation
- Trigger rate analysis
- Turn-on curve plotting
- Signal vs background efficiency plots

**Status:** Remains separate as standalone analysis tool

### 5. epoch_all.py (UNCHANGED)
**Functions (preserved as-is):**
- Loss vs epoch plotting from training logs

**Status:** Remains separate as standalone analysis tool

## Generated Plots

The evaluation system generates the following plots in the output directory:

### Distribution Plots
- `MET_x.png`: MET X-component distribution
- `MET_y.png`: MET Y-component distribution  
- `MET_pt.png`: MET magnitude distribution

### Performance Analysis
- `MET_response.png`: Response plots (prediction/truth ratios)
- `XY_resolution_plots.png`: Multi-panel X,Y resolution analysis
- `pt_resolution_plots.png`: Multi-panel Pt,Phi resolution analysis

### Error Analysis
- `rel_error_opaque.png`: Relative error comparison (ML vs PUPPI)
- `PrVSGen.png`: Binned prediction vs truth scatter plot
- `Phi_abs_err.png`: Phi absolute error comparison
- `Pt_abs_error.png`: Pt absolute error comparison

### Data Arrays
- `TTbar_feature_array_MLMET.npy`: ML predictions
- `TTbar_target_array_MLMET.npy`: Ground truth for ML
- `TTbar_feature_array_PUMET.npy`: PUPPI predictions  
- `TTbar_target_array_PUMET.npy`: Ground truth for PUPPI

## Usage Examples

### Enhanced Evaluation (Recommended)
```python
from evaluation import evaluate_model_performance

# After training completes - enhanced evaluation
results = evaluate_model_performance(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Legacy Compatible Evaluation
```python
from evaluation import legacy_compatible_test

# Drop-in replacement for original test() function
legacy_compatible_test(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Direct Plotting Module Usage
```python
from plotting import generate_all_plots

# Direct access to consolidated plotting functions
generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Original Functions (All Still Available)
```python
# Original functions remain fully functional
from utils import MakePlots
from Write_MET_binned_histogram import MET_rel_error_opaque

# Generate only resolution plots using original function
MakePlots(Yr_test, predict_test, PUPPI_pt, path_out)

# Generate error plots using original function
MET_rel_error_opaque(predict_test_ptphi[:, 0], PUPPI_pt_ptphi[:, 0], 
                     Yr_test_ptphi[:, 0], name=path_out + "rel_error.png")
```

## Migration Options

### Option 1: Use Enhanced Evaluation (Recommended)
```python
# Replace train.py test() calls with:
from evaluation import evaluate_model_performance
results = evaluate_model_performance(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Option 2: Keep Legacy Code Unchanged
```python
# Existing code in train.py continues to work exactly as before
# No changes needed - all original functions preserved
```

### Option 3: Direct Plotting Module
```python
# For advanced users who want consolidated plotting without evaluation wrapper
from plotting import generate_all_plots
generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
```

## Benefits of New Approach

1. **No Breaking Changes**: All legacy code remains untouched and functional
2. **Enhanced Functionality**: New evaluation module provides better error handling and documentation  
3. **Flexibility**: Choose between enhanced evaluation or original behavior
4. **Maintainability**: Consolidated plotting code is easier to maintain
5. **Future-Ready**: Foundation for additional evaluation features