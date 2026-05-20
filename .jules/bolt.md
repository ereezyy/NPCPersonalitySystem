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

## 2026-04-17 - Bypassing Python-level `__lt__` in heapq
**Learning:** `heapq` uses standard Python comparisons which can trigger custom `__lt__` methods on objects repeatedly during heap adjustments. This is slow in tight loops. A more performant approach is wrapping objects in a tuple structure like `(priority, tiebreaker, object)` because tuple comparison is highly optimized in C, falling back to earlier elements to resolve comparisons and completely avoiding custom object methods as long as the tiebreaker prevents equality.
**Action:** When using `heapq` with custom objects, store them within a tuple utilizing a tiebreaker like `itertools.count()` instead of overriding the `__lt__` method on the object itself. Unpack the tuple when retrieving the object.
## 2026-04-16 - Hot path function call and object overhead
**Learning:** `__slots__` reduces memory usage and speeds up attribute access in Python classes, particularly useful for high-volume objects like `MemoryEvent`. Also, Python built-in function calls like `min()` and `max()` have a large overhead compared to basic `if/elif` statements. In hot paths, even standard optimizations like `heapq.heappushpop()` can be bypassed with an early return if we know the new item won't be kept in the priority queue.
**Action:** Use `__slots__` on data container classes that are instantiated frequently. Replace `min/max` with `if-elif-else` inside heavily used loops or update paths. Short-circuit standard library operations when trivial checks (like comparing against the minimum element of a min-heap) can prevent unnecessary execution.

## 2024-05-19 - Skipping redundant dictionary updates in hot paths (addendum for relationships)
**Learning:** Similar to emotion state, relationship affinity tracking often hits bound limits (+1.0/-1.0) or receives redundant updates (0 delta) during frequent game loops. Skipping dictionary writes and early exiting when the state has not actually changed drastically reduces overhead and speeds up the hot path.
**Action:** When creating state management classes that process deltas (like affinities or statuses), immediately check for zero deltas and skip processing. Calculate the new clamped value, and if it matches the current value, return early before updating the underlying dictionary to save `__setitem__` overhead.

## 2026-04-20 - Indexing Error when Checking Min-Heap of Tuples
**Learning:** When storing objects in a `heapq` wrapped inside tuples for performance (e.g., `(priority, tiebreaker, object)`), accessing the minimum element via `heap[0]` returns the tuple, not the object. Attempting to directly access object attributes like `heap[0].importance` will cause an `AttributeError`.
**Action:** Always remember to access the first element of the tuple for comparisons when using the tuple-wrapping pattern with `heapq` (e.g., use `new_item[0] < heap[0][0]`), and do this early to avoid expensive push/pop operations when discarding elements lower than the heap minimum.

## 2026-04-22 - Early Exit Before Object Allocation
**Learning:** Instantiating objects (like `MemoryEvent`) inside hot paths can introduce significant overhead, especially if the object's constructor performs non-trivial operations (like calling `time.time()`). When elements are frequently rejected from a capacity-constrained collection (like a full priority queue dropping low-importance items), checking the rejection criteria *before* allocating the new object provides a large performance boost.
**Action:** When implementing `add` or `insert` methods for size-limited collections, check the fast-path rejection conditions (e.g., `importance < current_min_importance`) as early as possible, bypassing any object creation, variable assignment, or tuple construction if the item is guaranteed to be discarded.

## 2026-04-29 - [Optimizing dictionary access in hot loops]
**Learning:** Checking for key existence with `if key not in dict:` in a hot loop (like `Memory.add_event` processing tags) can cause significant overhead. In the `Memory` system where tag lookups are extremely frequent, utilizing `collections.defaultdict(set)` and avoiding explicit dictionary key existence checks improves performance notably.
**Action:** Always prefer `collections.defaultdict` over manual existence checks for grouping or categorizing data in hot loops where keys might be missing. Additionally, localizing attribute accesses (like caching `self.tag_index` to `tag_index`) within tight loops reduces bytecode instructions and increases execution speed.

## 2024-05-24 - Optimizing Memory and Initialization of Core Classes with __slots__
**Learning:** Using `__slots__` reduces memory footprint and speeds up attribute access and object instantiation. This is particularly valuable for core composition classes (like `NPC`, `Personality`, `EmotionState`, `Memory`, `Relationship`) that are instantiated frequently and in large quantities.
**Action:** Consistently apply `__slots__` to fundamental state-holding data classes that are generated in volume to save on object overhead and memory costs without altering any external behaviour.

## 2024-05-26 - Early Exit on Delta Direction against Boundaries
**Learning:** Even with clamping and 'new_val == curr_val' checks, performing arithmetic and clamp operations on states that are already at their boundary limits introduces measurable overhead in hot paths. Checking the delta direction against the boundary immediately after state retrieval bypasses this.
**Action:** When updating bounded values in hot paths (e.g., processing deltas in state management), implement early exit conditions by checking the delta direction against boundary limits immediately after retrieving the current state to skip redundant arithmetic and clamping logic.

## 2024-05-27 - heapreplace vs heappushpop for fixed-size min-heaps
**Learning:** When adding items to a fixed-size min-heap where we pre-check that the new item is greater than or equal to the minimum element (and thus will definitely be kept), `heapq.heapreplace` is more efficient than `heapq.heappushpop()`. `heapreplace` avoids unnecessary push-then-pop overhead and guarantees that the popped element is an existing one.
**Action:** Use `heapq.heapreplace` instead of `heapq.heappushpop` when replacing items in a fixed-size heap where it's guaranteed the new item will replace an existing item.
