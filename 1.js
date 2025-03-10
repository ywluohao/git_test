Yes, you can definitely put all your data in a single sheet instead of splitting it across multiple sheets. Here's how you can modify the chunking approach to create a single sheet with all your data:

```javascript
import * as XLSX from 'xlsx';

function exportLargeDatasetToSingleSheet(data, filename) {
  const CHUNK_SIZE = 10000; // Adjust based on your performance needs
  const workbook = XLSX.utils.book_new();
  
  // Create a worksheet with the headers (first row)
  let worksheet;
  
  if (data.length > 0) {
    // Initialize the worksheet with the first chunk
    const firstChunk = data.slice(0, Math.min(CHUNK_SIZE, data.length));
    worksheet = XLSX.utils.json_to_sheet(firstChunk);
    
    // Process remaining chunks
    for (let i = CHUNK_SIZE; i < data.length; i += CHUNK_SIZE) {
      const chunk = data.slice(i, Math.min(i + CHUNK_SIZE, data.length));
      // Append to existing worksheet, skipping the header row
      XLSX.utils.sheet_add_json(worksheet, chunk, { 
        origin: -1, // Append at the end
        skipHeader: true // Don't add headers again
      });
    }
  } else {
    // Handle empty data case
    worksheet = XLSX.utils.json_to_sheet([]);
  }
  
  // Add the worksheet to the workbook
  XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
  
  // Write to file
  XLSX.writeFile(workbook, filename);
}
```

This approach:
1. Creates a single worksheet with the first chunk of data (which includes the headers)
2. Processes the remaining data in chunks, appending each chunk to the same worksheet
3. Uses `origin: -1` to append rows at the end of the existing data
4. Uses `skipHeader: true` to avoid duplicating column headers

This method is more memory-efficient than trying to process all 48k rows at once, while still giving you a single sheet with all your data. The chunking happens only during processing, not in the final output.

Would you like me to explain any particular part of this solution in more detail?​​​​​​​​​​​​​​​​