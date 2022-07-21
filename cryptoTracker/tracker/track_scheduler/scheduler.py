from apscheduler.schedulers.background import BackgroundScheduler
from tracker.views import PositionTrackingAPIView

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# create a scheduler to run save_position_data function every 0.5 minutes (30 seconds)
class PositionTrackingSchduler(metaclass=Singleton):

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.position_tracking_view = PositionTrackingAPIView()

    def start(self):
        self.scheduler.add_job(self.position_tracking_view.save_position_data, 'interval', minutes=0.5, id='position001', replace_existing=True)
        self.scheduler.start()
    
