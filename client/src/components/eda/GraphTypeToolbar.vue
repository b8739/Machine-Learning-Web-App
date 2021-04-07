<template>
  <v-toolbar>
    <v-btn v-model="graphType[0]" @click="sendGraphType(graphType[0])">
      <font-awesome-icon icon="chart-line" />
    </v-btn>
    <v-btn v-model="graphType[1]" @click="sendGraphType(graphType[1])">
      <font-awesome-icon icon="chart-area" />
    </v-btn>
    <v-btn v-model="graphType[2]" @click="sendGraphType(graphType[2])">
      <font-awesome-icon icon="chart-bar" />
    </v-btn>
    <v-btn v-model="graphType[3]" @click="sendGraphType(graphType[3])">
      <font-awesome-icon icon="chart-pie" />
    </v-btn>
  </v-toolbar>
</template>

<script>
import { eventBus } from "@/main";
export default {
  data() {
    return {
      graphType: ["line", "area", "bar", "pie"]
    };
  },
  methods: {
    sendGraphType(graphType) {
      eventBus.$emit("graphTypeBeingSent", graphType);
    }
  }
};
</script>
