from typing import Dict, Any, Optional
from tailwind_merge import TailwindMerge

class cva:
    """
    Class Variance Authority (CVA) for Python/Django.
    Allows declarative class management with variants.
    """
    def __init__(
        self,
        base: str = "",
        variants: Optional[Dict[str, Dict[str, str]]] = None,
        default_variants: Optional[Dict[str, str]] = None
    ):
        self.base = base
        self.variants = variants or {}
        self.default_variants = default_variants or {}

    def __call__(self, **kwargs) -> str:
        classes = [self.base]

        for variant_name, variant_options in self.variants.items():
            # Get the variant value from kwargs or use the default
            variant_value = kwargs.get(variant_name)
            
            # Use default if not provided
            if variant_value is None:
                variant_value = self.default_variants.get(variant_name)

            if variant_value and str(variant_value) in variant_options:
                classes.append(variant_options[str(variant_value)])

        # Merge with user-provided extra classes
        extra_class = kwargs.get("class_") or kwargs.get("className") or kwargs.get("class")
        if extra_class:
            classes.append(extra_class)

        return TailwindMerge().merge(" ".join(filter(None, classes)))
