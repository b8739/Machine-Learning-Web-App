<template>
  <v-container>
    <v-navigation-drawer height="100vh" v-model="drawer" absolute :mini-variant.sync="mini">
      <v-list-item class="mt-10 px-2">
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-title>User123</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <keep-alive>
        <component v-bind:is="dynamicSideMenu"></component>
      </keep-alive>

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
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import TableSideMenu from "@/components/sideMenu/TableSideMenu";
import SummarySideMenu from "@/components/sideMenu/SummarySideMenu";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
import axios from "axios";
export default {
  data() {
    return {
      drawer: true,
      mini: false,

      tableItems: [
        { title: "Add Feature", icon: "mdi-plus" },
        { title: "Update Feature", icon: "mdi-pencil" },
        { title: "Delete Row", icon: "mdi-delete" }
      ],

      activeState: true,
      currentComponent: "SummaryTable"
    };
  },
  components: {
    TableSideMenu,
    SummarySideMenu
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    }),
    dataFeatures() {
      return this.$root.$refs.dataFeatures;
    },
    infiniteTable() {
      return this.$root.$refs.infiniteTable;
    },

    dynamicSideMenu() {
      if (this.currentComponent == "SummaryTable") return "SummarySideMenu";
      else return "TableSideMenu";
    }
  },
  methods: {
    ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapMutations("initialData", ["loadTableList"]),

    clickTableNameEvent() {
      this.loadFundamentalData("http://localhost:5000/loadData");
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
    eventBus.$on("changeComponent", componentName => {
      this.currentComponent = componentName;
    });
  },
  mounted() {
    this.showTables();
  }
};
</script>
