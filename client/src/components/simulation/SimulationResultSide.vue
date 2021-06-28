<template>
  <v-sheet height="100vh">
    <v-navigation-drawer v-model="drawer" absolute width="100%" app permanent>
      <!-- item -->
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-bold">Simulations</v-list-item-title>
        </v-list-item>
        <!-- item -->
        <v-list-item v-for="(simulationCase, index) in simulationList" :key="index">
          <v-sheet class="cursor-pointer" light outlined height="100" width="100%">
            <v-card-text class="font-weight-bold subheading pt-2 pb-0"> simulationCase</v-card-text>
            <v-card-text class="font-weight-light caption pt-2 pb-1"> simulationCase</v-card-text>
            <v-card-text class="font-weight-thin caption pt-1"> Created __ days ago</v-card-text>
          </v-sheet>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-sheet>
</template>
<script>
export default {
  data() {
    return {
      tab: null,
      drawer: true,
      simulationList: [1, 2]
    };
  }
};
</script>
