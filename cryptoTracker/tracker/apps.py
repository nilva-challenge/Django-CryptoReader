from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'
    def ready(self):
        print('start scheduler ...')
        from tracker.track_scheduler.scheduler import PositionTrackingSchduler
        position_schduler = PositionTrackingSchduler()
        position_schduler.start()
