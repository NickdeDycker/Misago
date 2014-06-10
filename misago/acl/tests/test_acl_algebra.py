from django.test import TestCase
from misago.acl import algebra


class ComparisionsTests(TestCase):
    def test_greater(self):
        """greater permission wins test"""

        self.assertEqual(algebra.greater(1, 3), 3)
        self.assertEqual(algebra.greater(4, 2), 4)
        self.assertEqual(algebra.greater(2, 2), 2)
        self.assertEqual(algebra.greater(True, False), True)

    def test_greater_or_zero(self):
        """greater or zero permission wins test"""

        self.assertEqual(algebra.greater_or_zero(1, 3), 3)
        self.assertEqual(algebra.greater_or_zero(4, 2), 4)
        self.assertEqual(algebra.greater_or_zero(2, 2), 2)
        self.assertEqual(algebra.greater_or_zero(True, False), False)
        self.assertEqual(algebra.greater_or_zero(2, 0), 0)
        self.assertEqual(algebra.greater_or_zero(0, 0), 0)
        self.assertEqual(algebra.greater_or_zero(0, 120), 0)

    def test_lower(self):
        """lower permission wins test"""

        self.assertEqual(algebra.lower(1, 3), 1)
        self.assertEqual(algebra.lower(4, 2), 2)
        self.assertEqual(algebra.lower(2, 2), 2)
        self.assertEqual(algebra.lower(True, False), False)


class SumACLTests(TestCase):
    def test_sum_acls(self):
        """acls are summed"""

        test_acls = [
            {
                'can_see': False,
                'can_hear': False,
                'max_speed': 10,
                'min_age': 16,
                'speed_limit': 50,
            },
            {
                'can_see': True,
                'can_hear': False,
                'max_speed': 40,
                'min_age': 20,
                'speed_limit': 0,
            },
            {
                'can_see': False,
                'can_hear': True,
                'max_speed': 80,
                'min_age': 18,
                'speed_limit': 40,
            },
        ]

        defaults = {
            'can_see': False,
            'can_hear': False,
            'max_speed': 30,
            'min_age': 18,
            'speed_limit': 60,
        }

        acl = algebra.sum_acls(
            defaults, test_acls,
            can_see=algebra.greater,
            can_hear=algebra.greater,
            max_speed=algebra.greater,
            min_age=algebra.lower,
            speed_limit=algebra.greater_or_zero
            )

        self.assertEqual(acl['can_see'], True)
        self.assertEqual(acl['can_hear'], True)
        self.assertEqual(acl['max_speed'], 80)
        self.assertEqual(acl['min_age'], 16)
        self.assertEqual(acl['speed_limit'], 0)
