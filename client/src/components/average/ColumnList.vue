<template>
  <v-card>
    <slot></slot>

    <v-list>
      <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex">
        <v-list-item-content>
          <v-list-item-title>{{ column }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>
<script>
import { mapState } from "vuex";

import { eventBus } from "@/main";
export default {
  data() {
    return {};
  },
  props: [],
  methods: {},
  components: {},
  computed: {
    ...mapState({
      dataset: state => state.initialDatadataset,
      indexNum: state => state.initialData.indexNum,
      columns: state => state.initialData.columns
      // columns: state => state.columns
    })
  }
};
</script>
