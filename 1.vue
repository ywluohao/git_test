// Install xlsx library
// npm install xlsx

// Import the necessary modules
import * as XLSX from 'xlsx';

export default {
  methods: {
    // Function to trigger Excel download
    downloadExcel() {
      // Get JSON data from Vuex store
      const jsonDataSheet1 = this.$store.state.dataSheet1; // Replace 'dataSheet1' with the actual state name
      const jsonDataSheet2 = this.$store.state.dataSheet2; // Replace 'dataSheet2' with the actual state name

      // Convert JSON data to Excel worksheets
      const wsSheet1 = XLSX.utils.json_to_sheet(jsonDataSheet1);
      const wsSheet2 = XLSX.utils.json_to_sheet(jsonDataSheet2);

      // Create Excel workbook and add sheets
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, wsSheet1, 'Sheet 1');
      XLSX.utils.book_append_sheet(wb, wsSheet2, 'Sheet 2');

      // Create a blob from the workbook
      const blob = XLSX.write(wb, { bookType: 'xlsx', type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

      // Create a link element and trigger the download
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = 'combined_data.xlsx';
      link.click();
    },
  },
};


// Install xlsx library
// npm install xlsx

// Import the necessary modules
import * as XLSX from 'xlsx';

export default {
  methods: {
    // Function to trigger Excel download
    downloadExcel() {
      // Get JSON data from Vuex store
      const jsonDataSheet1 = this.$store.state.dataSheet1; // Replace 'dataSheet1' with the actual state name
      const jsonDataSheet2 = this.$store.state.dataSheet2; // Replace 'dataSheet2' with the actual state name

      // Convert JSON data to Excel worksheets
      const wsSheet1 = XLSX.utils.json_to_sheet(jsonDataSheet1);
      const wsSheet2 = XLSX.utils.json_to_sheet(jsonDataSheet2);

      // Create Excel workbook and add sheets
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, wsSheet1, 'Sheet 1');
      XLSX.utils.book_append_sheet(wb, wsSheet2, 'Sheet 2');

      // Generate Blob directly from the workbook
      const blob = XLSX.write(wb, { bookType: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

      // Trigger download using Blob and ObjectURL
      const link = document.createElement('a');
      link.href = URL.createObjectURL(new Blob([blob], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }));
      link.download = 'combined_data.xlsx';
      link.click();
    },
  },
};

