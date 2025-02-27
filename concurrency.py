"""
Topic: Threads and Synchronization
Question: There are multiple users calling a method reg_cb at different intances of time, as shown below. Simultaneously, there is an event happening. All the user requests that were made during the execution of the event should wait till the event completes and then execute the reg_cb method. Once the event is finished, the user requests to the reg_cb method can be executed immediatly. Implement how to handle the given scenario.


					Event in progress
----|---------------|--------------------|-------------------|--------------> timeline
U1: reg_cb(f1)     U2: reg_cb(f2)      Event completed      U3:reg_cb(f3)
									   (execute f1,f2)      (execute f3)
Was asked many questions on basic fundamentals like,


When does a concurrant modification exception occur?
When is the possibility of same thread (user x) calling the reg_cb() twice?
What are the possible deadlock scenarios?
What is mutex? etc..
Expectations: Concentrate on how you handle different possible scenarios with a valid scenario and explanation. Wrinting code is secondary.
"""

"""
Let me explain the synchronization scenario and address the key concepts:

1. Handling Event-User Request Synchronization:
- Use a ReentrantLock with condition variables to manage access
- Maintain a queue of callbacks (f1, f2, etc.) that arrive during event execution
- Use a boolean flag to track event status (in progress/completed)
- When event completes, signal waiting threads to execute their callbacks
2. Concurrent Modification Exception:
- Occurs when modifying a collection while iterating over it
- In this case, could happen if callback queue is modified while processing callbacks
3. Same Thread Calling reg_cb Twice:
- Possible if user code doesn't implement proper request tracking
- Can lead to duplicate callbacks in queue
- Should implement request deduplication or tracking mechanism
4. Deadlock Prevention:
- Ensure consistent lock acquisition order
- Implement timeouts for lock acquisition
- Use tryLock() where appropriate
- Monitor thread states and implement deadlock detection
5. Mutex (Mutual Exclusion):
- Used to protect shared resources
- Only one thread can hold the mutex at a time
- In this case, protects the callback queue and event status flag
The key is implementing proper synchronization while maintaining thread safety and preventing deadlocks.
"""