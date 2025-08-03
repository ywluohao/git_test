<template>
  <div>
    <select v-model="selectedId" @change="fetchFiles">
      <option v-for="item in items" :key="item.id" :value="item.id">
        {{ item.name }}
      </option>
    </select>

    <div v-if="loading">Loading files…</div>
    <div v-else-if="files.length">
      <button
        v-for="filename in files"
        :key="filename"
        @click="openFile(filename)"
      >
        {{ filename }}
      </button>
    </div>
    <p v-else>No files to show.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],       // preload these however you like
      selectedId: null,
      files: [],
      loading: false,
    }
  },
  methods: {
    async fetchFiles() {
      if (!this.selectedId) return;
      this.loading = true;

      try {
        // build URL with query param
        const url = `/api/file-list/?${new URLSearchParams({ id: this.selectedId })}`;
        const resp = await fetch(url, {
          method: 'GET',
          credentials: 'same-origin',  // include cookies if needed
        });

        if (!resp.ok) {
          throw new Error(`Server error: ${resp.status}`);
        }

        const data = await resp.json();
        this.files = data.files || [];
      } catch (err) {
        console.error('fetchFiles error:', err);
        this.files = [];
      } finally {
        this.loading = false;
      }
    },

    openFile(filename) {
      // tweak this to your media URL scheme
      window.open(`/media/${filename}`, '_blank');
    }
  },
  mounted() {
    // e.g. fetch your items list here
    // fetch('/api/my-model-list/').then(r => r.json()).then(json => this.items = json)
  }
}
</script>