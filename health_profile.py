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

# ============================================================
# THE HEALTHPROFILE CLASS
# ============================================================


@dataclass
class HealthProfile:
    """
    A validated collection of health measurements for diabetes risk assessment.

    This class bundles all the health metrics a user enters, validates them,
    and provides convenient methods for working with the data.

    Attributes:
        glucose: Plasma glucose concentration (mg/dL) - 2 hours after oral glucose
        blood_pressure: Diastolic blood pressure (mm Hg)
        bmi: Body mass index (weight in kg / height in m²)
        age: Age in years
        skin_thickness: Triceps skin fold thickness (mm) - Optional
        insulin: 2-Hour serum insulin (mu U/ml) - Optional
        pregnancies: Number of pregnancies - Optional, defaults to 0
        diabetes_pedigree: Diabetes pedigree function score - Optional

    Example:
        # Create a basic profile (required fields only)
        profile = HealthProfile(
            glucose=120,
            blood_pressure=80,
            bmi=28.5,
            age=45
        )

        # Create a full profile (all fields)
        full_profile = HealthProfile(
            glucose=120,
            blood_pressure=80,
            bmi=28.5,
            age=45,
            skin_thickness=25,
            insulin=130,
            pregnancies=2,
            diabetes_pedigree=0.5
        )

        # Check if valid
        if profile.is_valid():
            print("Ready for analysis")
        else:
            print(profile.validation_errors)
    """

    # ----------------------------------------------------------
    # REQUIRED FIELDS (must be provided)
    # ----------------------------------------------------------
    # These are the core measurements needed for basic risk assessment

    glucose: float
    blood_pressure: float
    bmi: float
    age: int

    # ----------------------------------------------------------
    # OPTIONAL FIELDS (have default values)
    # ----------------------------------------------------------
    # These enhance the assessment but aren't always available
    # Note: Optional fields must come AFTER required fields in a dataclass

    skin_thickness: Optional[float] = None
    insulin: Optional[float] = None
    pregnancies: int = 0
    diabetes_pedigree: Optional[float] = None

    # ----------------------------------------------------------
    # INTERNAL FIELDS (not set by user)
    # ----------------------------------------------------------
    # field(default_factory=list) creates a new empty list for each instance
    # This stores any validation errors found

    _validation_errors: List[str] = field(default_factory=list, repr=False)

    def __post_init__(self):
        """
        Called automatically after __init__ creates the object.

        This is a special @dataclass feature - it runs after all the
        fields are set, perfect for validation.

        ANALOGY: Like the nurse checking the admission form after
        the patient fills it in - making sure everything makes sense
        before sending it to the doctor.
        """
        self._validation_errors = []  # Clear any previous errors
        self._validate()

    # ============================================================
    # VALIDATION METHODS
    # ============================================================

    def _validate(self) -> None:
        """
        Check all fields against valid ranges.

        Private method (starts with _) - only called internally.
        Populates self._validation_errors with any problems found.
        """
        # Validate required fields
        self._check_range('glucose', self.glucose)
        self._check_range('blood_pressure', self.blood_pressure)
        self._check_range('bmi', self.bmi)
        self._check_range('age', self.age)

        # Validate optional fields (only if provided)
        if self.skin_thickness is not None:
            self._check_range('skin_thickness', self.skin_thickness)

        if self.insulin is not None:
            self._check_range('insulin', self.insulin)

        if self.pregnancies != 0:  # 0 is always valid
            self._check_range('pregnancies', self.pregnancies)

        if self.diabetes_pedigree is not None:
            self._check_range('diabetes_pedigree', self.diabetes_pedigree)

    def _check_range(self, field_name: str, value: float) -> None:
        """
        Check if a single value is within its valid range.

        Args:
            field_name: Name of the field (must match VALID_RANGES keys)
            value: The value to check
        """
        if field_name not in VALID_RANGES:
            return  # Skip if no range defined

        min_val, max_val = VALID_RANGES[field_name]

        if value < min_val:
            self._validation_errors.append(
                f"{field_name.replace('_', ' ').title()} ({value}) is below "
                f"minimum expected value ({min_val})"
            )
        elif value > max_val:
            self._validation_errors.append(
                f"{field_name.replace('_', ' ').title()} ({value}) is above "
                f"maximum expected value ({max_val})"
            )

    def is_valid(self) -> bool:
        """
        Check if the profile passes all validation.

        Returns:
            True if no validation errors, False otherwise

        Example:
            if profile.is_valid():
                # Safe to proceed with analysis
                results = analyzer.analyze(profile)
            else:
                # Show errors to user
                for error in profile.validation_errors:
                    st.error(error)
        """
        return len(self._validation_errors) == 0

    @property
    def validation_errors(self) -> List[str]:
        """
        Get list of validation error messages.

        Using @property means you access it like an attribute:
            profile.validation_errors  (not profile.validation_errors())

        Returns:
            List of error message strings (empty if valid)
        """
        return self._validation_errors.copy()  # Return a copy to prevent modification

    # ============================================================
    # DATA ACCESS METHODS
    # ============================================================

    def to_dict(self) -> Dict[str, float]:
        """
        Convert profile to a dictionary.

        Useful for:
        - Saving to a file or database
        - Passing to pandas functions
        - Displaying in a table

        Returns:
            Dictionary with all field names and values

        Example:
            profile_dict = profile.to_dict()
            # {'glucose': 120, 'blood_pressure': 80, 'bmi': 28.5, ...}
        """
        result = {
            'glucose': self.glucose,
            'blood_pressure': self.blood_pressure,
            'bmi': self.bmi,
            'age': self.age,
            'pregnancies': self.pregnancies,
        }

        # Only include optional fields if they have values
        if self.skin_thickness is not None:
            result['skin_thickness'] = self.skin_thickness

        if self.insulin is not None:
            result['insulin'] = self.insulin

        if self.diabetes_pedigree is not None:
            result['diabetes_pedigree'] = self.diabetes_pedigree

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'HealthProfile':
        """
        Create a HealthProfile from a dictionary.

        @classmethod means this is called on the CLASS, not an instance:
            profile = HealthProfile.from_dict(my_dict)

        Useful for:
        - Loading saved profiles
        - Creating from form data
        - Converting pandas rows to profiles

        Args:
            data: Dictionary with field names and values

        Returns:
            New HealthProfile instance

        Example:
            saved_data = {'glucose': 120, 'blood_pressure': 80, 'bmi': 28.5, 'age': 45}
            profile = HealthProfile.from_dict(saved_data)
        """
        return cls(
            glucose=data.get('glucose', 0),
            blood_pressure=data.get('blood_pressure', 0),
            bmi=data.get('bmi', 0),
            age=data.get('age', 0),
            skin_thickness=data.get('skin_thickness'),
            insulin=data.get('insulin'),
            pregnancies=data.get('pregnancies', 0),
            diabetes_pedigree=data.get('diabetes_pedigree')
        )

    def get_core_features(self) -> Dict[str, float]:
        """
        Get only the four core features used in basic analysis.

        Returns:
            Dictionary with glucose, blood_pressure, bmi, age
        """
        return {
            'glucose': self.glucose,
            'blood_pressure': self.blood_pressure,
            'bmi': self.bmi,
            'age': self.age
        }

    def get_available_features(self) -> List[str]:
        """
        Get list of features that have values (not None).

        Useful when you want to know which optional fields were provided.

        Returns:
            List of feature names that have values
        """
        features = ['glucose', 'blood_pressure', 'bmi', 'age', 'pregnancies']

        if self.skin_thickness is not None:
            features.append('skin_thickness')
        if self.insulin is not None:
            features.append('insulin')
        if self.diabetes_pedigree is not None:
            features.append('diabetes_pedigree')

        return features

    # ============================================================
    # DISPLAY METHODS
    # ============================================================

    def summary(self) -> str:
        """
        Get a human-readable summary of the profile.

        Returns:
            Formatted string showing all values
        """
        lines = [
            "Health Profile Summary",
            "=" * 30,
            f"Age:              {self.age} years",
            f"BMI:              {self.bmi:.1f} kg/m²",
            f"Glucose:          {self.glucose:.0f} mg/dL",
            f"Blood Pressure:   {self.blood_pressure:.0f} mm Hg",
            f"Pregnancies:      {self.pregnancies}",
        ]

        if self.skin_thickness is not None:
            lines.append(f"Skin Thickness:   {self.skin_thickness:.1f} mm")

        if self.insulin is not None:
            lines.append(f"Insulin:          {self.insulin:.0f} mu U/ml")

        if self.diabetes_pedigree is not None:
            lines.append(f"Pedigree Score:   {self.diabetes_pedigree:.3f}")

        lines.append("=" * 30)

        if self.is_valid():
            lines.append("✓ All values within expected ranges")
        else:
            lines.append(
                f"⚠ {len(self._validation_errors)} validation issue(s)")

        return "\n".join(lines)


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("HealthProfile Class - Examples")
    print("=" * 50)

    # Example 1: Valid profile with required fields only
    print("\n--- Example 1: Basic Valid Profile ---")
    profile1 = HealthProfile(
        glucose=120,
        blood_pressure=80,
        bmi=28.5,
        age=45
    )
    print(profile1.summary())
    print(f"\nIs valid: {profile1.is_valid()}")

    # Example 2: Full profile with all fields
    print("\n--- Example 2: Full Profile ---")
    profile2 = HealthProfile(
        glucose=148,
        blood_pressure=72,
        bmi=33.6,
        age=50,
        skin_thickness=35,
        insulin=0,  # This will be invalid (below minimum)
        pregnancies=6,
        diabetes_pedigree=0.627
    )
    print(profile2.summary())
    print(f"\nIs valid: {profile2.is_valid()}")
    if not profile2.is_valid():
        print("Validation errors:")
        for error in profile2.validation_errors:
            print(f"  - {error}")

    # Example 3: Invalid values
    print("\n--- Example 3: Invalid Profile ---")
    profile3 = HealthProfile(
        glucose=500,    # Too high!
        blood_pressure=10,  # Too low!
        bmi=28.5,
        age=45
    )
    print(f"Is valid: {profile3.is_valid()}")
    print("Validation errors:")
    for error in profile3.validation_errors:
        print(f"  - {error}")

    # Example 4: Converting to/from dictionary
    print("\n--- Example 4: Dictionary Conversion ---")
    profile_dict = profile1.to_dict()
    print(f"As dictionary: {profile_dict}")

    # Recreate from dictionary
    profile_restored = HealthProfile.from_dict(profile_dict)
    print(f"Restored profile is valid: {profile_restored.is_valid()}")

    # Example 5: Get available features
    print("\n--- Example 5: Available Features ---")
    print(f"Profile 1 features: {profile1.get_available_features()}")
    print(f"Profile 2 features: {profile2.get_available_features()}")
