<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%">
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold">Cases</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-sheet light outlined height="100" width="100%">
          <v-card-subtitle> Case 1</v-card-subtitle>
          <v-card-text class="font-weight-thin body-2"> Created __ days ago</v-card-text>
        </v-sheet>
      </v-list-item>
      <!-- 여기 chip 들어감 -->
    </v-list>
  </v-navigation-drawer>
</template>
<script>
export default {
  data() {
    return {
      tab: null,
      drawer: true
    };
  }
};
</script>
