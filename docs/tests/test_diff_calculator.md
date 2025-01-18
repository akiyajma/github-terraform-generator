Module tests.test_diff_calculator
=================================

Functions
---------

`test_calculate_diff()`
:   Test the calculate_diff function.
    
    Test Cases:
    1. Verify that a repository present in 'requested' but not in 'existing' is added.
    2. Verify that a repository present in both 'existing' and 'requested' but with different attributes is updated.
    3. Verify that a repository present in 'existing' but not in 'requested' is deleted.