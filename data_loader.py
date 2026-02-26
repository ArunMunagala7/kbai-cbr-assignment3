"""
Data Loader Module
Loads and preprocesses both the Car Evaluation and Energy Efficiency datasets.
Creates Case objects suitable for CBR processing.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import random


@dataclass
class Case:
    """
    Represents a single case in the case base.
    
    Attributes:
        features (Dict[str, Any]): Dictionary of feature names to values
        solution (Any): The target variable (class for classification, value for regression)
        metadata (Dict): Optional metadata (like original index)
    """
    features: Dict[str, Any]
    solution: Any
    metadata: Dict = None


class DataLoader:
    """Loads and preprocesses datasets for CBR system."""
    
    @staticmethod
    def load_car_data(filepath: str = 'car.data') -> List[Case]:
        """
        Load car evaluation dataset.
        
        Features: buying, maint, doors, persons, lug_boot, safety
        Target: class (unacc, acc, good, v-good)
        
        Args:
            filepath: Path to car.data file
            
        Returns:
            List of Case objects
        """
        # Feature names as per car.names
        feature_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
        
        # Read CSV file
        try:
            data = pd.read_csv(filepath, header=None, names=feature_names + ['class'])
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find {filepath}")
        
        # Create Case objects
        cases = []
        for idx, row in data.iterrows():
            features = {name: row[name] for name in feature_names}
            case = Case(
                features=features,
                solution=row['class'],  # Target variable
                metadata={'original_index': idx}
            )
            cases.append(case)
        
        print(f"Loaded {len(cases)} car cases")
        return cases
    
    @staticmethod
    def load_energy_data(filepath: str = 'ENB2012_data.xlsx') -> List[Case]:
        """
        Load energy efficiency dataset.
        
        Features: X1 (relative_compactness), X2 (surface_area), X3 (wall_area), 
                 X4 (roof_area), X5 (orientation), X6 (glazing_area), 
                 X7 (glazing_area_distribution), X8 (glazing_type)
        Target: Y1 (heating_load), Y2 (cooling_load) - we use Y1 (heating_load)
        
        Args:
            filepath: Path to Excel file
            
        Returns:
            List of Case objects
        """
        try:
            data = pd.read_excel(filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find {filepath}")
        
        # Feature names are X1-X8, target is Y1 (heating load)
        feature_names = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8']
        
        # Rename for clarity
        feature_name_map = {
            'X1': 'relative_compactness',
            'X2': 'surface_area',
            'X3': 'wall_area',
            'X4': 'roof_area',
            'X5': 'orientation',
            'X6': 'glazing_area',
            'X7': 'glazing_area_distribution',
            'X8': 'glazing_type'
        }
        
        # Create Case objects
        cases = []
        for idx, row in data.iterrows():
            # Use original X names as keys for feature dict
            features = {feature_name_map.get(name, name): float(row[name]) for name in feature_names}
            case = Case(
                features=features,
                solution=float(row['Y1']),  # Y1 is heating load (target variable)
                metadata={'original_index': idx}
            )
            cases.append(case)
        
        print(f"Loaded {len(cases)} energy cases")
        return cases
    
    @staticmethod
    def normalize_features(cases: List[Case], feature_names: List[str], 
                          method: str = 'zscore') -> Tuple[List[Case], Dict[str, Tuple[float, float]]]:
        """
        Normalize numerical features in cases.
        
        Args:
            cases: List of Case objects
            feature_names: List of feature names to normalize
            method: 'zscore' or 'minmax'
            
        Returns:
            Tuple of (normalized_cases, normalization_params)
        """
        # Extract feature values
        feature_data = {name: [] for name in feature_names}
        for case in cases:
            for name in feature_names:
                if isinstance(case.features[name], (int, float)):
                    feature_data[name].append(case.features[name])
        
        # Calculate normalization parameters
        normalization_params = {}
        for name in feature_names:
            if not feature_data[name]:
                continue
                
            if method == 'zscore':
                mean = np.mean(feature_data[name])
                std = np.std(feature_data[name])
                normalization_params[name] = (mean, std)
            elif method == 'minmax':
                min_val = min(feature_data[name])
                max_val = max(feature_data[name])
                normalization_params[name] = (min_val, max_val)
        
        # Normalize cases
        normalized_cases = []
        for case in cases:
            new_features = case.features.copy()
            for name in feature_names:
                if name in normalization_params and isinstance(new_features[name], (int, float)):
                    val = new_features[name]
                    if method == 'zscore':
                        mean, std = normalization_params[name]
                        if std > 0:
                            new_features[name] = (val - mean) / std
                    elif method == 'minmax':
                        min_val, max_val = normalization_params[name]
                        if max_val > min_val:
                            new_features[name] = (val - min_val) / (max_val - min_val)
            
            new_case = Case(features=new_features, solution=case.solution, metadata=case.metadata)
            normalized_cases.append(new_case)
        
        return normalized_cases, normalization_params
    
    @staticmethod
    def train_test_split(cases: List[Case], train_ratio: float = 0.8, 
                        random_seed: int = 42) -> Tuple[List[Case], List[Case]]:
        """
        Split cases into training and test sets.
        
        Args:
            cases: List of Case objects
            train_ratio: Ratio for training set (0-1)
            random_seed: Seed for reproducibility
            
        Returns:
            Tuple of (train_cases, test_cases)
        """
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        indices = list(range(len(cases)))
        random.shuffle(indices)
        
        split_idx = int(len(cases) * train_ratio)
        train_indices = indices[:split_idx]
        test_indices = indices[split_idx:]
        
        train_cases = [cases[i] for i in train_indices]
        test_cases = [cases[i] for i in test_indices]
        
        print(f"Split: {len(train_cases)} training, {len(test_cases)} test")
        return train_cases, test_cases


def load_car_system_data(random_seed: int = 42) -> Tuple[List[Case], List[Case]]:
    """
    Load car data, split into train/test.
    
    Returns:
        Tuple of (train_cases, test_cases)
    """
    loader = DataLoader()
    cases = loader.load_car_data()
    train, test = loader.train_test_split(cases, train_ratio=0.8, random_seed=random_seed)
    return train, test


def load_energy_system_data(random_seed: int = 42) -> Tuple[List[Case], List[Case]]:
    """
    Load energy data, normalize, split into train/test.
    
    Returns:
        Tuple of (train_cases, test_cases)
    """
    loader = DataLoader()
    cases = loader.load_energy_data()
    
    # Get feature names (all except the last which is cooling load, and we use heating load)
    feature_names = list(cases[0].features.keys())
    
    # Normalize numerical features
    normalized_cases, params = loader.normalize_features(cases, feature_names, method='zscore')
    
    # Split
    train, test = loader.train_test_split(normalized_cases, train_ratio=0.8, random_seed=random_seed)
    
    return train, test


if __name__ == '__main__':
    # Test data loading
    print("=== Testing Car Data Loading ===")
    car_train, car_test = load_car_system_data()
    print(f"Sample car case: {car_train[0]}")
    
    print("\n=== Testing Energy Data Loading ===")
    energy_train, energy_test = load_energy_system_data()
    print(f"Sample energy case: {energy_train[0]}")
