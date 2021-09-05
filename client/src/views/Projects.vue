<template>
  <div>
    <v-app-bar>
      <a href="http://localhost:8080/"><img class="logo" src="@//assets/attic_logo.png" alt=""/></a>
    </v-app-bar>
    <v-container fluid>
      <v-row>
        <v-col v-if="project_list.length != 0" cols="3" class="pl-0 pt-1">
          <v-btn @click="loadProjects" block color="success">
            <v-icon left class="mdi-36">
              mdi-folder-plus-outline
            </v-icon>
            New Project
          </v-btn>
          <v-card height="900px">
            <v-navigation-drawer width="100%">
              <v-list>
                <v-list-item>
                  <v-list-item-title class="font-weight-bold">Projects</v-list-item-title>
                </v-list-item>
                <v-list-item v-for="(project, index) in project_list" :key="index">
                  <v-sheet light outlined height="100" width="100%" @click="enterProject">
                    <v-card-text class="font-weight-bold subheading pt-2 pb-0">
                      {{ project }}</v-card-text
                    >

                    <v-card-text class="font-weight-thin caption pt-1">
                      Created __ days ago</v-card-text
                    >
                  </v-sheet>
                </v-list-item>
              </v-list>
            </v-navigation-drawer>
          </v-card>
        </v-col>
        <v-col cols=""> </v-col>
      </v-row>
      <!-- <v-row> <div ref="tester"></div></v-row> -->
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      project_list: [],
      // plotly
      data: [
        {
          x: [1, 2, 3, 4],
          y: [10, 15, 13, 17],
          type: "scatter",
          marker: {
            // marker is an object, valid marker keys: #scatter-marker
            color: "rgb(16, 32, 77)" // more about "marker.color": #scatter-marker-color
          }
        },
        {
          type: "bar", // all "bar" chart attributes: #bar
          x: [1, 2, 3], // more about "x": #bar-x
          y: [3, 1, 6], // #bar-y
          name: "bar chart example" // #bar-name
        }
      ],
      layout: {
        title: "My graph"
      }
    };
  },
  methods: {
    createPlot() {
      let TESTER = this.$refs.tester;
      Plotly.newPlot(
        TESTER,
        [
          {
            x: [1, 2, 3, 4, 5],
            y: [1, 2, 4, 8, 16]
          }
        ],
        {
          width: 238,
          height: 200,
          margin: {
            l: 20,
            r: 20,
            b: 20,
            t: 20,
            pad: 4
          },
          yaxis: {
            automargin: true
          }
        },
        { showSendToCloud: true }
      );
    },
    ...mapMutations("initialData", ["setNavStatus"]),
    loadProjects() {
      let path = "http://localhost:5000/loadProjects";
      console.log(path);

      axios
        .get(path)
        .then(res => {
          this.project_list = res.data;
        })
        .catch(ex => {
          console.log("ERR!!!!! : ", ex);
        });
    },
    enterProject() {
      this.setNavStatus("datasets");
      this.$router.push({ name: "datasets" });
    }
  },
  components: {},
  created() {
    this.loadProjects();
  },
  mounted() {
    // this.createPlot();
  }
};
</script>
<style scoped>
.logo {
  width: 4%;
  position: absolute;
  top: 35%;
  left: 20px;
}
</style>
