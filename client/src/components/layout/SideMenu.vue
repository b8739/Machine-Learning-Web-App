<template>
  <v-container>
    <v-navigation-drawer v-model="drawer" absolute>
      <v-list-item class="px-2">
        <v-list-item-title>Options</v-list-item-title>
        <v-btn @click.stop="mini = !mini" icon>
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" link @click="callOption(item.title)">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <DeleteRowModal />
      <v-divider></v-divider>
      <v-list-item class="px-2">
        <v-list-item-title>List of Datasets</v-list-item-title>
      </v-list-item>
      <!-- 테이블 리스트 -->
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item v-for="(tableName, tableIndex) in tableList" :key="tableIndex">
          <v-list-item-content>
            <v-list-item-title>{{ tableName }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import DeleteRowModal from "@/components/modal/DeleteRowModal";
import { eventBus } from "@/main";
import axios from "axios";
export default {
  data() {
    return {
      drawer: true,
      mini: true,
      items: [
        { title: "Add Column", icon: "mdi-plus-circle-outline" },
        { title: "Update Column", icon: "mdi-select-drag" },
        { title: "Delete Row", icon: "mdi-trash-can-outline" }
      ],
      tableList: []
    };
  },
  components: {
    DeleteRowModal
  },
  methods: {
    callOption(title) {
      if (title == "Delete Row") {
        eventBus.$emit("openDeleteRowModal", true);
      }
    },
    showTables() {
      let path = "http://localhost:5000/showTables";
      axios
        .get(path)
        .then(res => {
          this.tableList = res.data;
        })
        .catch(error => {});
    }
  },
  created() {
    this.showTables();
  },
  mounted() {
    console.log("d");
    this.showTables();
  }
};
</script>
