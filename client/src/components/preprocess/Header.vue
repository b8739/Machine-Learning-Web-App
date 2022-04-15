<template>
  <div>
    <nav>
      <a class="home-link" href="http://localhost:8080/">
        ML WEB APP
        <!-- <img class="logo" src="../../assets/attic_logo.png" alt=""/>
        <!-- <v-img
          :src="require('../../assets/machine-learning.png')"
          aspect-ratio="1"
          height="40"
          contain
          width="40"
        ></v-img>  -->
      </a>

      <div class="nav-container">
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
      </div>
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
.home-link {
  width: 110px;
  position: absolute;
  margin-top: 1rem;
  top: 0px;
  left: 20px;
  font-weight: 700;
}

nav {
  height: 60px;
  background-color: #f5f5f5;
  overflow: hidden;
  border-bottom: 0.5px solid #cccbcbe7;
  display: flex;
  justify-content: center;
}

.nav-container {
  text-align: center;
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
