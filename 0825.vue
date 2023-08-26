import { saveAs } from 'file-saver';
import XLSX from 'xlsx';


export default {
  methods: {
    handleDownloadClick() {
      const workbook = XLSX.utils.book_new();

      // Create the first sheet
      const sheet1Data = [
        // ... Your first JSON data here
      ];
      const sheet1 = XLSX.utils.json_to_sheet(sheet1Data);
      XLSX.utils.book_append_sheet(workbook, sheet1, 'Sheet 1');

      // Create the second sheet
      const sheet2Data = [
        // ... Your second JSON data here
      ];
      const sheet2 = XLSX.utils.json_to_sheet(sheet2Data);
      XLSX.utils.book_append_sheet(workbook, sheet2, 'Sheet 2');

      // Save the workbook as an Excel file
      const buffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      saveAs(blob, 'data.xlsx');
    }
  }
}


<template>
  <div>
    <button @click="handleDownloadClick">Download Excel File</button>
  </div>
</template>
