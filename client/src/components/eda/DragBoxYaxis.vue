<template>
  <div class="dragYaxisBox">
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
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      columns: ["Drag Y axis Here"]
    };
  },
  methods: {
    onDrop(evt) {
      // console.log(evt);
      eventBus.$emit("yaxisBeingDragged", evt);
      this.columns = [evt.added.element];
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
<style scoped>
.dragYaxisBox {
  border: 1px solid rgb(90, 47, 47);
  margin: 40px 0;
}
</style>
