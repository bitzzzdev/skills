import unittest

from scan import scan_text


class OwnerVoiceTests(unittest.TestCase):
    def warning_names(self, text):
        _, warnings = scan_text("<test>", text, False)
        return [warning[2] for warning in warnings]

    def test_flags_third_person_maintainer_actions(self):
        warnings = self.warning_names("The developer implemented the parser.")
        self.assertIn(
            "third-person maintainer narration (use first person when describing your own work)",
            warnings,
        )

    def test_flags_ai_self_reference(self):
        warnings = self.warning_names("As an AI, I could not run the build.")
        self.assertIn(
            "AI or assistant self-reference in a project deliverable",
            warnings,
        )

    def test_accepts_first_person_maintainer_voice(self):
        warnings = self.warning_names("I implemented the parser and checked its tests.")
        self.assertNotIn(
            "third-person maintainer narration (use first person when describing your own work)",
            warnings,
        )

    def test_accepts_direct_reader_instruction(self):
        warnings = self.warning_names("Run the setup command from the repository root.")
        self.assertNotIn(
            "third-person maintainer narration (use first person when describing your own work)",
            warnings,
        )


if __name__ == "__main__":
    unittest.main()
