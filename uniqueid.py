from threading import Lock, Thread, Condition
from queue import Queue
from typing import List
import time

class UniqueIdGenerator:
    def __init__(self, buffer_size: int = 1000, refill_threshold: float = 0.2):
        """Initialize the ID generator with a buffer
        
        Args:
            buffer_size: Maximum number of IDs to store in buffer
            refill_threshold: When buffer is below this percentage, trigger refill
        """
        self.buffer = Queue(maxsize=buffer_size)
        self.buffer_size = buffer_size
        self.refill_threshold = refill_threshold
        self.last_id = 0
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.refill_thread = None
        self.running = True
        self._start_refill_thread()
    
    def _start_refill_thread(self):
        """Start the background thread for buffer refilling"""
        self.refill_thread = Thread(target=self._refill_buffer, daemon=True)
        self.refill_thread.start()
    
    def _refill_buffer(self):
        """Background thread function to refill buffer when needed"""
        while self.running:
            with self.lock:
                # Wait if buffer is sufficiently full
                while (self.buffer.qsize() / self.buffer_size) > self.refill_threshold and self.running:
                    self.condition.wait(timeout=1.0)
                
                # Generate new batch of IDs if buffer is below threshold
                if self.running and not self.buffer.full():
                    new_ids = self._generate_batch(self.buffer_size - self.buffer.qsize())
                    for id in new_ids:
                        if not self.buffer.full():
                            self.buffer.put(id)
                    self.condition.notify_all()
    
    def _generate_batch(self, n: int) -> List[int]:
        """Generate n new unique IDs
        
        Args:
            n: Number of IDs to generate
            
        Returns:
            List of n unique IDs
        """
        with self.lock:
            start_id = self.last_id + 1
            self.last_id += n
            return list(range(start_id, start_id + n))
    
    def getIds(self, n: int) -> List[int]:
        """Get n unique IDs
        
        Args:
            n: Number of IDs to get
            
        Returns:
            List of n unique IDs
        """
        if n <= 0:
            raise ValueError("Number of IDs requested must be positive")
        
        result = []
        with self.lock:
            while len(result) < n:
                # If buffer is empty, wait for refill
                while self.buffer.empty() and self.running:
                    self.condition.notify()  # Notify refill thread
                    self.condition.wait()
                
                # Get as many IDs as possible from buffer
                while len(result) < n and not self.buffer.empty():
                    result.append(self.buffer.get())
                
                if not self.running:
                    raise RuntimeError("ID Generator is stopped")
        
        return result
    
    def getOneId(self) -> int:
        """Get one unique ID
        
        Returns:
            A unique ID
        """
        return self.getIds(1)[0]
    
    def stop(self):
        """Stop the ID generator and its refill thread"""
        self.running = False
        with self.lock:
            self.condition.notify_all()
        if self.refill_thread:
            self.refill_thread.join()

# Example usage
if __name__ == "__main__":
    # Create ID generator with buffer size 1000 and refill threshold 20%
    id_gen = UniqueIdGenerator(buffer_size=1000, refill_threshold=0.2)
    
    try:
        # Get single ID
        print(f"Single ID: {id_gen.getOneId()}")
        
        # Get multiple IDs
        ids = id_gen.getIds(5)
        print(f"Multiple IDs: {ids}")
        
        # Demonstrate concurrent access
        def consumer_thread():
            for _ in range(3):
                id = id_gen.getOneId()
                print(f"Thread got ID: {id}")
                time.sleep(0.1)
        
        threads = [Thread(target=consumer_thread) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
    finally:
        # Clean up
        id_gen.stop()