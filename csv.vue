<template>
  <button @click="downloadCSV">Download CSV</button>
</template>

<script>
export default {
  data: () => ({
    jsonData: Array(35000).fill().map((_, i) => ({
      col1: `Name${i}`, col2: i, col3: `City${i}`, /* ... */ col27: `Data${i}`
    }))
  }),
  methods: {
    downloadCSV() {
      const headers = Object.keys(this.jsonData[0]);
      const csv = [
        headers.join(','),
        ...this.jsonData.map(r => headers.map(f => `"${(r[f] || '').toString().replace(/"/g, '""')}"`).join(','))
      ].join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'data_35000x27.csv';
      link.click();
    }
  }
}
</script>