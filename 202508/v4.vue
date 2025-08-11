async function testWrite(rows) {
  const ws = XLSX.utils.json_to_sheet(rows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'S');
  await XLSX.writeFile(wb, 'test.xlsx');
}

async function findBadRow(data) {
  let low = 0;
  let high = data.length; // we know the full dataset fails

  while (low + 1 < high) {
    const mid = Math.floor((low + high) / 2);
    try {
      await testWrite(data.slice(0, mid));
      low = mid; // up to mid is OK
    } catch {
      high = mid; // failure is before or at mid
    }
  }

  console.log('Last good row index:', low - 1);
  console.log('First bad row index:', low);
  console.log('Problematic row data:', data[low]);
}

// usage:
findBadRow(filteredJSON);