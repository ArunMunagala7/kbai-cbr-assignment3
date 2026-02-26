"""
Car Classification CBR System
Implements case-based reasoning for car evaluation classification.
"""

from typing import List, Tuple, Optional
from data_loader import Case
from cbr_system import CBRSystem


class CarCBRSystem(CBRSystem):
    """
    CBR System specialized for car evaluation classification.
    
    Predicts car acceptability: unacc, acc, good, v-good
    Features: buying, maint, doors, persons, lug_boot, safety
    """
    
    def __init__(self):
        """Initialize car classification system."""
        
        # Feature types (all categorical for cars)
        feature_types = {
            'buying': 'categorical',
            'maint': 'categorical',
            'doors': 'categorical',
            'persons': 'categorical',
            'lug_boot': 'categorical',
            'safety': 'categorical'
        }
        
        # Baseline weights (equal)
        baseline_weights = {
            'buying': 1.0,
            'maint': 1.0,
            'doors': 1.0,
            'persons': 1.0,
            'lug_boot': 1.0,
            'safety': 1.0
        }
        
        # Tuned weights based on domain knowledge
        # Safety is most important for car quality
        # Buying price and passenger capacity are secondary
        # Other features less critical
        self.tuned_weights = {
            'safety': 0.30,      # Most critical for quality
            'buying': 0.20,      # Price significantly affects rating
            'persons': 0.20,     # Capacity is important
            'maint': 0.10,       # Maintenance cost is secondary
            'lug_boot': 0.10,    # Trunk size (comfort feature)
            'doors': 0.10        # Door count least critical
        }
        
        super().__init__(feature_weights=baseline_weights, feature_types=feature_types)
    
    def set_tuned_mode(self):
        """Switch to tuned weights."""
        self.feature_weights = self.tuned_weights
    
    def set_baseline_mode(self):
        """Switch to baseline weights."""
        self.feature_weights = {
            'buying': 1.0,
            'maint': 1.0,
            'doors': 1.0,
            'persons': 1.0,
            'lug_boot': 1.0,
            'safety': 1.0
        }
    
    def adapt_classification(self, retrieved_case: Case, query: Case,
                            use_voting: bool = True) -> str:
        """
        Adapt retrieved case solution for classification.
        
        Implements 3 adaptation rules:
        1. Feature refinement: Adjust class based on feature improvements
        2. Multi-case voting: Retrieve top-3, vote on class
        3. Confidence threshold: Only adapt if confident
        
        Args:
            retrieved_case: Most similar case from case base
            query: Query case
            use_voting: Whether to use voting rule
            
        Returns:
            Adapted class prediction
        """
        
        # Rule 1: Feature-based refinement
        adapted_class = self._feature_refinement(retrieved_case, query)
        
        if not use_voting:
            return adapted_class
        
        # Rule 2: Multi-case voting for confidence
        top_3 = self.retrieve_top_k(query, k=3, use_weights=True)
        voted_classes = [case.solution for case, sim in top_3]
        
        # Rule 3: Confidence threshold
        if len(set(voted_classes)) == 1 and top_3[0][1] > 0.75:
            # All cases vote the same AND similarity is high
            return voted_classes[0]
        elif len([c for c in voted_classes if c == voted_classes[0]]) >= 2:
            # Majority vote
            from collections import Counter
            counts = Counter(voted_classes)
            return counts.most_common(1)[0][0]
        else:
            # No consensus, use feature refinement
            return adapted_class
    
    def _feature_refinement(self, retrieved_case: Case, query: Case) -> str:
        """
        Rule 1: Feature-based class refinement.
        
        Logic:
        - If safety improves (low->med or med->high): upgrade class
        - If persons increases: upgrade class
        - If buying improves (vhigh->high or high->med): upgrade class
        - If maint worsens significantly: downgrade class
        
        Args:
            retrieved_case: Reference case
            query: Query case
            
        Returns:
            Adjusted class
        """
        base_class = retrieved_case.solution
        
        # Class ordering
        class_order = ['unacc', 'acc', 'good', 'v-good']
        current_level = class_order.index(base_class) if base_class in class_order else 0
        
        adjustment = 0
        
        # Safety improvement: +1 level
        safety_order = {'low': 0, 'med': 1, 'high': 2}
        if (query.features.get('safety') in safety_order and 
            retrieved_case.features.get('safety') in safety_order):
            safety_diff = (safety_order.get(query.features['safety'], 0) - 
                          safety_order.get(retrieved_case.features['safety'], 0))
            if safety_diff > 0:
                adjustment += 1
        
        # Persons increase: +0.5 level
        persons_order = {'2': 1, '4': 2, 'more': 3}
        if (query.features.get('persons') in persons_order and 
            retrieved_case.features.get('persons') in persons_order):
            persons_diff = (persons_order.get(query.features['persons'], 0) - 
                           persons_order.get(retrieved_case.features['persons'], 0))
            if persons_diff > 0:
                adjustment += 0.5
        
        # Buying improvement: +0.5 level
        buying_order = {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0}
        if (query.features.get('buying') in buying_order and 
            retrieved_case.features.get('buying') in buying_order):
            buying_diff = (buying_order.get(query.features['buying'], 0) - 
                          buying_order.get(retrieved_case.features['buying'], 0))
            if buying_diff > 0:
                adjustment += 0.5
        
        # Maint worsening: -0.5 level
        maint_order = {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0}
        if (query.features.get('maint') in maint_order and 
            retrieved_case.features.get('maint') in maint_order):
            maint_diff = (maint_order.get(query.features['maint'], 0) - 
                         maint_order.get(retrieved_case.features['maint'], 0))
            if maint_diff < 0:  # Worsening (lower value)
                adjustment -= 0.5
        
        # Apply adjustment
        adjusted_level = int(round(current_level + adjustment))
        adjusted_level = max(0, min(len(class_order) - 1, adjusted_level))
        
        return class_order[adjusted_level]


if __name__ == '__main__':
    from data_loader import load_car_system_data
    
    print("=== Testing Car CBR System ===")
    train, test = load_car_system_data()
    
    # Create and test
    system = CarCBRSystem()
    system.set_case_base(train)
    
    print(f"\nBaseline weights: {system.feature_weights}")
    system.set_tuned_mode()
    print(f"Tuned weights: {system.feature_weights}")
    
    # Test on first few test cases
    print("\n=== Testing Predictions ===")
    for i in range(3):
        query = test[i]
        retrieved, sim = system.retrieve_most_similar(query, use_weights=True)
        adapted = system.adapt_classification(retrieved, query)
        print(f"\nCase {i}:")
        print(f"  Actual: {query.solution}")
        print(f"  Retrieved (similarity {sim:.3f}): {retrieved.solution}")
        print(f"  Adapted: {adapted}")
