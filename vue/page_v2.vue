<template>
  <div>
    <div class="tabs">
      <button @click="activeTab = 0">Tab 1</button>
      <button @click="activeTab = 1">Tab 2</button>
    </div>
    <div v-if="activeTab === 0">
      <tab1></tab1>
    </div>
    <div v-else-if="activeTab === 1">
      <tab2></tab2>
    </div>
  </div>
</template>

<script>
import Tab1 from './components/Tab1.vue';
import Tab2 from './components/Tab2.vue';

export default {
  components: {
    Tab1,
    Tab2
  },
  data() {
    return {
      activeTab: 0
    };
  }
};
</script>

<style>
/* Add styling as needed */
</style>
