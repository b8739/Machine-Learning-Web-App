<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%">
    <v-tabs v-model="tab" centered>
      <v-tab>Build</v-tab>
      <v-tab>Settings</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-list-group>
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon>mdi-vector-rectangle</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Snippets</v-list-item-title>
          </template>
          <v-list-item v-for="(snippet, index) in snippets" :key="index">
            <v-chip draggable label>{{ snippet }}</v-chip>
          </v-list-item>
          <!-- 여기 chip 들어감 -->
        </v-list-group>

        <v-list-group>
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon>mdi-rectangle-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Blocks</v-list-item-title>
          </template>
          <v-list-item v-for="(block, index) in blocks" :key="index">
            <v-chip draggable label>{{ block }}</v-chip>
          </v-list-item>
          <!-- 여기 chip 들어감 -->
        </v-list-group>
      </v-tab-item>
      <!-- settings -->
      <v-tab-item>
        <v-list-group>
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon>mdi-play-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Run Settings</v-list-item-title>
          </template>

          <!-- 여기 chip 들어감 -->
        </v-list-group>

        <v-list-group>
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon>mdi-database-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Dataset Settings</v-list-item-title>
          </template>

          <!-- 여기 chip 들어감 -->
        </v-list-group>
      </v-tab-item>
    </v-tabs-items>
  </v-navigation-drawer>
</template>
<script>
export default {
  data() {
    return {
      tab: null,
      drawer: true,
      mini: true,
      snippets: ["XGBoost", "Random Forest", "SVR"],
      blocks: ["Input", "Output"]
    };
  }
};
</script>
