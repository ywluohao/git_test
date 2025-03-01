<template>
  <div>
    <v-tabs v-model="tab">
      <v-tab>Tab 1</v-tab>
      <v-tab>Tab 2</v-tab>
    </v-tabs>
    <v-tab-item v-for="(component, index) in tabComponents" :key="index">
      <component :is="component"></component>
    </v-tab-item>
  </div>
</template>

<script>
import Tab1 from './Tab1.vue';
import Tab2 from './Tab2.vue';

export default {
  components: {
    Tab1,
    Tab2
  },
  data() {
    return {
      tab: 0,
      tabComponents: [Tab1, Tab2]
    };
  }
};
</script>
