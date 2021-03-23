<template>
  <div>
    <slot></slot>
    <v-chip-group :style="styleObject" column>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        @change="onDrop"
        :list="columns"
      >
        <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex">{{ column }}</v-chip>
      </draggable>
    </v-chip-group>
  </div>
</template>
<script>
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      columns: [1, 5, 6]
    };
  },
  methods: {
    onDrop(evt) {
      console.log(evt);
    }
  },
  props: ["styleObject"],

  components: {
    draggable
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
