Here’s a compact version of Option 1 (pure JavaScript, no dependencies) tailored for your 35,000 × 27 dataset. It minimizes lines while keeping functionality:


Notes
	•	Size: Handles your 35,000 × 27 (~14-50 MB CSV) on modern hardware.
	•	Compactness: Single method, no batching or async for brevity (trade-off: UI might freeze for 5-15 seconds).
	•	Risk: If it fails (e.g., memory crash), try papaparse instead.
For your dataset, this should work unless your machine is very constrained. Test it and let me know!
