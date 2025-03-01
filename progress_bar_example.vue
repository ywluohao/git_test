<template>
  <div>
    <ProgressBar :progress="overallProgress" />

    <div>{{ loadingMessage }}</div>
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue'; // Import your ProgressBar component

export default {
  components: {
    ProgressBar
  },
  data() {
    return {
      loadingMessage: 'Loading...',
      tables: ['Table1', 'Table2'], // Names of the tables to load
      overallProgress: 0
    };
  },
  methods: {
    async loadDataFromTables() {
      const totalTables = this.tables.length;
      let completedTables = 0;

      for (const tableName of this.tables) {
        await this.loadTableData(tableName);
        completedTables++;
        this.calculateOverallProgress(completedTables, totalTables);
      }

      this.loadingMessage = 'Loading complete!';
    },
    async loadTableData(tableName) {
      // Simulate loading data from the table asynchronously
      const tableSize = await this.getTableSize(tableName); // Replace with your logic
      let loadedData = 0;

      while (loadedData < tableSize) {
        // Simulate data loading progress
        loadedData += 100; // Simulated progress increment
        await new Promise(resolve => setTimeout(resolve, 50)); // Simulate data loading delay
      }
    },
    async getTableSize(tableName) {
      // Simulate fetching table size asynchronously
      await new Promise(resolve => setTimeout(resolve, 100)); // Simulate data fetching delay
      return 1000; // Replace with your logic to get the actual table size
    },
    calculateOverallProgress(completedTables, totalTables) {
      this.overallProgress = (completedTables / totalTables) * 100;
    }
  },
  mounted() {
    this.loadDataFromTables();
  }
};
</script>
