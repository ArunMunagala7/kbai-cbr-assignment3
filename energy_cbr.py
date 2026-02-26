"""
Energy Efficiency Regression CBR System
Implements case-based reasoning for predicting building heating loads.
"""

from typing import List, Tuple, Optional
import numpy as np
from data_loader import Case
from cbr_system import CBRSystem


class EnergyCBRSystem(CBRSystem):
    """
    CBR System specialized for energy efficiency regression.
    
    Predicts heating load (continuous value in kWh)
    Features: X1-X8 (8 numerical features)
    """
    
    def __init__(self):
        """Initialize energy regression system."""
        
        # All features are numerical
        feature_types = {
            'relative_compactness': 'numerical',
            'surface_area': 'numerical',
            'wall_area': 'numerical',
            'roof_area': 'numerical',
            'orientation': 'numerical',
            'glazing_area': 'numerical',
            'glazing_area_distribution': 'numerical',
            'glazing_type': 'numerical'
        }
        
        # Baseline weights (equal)
        baseline_weights = {
            'relative_compactness': 1.0,
            'surface_area': 1.0,
            'wall_area': 1.0,
            'roof_area': 1.0,
            'orientation': 1.0,
            'glazing_area': 1.0,
            'glazing_area_distribution': 1.0,
            'glazing_type': 1.0
        }
        
        # Tuned weights based on feature importance
        # Surface area has high correlation with heating load
        # Wall area and relative compactness also important
        # Glazing features affect energy loss
        self.tuned_weights = {
            'relative_compactness': 0.18,      # Inverse relation to heating
            'surface_area': 0.22,              # Highest correlation
            'wall_area': 0.18,                 # Heat loss through walls
            'roof_area': 0.13,                 # Heat loss through roof
            'orientation': 0.08,               # Solar gain affects heating/cooling
            'glazing_area': 0.12,              # Heat loss through windows
            'glazing_area_distribution': 0.05, # Less critical
            'glazing_type': 0.04               # Least critical for heating
        }
        
        super().__init__(feature_weights=baseline_weights, feature_types=feature_types)
        self.case_base_with_solutions: List[Tuple[Case, float]] = []
        self._computed_tuned_weights: Optional[dict] = None
    
    def set_tuned_mode(self):
        """Switch to tuned weights."""
        if self._computed_tuned_weights:
            self.feature_weights = self._computed_tuned_weights
        else:
            self.feature_weights = self.tuned_weights
    
    def set_baseline_mode(self):
        """Switch to baseline weights."""
        self.feature_weights = {
            'relative_compactness': 1.0,
            'surface_area': 1.0,
            'wall_area': 1.0,
            'roof_area': 1.0,
            'orientation': 1.0,
            'glazing_area': 1.0,
            'glazing_area_distribution': 1.0,
            'glazing_type': 1.0
        }
    
    def set_case_base(self, cases: List[Case]):
        """Override to store both cases and solutions for adaptation."""
        super().set_case_base(cases)
        self.case_base_with_solutions = [(case, case.solution) for case in cases]
        self._computed_tuned_weights = self._compute_correlation_weights(cases)
    
    def add_case(self, case: Case):
        """Override to maintain parallel structure."""
        super().add_case(case)
        self.case_base_with_solutions.append((case, case.solution))
    
    def adapt_regression(self, retrieved_case: Case, query: Case,
                        use_multiple_rules: bool = True) -> float:
        """
        Adapt retrieved case solution for regression.
        
        Implements 4+ adaptation rules:
        1. Difference scaling: Scale by magnitude of feature differences
        2. Linear extrapolation: Learn slopes from case base
        3. Multi-case averaging: Average top-3 similar cases
        4. Segment-based adaptation: Apply segment-specific rules
        
        Args:
            retrieved_case: Most similar case from case base
            query: Query case
            use_multiple_rules: Whether to use multiple rules (True) or just retrieved
            
        Returns:
            Adapted heating load prediction
        """
        
        if not use_multiple_rules:
            return retrieved_case.solution
        
        predictions = []
        
        # Rule 1: Difference scaling
        rule1_pred = self._difference_scaling(retrieved_case, query)
        predictions.append(rule1_pred)
        
        # Rule 2: Linear extrapolation
        rule2_pred = self._linear_extrapolation(retrieved_case, query)
        predictions.append(rule2_pred)
        
        # Rule 3: Multi-case averaging
        rule3_pred = self._multi_case_averaging(query)
        predictions.append(rule3_pred)
        
        # Rule 4: Segment-based adaptation
        rule4_pred = self._segment_based_adaptation(retrieved_case, query)
        predictions.append(rule4_pred)
        
        # Blend adapted predictions with retrieved solution for stability
        adapted_mean = np.mean(predictions) if predictions else retrieved_case.solution
        blended = (retrieved_case.solution * 0.6) + (adapted_mean * 0.4)
        
        # Safeguard: avoid large deviations from retrieved case
        top_k = self.retrieve_top_k(query, k=5, use_weights=True)
        top_solutions = [case.solution for case, _ in top_k] if top_k else []
        if top_solutions:
            std_dev = np.std(top_solutions)
            threshold = max(0.5, 0.5 * std_dev)
            if abs(blended - retrieved_case.solution) > threshold:
                return retrieved_case.solution
        
        return blended
    
    def _difference_scaling(self, retrieved_case: Case, query: Case) -> float:
        """
        Rule 1: Scale solution by magnitude of feature differences.
        
        Logic:
        - Calculate how much each feature differs
        - If features differ significantly, scale the retrieved solution
        - Larger differences = larger adjustment
        
        Args:
            retrieved_case: Reference case
            query: Query case
            
        Returns:
            Adapted prediction
        """
        retrieved_solution = retrieved_case.solution
        
        # Calculate difference magnitude for each feature
        differences = []
        for feature_name in retrieved_case.features:
            if feature_name in query.features:
                val_r = retrieved_case.features[feature_name]
                val_q = query.features[feature_name]
                
                try:
                    diff = abs(float(val_q) - float(val_r))
                    differences.append(diff)
                except (TypeError, ValueError):
                    pass
        
        if not differences:
            return retrieved_solution
        
        # Calculate mean difference
        mean_diff = np.mean(differences)
        
        # Scale factor: features are normalized, so mean_diff is typically in [0, 2]
        # Use conservative scaling to avoid over-adjustment
        scale_factor = 1.0 + (mean_diff * 0.05)
        
        return retrieved_solution * scale_factor
    
    def _linear_extrapolation(self, retrieved_case: Case, query: Case) -> float:
        """
        Rule 2: Linear extrapolation using learned feature-solution relationships.
        
        Logic:
        - For each feature, learn relationship with heating load
        - Apply learned slopes to predict adjustment
        
        Args:
            retrieved_case: Reference case
            query: Query case
            
        Returns:
            Adapted prediction
        """
        base_solution = retrieved_case.solution
        adjustment = 0.0
        
        # Learn slopes from case base (use top 10 similar cases to query)
        similar_cases = self.retrieve_top_k(query, k=min(10, len(self.case_base)))
        
        for feature_name in retrieved_case.features:
            if feature_name not in query.features:
                continue
            
            # Calculate correlation of this feature with heating load
            feature_values = []
            solutions = []
            
            for case, sim in similar_cases:
                if feature_name in case.features:
                    try:
                        feature_values.append(float(case.features[feature_name]))
                        solutions.append(float(case.solution))
                    except (TypeError, ValueError):
                        pass
            
            if len(feature_values) > 2:
                try:
                    # Calculate slope using simple linear regression
                    feature_values = np.array(feature_values)
                    solutions = np.array(solutions)
                    
                    # Normalize for comparison
                    if np.std(feature_values) > 0 and np.std(solutions) > 0:
                        feature_values_norm = (feature_values - np.mean(feature_values)) / np.std(feature_values)
                        solutions_norm = (solutions - np.mean(solutions)) / np.std(solutions)
                        
                        # Simple correlation coefficient as slope
                        correlation = np.corrcoef(feature_values_norm, solutions_norm)[0, 1]
                        if np.isnan(correlation):
                            continue
                        
                        # Calculate feature difference
                        feature_diff = (float(query.features[feature_name]) - 
                                       float(retrieved_case.features[feature_name]))
                        
                        # Adjust prediction (correlation tells us direction and magnitude)
                        adjustment += feature_diff * correlation * 0.1
                except:
                    pass
        
        return base_solution + adjustment

    def _compute_correlation_weights(self, cases: List[Case]) -> dict:
        """
        Compute tuned weights based on absolute correlation with heating load.
        
        Args:
            cases: List of cases from training data
            
        Returns:
            Dictionary of feature weights summing to 1.0
        """
        if not cases:
            return self.tuned_weights
        
        feature_names = list(cases[0].features.keys())
        solutions = np.array([case.solution for case in cases], dtype=float)
        
        weights = {}
        for name in feature_names:
            values = np.array([case.features.get(name, 0.0) for case in cases], dtype=float)
            if np.std(values) == 0 or np.std(solutions) == 0:
                weights[name] = 0.0
                continue
            corr = np.corrcoef(values, solutions)[0, 1]
            if np.isnan(corr):
                weights[name] = 0.0
            else:
                weights[name] = abs(float(corr))
        
        total = sum(weights.values())
        if total == 0:
            return self.tuned_weights
        
        # Normalize to sum to 1
        return {k: v / total for k, v in weights.items()}
    
    def _multi_case_averaging(self, query: Case) -> float:
        """
        Rule 3: Average solutions from top-3 similar cases.
        
        Logic:
        - Retrieve top-3 most similar cases
        - Adapt each one using difference scaling
        - Return weighted average
        
        Args:
            query: Query case
            
        Returns:
            Adapted prediction
        """
        top_3 = self.retrieve_top_k(query, k=3, use_weights=True)
        
        if not top_3:
            return 0.0
        
        predictions = []
        weights = []
        
        for case, similarity in top_3:
            # Apply difference scaling to each
            pred = self._difference_scaling(case, query)
            predictions.append(pred)
            weights.append(similarity)
        
        # Weighted average
        total_weight = sum(weights)
        if total_weight > 0:
            return sum(p * w for p, w in zip(predictions, weights)) / total_weight
        else:
            return np.mean(predictions)
    
    def _segment_based_adaptation(self, retrieved_case: Case, query: Case) -> float:
        """
        Rule 4: Segment-based adaptation.
        
        Logic:
        - Divide case base into segments by heating load level
        - Identify which segment the query belongs to
        - Apply segment-specific rules
        
        Args:
            retrieved_case: Reference case
            query: Query case
            
        Returns:
            Adapted prediction
        """
        base_solution = retrieved_case.solution
        
        # Get all solutions to determine segments
        if not self.case_base_with_solutions:
            return base_solution
        
        all_solutions = [sol for case, sol in self.case_base_with_solutions]
        min_sol = min(all_solutions)
        max_sol = max(all_solutions)
        
        # Define segments
        q1 = min_sol + (max_sol - min_sol) * 0.25
        q2 = min_sol + (max_sol - min_sol) * 0.5
        q3 = min_sol + (max_sol - min_sol) * 0.75
        
        # Determine segment of base solution
        if base_solution < q1:
            scale = 0.98  # In low segment, be conservative
        elif base_solution < q2:
            scale = 1.0
        elif base_solution < q3:
            scale = 1.02
        else:
            scale = 1.04  # In high segment, be slightly more aggressive
        
        # Apply segment-specific scaling
        return base_solution * scale


if __name__ == '__main__':
    from data_loader import load_energy_system_data
    
    print("=== Testing Energy CBR System ===")
    train, test = load_energy_system_data()
    
    # Create and test
    system = EnergyCBRSystem()
    system.set_case_base(train)
    
    print(f"\nBaseline weights (sum should be 8.0): {sum(system.feature_weights.values()):.1f}")
    system.set_tuned_mode()
    print(f"Tuned weights (sum should be ~1.0): {sum(system.feature_weights.values()):.2f}")
    
    # Test on first few test cases
    print("\n=== Testing Predictions ===")
    for i in range(3):
        query = test[i]
        retrieved, sim = system.retrieve_most_similar(query, use_weights=True)
        adapted = system.adapt_regression(retrieved, query)
        error = abs(adapted - query.solution)
        print(f"\nCase {i}:")
        print(f"  Actual heating load: {query.solution:.2f}")
        print(f"  Retrieved (similarity {sim:.3f}): {retrieved.solution:.2f}")
        print(f"  Adapted: {adapted:.2f}")
        print(f"  Error: {error:.2f}")
