"""
Core CBR System Module
Implements the core Case-Based Reasoning logic:
- Similarity computation
- Case retrieval
- Case storage and learning
"""

from typing import List, Dict, Tuple, Any, Optional, Callable
import numpy as np
from data_loader import Case


class CBRSystem:
    """
    Core Case-Based Reasoning System.
    
    Implements retrieval of similar cases and their storage in a case base.
    Adaptation and solution logic are handled by subclasses.
    """
    
    def __init__(self, feature_weights: Optional[Dict[str, float]] = None,
                 feature_types: Optional[Dict[str, str]] = None):
        """
        Initialize CBR System.
        
        Args:
            feature_weights: Dictionary of feature names to weights (for similarity)
            feature_types: Dictionary of feature names to types ('numerical' or 'categorical')
        """
        self.feature_weights = feature_weights or {}
        self.feature_types = feature_types or {}
        self.case_base: List[Case] = []
    
    def set_case_base(self, cases: List[Case]):
        """Set the initial case base."""
        self.case_base = cases.copy()
        print(f"Case base initialized with {len(self.case_base)} cases")
    
    def add_case(self, case: Case):
        """Add a new case to the case base (learning)."""
        self.case_base.append(case)
    
    def feature_similarity(self, val1: Any, val2: Any, feature_name: str = None) -> float:
        """
        Calculate similarity between two feature values.
        
        For numerical features: normalized distance (0-1, where 1 = identical)
        For categorical features: direct match (1.0 if same, 0.0 if different)
        
        Args:
            val1: First value
            val2: Second value
            feature_name: Name of feature (for type lookup)
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Handle None values
        if val1 is None or val2 is None:
            return 0.0 if val1 != val2 else 1.0
        
        # Determine feature type
        feature_type = self.feature_types.get(feature_name, 'categorical')
        
        if feature_type == 'numerical':
            # For numerical features: convert to float and use distance
            try:
                v1 = float(val1)
                v2 = float(val2)
                
                # If both are normalized (between -3 and 3, typical z-score range)
                # use simple distance. Otherwise normalize.
                diff = abs(v1 - v2)
                
                # Use a sigmoid-like function to convert distance to similarity
                # Closer values get higher similarity
                # This assumes normalized features are typically in range [-3, 3]
                similarity = 1.0 / (1.0 + diff)
                return min(1.0, max(0.0, similarity))
            except (TypeError, ValueError):
                # If conversion fails, treat as categorical
                return 1.0 if val1 == val2 else 0.0
        else:
            # For categorical features: direct match or ordinal similarity
            if val1 == val2:
                return 1.0
            
            # Check if feature has ordinal encoding (for features like buying, safety, etc.)
            ordinal_map = self._get_ordinal_map(feature_name)
            if ordinal_map:
                try:
                    rank1 = ordinal_map.get(str(val1), None)
                    rank2 = ordinal_map.get(str(val2), None)
                    if rank1 is not None and rank2 is not None:
                        # Ordinal similarity based on rank distance
                        max_distance = len(ordinal_map) - 1
                        distance = abs(rank1 - rank2)
                        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
                except:
                    pass
            
            # Default: exact match only
            return 0.0
    
    def _get_ordinal_map(self, feature_name: str) -> Optional[Dict[str, int]]:
        """
        Get ordinal mapping for a feature if it has one.
        
        Features like 'buying', 'safety', 'maint' have ordinal values.
        vhigh > high > med > low (in terms of price/cost/risk)
        
        Args:
            feature_name: Name of feature
            
        Returns:
            Dictionary mapping values to ranks, or None if not ordinal
        """
        ordinal_maps = {
            'buying': {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0},
            'maint': {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0},
            'safety': {'low': 0, 'med': 1, 'high': 2},
            'lug_boot': {'small': 0, 'med': 1, 'big': 2},
            'persons': {'2': 1, '4': 2, 'more': 3},
            'doors': {'2': 1, '3': 2, '4': 3, '5-more': 4, '5more': 4}
        }
        return ordinal_maps.get(feature_name)
    
    def calculate_similarity(self, case1: Case, case2: Case, 
                           use_weights: bool = True) -> float:
        """
        Calculate overall similarity between two cases.
        
        Uses weighted average of feature similarities.
        
        Args:
            case1: First case
            case2: Second case
            use_weights: Whether to use feature weights (True=tuned, False=baseline)
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not case1.features or not case2.features:
            return 0.0
        
        # Get all feature names
        feature_names = set(case1.features.keys()) & set(case2.features.keys())
        
        if not feature_names:
            return 0.0
        
        # Calculate feature similarities
        feature_sims = {}
        total_weight = 0.0
        
        for feature_name in feature_names:
            val1 = case1.features[feature_name]
            val2 = case2.features[feature_name]
            
            # Calculate feature-level similarity
            sim = self.feature_similarity(val1, val2, feature_name)
            feature_sims[feature_name] = sim
            
            # Get weight for this feature
            if use_weights and self.feature_weights:
                weight = self.feature_weights.get(feature_name, 1.0)
            else:
                weight = 1.0
            
            total_weight += weight
        
        # Calculate weighted average
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(feature_sims[name] * self.feature_weights.get(name, 1.0)
                          for name in feature_names
                          if (not use_weights or not self.feature_weights) or True)
        
        if use_weights and self.feature_weights:
            weighted_sum = sum(feature_sims[name] * self.feature_weights.get(name, 1.0)
                              for name in feature_names)
        else:
            weighted_sum = sum(feature_sims[name] for name in feature_names)
        
        return weighted_sum / total_weight
    
    def retrieve_most_similar(self, query: Case, use_weights: bool = True) -> Tuple[Case, float]:
        """
        Retrieve the most similar case from case base.
        
        Args:
            query: Query case
            use_weights: Whether to use weighted similarity (True=tuned, False=baseline)
            
        Returns:
            Tuple of (most_similar_case, similarity_score)
        """
        if not self.case_base:
            raise ValueError("Case base is empty")
        
        max_similarity = -1
        best_case = None
        
        for case in self.case_base:
            sim = self.calculate_similarity(query, case, use_weights=use_weights)
            if sim > max_similarity:
                max_similarity = sim
                best_case = case
        
        return best_case, max_similarity
    
    def retrieve_top_k(self, query: Case, k: int = 3, 
                      use_weights: bool = True) -> List[Tuple[Case, float]]:
        """
        Retrieve top-k most similar cases from case base.
        
        Args:
            query: Query case
            k: Number of cases to retrieve
            use_weights: Whether to use weighted similarity
            
        Returns:
            List of (case, similarity) tuples, sorted by similarity (descending)
        """
        if not self.case_base:
            raise ValueError("Case base is empty")
        
        similarities = []
        for case in self.case_base:
            sim = self.calculate_similarity(query, case, use_weights=use_weights)
            similarities.append((case, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:k]
    
    def run_query(self, query: Case, tuned: bool = False, 
                 adapt_fn: Optional[Callable] = None,
                 learning: bool = True) -> Tuple[Any, Case]:
        """
        Run the CBR cycle for a query.
        
        Main CBR cycle:
        1. Retrieve: Find most similar case
        2. Adapt: Modify solution if adaptation function provided
        3. Solve: Return solution
        4. Retain: Add new case to base if learning enabled
        
        Args:
            query: Query case (without solution)
            tuned: Whether to use tuned similarity (weighted) or baseline (equal)
            adapt_fn: Optional adaptation function(retrieved_case, query) -> solution
            learning: Whether to add new case to case base
            
        Returns:
            Tuple of (solution, new_case_with_solution)
        """
        # 1. RETRIEVE: Find most similar case
        retrieved_case, similarity = self.retrieve_most_similar(query, use_weights=tuned)
        
        # 2. ADAPT & 3. SOLVE: Get solution (with or without adaptation)
        if adapt_fn:
            solution = adapt_fn(retrieved_case, query, self)
        else:
            solution = retrieved_case.solution
        
        # Create new case with solution
        new_case = Case(features=query.features, solution=solution)
        
        # 4. RETAIN: Add to case base if learning enabled
        if learning:
            self.add_case(new_case)
        
        return solution, new_case


if __name__ == '__main__':
    # Test basic functionality
    from data_loader import load_car_system_data
    
    print("=== Testing CBR System ===")
    train, test = load_car_system_data()
    
    # Create system with equal weights
    system = CBRSystem(feature_types={
        'buying': 'categorical',
        'maint': 'categorical',
        'doors': 'categorical',
        'persons': 'categorical',
        'lug_boot': 'categorical',
        'safety': 'categorical'
    })
    system.set_case_base(train)
    
    # Test retrieval
    query = test[0]
    retrieved, sim = system.retrieve_most_similar(query, use_weights=False)
    print(f"Query features: {query.features}")
    print(f"Actual class: {query.solution}")
    print(f"Retrieved class: {retrieved.solution}")
    print(f"Similarity: {sim:.4f}")
    
    # Test run_query
    solution, new_case = system.run_query(query, tuned=False, learning=False)
    print(f"Predicted solution: {solution}")
