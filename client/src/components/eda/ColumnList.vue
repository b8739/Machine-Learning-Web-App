<template>
  <div>
    <!-- 여기에 요소 추가 -->
    <!-- column list -->

    <v-subheader>{{ columns.length }} 개 열</v-subheader>
    <!-- <v-divider></v-divider> -->
    <v-list style="height: 300px; overflow-y: scroll">
      <draggable :options="{ group: 'your-group' }" @start="drag = true" @end="drag = false">
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
  components: {
    draggable
  },
  computed: {
    ...mapState({
      dataset: state => state.dataset,
      indexNum: state => state.indexNum,
      columns: state => state.columns
    })
  }
};
</script>
