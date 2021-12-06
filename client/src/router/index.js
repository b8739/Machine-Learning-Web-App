import Vue from "vue";
import VueRouter from "vue-router";

import Projects from "../views/Projects";
import Datasets from "../views/Datasets";

import ModelingResult from "../views/modeling/ModelingResult";

import GraphBuilder from "../views/GraphBuilder";

import SimulationResult from "../views/simulation/SimulationResult";

import LoginForm from "@/components/login/LoginForm";

import "@/assets/css/main.css";

// lazyloading
const Preprocess = () => import(/* webpackChunkName: "preprocess" */ "../views/Preprocess");
const Models = () => import(/* webpackChunkName: "models" */ "../views/modeling/Models");
const Simulations = () =>
  import(/* webpackChunkName: "simulations" */ "../views/simulation/Simulations");
const ModelingProcess = () =>
  import(/* webpackChunkName: "modelingProcess" */ "../views/modeling/ModelingProcess");

Vue.use(VueRouter); //Vue Router를 사용했다고 선언

const router = new VueRouter({
  mode: "history",

  routes: [
    {
      path: "/",
      component: LoginForm,
      props: true
    },
    {
      path: "/projects",
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
    }
    // {
    //   path: "/modelingSingleResult/:case",
    //   name: "modelingSingleResult",
    //   component: ModelingSingleResult,
    //   props: true
    // }
  ]
});

export default router;
