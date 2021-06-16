import Vue from "vue";
import VueRouter from "vue-router";
import Projects from "../views/Projects";
import Datasets from "../views/Datasets";
import Preprocess from "../views/Preprocess";
import Modeling from "../views/Modeling";
import Models from "../views/Models";
import GraphBuilder from "../views/GraphBuilder";
import ModelingResult from "../components/modeling/ModelingResult";
import "../assets/css/main.css";

// import Login from "../views/Login";

Vue.use(VueRouter); //View Router를 사용했다고 선언

const router = new VueRouter({
  mode: "history",

  routes: [
    {
      path: "/",
      component: Projects,
      props: true
    },
    {
      path: "/datasets",
      name: "datasets",
      component: Datasets,
      props: true
    },
    {
      path: "/preprocess",
      name: "preprocess",
      component: Preprocess,
      props: true
    },
    {
      path: "/eda",
      component: GraphBuilder,
      props: true
    },
    {
      path: "/models",
      component: Models,
      props: true
    },
    {
      path: "/modeling/:case",
      name: "modeling",
      component: Modeling,
      props: true
    },
    // {
    //   path: "/modeling",
    //   name: "modeling",
    //   component: Modeling,
    //   props: true
    // },
    {
      path: "/modelingResult",
      name: "modelingResult",
      component: ModelingResult,
      props: true
    }
  ]
});

export default router;
