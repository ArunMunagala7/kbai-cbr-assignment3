"""
Interactive Query Tester
========================
Edit the queries below and run:  python query_test.py

CAR feature options:
  buying   : vhigh | high | med | low
  maint    : vhigh | high | med | low
  doors    : 2 | 3 | 4 | 5more
  persons  : 2 | 4 | more
  lug_boot : small | med | big
  safety   : low | med | high

ENERGY features are normalized (z-score). Use values roughly in [-2, 2].
  Positive values = above average for that feature.
  Negative values = below average.
  Typical real-world intuition after normalization:
    relative_compactness : higher = more compact building
    surface_area         : higher = larger surface
    wall_area            : higher = more wall area
    roof_area            : higher = larger roof
    orientation          : 1=North, 2=East, 3=South, 4=West (then z-scored)
    glazing_area         : higher = more glass
    glazing_area_distribution : 0=uniform ... 5=concentrated
    glazing_type         : 0=no glazing ... 5=double glazing
"""

from data_loader import load_car_system_data, load_energy_system_data, Case
from car_cbr import CarCBRSystem
from energy_cbr import EnergyCBRSystem

# ================================================================
#  ✏️  EDIT YOUR CAR QUERY HERE
# ================================================================
my_car_query = Case(features={
    'buying':   'med',      # <-- change me
    'maint':    'low',      # <-- change me
    'doors':    '4',        # <-- change me
    'persons':  'more',     # <-- change me
    'lug_boot': 'big',      # <-- change me
    'safety':   'high'      # <-- change me
}, solution=None)

# ================================================================
#  ✏️  EDIT YOUR ENERGY QUERY HERE (normalized z-score values)
#      0.0 = exactly average,  1.5 = well above average,  -1.5 = well below
# ================================================================
my_energy_query = Case(features={
    'relative_compactness':      1.2,   # <-- change me (compact building)
    'surface_area':             -1.0,   # <-- change me (small surface)
    'wall_area':                 0.5,   # <-- change me
    'roof_area':                -0.5,   # <-- change me
    'orientation':               0.0,   # <-- change me
    'glazing_area':              1.5,   # <-- change me (lots of glazing)
    'glazing_area_distribution': 0.0,   # <-- change me
    'glazing_type':              0.0    # <-- change me
}, solution=None)


# ================================================================
#  RUN — no need to edit below this line
# ================================================================

def test_car(query):
    print("=" * 60)
    print("CAR CLASSIFICATION QUERY")
    print("=" * 60)
    print("  Your query:")
    for k, v in query.features.items():
        print(f"    {k}: {v}")

    train, _ = load_car_system_data(random_seed=42)
    sys = CarCBRSystem()
    sys.set_case_base(train)
    cb = sys.case_base.copy()

    # Baseline
    sys.set_baseline_mode()
    r_base = sys.run_query(cb, query, tuned=False, adapt_fn=None, learning=False)
    print(f"\n  [Baseline]       Prediction: {r_base[0]}")

    # Tuned
    sys.set_tuned_mode()
    r_tuned = sys.run_query(cb, query, tuned=True, adapt_fn=None, learning=False)
    print(f"  [Tuned]          Prediction: {r_tuned[0]}")

    # Tuned + Adaptation
    def adapt_fn(retrieved, q, s):
        return sys.adapt_classification(retrieved, q, use_voting=True)
    r_adapt = sys.run_query(cb, query, tuned=True, adapt_fn=adapt_fn, learning=False)
    print(f"  [Tuned+Adapt]    Prediction: {r_adapt[0]}")

    # Show most similar case
    retrieved, sim = sys.retrieve_most_similar(query, use_weights=True)
    print(f"\n  Most similar case in CB:")
    for k, v in retrieved.features.items():
        print(f"    {k}: {v}")
    print(f"  -> Solution: {retrieved.solution}  (similarity: {sim:.3f})")


def test_energy(query):
    print("\n" + "=" * 60)
    print("ENERGY REGRESSION QUERY")
    print("=" * 60)
    print("  Your query (normalized values):")
    for k, v in query.features.items():
        print(f"    {k}: {v:.2f}")

    train, _ = load_energy_system_data(random_seed=42)
    sys = EnergyCBRSystem()
    sys.set_case_base(train)
    ecb = sys.case_base.copy()

    # Baseline
    sys.set_baseline_mode()
    r_base = sys.run_query(ecb, query, tuned=False, adapt_fn=None, learning=False)
    print(f"\n  [Baseline]       Predicted heating load: {r_base[0]:.2f} kWh")

    # Tuned + Adaptation
    sys.set_tuned_mode()
    def adapt_fn(retrieved, q, s):
        return sys.adapt_regression(retrieved, q, use_multiple_rules=True)
    r_adapt = sys.run_query(ecb, query, tuned=True, adapt_fn=adapt_fn, learning=False)
    print(f"  [Tuned+Adapt]    Predicted heating load: {r_adapt[0]:.2f} kWh")

    # Show most similar case
    retrieved, sim = sys.retrieve_most_similar(query, use_weights=True)
    print(f"\n  Most similar case in CB:")
    print(f"  -> Heating load: {retrieved.solution:.2f} kWh  (similarity: {sim:.4f})")


if __name__ == '__main__':
    test_car(my_car_query)
    test_energy(my_energy_query)
