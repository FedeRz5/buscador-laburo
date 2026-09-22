"""Tests for salary_lookup.py — format_entry, match_score, and search_company."""

import unittest

from salary_lookup import (
    format_entry,
    normalize,
    anglicize,
    extract_core_words,
    match_score,
    search_company,
)


# ---------------------------------------------------------------------------
# format_entry tests (from #75 / #98)
# ---------------------------------------------------------------------------

class FormatEntryTests(unittest.TestCase):
    def test_zero_count_is_displayed_as_zero(self):
        entry = {
            "company": "Example Corp",
            "city": "",
            "categories": {
                "public_data": {
                    "count": 0,
                    "index": 100.0,
                },
            },
        }

        rendered = format_entry(entry, {"index_baseline": 100, "index_label": "Index"})

        self.assertRegex(rendered, r"Public Data\s+0\s+100\.0")

    def test_text_index_does_not_crash(self):
        entry = {
            "company": "Example Corp",
            "city": "",
            "categories": {
                "sample": {
                    "count": 3,
                    "index": "private",
                },
            },
        }

        rendered = format_entry(entry, {"index_baseline": 100, "index_label": "Index"})

        self.assertIn("private", rendered)

    def test_format_entry_with_zero_baseline(self):
        entry = {
            "company": "Example Corp",
            "city": "",
            "categories": {
                "it": {
                    "count": None,
                    "index": 45000.0,
                },
            },
        }
        rendered = format_entry(entry, {"index_baseline": 0, "index_label": "Salary"})
        self.assertIn("45000.0", rendered)
        self.assertNotIn("%", rendered)

    def test_format_entry_with_custom_baseline(self):
        entry = {
            "company": "Example Corp",
            "city": "",
            "categories": {
                "it": {
                    "count": None,
                    "index": 45000.0,
                },
            },
        }
        rendered = format_entry(entry, {"index_baseline": 40000, "index_label": "Salary"})
        self.assertIn("45000.0", rendered)
        self.assertIn("+12.5%", rendered)


# ---------------------------------------------------------------------------
# match_score tests (from #106)
# ---------------------------------------------------------------------------

class TestMatchScoreExactMatch(unittest.TestCase):
    def test_exact_match_returns_100(self):
        self.assertEqual(match_score("Luna Sistemas", "Luna Sistemas"), 100)

    def test_exact_match_case_insensitive(self):
        self.assertEqual(match_score("LUNA SISTEMAS", "Luna Sistemas"), 100)

    def test_exact_match_after_suffix_stripping(self):
        self.assertEqual(match_score("Peña", "Peña S.A."), 100)


class TestMatchScoreSubstring(unittest.TestCase):
    def test_query_contained_in_entry_gives_high_score(self):
        score = match_score("Sol Bebidas", "Sol Bebidas Argentina S.A.")
        self.assertGreaterEqual(score, 80)

    def test_entry_contained_in_query_gives_high_score(self):
        score = match_score("Sol Bebidas Argentina", "Sol Bebidas")
        self.assertGreaterEqual(score, 80)


class TestMatchScoreShortQuery(unittest.TestCase):
    def test_short_query_no_word_overlap_returns_zero(self):
        score = match_score("ab", "Something Unrelated Company")
        self.assertEqual(score, 0)

    def test_short_query_with_word_overlap_scores(self):
        score = match_score("IBM", "IBM Corporation")
        self.assertGreater(score, 0)


class TestMatchScoreAnglicize(unittest.TestCase):
    def test_name_with_tilde_matches_without_it(self):
        score = match_score("Pena", "Peña S.A.")
        self.assertGreater(score, 0)

    def test_plain_name_matches_itself(self):
        self.assertEqual(match_score("Andes", "Andes"), 100)

    def test_spanish_characters_roundtrip(self):
        score = match_score("Pena", "Peña S.A.")
        self.assertGreater(score, 0)


class TestMatchScoreNoOverlap(unittest.TestCase):
    def test_completely_unrelated_names_return_zero(self):
        self.assertEqual(match_score("Apple", "Viento Energía"), 0)

    def test_empty_query_returns_zero(self):
        self.assertEqual(match_score("", "Luna Sistemas"), 0)

    def test_empty_entry_returns_zero(self):
        self.assertEqual(match_score("Luna Sistemas", ""), 0)


# ---------------------------------------------------------------------------
# search_company tests (from #75 / #98 and #106)
# ---------------------------------------------------------------------------

def _make_data(*entries):
    return {"companies": list(entries)}


def _entry(company, city=""):
    return {"company": company, "city": city}


class SearchCompanyTests(unittest.TestCase):
    def test_search_company_with_none_city(self):
        data = {
            "companies": [
                {
                    "company": "Acme",
                    "city": None,
                }
            ]
        }
        results = search_company(data, "Acme", city="Córdoba")
        self.assertEqual(results, [])


class UtilityTests(unittest.TestCase):
    def test_normalize_strips_suffix_and_noise(self):
        self.assertEqual(normalize("Luna Sistemas S.A."), "lunasistemas")
        self.assertEqual(normalize("Álamo (VG) Holding"), "álamo")
        self.assertEqual(normalize("Chr. Hansen, División Argentina"), "chrhansen")
        self.assertEqual(normalize("Simple Corp S.R.L."), "simplecorp")

    def test_anglicize_replaces_spanish_chars(self):
        self.assertEqual(anglicize("álamo"), "alamo")
        self.assertEqual(anglicize("peña"), "pena")
        self.assertEqual(anglicize("córdoba"), "cordoba")

    def test_extract_core_words(self):
        self.assertEqual(extract_core_words("Luna Sistemas S.A."), ["luna", "sistemas"])
        self.assertEqual(extract_core_words("S.A."), [])
        self.assertEqual(extract_core_words("Test Company (Sub-entity)"), ["test", "company"])


class MatchScoreTests(unittest.TestCase):
    def test_exact_match_score(self):
        self.assertEqual(match_score("Luna Sistemas", "Luna Sistemas"), 100)
        self.assertEqual(match_score("luna sistemas", "Luna Sistemas S.A."), 100)

    def test_partial_match_score(self):
        self.assertGreater(match_score("Luna", "Luna Sistemas S.A."), 80)
        self.assertEqual(match_score("Luna Sistemas", "Luna"), 75)

    def test_anglicized_match_score(self):
        self.assertEqual(match_score("Alamo", "Álamo S.A."), 85)

    def test_overlap_match_score(self):
        # Overlap of multiple words
        self.assertGreater(match_score("Luna Tech", "Luna Sistemas Tech S.A."), 30)

    def test_no_match_score(self):
        self.assertEqual(match_score("Google", "Microsoft"), 0)


class SearchCompanyRefactoredTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "companies": [
                {"company": "Luna Sistemas S.A.", "city": "Rosario"},
                {"company": "Álamo", "city": "Mendoza"},
                {"company": "Viento Energía", "city": "Córdoba"},
            ]
        }

    def test_search_by_name(self):
        results = search_company(self.data, "Luna")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["company"], "Luna Sistemas S.A.")

    def test_search_with_city_filter(self):
        results = search_company(self.data, "Álamo", city="Mendoza")
        self.assertEqual(len(results), 1)

        # Mismatching city
        results_wrong_city = search_company(self.data, "Álamo", city="Rosario")
        self.assertEqual(len(results_wrong_city), 0)


class TestSearchCompanyBasicMatch(unittest.TestCase):
    def test_exact_name_returns_match(self):
        data = _make_data(_entry("Luna Sistemas", "Rosario"))
        results = search_company(data, "Luna Sistemas")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["company"], "Luna Sistemas")

    def test_no_match_returns_empty_list(self):
        data = _make_data(_entry("Viento Energía", "Córdoba"))
        results = search_company(data, "Apple")
        self.assertEqual(results, [])

    def test_multiple_candidates_all_returned(self):
        data = _make_data(
            _entry("Sol Bebidas S.A.", "Buenos Aires"),
            _entry("Sol Bebidas Argentina", "Mendoza"),
            _entry("Unrelated Corp", "Salta"),
        )
        results = search_company(data, "Sol Bebidas")
        companies = [r["company"] for r in results]
        self.assertIn("Sol Bebidas S.A.", companies)
        self.assertIn("Sol Bebidas Argentina", companies)
        self.assertNotIn("Unrelated Corp", companies)


class TestSearchCompanyCityFilter(unittest.TestCase):
    def test_matching_city_is_included(self):
        data = _make_data(
            _entry("Luna Sistemas", "Rosario"),
            _entry("Luna Sistemas", "Córdoba"),
        )
        results = search_company(data, "Luna Sistemas", city="Córdoba")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["city"], "Córdoba")

    def test_non_matching_city_is_excluded(self):
        data = _make_data(_entry("Luna Sistemas", "Rosario"))
        results = search_company(data, "Luna Sistemas", city="Salta")
        self.assertEqual(results, [])

    def test_no_city_filter_returns_all_cities(self):
        data = _make_data(
            _entry("Luna Sistemas", "Rosario"),
            _entry("Luna Sistemas", "Córdoba"),
        )
        results = search_company(data, "Luna Sistemas")
        self.assertEqual(len(results), 2)

    def test_city_filter_case_insensitive(self):
        data = _make_data(_entry("Luna Sistemas", "Tucumán"))
        results = search_company(data, "Luna Sistemas", city="tucumán")
        self.assertEqual(len(results), 1)

    def test_anglicized_city_matches_spanish_city(self):
        data = _make_data(_entry("Luna Sistemas", "Tucumán"))
        results = search_company(data, "Luna Sistemas", city="tucuman")
        self.assertEqual(len(results), 1)


class TestSearchCompanyScoreThreshold(unittest.TestCase):
    def test_low_score_matches_excluded(self):
        data = _make_data(_entry("Luna Sistemas", "Rosario"))
        results = search_company(data, "xyz")
        self.assertEqual(results, [])

    def test_results_sorted_by_relevance_descending(self):
        data = _make_data(
            _entry("Luna Sistemas International", "Rosario"),
            _entry("Luna Sistemas", "Rosario"),
        )
        results = search_company(data, "Luna Sistemas")
        self.assertEqual(results[0]["company"], "Luna Sistemas")




class ArgentinaCompanyTests(unittest.TestCase):
    def test_local_legal_suffixes(self):
        for suffix in ["SA", "S.A.", "SRL", "S.R.L.", "SAS", "S.A.S."]:
            with self.subTest(suffix=suffix):
                self.assertEqual(match_score("Empresa Ejemplo", "Empresa Ejemplo " + suffix), 100)

    def test_legal_suffix_does_not_remove_part_of_name(self):
        self.assertEqual(normalize("Casa"), "casa")

    def test_accents_are_preserved_for_matching(self):
        self.assertEqual(normalize("Córdoba"), "córdoba")
        self.assertGreater(match_score("Cordoba", "Córdoba"), 0)


if __name__ == "__main__":
    unittest.main()
