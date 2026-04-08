## 2024-05-24 - O(N) filtering to O(1) tag index
**Learning:** Iterating through an array for filtering can be costly for repetitive calls. Indexing tags provides a large speed up for queries. Also, `O(N log N)` sort just to find the min element is an anti-pattern.
**Action:** Use dictionary indexing for tag-based lookups and `min()` for finding extreme values instead of sorting entire lists.
