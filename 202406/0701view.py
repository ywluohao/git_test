<template>
  <div>
    <button @click="startFileGeneration">Generate Excel File</button>
  </div>
</template>

<script>
export default {
  methods: {
    startFileGeneration() {
      const job_id = Date.now(); // Generate job ID using current timestamp
      fetch(`/start-file-generation/?param1=${this.param1}&param2=${this.param2}&param3=${this.param3}&param4=${this.param4}&job_id=${job_id}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          this.checkFileStatus(job_id); // Start checking file status
        })
        .catch(error => {
          console.error('Error starting file generation:', error);
        });
    },
    checkFileStatus(job_id) {
      fetch(`/check-file-status/${job_id}/`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.blob();
        })
        .then(blob => {
          if (blob.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${job_id}.xlsx`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          } else {
            setTimeout(() => this.checkFileStatus(job_id), 10000); // Poll every 10 seconds
          }
        })
        .catch(error => {
          console.error('Error checking file status:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>