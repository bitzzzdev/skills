import unittest

from scan import scan_text


class WritingStyleTests(unittest.TestCase):
    def warnings(self, text):
        _, soft = scan_text("<test>", text)
        return [item[2] for item in soft]

    def test_flags_generic_standards_heading(self):
        self.assertIn(
            "generic standards language that should be replaced with project facts",
            self.warnings("## Engineering and Writing Standards"),
        )

    def test_flags_policy_announcement(self):
        self.assertIn(
            "generic standards language that should be replaced with project facts",
            self.warnings("All prose follows strict human writing standards."),
        )

    def test_flags_generic_configuration_rule(self):
        self.assertIn(
            "generic standards language that should be replaced with project facts",
            self.warnings("Configurations must include exact file locations."),
        )

    def test_accepts_actual_project_details(self):
        warnings = self.warnings(
            "The service reads config/server.toml. Set port to an integer and restart the service."
        )
        self.assertNotIn(
            "generic standards language that should be replaced with project facts",
            warnings,
        )

    def test_accepts_first_person_maintainer_voice(self):
        self.assertNotIn(
            "third-person maintainer narration",
            self.warnings("I tested the session route against the local server."),
        )


if __name__ == "__main__":
    unittest.main()
