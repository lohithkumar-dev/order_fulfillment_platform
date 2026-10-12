from app.db.models.audit import AuditLog
def audit(db,user_id,action,entity,entity_id,metadata=None,ip=None):
    db.add(AuditLog(user_id=user_id,action=action,entity=entity,entity_id=str(entity_id),metadata_json=metadata,ip_address=ip))
