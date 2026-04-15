## 2024-05-24 - O(N) filtering to O(1) tag index
**Learning:** Iterating through an array for filtering can be costly for repetitive calls. Indexing tags provides a large speed up for queries. Also, `O(N log N)` sort just to find the min element is an anti-pattern.
**Action:** Use dictionary indexing for tag-based lookups and `min()` for finding extreme values instead of sorting entire lists.

## 2024-06-25 - Memory Eviction Bottleneck
**Learning:** NPC memory eviction exceeded capacity using an $O(N)$ lookup operation `min()` when adding every single event, resulting in very poor performance when managing many events or with large capacities. This is a common performance bottleneck with accumulation of memory over time.
**Action:** Replaced the array representation in `Memory` class with a min-heap structure (`heapq` module) relying on an overriding `__lt__` method on `MemoryEvent`. This brings insertion and capacity-driven eviction down to $O(\log N)$, making adding and popping memories efficiently scaling. Look for similar O(N) linear scans when selecting min/max in collections, especially when running inside frequent operations.

## 2024-07-20 - O(N) vs O(1) in eviction mechanisms
**Learning:** Removing elements from a list via `.remove()` during memory eviction is O(N) and can drastically reduce performance when limits are hit frequently.
**Action:** Use sets for indexing elements when individual removal is required and insertion order isn't strictly necessary, maintaining O(1) removal.

## 2026-04-12 - Atomically replacing heap items
**Learning:** Calling `heapq.heappush` followed by `heapq.heappop` is noticeably slower than using `heapq.heappushpop()`. Additionally, when managing a cache with `heappushpop`, we can avoid the overhead of adding and immediately removing tags/indexes if the newly pushed item is the one that gets popped right back out due to low priority.
**Action:** Always prefer `heappushpop()` over a push-then-pop sequence when dealing with fixed-size priority queues. Use the returned value of `heappushpop()` to conditionally execute expensive operations (like updating tag indexes) only if the item is actually kept in the cache.

## 2024-05-18 - Caching O(N) read-heavy operations
**Learning:** Frequent calls to `EmotionState.get_dominant_emotion()` cause performance bottlenecks due to O(N) dictionary iteration in game loops where reads outnumber writes. Also, LBYL (Look Before You Leap) pattern `if key in dict:` is slightly slower than EAFP (Easier to Ask for Forgiveness than Permission) `try...except KeyError:` on the happy path.
**Action:** When working on NPC stat getters or similar read-heavy functions, cache the result during state updates to achieve O(1) reads, and prefer EAFP for dictionary lookups on the happy path.

## 2024-05-19 - Skipping redundant dictionary updates in hot paths
**Learning:** Functions like `EmotionState.update_emotion` are frequently called, often with a 0 delta or resulting in no change due to hitting boundary limits (e.g., 0.0 or 1.0). In such cases, unconditionally recalculating `max(min(...))` and writing back to the dictionary adds unnecessary overhead. Furthermore, Python's built-in `max` and `min` function call overhead is significant inside tight loops compared to basic `if` statements.
**Action:** When updating states that have boundaries, replace `max/min` calls with `if` condition clamping. Additionally, use early returns if the state is not actually changing (`delta == 0` or `new_val == curr_val`) to skip the expensive dictionary writes and subsequent evaluation logic.
