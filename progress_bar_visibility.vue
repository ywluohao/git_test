<template>
  <div>
    <Button @click="startLoading">Start Loading</Button>
    
    <ProgressBar v-if="showProgressBar" :progress="overallProgress" />

    <div>{{ loadingMessage }}</div>
  </div>
</template>

<script>
import Button from './Button.vue'; // Import your Button component
import ProgressBar from './ProgressBar.vue'; // Import your ProgressBar component

export default {
  components: {
    Button,
    ProgressBar
  },
  data() {
    return {
      showProgressBar: false,
      loadingMessage: '',
      tables: ['Table1', 'Table2'], // Names of the tables to load
      overallProgress: 0
    };
  },
  methods: {
    async startLoading() {
      this.showProgressBar = true;
      this.loadingMessage = 'Loading...';
      
      await this.loadDataFromTables();

      this.loadingMessage = 'Loading complete!';
      this.showProgressBar = false;
    },
    // ... other methods as in the previous example
  }
};
</script>
