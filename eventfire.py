"""Event fire.
1. callbacks to execute when the event fires
2. if event is already fired, new registration comes, run the callback immediately
"""

from threading import Lock
from typing import Callable, List

class EventFire:
    def __init__(self):
        """Initialize the event fire system."""
        self._callbacks: List[Callable] = []
        self._is_fired = False
        self._lock = Lock()

    def register_callback(self, callback: Callable) -> None:
        """Register a callback to be executed when the event fires.
        If the event has already fired, execute the callback immediately.

        Args:
            callback: A callable function to be executed
        """
        with self._lock:
            if self._is_fired:
                # If event already fired, execute callback immediately
                try:
                    callback()
                except Exception as e:
                    print(f"Error executing callback: {e}")
            else:
                # Add callback to the list for future execution
                self._callbacks.append(callback)

    def fire(self) -> None:
        """Fire the event and execute all registered callbacks.
        Once fired, the event stays in fired state and future registrations
        will be executed immediately."""
        callbacks_to_execute = []

        with self._lock:
            if self._is_fired:
                return  # Event already fired
            
            self._is_fired = True
            callbacks_to_execute = self._callbacks.copy()
            self._callbacks.clear()

        # Execute callbacks outside the lock to prevent deadlocks
        for callback in callbacks_to_execute:
            try:
                callback()
            except Exception as e:
                print(f"Error executing callback: {e}")

    def reset(self) -> None:
        """Reset the event fire system to its initial state."""
        with self._lock:
            self._is_fired = False
            self._callbacks.clear()

    @property
    def is_fired(self) -> bool:
        """Check if the event has been fired.

        Returns:
            bool: True if the event has been fired, False otherwise
        """
        with self._lock:
            return self._is_fired

# Example usage
if __name__ == "__main__":
    def callback1():
        print("Callback 1 executed")

    def callback2():
        print("Callback 2 executed")

    # Create event fire instance
    event = EventFire()

    # Register callbacks before firing
    event.register_callback(callback1)
    event.register_callback(callback2)

    # Fire the event
    event.fire()

    # Register callback after firing (will execute immediately)
    def callback3():
        print("Callback 3 executed immediately")

    event.register_callback(callback3)