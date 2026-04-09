## 2024-05-24 - O(N) filtering to O(1) tag index
**Learning:** Iterating through an array for filtering can be costly for repetitive calls. Indexing tags provides a large speed up for queries. Also, `O(N log N)` sort just to find the min element is an anti-pattern.
**Action:** Use dictionary indexing for tag-based lookups and `min()` for finding extreme values instead of sorting entire lists.

## 2024-06-25 - Memory Eviction Bottleneck
**Learning:** NPC memory eviction exceeded capacity using an $O(N)$ lookup operation `min()` when adding every single event, resulting in very poor performance when managing many events or with large capacities. This is a common performance bottleneck with accumulation of memory over time.
**Action:** Replaced the array representation in `Memory` class with a min-heap structure (`heapq` module) relying on an overriding `__lt__` method on `MemoryEvent`. This brings insertion and capacity-driven eviction down to $O(\log N)$, making adding and popping memories efficiently scaling. Look for similar O(N) linear scans when selecting min/max in collections, especially when running inside frequent operations.
