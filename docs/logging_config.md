Module logging_config
=====================

Functions
---------

`setup_logging()`
:   Sets up logging configuration using loguru.
    
    This function removes any existing loggers and adds new loggers for different
    log levels (INFO, WARNING, ERROR) with specific formats. It logs INFO and WARNING
    messages to stdout and ERROR messages to stderr. The log messages include the
    time, log level, and message. Additionally, backtrace and diagnose options are
    enabled for detailed error information.