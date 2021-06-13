<template>
  <div>
    <a href="http://localhost:8080"><img class="logo" src="../../assets/attic_logo.png" alt=""/></a>
    <nav>
      <router-link id="routerLink" :class="{ underline: navStatus == 'datasets' }" to="/datasets"
        >Datasets</router-link
      >
      <router-link
        id="routerLink"
        :class="{ underline: navStatus == 'datasummary' }"
        to="dataSummary"
        >Preprocess</router-link
      >
      <a id="routerLink" @click="openDialogue()">EDA</a>
      <router-link id="routerLink" :class="{ underline: navStatus == 'models' }" to="/models"
        >Modeling</router-link
      >
      <router-link id="routerLink" :class="{ underline: navStatus == 'optimize' }" to=""
        >Optimize</router-link
      >
    </nav>
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
    openDialogue() {
      eventBus.$emit("openDialogue", true);
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
