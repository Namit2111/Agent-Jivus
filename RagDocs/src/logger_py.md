# Logger Class Documentation

This Python class extends the built-in `logging.Logger` to provide enhanced logging capabilities, including latency measurement and rotating file handling.

## Class: `Logger`

This class inherits from `logging.Logger` and adds functionality for:

*   **Latency Measurement:**  Tracks execution time between calls to `start_latency_timer` and `log_latency`.
*   **Rotating File Logging:** Logs messages to a rotating file (logs.log) in the Logs directory.  The file size is capped at 10MB, and up to 10 rotated files are kept.
*   **Environment-Based Log Level:**  The log level defaults to DEBUG, regardless of environment variable.  (Note: The provided code sets the log level to DEBUG in both dev and non-dev environments. This section can be improved for better clarity and functionality depending on needs.)

### Attributes:

*   `INFO`, `WARNING`, `ERROR`, `DEBUG`: Constants mirroring logging levels from the `logging` module.
*   `latency_timer`: An integer representing the nanoseconds when the timer was last started.


### Methods:

*   `start_latency_timer()`: Starts a timer to measure latency.  Stores the current nanosecond timestamp in `latency_timer`.

*   `log_latency(pre_message: str)`: Logs the elapsed time since the last call to `start_latency_timer` in milliseconds with a given prefix message.  Resets the latency timer after logging.

*   `__init__(self, name: str = "root")`: Constructor.  Initializes the logger with a specified name (defaults to "root"). Configures a `StreamHandler` for console output and a `RotatingFileHandler` for file output.  The log formatter includes timestamps, file names, line numbers, process and thread IDs, and the log level.

### Usage Example:

```python
from my_logger import Logger  # Assuming the class is in my_logger.py

logger = Logger("my_module")
logger.start_latency_timer()
# ... some code ...
logger.log_latency("Operation X")
logger.info("Some informational message")
logger.error("An error occurred!")

```

This will output log messages to both the console and the `logs.log` file in the `Logs` directory, including latency information for the code section between `start_latency_timer` and `log_latency`.


### File Handling:

The logger automatically creates a `Logs` directory if it doesn't exist.  The log file (`logs.log`) is configured with:

*   `maxBytes=10000000`: Maximum file size of 10MB.
*   `backupCount=10`: Keeps up to 10 rotated log files.


### Log Format:

The log format is:

`[<timestamp>] <logger_name> | <filename>-><function_name>():<line_number> | <process_id> <thread_id> <task_name> | <log_level>: <message>`


This provides detailed context for each log entry.


### Environment Variable:

The code currently ignores the `ENV` environment variable.  To make use of it, uncomment the else block and update it to handle different environment configurations appropriately, such as setting a different logging level based on the environment.
