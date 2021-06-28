<template>
  <v-card>
    <slot></slot>

    <v-list dense>
      <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex">
        <v-list-item-content @click="clickFeatureEvent(column)">
          <v-list-item-title>{{ column }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>
<script>
import { mapState, mapGetters } from "vuex";

import { eventBus } from "@/main";
export default {
  data() {
    return {
      hoverStatus: true
    };
  },
  props: [],
  methods: {
    clickFeatureEvent(column) {
      eventBus.$emit("featureClickedEvent", column);
    }
  },
  components: {},
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset
    })
    // ...mapGetters("initialData", ["columns", "indexNum"])
  }
};
</script>
