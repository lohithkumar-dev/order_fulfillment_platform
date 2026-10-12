from app.db.models.notification import Notification
def notify(db,user_id,event_type,message,payload=None): db.add(Notification(user_id=user_id,event_type=event_type,message=message,payload=payload))
