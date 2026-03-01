"""
Interactive CBR Tester
======================
Runs all 6 evaluation conditions, then lets you enter your own queries.
"""

from data_loader import load_car_system_data, load_energy_system_data, Case
from car_cbr import CarCBRSystem
from energy_cbr import EnergyCBRSystem
from evaluation import Evaluator
import warnings
warnings.filterwarnings('ignore')  # suppress numpy divide warnings


def run_full_evaluation(car_train, car_test, energy_train, energy_test):
    print("\n" + "="*60)
    print("RUNNING ALL 6 CONDITIONS")
    print("="*60)

    # --- CAR ---
    print("\n--- CAR CLASSIFICATION ---")
    car_sys = CarCBRSystem()
    car_sys.set_case_base(car_train)

    car_sys.set_baseline_mode()
    cb = car_sys.case_base.copy()
    preds = [car_sys.run_query(cb, t, tuned=False, learning=False)[0] for t in car_test]
    acc1 = Evaluator.calculate_accuracy(preds, [c.solution for c in car_test])
    print(f"  Condition 1 - Untuned (baseline, no adapt):     {acc1:.2f}%")

    car_sys.set_tuned_mode()
    cb = car_sys.case_base.copy()
    preds = [car_sys.run_query(cb, t, tuned=True, learning=False)[0] for t in car_test]
    acc2 = Evaluator.calculate_accuracy(preds, [c.solution for c in car_test])
    print(f"  Condition 2 - Tuned (weighted, no adapt):       {acc2:.2f}%")

    car_sys.set_tuned_mode()
    cb = car_sys.case_base.copy()
    def car_adapt(r, q, s): return car_sys.adapt_classification(r, q, use_voting=True)
    preds = [car_sys.run_query(cb, t, tuned=True, adapt_fn=car_adapt, learning=False)[0] for t in car_test]
    acc3 = Evaluator.calculate_accuracy(preds, [c.solution for c in car_test])
    print(f"  Condition 3 - Tuned + Adaptation:               {acc3:.2f}%")

    # --- ENERGY ---
    print("\n--- ENERGY REGRESSION ---")
    en_sys = EnergyCBRSystem()
    en_sys.set_case_base(energy_train)

    en_sys.set_baseline_mode()
    cb = en_sys.case_base.copy()
    preds = []
    for t in energy_test:
        r = en_sys.run_query(cb, t, tuned=False, learning=True)
        preds.append(r[0]); cb = r[1]
    mae1 = Evaluator.calculate_mae(preds, [c.solution for c in energy_test])
    rmse1 = Evaluator.calculate_rmse(preds, [c.solution for c in energy_test])
    print(f"  Condition 4 - Untuned (baseline, learn ON):     MAE={mae1:.4f}  RMSE={rmse1:.4f}")

    en_sys.set_tuned_mode()
    cb = en_sys.case_base.copy()
    def en_adapt(r, q, s): return en_sys.adapt_regression(r, q, use_multiple_rules=True)
    preds = []
    for t in energy_test:
        r = en_sys.run_query(cb, t, tuned=True, adapt_fn=en_adapt, learning=True)
        preds.append(r[0]); cb = r[1]
    mae2 = Evaluator.calculate_mae(preds, [c.solution for c in energy_test])
    rmse2 = Evaluator.calculate_rmse(preds, [c.solution for c in energy_test])
    print(f"  Condition 5 - Tuned+Adapt (learn ON):           MAE={mae2:.4f}  RMSE={rmse2:.4f}")

    en_sys.set_tuned_mode()
    cb = en_sys.case_base.copy()
    preds = [en_sys.run_query(cb, t, tuned=True, adapt_fn=en_adapt, learning=False)[0] for t in energy_test]
    mae3 = Evaluator.calculate_mae(preds, [c.solution for c in energy_test])
    rmse3 = Evaluator.calculate_rmse(preds, [c.solution for c in energy_test])
    print(f"  Condition 6 - Tuned+Adapt (learn OFF):          MAE={mae3:.4f}  RMSE={rmse3:.4f}")

    return car_sys, en_sys


def interactive_car_query(car_sys):
    print("\n" + "="*60)
    print("ENTER YOUR OWN CAR QUERY")
    print("="*60)
    print("Valid values:")
    print("  buying / maint : vhigh | high | med | low")
    print("  doors          : 2 | 3 | 4 | 5more")
    print("  persons        : 2 | 4 | more")
    print("  lug_boot       : small | med | big")
    print("  safety         : low | med | high")
    print()

    fields = {
        'buying':   ['vhigh', 'high', 'med', 'low'],
        'maint':    ['vhigh', 'high', 'med', 'low'],
        'doors':    ['2', '3', '4', '5more'],
        'persons':  ['2', '4', 'more'],
        'lug_boot': ['small', 'med', 'big'],
        'safety':   ['low', 'med', 'high'],
    }

    features = {}
    for field, options in fields.items():
        while True:
            val = input(f"  {field} ({'/'.join(options)}): ").strip().lower()
            if val in options:
                features[field] = val
                break
            print(f"    ⚠️  Invalid. Choose from: {options}")

    query = Case(features=features, solution=None)
    cb = car_sys.case_base.copy()

    car_sys.set_baseline_mode()
    r1 = car_sys.run_query(cb, query, tuned=False, adapt_fn=None, learning=False)

    car_sys.set_tuned_mode()
    r2 = car_sys.run_query(cb, query, tuned=True, adapt_fn=None, learning=False)

    def car_adapt(r, q, s): return car_sys.adapt_classification(r, q, use_voting=True)
    r3 = car_sys.run_query(cb, query, tuned=True, adapt_fn=car_adapt, learning=False)

    retrieved, sim = car_sys.retrieve_most_similar(query, use_weights=True)

    print(f"\n  Results:")
    print(f"    Baseline prediction:   {r1[0]}")
    print(f"    Tuned prediction:      {r2[0]}")
    print(f"    Tuned+Adapt prediction:{r3[0]}")
    print(f"    Most similar case:     {dict(retrieved.features)} → {retrieved.solution}  (sim={sim:.3f})")


def interactive_energy_query(en_sys):
    print("\n" + "="*60)
    print("ENTER YOUR OWN ENERGY QUERY")
    print("="*60)
    print("Enter normalized (z-score) values. Typical range: -2.0 to 2.0")
    print("  0.0  = exactly average")
    print("  1.5  = well above average")
    print(" -1.5  = well below average")
    print()

    fields = [
        'relative_compactness',
        'surface_area',
        'wall_area',
        'roof_area',
        'orientation',
        'glazing_area',
        'glazing_area_distribution',
        'glazing_type',
    ]

    features = {}
    for field in fields:
        while True:
            try:
                val = float(input(f"  {field}: ").strip())
                features[field] = val
                break
            except ValueError:
                print("    ⚠️  Please enter a number (e.g. 0.5 or -1.2)")

    query = Case(features=features, solution=None)
    ecb = en_sys.case_base.copy()

    en_sys.set_baseline_mode()
    r1 = en_sys.run_query(ecb, query, tuned=False, adapt_fn=None, learning=False)

    en_sys.set_tuned_mode()
    def en_adapt(r, q, s): return en_sys.adapt_regression(r, q, use_multiple_rules=True)
    r2 = en_sys.run_query(ecb, query, tuned=True, adapt_fn=en_adapt, learning=False)

    retrieved, sim = en_sys.retrieve_most_similar(query, use_weights=True)

    print(f"\n  Results:")
    print(f"    Baseline prediction:    {r1[0]:.2f} kWh")
    print(f"    Tuned+Adapt prediction: {r2[0]:.2f} kWh")
    print(f"    Most similar case:      {retrieved.solution:.2f} kWh  (sim={sim:.4f})")


def main():
    print("\nLoading datasets...")
    car_train, car_test = load_car_system_data(random_seed=42)
    energy_train, energy_test = load_energy_system_data(random_seed=42)

    car_sys, en_sys = run_full_evaluation(car_train, car_test, energy_train, energy_test)

    while True:
        print("\n" + "="*60)
        print("INTERACTIVE QUERY MODE")
        print("="*60)
        print("  1 - Test a car query")
        print("  2 - Test an energy query")
        print("  q - Quit")
        choice = input("\nYour choice: ").strip().lower()

        if choice == '1':
            interactive_car_query(car_sys)
        elif choice == '2':
            interactive_energy_query(en_sys)
        elif choice == 'q':
            print("Bye!")
            break
        else:
            print("Please enter 1, 2, or q.")


if __name__ == '__main__':
    main()
