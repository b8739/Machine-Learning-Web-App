<template>
  <div>
    <slot></slot>
    <v-chip-group :style="styleObject" row>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        :list="columns"
        @change="onDrop"
      >
        <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex">{{ column }}</v-chip>
      </draggable>
    </v-chip-group>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";

export default {
  data() {
    return {
      columns: [4, 5, 6]
    };
  },
  props: ["styleObject"],

  components: {
    draggable
  },
  methods: {
    onDrop(evt) {
      // console.log(evt);
      eventBus.$emit("xaxisBeingDragged", evt);
    }
  },
  computed: {
    ...mapState({
      dataset: state => state.dataset,
      indexNum: state => state.indexNum
      // columns: state => state.columns
    })
  }
};
</script>
