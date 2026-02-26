"""
Evaluation Module
Implements evaluation metrics for regression and classification tasks.
"""

from typing import List, Tuple, Union
import numpy as np


class Evaluator:
    """Evaluator for regression and classification metrics."""
    
    @staticmethod
    def calculate_mae(predictions: List[float], actuals: List[float]) -> float:
        """
        Calculate Mean Absolute Error.
        
        MAE = mean(|prediction - actual|)
        
        Args:
            predictions: List of predicted values
            actuals: List of actual values
            
        Returns:
            Mean Absolute Error
        """
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        errors = [abs(p - a) for p, a in zip(predictions, actuals)]
        return np.mean(errors)
    
    @staticmethod
    def calculate_rmse(predictions: List[float], actuals: List[float]) -> float:
        """
        Calculate Root Mean Squared Error.
        
        RMSE = sqrt(mean((prediction - actual)²))
        
        Args:
            predictions: List of predicted values
            actuals: List of actual values
            
        Returns:
            Root Mean Squared Error
        """
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        errors = [(p - a) ** 2 for p, a in zip(predictions, actuals)]
        return np.sqrt(np.mean(errors))
    
    @staticmethod
    def calculate_accuracy(predictions: List[str], actuals: List[str]) -> float:
        """
        Calculate Classification Accuracy (percentage).
        
        Accuracy = (correct_predictions / total_predictions) * 100
        
        Args:
            predictions: List of predicted classes
            actuals: List of actual classes
            
        Returns:
            Accuracy as percentage (0-100)
        """
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        correct = sum(1 for p, a in zip(predictions, actuals) if p == a)
        return (correct / len(actuals)) * 100
    
    @staticmethod
    def calculate_metrics_summary(predictions: List[Union[float, str]], 
                                  actuals: List[Union[float, str]],
                                  task_type: str = 'regression') -> dict:
        """
        Calculate comprehensive metrics summary.
        
        Args:
            predictions: List of predictions
            actuals: List of actual values
            task_type: 'regression' or 'classification'
            
        Returns:
            Dictionary with metrics
        """
        metrics = {}
        
        if task_type == 'regression':
            # Convert to float
            try:
                predictions = [float(p) for p in predictions]
                actuals = [float(a) for a in actuals]
            except (TypeError, ValueError):
                raise ValueError("Regression task requires numerical predictions and actuals")
            
            metrics['mae'] = Evaluator.calculate_mae(predictions, actuals)
            metrics['rmse'] = Evaluator.calculate_rmse(predictions, actuals)
            
            # Additional regression metrics
            metrics['min_error'] = min(abs(p - a) for p, a in zip(predictions, actuals))
            metrics['max_error'] = max(abs(p - a) for p, a in zip(predictions, actuals))
            metrics['mean_prediction'] = np.mean(predictions)
            metrics['mean_actual'] = np.mean(actuals)
            
        elif task_type == 'classification':
            # Convert to string
            predictions = [str(p) for p in predictions]
            actuals = [str(a) for a in actuals]
            
            metrics['accuracy'] = Evaluator.calculate_accuracy(predictions, actuals)
            
            # Additional classification metrics
            unique_classes = set(actuals)
            metrics['num_classes'] = len(unique_classes)
            
            # Per-class accuracy
            for class_label in unique_classes:
                class_indices = [i for i, a in enumerate(actuals) if a == class_label]
                if class_indices:
                    class_correct = sum(1 for i in class_indices if predictions[i] == class_label)
                    class_acc = (class_correct / len(class_indices)) * 100
                    metrics[f'accuracy_{class_label}'] = class_acc
        
        return metrics


if __name__ == '__main__':
    print("=== Testing Evaluator ===")
    
    # Test regression metrics
    print("\n--- Regression Metrics ---")
    pred_reg = [10.5, 20.3, 15.8, 25.1]
    actual_reg = [10.2, 21.0, 16.5, 24.0]
    
    mae = Evaluator.calculate_mae(pred_reg, actual_reg)
    rmse = Evaluator.calculate_rmse(pred_reg, actual_reg)
    
    print(f"Predictions: {pred_reg}")
    print(f"Actuals: {actual_reg}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Test classification metrics
    print("\n--- Classification Metrics ---")
    pred_class = ['unacc', 'acc', 'good', 'unacc', 'acc', 'good']
    actual_class = ['unacc', 'acc', 'acc', 'unacc', 'good', 'good']
    
    acc = Evaluator.calculate_accuracy(pred_class, actual_class)
    print(f"Predictions: {pred_class}")
    print(f"Actuals: {actual_class}")
    print(f"Accuracy: {acc:.2f}%")
    
    # Test summary
    print("\n--- Summary Metrics ---")
    summary = Evaluator.calculate_metrics_summary(pred_reg, actual_reg, task_type='regression')
    print("Regression Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value:.4f}")
    
    summary = Evaluator.calculate_metrics_summary(pred_class, actual_class, task_type='classification')
    print("\nClassification Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
