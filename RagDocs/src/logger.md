# Logger Class Documentation

This Python file defines a custom `Logger` class extending the built-in `logging.Logger` to provide enhanced logging functionality, including latency measurement and rotating file logging.


## Class: `Logger`

This class inherits from `logging.Logger` and adds features for:

*   **Latency Measurement:**  Tracks execution time using nanoseconds.
*   **Rotating File Logging:** Logs messages to a file, creating new files when the maximum size is reached.  Keeps a maximum of 10 log files.
*   **Detailed Log Formatting:**  Includes timestamp, filename, function name, line number, process and thread IDs, and task name (if available).


### Attributes:

*   `INFO`, `WARNING`, `ERROR`, `DEBUG`: Constants mirroring logging levels from the standard library.
*   `latency_timer`: An integer storing the start time for latency measurements (in nanoseconds).


### Methods:

*   `start_latency_timer()`: Resets the `latency_timer` to the current nanosecond timestamp.

*   `log_latency(pre_message: str)`:  Calculates and logs the elapsed time since the last `start_latency_timer()` call.  The elapsed time is expressed in milliseconds. It then calls `start_latency_timer()` to reset the timer for subsequent measurements.

*   `__init__(self, name: str = "root")`: The constructor initializes the logger.
    *   It sets up a `StreamHandler` for console output and a `RotatingFileHandler` for logging to a file located at `./Logs/logs.log`.
    *   The file handler is configured to create a maximum of 10 rotated log files with a maximum size of 10 MB each.
    *   The log format includes detailed information as described above.
    *   The logging level is set to `DEBUG` regardless of the environment (currently, there is no conditional logic that changes this based on the environment variable).  The code has a placeholder for environment-based log level selection but it's currently not functional.


### Usage Example:

```python
from your_logger_file import Logger  # Replace 'your_logger_file' with the actual filename

logger = Logger("my_module")  # create logger with name 'my_module'
logger.start_latency_timer()
# ... some code ...
logger.log_latency("My operation")
logger.info("Something happened")
logger.error("An error occurred")

```


## File Structure and Setup:

The script first checks for the existence of a `Logs` directory. If it doesn't exist, it creates one. This ensures that the log files are written to a dedicated directory.


## Environment Variables:


The code includes a check for an environment variable `ENV`.  The intended functionality was to set the logging level based on this variable (e.g., "dev" for DEBUG, "prod" for INFO or higher). However, currently the `if` block always sets the logging level to `DEBUG`.  This section needs to be updated to make use of the `ENV` variable.
