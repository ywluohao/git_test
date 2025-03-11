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
    exportData() {
      const CHUNK_SIZE = 10000; // Adjust based on performance needs
      const workbook = XLSX.utils.book_new();
      let worksheet;

      if (this.data.length > 0) {
        // Process the first chunk with headers
        const firstChunk = this.data.slice(0, Math.min(CHUNK_SIZE, this.data.length));
        worksheet = XLSX.utils.json_to_sheet(firstChunk);

        // Append remaining chunks without headers
        for (let i = CHUNK_SIZE; i < this.data.length; i += CHUNK_SIZE) {
          const chunk = this.data.slice(i, Math.min(i + CHUNK_SIZE, this.data.length));
          XLSX.utils.sheet_add_json(worksheet, chunk, { origin: -1, skipHeader: true });
        }
      } else {
        worksheet = XLSX.utils.json_to_sheet([]);
      }

      XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
      XLSX.writeFile(workbook, this.filename);
    }
  }
};
</script>