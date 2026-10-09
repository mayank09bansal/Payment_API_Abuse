import unittest
from src.detector import score_request


class DetectorTests(unittest.TestCase):
    def test_low_risk_event_is_allowed(self):
        result = score_request({
            "user_id": "normal",
            "endpoint": "account_view",
            "requests_per_minute": 2,
            "auth_failures": 0,
            "transaction_velocity": 0,
            "amount_deviation": 0.0,
            "endpoint_diversity": 1,
        })
        self.assertEqual(result["recommended_action"], "allow")
        self.assertEqual(result["risk_band"], "low")

    def test_replay_and_high_velocity_trigger_block(self):
        result = score_request({
            "user_id": "suspicious",
            "endpoint": "payment_initiation",
            "requests_per_minute": 38,
            "auth_failures": 7,
            "transaction_velocity": 9,
            "amount_deviation": 0.95,
            "endpoint_diversity": 8,
            "device_changed": True,
            "network_changed": True,
            "beneficiary_changes": 4,
            "duplicate_request": True,
        })
        self.assertEqual(result["recommended_action"], "block_and_alert")
        self.assertGreater(result["risk_score"], 0.5)

    def test_result_contains_explanation(self):
        result = score_request({"requests_per_minute": 35})
        self.assertIn("reasons", result)
        self.assertGreater(len(result["reasons"]), 0)


if __name__ == "__main__":
    unittest.main()
