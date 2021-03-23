<template>
  <div>
    <!-- 여기에 요소 추가 -->
    <!-- column list -->
    <slot></slot>
    <!-- <v-divider></v-divider> -->
    <v-list :style="styleObject">
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        @change="onDrop"
        :list="columns"
      >
        <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex">
          <v-list-item-content>
            <v-list-item-title>{{ column }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </draggable>
    </v-list>

    <!-- <v-card>
            <draggable :options="{ group: 'your-group' }"> </draggable>
            second list
          </v-card> -->
  </div>
</template>
<script>
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  props: ["columns", "styleObject"],
  methods: {
    onDrop(evt) {
      // console.log(added);
      console.log(evt);
    }
  },
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
