import Vue from "vue";
import VueRouter from "vue-router";

import Projects from "../views/Projects";
import Datasets from "../views/Datasets";
import Preprocess from "../views/Preprocess";
// modeling
import ModelingProcess from "../views/modeling/ModelingProcess";
import Models from "../views/modeling/Models";
import ModelingResult from "../views/modeling/ModelingResult";
import ModelingSingleResult from "../views/modeling/ModelingSingleResult";

import GraphBuilder from "../views/GraphBuilder";

import Simulations from "../views/simulation/Simulations";
import SimulationResult from "../views/simulation/SimulationResult";

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
      path: "/modelingProcess",
      name: "modelingProcess",
      component: ModelingProcess,
      props: true
    },
    {
      path: "/simulations",
      name: "simulations",
      component: Simulations,
      props: true
    },
    {
      path: "/simulation/result",
      name: "simulationResult",
      component: SimulationResult,
      props: true
    },

    {
      path: "/modelingResult/:case",
      name: "modelingResult",
      component: ModelingResult,
      props: true
    },
    {
      path: "/modelingSingleResult/:case",
      name: "modelingSingleResult",
      component: ModelingSingleResult,
      props: true
    }
  ]
});

export default router;
