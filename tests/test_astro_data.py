from astro_computation import astro_data

def test_astro_data():
    docs = astro_data("2025-07-03T00:00:00Z", "Taiwan")
    assert len(docs) == 3

