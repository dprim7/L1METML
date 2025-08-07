#!/usr/bin/env python3
"""
Test script for consolidated plotting functionality.

This script tests the new plotting.py module to ensure all plotting
functions work correctly and generate the expected outputs.
"""

import numpy as np
import os
import tempfile
import sys
sys.path.append('/home/runner/work/L1METML/L1METML')

def test_plotting_module():
    """Test the consolidated plotting module with synthetic data."""
    print("Testing consolidated plotting module...")
    
    # Create synthetic test data
    n_events = 1000
    np.random.seed(42)  # For reproducible results
    
    # Generate synthetic MET data (X, Y coordinates)
    true_met_x = np.random.normal(0, 50, n_events)
    true_met_y = np.random.normal(0, 50, n_events)
    Yr_test = np.column_stack([true_met_x, true_met_y])
    
    # ML predictions (with some bias and resolution effects)
    ml_met_x = true_met_x + np.random.normal(0, 10, n_events)
    ml_met_y = true_met_y + np.random.normal(0, 10, n_events)
    predict_test = np.column_stack([ml_met_x, ml_met_y])
    
    # PUPPI predictions (different bias/resolution)
    puppi_met_x = true_met_x + np.random.normal(5, 15, n_events)
    puppi_met_y = true_met_y + np.random.normal(-3, 12, n_events)
    PUPPI_pt = np.column_stack([puppi_met_x, puppi_met_y])
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = temp_dir + "/"
        print(f"Using temporary output directory: {output_path}")
        
        try:
            # Import and test the plotting module
            from plotting import generate_all_plots
            
            # Generate all plots
            print("Generating all plots...")
            generate_all_plots(Yr_test, predict_test, PUPPI_pt, output_path)
            
            # Check that expected files were created
            expected_files = [
                "MET_x.png",
                "MET_y.png", 
                "MET_pt.png",
                "MET_response.png",
                "XY_resolution_plots.png",
                "pt_resolution_plots.png",
                "rel_error_opaque.png",
                "PrVSGen.png",
                "Phi_abs_err.png",
                "Pt_abs_error.png",
                "TTbar_feature_array_MLMET.npy",
                "TTbar_target_array_MLMET.npy",
                "TTbar_feature_array_PUMET.npy", 
                "TTbar_target_array_PUMET.npy"
            ]
            
            created_files = os.listdir(output_path)
            print(f"Created {len(created_files)} files:")
            for f in sorted(created_files):
                print(f"  - {f}")
            
            # Check if all expected files were created
            missing_files = []
            for expected_file in expected_files:
                if expected_file not in created_files:
                    missing_files.append(expected_file)
            
            if missing_files:
                print(f"❌ Missing expected files: {missing_files}")
                return False
            else:
                print("✅ All expected files were created successfully!")
                
            # Test individual plotting functions
            print("\nTesting individual plotting functions...")
            
            from plotting import Make1DHists, MakeEdgeHist
            
            # Test 1D histogram function
            Make1DHists(
                Yr_test[:, 0], predict_test[:, 0], PUPPI_pt[:, 0],
                -200, 200, 20, False, "Test MET X [GeV]", "Events",
                f"{output_path}test_1d_hist.png"
            )
            
            # Test edge histogram function  
            edge_features = np.random.normal(0, 1, 500)
            MakeEdgeHist(
                edge_features, "Test Edge Feature", 
                f"{output_path}test_edge_hist.png"
            )
            
            # Verify these additional files were created
            if os.path.exists(f"{output_path}test_1d_hist.png"):
                print("✅ 1D histogram test passed")
            else:
                print("❌ 1D histogram test failed")
                return False
                
            if os.path.exists(f"{output_path}test_edge_hist.png"):
                print("✅ Edge histogram test passed")
            else:
                print("❌ Edge histogram test failed")
                return False
                
            print("\n✅ All plotting tests passed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during plotting test: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_backwards_compatibility():
    """Test that the original functions still work for backwards compatibility."""
    print("\nTesting backwards compatibility...")
    
    try:
        # Test that original imports still work
        from utils import convertXY2PtPhi
        print("✅ utils.convertXY2PtPhi import works")
        
        # Test conversion function
        test_xy = np.array([[100, 50], [0, 100], [-50, -50]])
        test_ptphi = convertXY2PtPhi(test_xy)
        print(f"✅ convertXY2PtPhi function works: {test_ptphi.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backwards compatibility test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("L1METML Consolidated Plotting Test Suite")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_plotting_module()
    test2_passed = test_backwards_compatibility()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Plotting Module Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Backwards Compatibility: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The plotting consolidation is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the implementation.")
        sys.exit(1)