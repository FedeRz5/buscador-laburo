import subprocess
import unittest
from unittest.mock import patch
from buscar import construir_comando, crear_parser, main


class BuscarArgentinaTests(unittest.TestCase):
    def command(self, *args):
        return construir_comando(crear_parser().parse_args(list(args)))

    def test_default_is_linkedin_argentina(self):
        cmd = self.command("administrativo")
        self.assertEqual(cmd[cmd.index("--location") + 1], "Argentina")
        self.assertEqual(cmd[cmd.index("--jobage") + 1], "14")

    def test_city_keeps_country_and_remote_filter(self):
        cmd = self.command("ventas", "--ciudad", "Córdoba", "--modalidad", "remoto")
        self.assertEqual(cmd[cmd.index("--location") + 1], "Córdoba, Argentina")
        self.assertEqual(cmd[cmd.index("--remote") + 1], "remote")

    def test_freehire_always_sets_argentina(self):
        cmd = self.command("python", "--portal", "freehire", "--ciudad", "Rosario")
        self.assertEqual(cmd[cmd.index("--country") + 1], "AR")
        self.assertEqual(cmd[cmd.index("--city") + 1], "Rosario")

    def test_getonbrd_country_and_boolean_remote(self):
        cmd = self.command("diseño", "--portal", "getonbrd", "--modalidad", "remoto")
        self.assertEqual(cmd[cmd.index("--location") + 1], "Argentina")
        self.assertIn("--remote", cmd)
        self.assertNotIn("remote", cmd)

    def test_unsupported_filters_fail_instead_of_being_ignored(self):
        for flags in [("--ciudad", "Córdoba"), ("--modalidad", "hibrido"), ("--modalidad", "presencial")]:
            with self.subTest(flags=flags), self.assertRaises(ValueError):
                self.command("diseño", "--portal", "getonbrd", *flags)

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            self.command("   ")

    def test_query_stays_one_argument_without_a_shell(self):
        query = "ventas; echo ejemplo"
        cmd = self.command(query)
        self.assertEqual(cmd[cmd.index("--query") + 1], query)

    @patch("buscar.subprocess.run")
    @patch("buscar.shutil.which", return_value="bun")
    def test_portal_exit_code_propagates(self, which, run):
        run.return_value.returncode = 1
        self.assertEqual(main(["ventas"]), 1)
        self.assertNotIn("shell", run.call_args.kwargs)

    @patch("buscar.shutil.which", return_value=None)
    def test_missing_bun_returns_error(self, which):
        self.assertEqual(main(["ventas"]), 1)

    @patch("buscar.subprocess.run", side_effect=subprocess.TimeoutExpired("bun", 120))
    @patch("buscar.shutil.which", return_value="bun")
    def test_timeout_returns_error(self, which, run):
        self.assertEqual(main(["ventas"]), 1)
