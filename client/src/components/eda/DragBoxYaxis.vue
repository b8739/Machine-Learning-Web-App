<template>
  <div class="dragYaxisBox">
    <v-row class="vrow" align="center">
      <v-col>
        <draggable
          :options="{ group: 'dragGroup' }"
          @start="drag = true"
          @end="drag = false"
          @change="onDragEvent"
          :list="columns"
        >
          <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex" small outlined>{{
            column
          }}</v-chip>
        </draggable>
      </v-col>
    </v-row>
    <!-- <slot></slot> -->
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      columns: [],
      numOfDragElement: 0
    };
  },
  methods: {
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      console.log(evt);
      switch (eventName) {
        case "added":
          let axisInfo = {
            evt: evt,
            type: "axis",
            numOfDragElement: this.numOfDragElement
          };
          eventBus.$emit("yaxisBeingDragged", axisInfo);
          this.numOfDragElement++;
          //드래그 박스에 chip 하나만 유지하도록 초기화
          // this.columns = [evt.added.element];
          break;
        case "removed":
          numOfDragElement--;
          eventBus.$emit("yaxisBeingRemoved", false);
          break;
      }
    }
  },
  props: ["styleObject", "axisPosition"],

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
  /* border: 1px solid rgb(90, 47, 47); */
  /* margin: 50px 0; */
}
</style>
