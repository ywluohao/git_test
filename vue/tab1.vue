<template>
  <div>
    <pre>{{ jsonData }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      jsonData: null
    };
  },
  mounted() {
    this.loadJsonData();
  },
  methods: {
    async loadJsonData() {
      try {
        const response = await fetch('path/to/your/json/file.json');
        this.jsonData = await response.json();
      } catch (error) {
        console.error('Error loading JSON data:', error);
      }
    }
  }
};
</script>
