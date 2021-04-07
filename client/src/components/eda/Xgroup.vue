<template>
  <div class="xGroup">
    <slot></slot>
    <v-chip-group :style="styleObject" row>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        :list="columns"
        @change="onDragEvent"
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
      columns: []
    };
  },
  props: ["styleObject", "axisPosition"],

  components: {
    draggable
  },
  methods: {
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      console.log(eventName);
      switch (eventName) {
        case "added":
          let axisInfo = { evt: evt, type: "xGroup" };
          eventBus.$emit("xGroupBeingDragged", axisInfo);
          //드래그 박스에 chip 하나만 유지하도록 초기화
          this.columns = [evt.added.element];
          break;
        case "removed":
          eventBus.$emit("xGroupBeingRemoved", false);
          break;
      }
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
<style scoped>
.xGroup {
  /* border: 1px solid rgb(90, 47, 47); */
}
</style>
