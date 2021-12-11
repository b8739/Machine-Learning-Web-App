<template>
  <div>
    <a href="http://localhost:8080/"
      ><img class="logo" src="../../assets/attic_logo.png" alt=""
    /></a>
    <nav>
      <!-- Dataset -->
      <router-link id="routerLink" :class="{ underline: navStatus == 'datasets' }" to="/datasets"
        >Datasets</router-link
      >
      <!-- Preprocess -->
      <router-link
        id="routerLink"
        :class="{ underline: navStatus == 'preprocess' }"
        to="/preprocess"
        >Preprocess</router-link
      >
      <!-- EDA -->
      <a id="routerLink" @click="openDialog(true)">EDA</a>
      <!-- Modeling -->
      <router-link id="routerLink" :class="{ underline: navStatus == 'models' }" to="/models"
        >Modeling</router-link
      >
      <!-- Simulation -->
      <!-- <router-link
        id="routerLink"
        :class="{ underline: navStatus == 'simulation' }"
        to="/Simulations"
        >Simulation</router-link
      > -->
    </nav>
    <v-spacer></v-spacer>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },
  methods: {
    // openGraphBuilder() {
    //   let w = screen.width * 0.8;
    //   let h = screen.height * 0.8;
    //   let leftPosition = (screen.width - w) / 2;
    //   let topPosition = (screen.height - h) / 2;
    //   let url = "http://localhost:5000/eda";
    //   window.open(
    //     url,
    //     "modelingResult",
    //     "width=" +
    //       w +
    //       ",height=" +
    //       h +
    //       ",top=" +
    //       topPosition +
    //       ",left=" +
    //       leftPosition +
    //       ", scrollbars=no"
    //   );
    // },
    openDialog() {
      eventBus.$emit("openDialog", true);
    }
  },
  computed: {
    ...mapState({
      navStatus: state => state.initialData.navStatus
    })
  }
};
</script>
<style scoped>
/* reset */

body {
  background-color: #f0f0f0;
}

/* base.html */
.logo {
  width: 4%;
  position: absolute;
  top: 18px;
  left: 20px;
}

nav {
  text-align: center;
  height: 60px;
  /* background-color: #87ceeb; */
  background-color: #f5f5f5;
  overflow: hidden;
  border-bottom: 0.5px solid #cccbcbe7;
}
nav #routerLink {
  display: inline-block;
  color: rgb(53, 53, 53);
  margin: 13px 60px 0 0;
  font-size: 20px;
}
.underline {
  text-decoration: underline;
}
/* index.html */
</style>
