<template>
  <button @click="exportData">Export to Excel</button>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
  props: {
    data: {
      type: Array,
      required: true
    },
    filename: {
      type: String,
      default: "export.xlsx"
    }
  },
  methods: {
    jsonToAoa(jsonData) {
      if (!jsonData || jsonData.length === 0) return [];

      const headers = Object.keys(jsonData[0]); // Extract column headers
      const aoaData = [headers]; // First row = headers

      jsonData.forEach(row => {
        aoaData.push(headers.map(h => row[h] || "")); // Convert row to array format
      });

      return aoaData;
    },

    exportData() {
      if (!this.data || this.data.length === 0) {
        console.error("No data to export.");
        return;
      }

      const workbook = XLSX.utils.book_new();
      let worksheet;

      try {
        console.log("Total rows to export:", this.data.length);

        // Convert JSON to AOA
        const aoaData = this.jsonToAoa(this.data);
        console.log("AOA Data:", aoaData.slice(0, 5)); // Log first 5 rows for debugging

        worksheet = XLSX.utils.aoa_to_sheet(aoaData);

        XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
        console.log("Workbook sheets:", workbook.SheetNames);

        XLSX.writeFile(workbook, this.filename);
        console.log("Excel file saved successfully.");
      } catch (error) {
        console.error("Error exporting data:", error);
      }
    }
  }
};
</script>