<template>
  <v-card>
    <slot></slot>

    <v-list>
      <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex" dense>
        <v-list-item-content class="pa-0">
          <v-list-item
            color="dark"
            class="columnItem"
            @click="changeColor(columnIndex)"
            :style="dynamicColumnStyle(columnIndex)"
          >
            {{ column }}
          </v-list-item>
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
    return {
      clickedColumnIndex: null,
      unClickedColumnItemStyle: {
        // "background-color": "none"
      },
      clickedColumnItemStyle: {
        "background-color": "lightgrey"
      }
    };
  },
  props: [],

  methods: {
    changeColor(columnIndex) {
      this.clickedColumnIndex = columnIndex;
    },
    dynamicColumnStyle(columnIndex) {
      if (this.clickedColumnIndex == columnIndex) {
        return this.clickedColumnItemStyle;
      } else return this.unClickedColumnItemStyle;
    }
  },
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
<style scoped></style>
