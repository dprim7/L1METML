# L1METML Plotting Documentation

## Overview

The L1METML project previously had plotting functionality distributed across multiple files, making it difficult to maintain and understand. This document describes the consolidated plotting system and maps where each plot type was originally located.

## Consolidated Plotting Module

All post-training plotting functionality has been consolidated into `plotting.py`, which provides a unified interface for generating analysis plots.

### Main Entry Point

```python
from plotting import generate_all_plots

# Generate all post-training plots
generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
```

## Original Distribution of Plotting Functions

### 1. train.py
**Original Functions:**
- `test()` (lines 529-567): Orchestrated all post-training plotting
- `MakeEdgeHist()` (lines 417-433): Edge feature histograms for graph networks

**Current Status:**
- `test()` function simplified to call `generate_all_plots()`
- `MakeEdgeHist()` moved to `plotting.py`

### 2. utils.py  
**Original Functions:**
- `MakePlots()` (lines 68-575): Main plotting function generating:
  - Resolution plots (X, Y, Pt, Phi)
  - Response plots showing ML vs PUPPI performance
  - Error analysis with statistical significance
  - Multi-panel comparison plots
- `Make1DHists()` (lines 577-627): 1D histogram distributions

**Current Status:**
- Both functions moved to `plotting.py` with same functionality
- Original functions remain in `utils.py` for backwards compatibility (deprecated)

### 3. Write_MET_binned_histogram.py
**Original Functions:**
- `MET_rel_error_opaque()`: Relative error comparison plots
- `MET_binned_predict_mean_opaque()`: Binned prediction vs truth plots  
- `Phi_abs_error_opaque()`: Phi absolute error comparison
- `Pt_abs_error_opaque()`: Pt absolute error comparison
- `extract_result()`: Save prediction arrays for analysis

**Current Status:**
- Error plotting functions moved to `plotting.py`
- Original functions remain for standalone use
- `extract_result()` copied to both locations

### 4. rate_test.py
**Functions (Still Standalone):**
- ROC curve generation
- Trigger rate analysis
- Turn-on curve plotting
- Signal vs background efficiency plots

**Current Status:**
- Remains separate as it's a standalone analysis tool
- Not part of the training pipeline plotting

### 5. epoch_all.py
**Functions (Still Standalone):**
- Loss vs epoch plotting from training logs

**Current Status:**
- Remains separate as it's a standalone analysis tool
- Interactive tool for examining training history

## Generated Plots

The consolidated plotting system generates the following plots in the output directory:

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

### Basic Usage (Recommended)
```python
from plotting import generate_all_plots

# After training completes
generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
```

### Individual Plot Generation
```python
from plotting import MakePlots, make_error_plots, Make1DHists

# Generate only resolution plots
MakePlots(Yr_test, predict_test, PUPPI_pt, path_out)

# Generate only error analysis plots  
make_error_plots(predict_test_ptphi, PUPPI_pt_ptphi, Yr_test_ptphi, path_out)

# Generate only 1D histograms
Make1DHists(truth, ML, PUPPI, 0, 400, 40, False, "MET [GeV]", "A.U.", "output.png")
```

### Edge Feature Plots (for Graph Networks)
```python
from plotting import MakeEdgeHist

# Generate edge feature histogram
MakeEdgeHist(edge_features, "Edge Feature", "edge_hist.png")
```

## Migration Guide

### For Existing Code
- Replace calls to `utils.MakePlots()` with `plotting.generate_all_plots()`
- Replace calls to `train.MakeEdgeHist()` with `plotting.MakeEdgeHist()`
- The `test()` function in `train.py` now automatically uses consolidated plotting

### Backwards Compatibility
- Original functions remain available in their original locations
- Existing scripts will continue to work without modification
- New development should use the consolidated `plotting.py` module

## Benefits of Consolidation

1. **Maintainability**: All plotting code in one location
2. **Consistency**: Unified styling and error handling
3. **Documentation**: Clear function signatures and docstrings
4. **Modularity**: Easy to add new plot types or modify existing ones
5. **Testing**: Easier to write comprehensive tests for plotting functionality

## Future Enhancements

- Add configuration options for plot styling
- Implement plot type selection (generate only specific plots)
- Add support for different output formats (PDF, SVG, etc.)
- Integration with tensorboard logging
- Automated plot comparison between training runs