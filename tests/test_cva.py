"""Tests for djinn.core.cva"""

from djinn.core.cva import cva


class TestCVA:
    def test_base_only(self):
        button = cva(base="btn")
        assert button() == "btn"

    def test_default_variant_applied(self):
        button = cva(
            base="btn",
            variants={"size": {"sm": "btn-sm", "lg": "btn-lg"}},
            default_variants={"size": "sm"},
        )
        assert button() == "btn btn-sm"

    def test_explicit_variant_overrides_default(self):
        button = cva(
            base="btn",
            variants={"size": {"sm": "btn-sm", "lg": "btn-lg"}},
            default_variants={"size": "sm"},
        )
        assert button(size="lg") == "btn btn-lg"

    def test_unknown_variant_ignored(self):
        button = cva(
            base="btn",
            variants={"size": {"sm": "btn-sm"}},
            default_variants={"size": "sm"},
        )
        # Explicitly passing an unknown variant yields just the base (no fallback)
        assert button(size="xl") == "btn"
        # Omitting the variant entirely falls back to the default
        assert button() == "btn btn-sm"

    def test_extra_class_merged(self):
        button = cva(base="btn")
        assert button(class_="extra-class") == "btn extra-class"
        assert button(className="extra-class") == "btn extra-class"
        assert button(**{"class": "extra-class"}) == "btn extra-class"

    def test_tailwind_merge_deduplicates(self):
        from tailwind_merge import TailwindMerge

        button = cva(base="px-4 py-2")
        result = button(class_="px-6")
        # tailwind-merge should dedupe conflicting px utilities
        assert "px-6" in result
        assert "px-4" not in result

    def test_multiple_variants(self):
        button = cva(
            base="btn",
            variants={
                "variant": {"default": "bg-primary", "destructive": "bg-red"},
                "size": {"sm": "text-sm", "lg": "text-lg"},
            },
            default_variants={"variant": "default", "size": "sm"},
        )
        assert button(variant="destructive", size="lg") == "btn bg-red text-lg"
