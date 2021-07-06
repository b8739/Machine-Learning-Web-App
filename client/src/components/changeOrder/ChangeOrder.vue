<template>
  <v-dialog v-model="dialog" persistent max-width="800">
    <v-card>
      <v-container class="columnList">
        <v-row>
          <v-card-title>Table 컬럼 순서 변경</v-card-title>

          <v-spacer></v-spacer>
          <v-btn x-small min-width="20" min-height="30" @click="closeStepper"
            ><v-icon small>mdi-close</v-icon>
          </v-btn>
        </v-row>
        <v-divider></v-divider>
        <v-list outlined dense>
          <v-list-item-group active-class="border">
            <draggable :list="columns" @change="onDragEvent">
              <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex">
                <v-list-item-content>
                  <v-list-item-title>{{ column }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </draggable>
          </v-list-item-group>
        </v-list>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import draggable from "vuedraggable";
import axios from "axios";

export default {
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    closeStepper() {
      this.dialog = false;
    },
    onDragEvent(evt) {
      let movedColumnName = evt.moved.element;
      let oldIndex = evt.moved.oldIndex + 3;
      let newIndex = evt.moved.newIndex + 3;
      //컬럼 left 이동
      if (oldIndex > newIndex) {
        this.changeColumnOrder("left", movedColumnName, newIndex);
      }
      //컬럼 right 이동
      else {
        this.changeColumnOrder("right", movedColumnName, newIndex);
      }
    },
    changeColumnOrder(position, movedColumnName, newIndex) {
      const api = "http://localhost:5000/changeColumnOrder";
      axios
        .get(api, {
          params: {
            position: position,
            movedColumnName: movedColumnName,
            newIndex: newIndex
          }
        })
        .then(res => {})
        .catch(error => {
          console.error(error);
        });
    }
  },
  components: {
    draggable
  },
  computed: {
    ...mapGetters("initialData", ["columns"]),
    ...mapState({
      // columns: state => state.columns
    })
  },

  created() {
    eventBus.$on("openChangeOrderModal", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>
<style scoped>
.columnList {
  /* height: 230px; */
  /* overflow-y: scroll; */
}
</style>
