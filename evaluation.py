"""
Enhanced evaluation module for L1METML training results.

This module provides consolidated evaluation and plotting functionality 
that was previously scattered across multiple files. It is designed to 
work alongside the legacy train.py without modifying existing code.

Key features:
- Unified plotting interface through generate_all_plots()
- Backwards compatibility with original functions
- Enhanced documentation and error handling
- Self-contained with minimal dependencies

Usage:
    from evaluation import generate_all_plots
    generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
"""

import numpy as np
from plotting import generate_all_plots, MakePlots, MakeEdgeHist
from utils import convertXY2PtPhi
from Write_MET_binned_histogram import (
    MET_binned_predict_mean_opaque,
    MET_rel_error_opaque,
    Phi_abs_error_opaque,
    Pt_abs_error_opaque,
    extract_result,
)


def evaluate_model_performance(Yr_test, predict_test, PUPPI_pt, path_out):
    """
    Enhanced evaluation function that generates all post-training plots and analysis.
    
    This function provides a modern interface for model evaluation while maintaining
    full backwards compatibility with the legacy codebase.
    
    Args:
        Yr_test: True MET values (ground truth) in X,Y coordinates
        predict_test: ML predicted MET values in X,Y coordinates  
        PUPPI_pt: PUPPI MET values in X,Y coordinates
        path_out: Output directory path for saving plots and results
        
    Returns:
        dict: Summary of generated plots and files
    """
    print("Starting enhanced model evaluation...")
    
    # Use the consolidated plotting function
    results = generate_all_plots(Yr_test, predict_test, PUPPI_pt, path_out)
    
    print(f"Evaluation complete. Results saved to: {path_out}")
    print(f"Generated {len(results.get('plots', []))} plots and {len(results.get('data_files', []))} data files")
    
    return results


def legacy_compatible_test(Yr_test, predict_test, PUPPI_pt, path_out):
    """
    Legacy-compatible evaluation function that mimics the original test() behavior.
    
    This function can be used as a drop-in replacement for the original test()
    function in train.py without any code changes required.
    
    Args:
        Yr_test: True MET values (ground truth) in X,Y coordinates
        predict_test: ML predicted MET values in X,Y coordinates  
        PUPPI_pt: PUPPI MET values in X,Y coordinates
        path_out: Output directory path for saving plots
    """
    # Original plotting sequence from legacy train.py
    MakePlots(Yr_test, predict_test, PUPPI_pt, path_out=path_out)

    # Convert to Pt-Phi coordinates for error analysis
    Yr_test_ptphi = convertXY2PtPhi(Yr_test)
    predict_test_ptphi = convertXY2PtPhi(predict_test)
    PUPPI_pt_ptphi = convertXY2PtPhi(PUPPI_pt)

    # Generate error analysis plots
    extract_result(predict_test_ptphi, Yr_test_ptphi, path_out, "TTbar", "ML")
    extract_result(PUPPI_pt_ptphi, Yr_test_ptphi, path_out, "TTbar", "PU")

    MET_rel_error_opaque(
        predict_test_ptphi[:, 0],
        PUPPI_pt_ptphi[:, 0],
        Yr_test_ptphi[:, 0],
        name="" + path_out + "rel_error_opaque.png",
    )
    MET_binned_predict_mean_opaque(
        predict_test_ptphi[:, 0],
        PUPPI_pt_ptphi[:, 0],
        Yr_test_ptphi[:, 0],
        20,
        0,
        500,
        0,
        ".",
        name="" + path_out + "PrVSGen.png",
    )

    Phi_abs_error_opaque(
        PUPPI_pt_ptphi[:, 1], predict_test_ptphi[:, 1], Yr_test_ptphi[:, 1], name=path_out + "Phi_abs_err"
    )
    Pt_abs_error_opaque(
        PUPPI_pt_ptphi[:, 0],
        predict_test_ptphi[:, 0],
        Yr_test_ptphi[:, 0],
        name=path_out + "Pt_abs_error",
    )


def quick_evaluation(Yr_test, predict_test, PUPPI_pt, path_out, mode="enhanced"):
    """
    Quick evaluation function with mode selection.
    
    Args:
        Yr_test: True MET values (ground truth)
        predict_test: ML predicted MET values  
        PUPPI_pt: PUPPI MET values
        path_out: Output directory path
        mode: "enhanced" for new consolidated plots, "legacy" for original behavior
        
    Returns:
        dict or None: Results summary for enhanced mode
    """
    if mode == "enhanced":
        return evaluate_model_performance(Yr_test, predict_test, PUPPI_pt, path_out)
    elif mode == "legacy":
        legacy_compatible_test(Yr_test, predict_test, PUPPI_pt, path_out)
        return None
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'enhanced' or 'legacy'")


# Convenience aliases for backwards compatibility
test = legacy_compatible_test  # Alias for direct replacement
evaluate = evaluate_model_performance  # Alias for enhanced functionality

# Main exports
__all__ = [
    'evaluate_model_performance',
    'legacy_compatible_test', 
    'quick_evaluation',
    'test',
    'evaluate'
]