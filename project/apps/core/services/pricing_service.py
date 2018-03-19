from decimal import Decimal
import datetime

SECONDS_IN_A_DAY = 60 * 60 * 24


class PricingService:

    def __init__(self):
        self.standing_charge = Decimal('0.36')
        self.normal_minute = Decimal('0.09')
        self.reduced_minute = Decimal('0.00')

        self.start_normal_fares = datetime.time(6, 0, 0)
        self.start_reduced_fares = datetime.time(22, 0, 0)

    def get_price(self, call):
        entire_days = self._get_entire_days_value(call)
        normal_minutes = self._get_normal_minutes_value(call)
        reduced_minutes = self._get_reduced_minutes_value(call)
        return (
            self.standing_charge +
            normal_minutes +
            reduced_minutes +
            entire_days
        )

    def _get_normal_minutes_value(self, call):
        return self._get_normal_minutes(call) * self.normal_minute

    def _get_reduced_minutes_value(self, call):
        return self._get_reduced_minutes(call) * self.reduced_minute

    def _get_normal_minutes(self, call):
        call_start = datetime.datetime.combine(
            datetime.date.min, call.start_timestamp.time()
        )
        call_end = datetime.datetime.combine(
            datetime.date.min,
            (
                call_start +
                datetime.timedelta(minutes=call.duration.seconds // 60)
            ).time()
        )

        normal_start = datetime.datetime.combine(
            datetime.datetime.min,
            self.start_normal_fares
        )

        normal_end = datetime.datetime.combine(
            datetime.datetime.min,
            self.start_reduced_fares
        )

        if call_end > call_start:
            start = max(call_start, normal_start)
            end = min(call_end, normal_end)
            return (end - start).seconds // 60
        else:
            morning = (call_end - normal_start) if call_end > normal_start \
                else datetime.timedelta(seconds=0)
            night = (normal_end - call_start) if normal_end > call_start \
                else datetime.timedelta(seconds=0)
            return (morning + night).seconds // 60

    def _get_entire_days_value(self, call):
        days = call.duration.days
        normal_hours = (
            self.start_reduced_fares.hour - self.start_normal_fares.hour)
        reduced_hours = 24 - normal_hours

        return days * (normal_hours * 60 * self.normal_minute +
                       reduced_hours * 60 * self.reduced_minute)

    def _get_reduced_minutes(self, call):
        """ 
        Since the value will always be 0, we can implement it when the reduced
        minutes gets a price other than 0
        """
        return 0
