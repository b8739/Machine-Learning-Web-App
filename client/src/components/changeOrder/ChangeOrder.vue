<template>
  <v-dialog v-model="dialogInstance" @click:outside="leaveDialog()" max-width="800">
    <v-card>
      <v-container class="columnList">
        <v-row>
          <div>
            <v-card-title>Table 컬럼 순서 변경</v-card-title>
            <!-- <v-card-subtitle class="red--text"
              >Confirm 누르고 '새로고침'까지 해야 그래프 위치까지 정상적으로 변경되는 상태입니다.
            </v-card-subtitle> -->
          </div>
          <v-spacer></v-spacer>
          <v-btn x-small min-width="20" min-height="30" @click="closeStepper"
            ><v-icon small>mdi-close</v-icon>
          </v-btn>
        </v-row>
        <v-divider></v-divider>
        <v-list outlined dense>
          <v-list-item-group active-class="border">
            <draggable v-model="duplicatedColumns" @change="onDragEvent">
              <v-list-item v-for="(column, columnIndex) in duplicatedColumns" :key="columnIndex">
                <v-list-item-content>
                  <v-list-item-title>{{ column.columnName }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </draggable>
          </v-list-item-group>
        </v-list>
      </v-container>
      <v-card-actions>
        <!-- <v-btn right @click="confirmChanges()">Confirm</v-btn> -->
        <portal-target name="summaryChangeOrderModal"> </portal-target>
      </v-card-actions>
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
    return {};
  },
  props: ["duplicatedColumns"],
  methods: {
    ...mapMutations("saveFlag", ["ChangeColumnOrderFlag"]),
    ...mapMutations("summaryTableHandler", ["setDialog"]),
    ...mapMutations("summaryTableHandler", ["changeColumnOrder"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),

    ...mapMutations("initialData", ["updateColumnOrder"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),

    leaveDialog() {
      this.cancelEvent();
      this.resetDataTableVuex();
      this.setDialog(false);
    },
    confirmChanges() {
      eventBus.$emit("columnOrderUpdated", this.duplicatedColumns);
    },
    closeStepper() {
      this.dialog = false;
    },

    onDragEvent(evt) {
      let columnName = evt.moved.element;
      let oldIndex = evt.moved.oldIndex;
      let newIndex = evt.moved.newIndex;
      let movedInfo = { columnName: columnName, oldIndex: oldIndex, newIndex: newIndex };
      this.changeColumnOrder(movedInfo);
    }
    // changeColumnOrder(position, movedColumnName, newIndex) {
    //   const api = "http://localhost:5000/changeColumnOrder";
    //   axios
    //     .get(api, {
    //       params: {
    //         position: position,
    //         movedColumnName: movedColumnName,
    //         newIndex: newIndex
    //       }
    //     })
    //     .then(res => {})
    //     .catch(error => {
    //       console.error(error);
    //     });
    // }
  },
  components: {
    draggable
  },
  computed: {
    dialogInstance: {
      get() {
        return this.dialog;
      },
      set() {
        this.setDialog(!this.dialog);
      }
    },
    // ...mapGetters("initialData", ["columns"]),
    duplicatedColumnsInstance: {
      get() {
        return this.duplicatedColumns;
      }
      // set(value) {
      //   console.log(value);
      //   this.changeColumnOrder(value);
      // }
    },
    ...mapState({
      columns: state => state.initialData.columns,
      dialog: state => state.summaryTableHandler.dialog
    })
  },

  created() {
    // this.selectionTimer = setTimeout(() => {
    //   this.duplicatedColumns.splice(0, this.duplicatedColumns.length);
    //   this.columns.forEach(element => {
    //     this.duplicatedColumns.push(element);
    //   });
    // }, 1000);
  }
};
</script>
<style scoped>
.columnList {
  /* height: 230px; */
  /* overflow-y: scroll; */
}
</style>
