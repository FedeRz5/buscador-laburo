import unittest
from tools.check_publication import findings

class PublicationTests(unittest.TestCase):
    def test_example_email_is_allowed(self):
        self.assertEqual(findings("example.md", "contacto@example.com"), [])

    def test_personal_email_is_flagged_without_echoing_it(self):
        address = "persona" + "@" + "correo.invalid"
        result = findings("profile.md", address)
        self.assertTrue(result)
        self.assertNotIn(address, str(result))

    def test_missing_template_marker_is_flagged(self):
        self.assertTrue(findings("CLAUDE.md", "Perfil personalizado"))

    def test_private_key_is_flagged(self):
        self.assertTrue(findings("config.txt", "-----BEGIN " + "PRIVATE KEY-----"))
