"""
Main Module - Run all 6 test conditions
Executes the complete evaluation of both CBR systems:
- 3 conditions for regression (energy efficiency)
- 3 conditions for classification (car evaluation)
"""

from typing import List, Dict, Tuple
import sys
from data_loader import load_car_system_data, load_energy_system_data, Case
from car_cbr import CarCBRSystem
from energy_cbr import EnergyCBRSystem
from evaluation import Evaluator


def run_car_tests(train_cases: List[Case], test_cases: List[Case]) -> Dict[str, Dict]:
    """
    Run 3 car classification test conditions.
    
    Condition 1: Untuned (baseline similarity, no adaptation)
    Condition 2: Tuned similarity, no adaptation
    Condition 3: Tuned similarity, with adaptation
    
    Args:
        train_cases: Training case base
        test_cases: Test cases
        
    Returns:
        Dictionary with results for each condition
    """
    results = {}
    
    print("\n" + "="*70)
    print("CAR CLASSIFICATION - 3 Test Conditions")
    print("="*70)
    
    # ===== Condition 1: Untuned (Baseline) =====
    print("\n[Condition 1] Untuned - Baseline Similarity, No Adaptation")
    print("-" * 70)
    
    system1 = CarCBRSystem()
    system1.set_case_base(train_cases)
    system1.set_baseline_mode()
    
    predictions1 = []
    for i, test_case in enumerate(test_cases):
        solution, _ = system1.run_query(test_case, tuned=False, adapt_fn=None, learning=False)
        predictions1.append(solution)
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    accuracy1 = Evaluator.calculate_accuracy(predictions1, [case.solution for case in test_cases])
    results['untuned'] = {
        'accuracy': accuracy1,
        'condition': 'Baseline (equal weights, no adaptation)',
        'learning': False
    }
    print(f"Accuracy: {accuracy1:.2f}%")
    
    # ===== Condition 2: Tuned Similarity, No Adaptation =====
    print("\n[Condition 2] Tuned Similarity - No Adaptation")
    print("-" * 70)
    
    system2 = CarCBRSystem()
    system2.set_case_base(train_cases)
    system2.set_tuned_mode()
    
    predictions2 = []
    for i, test_case in enumerate(test_cases):
        solution, _ = system2.run_query(test_case, tuned=True, adapt_fn=None, learning=False)
        predictions2.append(solution)
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    accuracy2 = Evaluator.calculate_accuracy(predictions2, [case.solution for case in test_cases])
    results['tuned'] = {
        'accuracy': accuracy2,
        'condition': 'Tuned weights, no adaptation',
        'learning': False
    }
    print(f"Accuracy: {accuracy2:.2f}%")
    print(f"Improvement over untuned: {accuracy2 - accuracy1:.2f}%")
    
    # ===== Condition 3: Tuned with Adaptation =====
    print("\n[Condition 3] Tuned + Adaptation Rules")
    print("-" * 70)
    
    system3 = CarCBRSystem()
    system3.set_case_base(train_cases)
    system3.set_tuned_mode()
    
    predictions3 = []
    for i, test_case in enumerate(test_cases):
        retrieved, _ = system3.retrieve_most_similar(test_case, use_weights=True)
        solution = system3.adapt_classification(retrieved, test_case, use_voting=True)
        new_case = Case(features=test_case.features, solution=solution)
        # Don't add to case base for this test
        predictions3.append(solution)
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    accuracy3 = Evaluator.calculate_accuracy(predictions3, [case.solution for case in test_cases])
    results['tuned_adapt'] = {
        'accuracy': accuracy3,
        'condition': 'Tuned weights + adaptation rules',
        'learning': False
    }
    print(f"Accuracy: {accuracy3:.2f}%")
    print(f"Improvement over tuned (no adapt): {accuracy3 - accuracy2:.2f}%")
    
    return results


def run_energy_tests(train_cases: List[Case], test_cases: List[Case]) -> Dict[str, Dict]:
    """
    Run 3 energy regression test conditions.
    
    Condition 1: Untuned (baseline, no adaptation, with learning)
    Condition 2: Tuned + adaptation (with learning)
    Condition 3: Tuned + adaptation (WITHOUT learning)
    
    Args:
        train_cases: Training case base
        test_cases: Test cases
        
    Returns:
        Dictionary with results for each condition
    """
    results = {}
    
    print("\n" + "="*70)
    print("ENERGY REGRESSION - 3 Test Conditions")
    print("="*70)
    
    # ===== Condition 1: Untuned (Baseline) =====
    print("\n[Condition 1] Untuned - Baseline Similarity, No Adaptation, With Learning")
    print("-" * 70)
    
    system1 = EnergyCBRSystem()
    system1.set_case_base(train_cases)
    system1.set_baseline_mode()
    
    predictions1 = []
    case_base_size_before = len(system1.case_base)
    
    for i, test_case in enumerate(test_cases):
        retrieved, _ = system1.retrieve_most_similar(test_case, use_weights=False)
        solution = retrieved.solution  # No adaptation
        # Add to case base (learning enabled)
        new_case = Case(features=test_case.features, solution=solution)
        system1.add_case(new_case)
        predictions1.append(solution)
        if (i + 1) % 30 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    case_base_size_after_1 = len(system1.case_base)
    mae1 = Evaluator.calculate_mae(predictions1, [case.solution for case in test_cases])
    rmse1 = Evaluator.calculate_rmse(predictions1, [case.solution for case in test_cases])
    
    results['untuned'] = {
        'mae': mae1,
        'rmse': rmse1,
        'condition': 'Baseline (equal weights, no adaptation, learning enabled)',
        'learning': True,
        'case_base_growth': case_base_size_after_1 - case_base_size_before
    }
    print(f"MAE: {mae1:.4f} kWh")
    print(f"RMSE: {rmse1:.4f} kWh")
    print(f"Case base grew from {case_base_size_before} to {case_base_size_after_1} cases")
    
    # ===== Condition 2: Tuned + Adaptation WITH Learning =====
    print("\n[Condition 2] Tuned + Adaptation - WITH Learning")
    print("-" * 70)
    
    system2 = EnergyCBRSystem()
    system2.set_case_base(train_cases)
    system2.set_tuned_mode()
    
    predictions2 = []
    case_base_size_before = len(system2.case_base)
    
    for i, test_case in enumerate(test_cases):
        retrieved, _ = system2.retrieve_most_similar(test_case, use_weights=True)
        solution = system2.adapt_regression(retrieved, test_case, use_multiple_rules=True)
        # Add to case base (learning enabled)
        new_case = Case(features=test_case.features, solution=solution)
        system2.add_case(new_case)
        predictions2.append(solution)
        if (i + 1) % 30 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    case_base_size_after_2 = len(system2.case_base)
    mae2 = Evaluator.calculate_mae(predictions2, [case.solution for case in test_cases])
    rmse2 = Evaluator.calculate_rmse(predictions2, [case.solution for case in test_cases])
    
    results['tuned'] = {
        'mae': mae2,
        'rmse': rmse2,
        'condition': 'Tuned weights + adaptation (learning enabled)',
        'learning': True,
        'case_base_growth': case_base_size_after_2 - case_base_size_before
    }
    print(f"MAE: {mae2:.4f} kWh")
    print(f"RMSE: {rmse2:.4f} kWh")
    print(f"Case base grew from {case_base_size_before} to {case_base_size_after_2} cases")
    print(f"Improvement over untuned (MAE): {mae1 - mae2:.4f} kWh ({((mae1-mae2)/mae1*100):.1f}% better)")
    
    # ===== Condition 3: Tuned + Adaptation WITHOUT Learning =====
    print("\n[Condition 3] Tuned + Adaptation - NO Learning")
    print("-" * 70)
    
    system3 = EnergyCBRSystem()
    system3.set_case_base(train_cases)
    system3.set_tuned_mode()
    
    predictions3 = []
    case_base_size_before = len(system3.case_base)
    
    for i, test_case in enumerate(test_cases):
        retrieved, _ = system3.retrieve_most_similar(test_case, use_weights=True)
        solution = system3.adapt_regression(retrieved, test_case, use_multiple_rules=True)
        # DO NOT add to case base (learning disabled)
        new_case = Case(features=test_case.features, solution=solution)
        # system3.add_case(new_case)  # Commented out
        predictions3.append(solution)
        if (i + 1) % 30 == 0:
            print(f"  Processed {i + 1}/{len(test_cases)} cases")
    
    case_base_size_after_3 = len(system3.case_base)
    mae3 = Evaluator.calculate_mae(predictions3, [case.solution for case in test_cases])
    rmse3 = Evaluator.calculate_rmse(predictions3, [case.solution for case in test_cases])
    
    results['tuned_nolearn'] = {
        'mae': mae3,
        'rmse': rmse3,
        'condition': 'Tuned weights + adaptation (learning DISABLED)',
        'learning': False,
        'case_base_growth': case_base_size_after_3 - case_base_size_before
    }
    print(f"MAE: {mae3:.4f} kWh")
    print(f"RMSE: {rmse3:.4f} kWh")
    print(f"Case base size unchanged: {case_base_size_after_3} cases")
    print(f"Learning effect (MAE difference): {mae3 - mae2:.4f} kWh")
    
    return results


def print_results_summary(car_results: Dict, energy_results: Dict):
    """Print comprehensive results summary."""
    
    print("\n" + "="*70)
    print("COMPREHENSIVE RESULTS SUMMARY")
    print("="*70)
    
    # Car Classification Results
    print("\n--- CAR CLASSIFICATION (Accuracy %) ---")
    print(f"{'Condition':<40} {'Accuracy':<15} {'vs Baseline'}")
    print("-" * 70)
    
    baseline_car = car_results['untuned']['accuracy']
    for key, result in car_results.items():
        acc = result['accuracy']
        improvement = acc - baseline_car if key != 'untuned' else 0.0
        imp_str = f"(+{improvement:.2f}%)" if improvement > 0 else "Baseline"
        print(f"{result['condition']:<40} {acc:>7.2f}%        {imp_str}")
    
    # Energy Regression Results
    print("\n--- ENERGY REGRESSION (MAE in kWh) ---")
    print(f"{'Condition':<40} {'MAE':<15} {'vs Baseline'}")
    print("-" * 70)
    
    baseline_mae = energy_results['untuned']['mae']
    for key, result in energy_results.items():
        mae = result['mae']
        improvement = baseline_mae - mae
        imp_pct = (improvement / baseline_mae * 100) if baseline_mae > 0 else 0
        imp_str = f"({imp_pct:.1f}% better)" if improvement > 0 else "Baseline"
        print(f"{result['condition']:<40} {mae:>7.4f}        {imp_str}")
    
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    
    # Car insights
    print("\n📊 CLASSIFICATION (Cars):")
    print(f"  • Baseline accuracy: {car_results['untuned']['accuracy']:.2f}%")
    print(f"  • Tuned weights improved by: {car_results['tuned']['accuracy'] - car_results['untuned']['accuracy']:.2f}%")
    print(f"  • Adaptation rules improved by: {car_results['tuned_adapt']['accuracy'] - car_results['tuned']['accuracy']:.2f}%")
    print(f"  • Best result: {max(r['accuracy'] for r in car_results.values()):.2f}%")
    
    # Energy insights
    print("\n📈 REGRESSION (Energy):")
    print(f"  • Baseline MAE: {energy_results['untuned']['mae']:.4f} kWh")
    print(f"  • Tuned+Learn MAE: {energy_results['tuned']['mae']:.4f} kWh")
    print(f"  • Tuned+NoLearn MAE: {energy_results['tuned_nolearn']['mae']:.4f} kWh")
    improvement_tuning = energy_results['untuned']['mae'] - energy_results['tuned']['mae']
    improvement_learning = energy_results['tuned_nolearn']['mae'] - energy_results['tuned']['mae']
    print(f"  • Improvement from tuning: {improvement_tuning:.4f} kWh ({improvement_tuning/energy_results['untuned']['mae']*100:.1f}%)")
    print(f"  • Improvement from learning: {improvement_learning:.4f} kWh ({improvement_learning/energy_results['tuned_nolearn']['mae']*100:.1f}%)")


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("CBR SYSTEM - COMPLETE EVALUATION")
    print("6 Test Conditions: 3 Classification + 3 Regression")
    print("="*70)
    
    # Load data
    print("\n[Loading Data]")
    car_train, car_test = load_car_system_data(random_seed=42)
    energy_train, energy_test = load_energy_system_data(random_seed=42)
    print(f"Car data: {len(car_train)} training, {len(car_test)} test")
    print(f"Energy data: {len(energy_train)} training, {len(energy_test)} test")
    
    # Run tests
    car_results = run_car_tests(car_train, car_test)
    energy_results = run_energy_tests(energy_train, energy_test)
    
    # Print summary
    print_results_summary(car_results, energy_results)
    
    return car_results, energy_results


if __name__ == '__main__':
    car_results, energy_results = main()
