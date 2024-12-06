# class TestAccessibility:
#
#     def test_accessibility_default_counts(self, axe_playwright, page):
#         axe_playwright.check_accessibility(page)
#
#     def test_accessibility_custom_counts(self, axe_playwright, page):
#         axe_playwright.check_accessibility(page, maximum_allowed_violations_by_impact={
#                 "minor": 2,
#                 "moderate": 5,
#                 "serious": 0,
#                 "critical": 0,
#             }
#         )
