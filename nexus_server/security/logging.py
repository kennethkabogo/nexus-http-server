import logging


# Separate security log
security_logger = logging.getLogger('security_logger')
security_logger.setLevel(logging.WARNING)
security_handler = logging.FileHandler('security.log')
security_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
security_handler.setFormatter(security_formatter)
security_logger.addHandler(security_handler)


def log_security_event(event_type, details, severity='medium'):
    """
    Logs a security event to a dedicated security log file.
    """
    security_logger.warning(f"SECURITY_EVENT: Type={event_type}, Severity={severity}, Details={details}")