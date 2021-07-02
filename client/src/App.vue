<template>
  <div id="app">
    <v-app>
      <div id="content" class="content">
        <router-view></router-view>
      </div>
    </v-app>
  </div>
</template>

<script>
import Header from "./components/layout/Header.vue";
// import Sidebar from "./components/Sidebar.vue"
import Preprocess from "./views/Preprocess.vue";

export default {
  name: "App",

  components: {
    Header,
    Preprocess
  },
  mounted() {}
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans&family=Nunito+Sans&display=swap");
@import url(//spoqa.github.io/spoqa-han-sans/css/SpoqaHanSans-kr.css);
/* reset */
* {
  font-family: "Spoqa Han Sans", "Sans-serif", "Nunito Sans", sans-serif, "Noto Sans", sans-serif;
  /* color: #2b2b2b; */
  margin: 0;
  padding: 0;
}
a {
  text-decoration: none;
}
.cursor-pointer {
  cursor: pointer;
}

/* base.html */
</style>
