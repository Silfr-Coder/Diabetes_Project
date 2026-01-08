from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ============================================================
# VALIDATION RANGES
# ============================================================
# These come from the raw data cleaning.
# These ranges define what's "realistic" for each measurement.

VALID_RANGES = {
    # 0 is valid here (men, or women with no pregnancies)
    'pregnancies': (0, 20),
    # Fasting glucose in mg/dL (you found min was 44 in cleaned data)
    'glucose': (44, 199),
    # Diastolic BP in mm Hg (from your cleaned data)
    'blood_pressure': (24, 122),
    # Triceps fold in mm (from your cleaned data)
    'skin_thickness': (7, 99),
    'insulin': (14, 846),          # 2-hour serum insulin in mu U/ml
    'bmi': (18.2, 67.1),           # Body mass index (from your cleaned data)
    'diabetes_pedigree': (0.078, 2.42),  # Diabetes pedigree function
    'age': (21, 81)                # Age in years (dataset was women 21+)
}
