<template>
  <v-container>
    <v-navigation-drawer v-model="drawer" absolute>
      <!-- <v-list-item class="pt-2">
        <v-list-item-title class="text-uppercase">Options</v-list-item-title>
      </v-list-item>

      <v-divider></v-divider> -->
      <!-- 
      <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" link @click="callOption(item.title)">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <p class="grey--text text--darken-3 body-2">{{ item.title }}</p>
          </v-list-item-content>
        </v-list-item>
      </v-list> -->
      <v-list dense>
        <v-list-group v-model="activeState">
          <template v-slot:activator>
            <v-list-item-title active>Options</v-list-item-title>
          </template>
          <v-list-item v-for="item in items" :key="item.title" link @click="callOption(item.title)">
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
      </v-list>
      <!-- 구분선 -->
      <!-- <v-divider class=""></v-divider> -->
      <v-list dense>
        <v-list-group v-model="activeState">
          <template v-slot:activator>
            <v-list-item-title>List of Datasets</v-list-item-title>
          </template>
          <v-list-item v-for="(tableName, tableIndex) in tableList" :key="tableIndex">
            <v-list-item-title @click="clickTableNameEvent">{{ tableName }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
      </v-list>
      <!-- <v-list-item class="">
        <v-list-item-title class="body-1">List of Datasets</v-list-item-title>
      </v-list-item> -->
      <!-- 테이블 리스트 -->
      <!-- <v-divider></v-divider>
      <v-list dense>
        <v-list-item v-for="(tableName, tableIndex) in tableList" :key="tableIndex">
          <v-list-item-content>
            <v-list-item-title @click="clickTableNameEvent">{{ tableName }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list> -->
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
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
        { title: "Delete Row", icon: "mdi-trash-can-outline" },
        { title: "Change Order", icon: "mdi-swap-vertical" },
        { title: "Moving Average", icon: "mdi-chart-timeline-variant" }
      ],
      activeState: true
    };
  },
  components: {},
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    })
  },
  methods: {
    ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapMutations("initialData", ["loadTableList"]),
    clickTableNameEvent() {
      this.loadFundamentalData("http://localhost:5000/loadData");
    },
    callOption(title) {
      if (title == "Delete Row") {
        eventBus.$emit("openDeleteRowModal", true);
      } else if (title == "Moving Average") {
        eventBus.$emit("openMovingAverageModal", true);
      } else if (title == "Change Order") {
        eventBus.$emit("openChangeOrderModal", true);
      }
    },
    showTables() {
      let path = "http://localhost:5000/showTables";
      axios
        .get(path)
        .then(res => {
          // this.tableList = res.data;
          this.loadTableList(res.data);
        })
        .catch(error => {});
    }
  },
  created() {
    this.showTables();
  },
  mounted() {
    this.showTables();
  }
};
</script>
