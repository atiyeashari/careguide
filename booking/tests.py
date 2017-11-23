from django.test import TestCase
from booking.helper_methods import *
import datetime
import pytz
# Create your tests here.

utc=pytz.UTC

class BabySitterTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='b1', password='useruser', email='b1@example.com', first_name='b1first',
                                 last_name='b1last')
        b1 = BabySitter.objects.create(user=u1, phone_number='4168814341')

    def test_baby_sitter_permission(self):
        """Baby sitters have baby_sitter permission"""
        u1 = User.objects.get(username='b1')
        self.assertTrue(u1.has_perm('booking.baby_sitter'))

    def test_baby_sitter_phone_number(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        self.assertEqual(b1.phone_number, '4168814341')


class FamilyTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='f1', password='useruser', email='f1@example.com', first_name='f1first',
                                 last_name='f1last')
        f1 = Family.objects.create(user=u1, phone_number='4168824341')

    def test_baby_sitter_permission(self):
        """Families have family permission"""
        u1 = User.objects.get(username='f1')
        self.assertTrue(u1.has_perm('booking.family'))

    def test_baby_sitter_phone_number(self):
        u1 = User.objects.get(username='f1')
        f1 = Family.objects.get(user=u1)
        self.assertEqual(f1.phone_number, '4168824341')


class AvailabilityTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='b1', password='useruser', email='b1@example.com', first_name='b1first',
                                 last_name='b1last')
        u2 = User.objects.create_user(username='b2', password='useruser', email='b2@example.com', first_name='b2first',
                                      last_name='b2last')
        b1 = BabySitter.objects.create(user=u1, phone_number='4168814341')
        b2 = BabySitter.objects.create(user=u2, phone_number='4168824341')
        a1 = Availability.objects.create(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 9, 0)),
                         end_time=utc.localize(datetime.datetime(2017, 11, 23, 14, 0)))
        a2 = Availability.objects.create(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 24, 9, 0)),
                          end_time=utc.localize(datetime.datetime(2017, 11, 24, 14, 0)))
        a3 = Availability.objects.create(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 25, 9, 0)),
                          end_time=utc.localize(datetime.datetime(2017, 11, 25, 14, 0)))

    def test_start_great_than_end(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        with self.assertRaises(ValueError):
            Availability.objects.create(baby_sitter=b1, start_time=datetime.datetime(2017, 11, 22, 13, 30),
                                        end_time=datetime.datetime(2017, 11, 22, 9, 0))

    def test_overlap(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        availabilities = Availability.objects.filter(baby_sitter=b1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 12, 0)),
                          end_time=utc.localize(datetime.datetime(2017, 11, 24, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [1, 2])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 22, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [2])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 21, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 22, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 25, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 26, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [0])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 26, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 27, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 22, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 26, 12, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [0, 1, 2])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 22, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 9, 0)))
        overlapped = overlap(availabilities, availability)
        self.assertEqual(overlapped, [2])

    def test_included(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        availabilities = Availability.objects.filter(baby_sitter=b1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 9, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 14, 0)))
        self.assertEqual(included(availabilities, availability), availabilities[2])

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 10, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))
        self.assertEqual(included(availabilities, availability), -1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 6, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 10, 0)))
        self.assertEqual(included(availabilities, availability), -1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 6, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))
        self.assertEqual(included(availabilities, availability), -1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 24, 10, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 24, 12, 0)))
        self.assertEqual(included(availabilities, availability), availabilities[1])


    def test_merge_interval(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        availabilities = Availability.objects.filter(baby_sitter=b1)

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 24, 12, 0)))
        availability = merge_interval(availabilities, availability)
        self.assertEqual(availability.start_time, utc.localize(datetime.datetime(2017, 11, 23, 9, 0)))
        self.assertEqual(availability.end_time, utc.localize(datetime.datetime(2017, 11, 24, 14, 0)))

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 12, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))
        availability = merge_interval(availabilities, availability)
        self.assertEqual(availability.start_time, utc.localize(datetime.datetime(2017, 11, 23, 9, 0)))
        self.assertEqual(availability.end_time, utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 24, 6, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 24, 12, 0)))
        availability = merge_interval(availabilities, availability)
        self.assertEqual(availability.start_time, utc.localize(datetime.datetime(2017, 11, 24, 6, 0)))
        self.assertEqual(availability.end_time, utc.localize(datetime.datetime(2017, 11, 24, 14, 0)))

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 6, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 24, 15, 0)))
        availability = merge_interval(availabilities, availability)
        self.assertEqual(availability.start_time, utc.localize(datetime.datetime(2017, 11, 23, 6, 0)))
        self.assertEqual(availability.end_time, utc.localize(datetime.datetime(2017, 11, 24, 15, 0)))

        availability = Availability(baby_sitter=b1, start_time=utc.localize(datetime.datetime(2017, 11, 23, 6, 0)),
                                    end_time=utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))
        availability = merge_interval(availabilities, availability)
        self.assertEqual(availability.start_time, utc.localize(datetime.datetime(2017, 11, 23, 6, 0)))
        self.assertEqual(availability.end_time, utc.localize(datetime.datetime(2017, 11, 23, 15, 0)))


class BookedTimeTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='b1', password='useruser', email='b1@example.com', first_name='b1first',
                                 last_name='b1last')
        b1 = BabySitter.objects.create(user=u1, phone_number='4168814341')

        u2 = User.objects.create(username='f1', password='useruser', email='f1@example.com', first_name='f1first',
                                 last_name='f1last')
        f1 = Family.objects.create(user=u2, phone_number='4168824341')

    def test_start_great_than_end(self):
        u1 = User.objects.get(username='b1')
        b1 = BabySitter.objects.get(user=u1)
        u2 = User.objects.get(username='f1')
        f1 = Family.objects.get(user=u2)
        with self.assertRaises(ValueError):
            BookedTime.objects.create(baby_sitter=b1, family=f1, start_time=datetime.datetime(2017, 11, 22, 13, 30),
                                        end_time=datetime.datetime(2017, 11, 22, 9, 0))